"""Metaplastic Field — per-node learning rates + inhibitor diffusion.

Extends MultiField with two mechanisms that enable Turing-like
symmetry breaking at the metaplastic level:

1. Per-node learning rate (metaplasticity): each node's eta adjusts
   homeostatically based on its activity vs a LOCAL target (mean of
   grid neighbors' activity). High-activity nodes consolidate (lower
   eta), low-activity nodes explore (higher eta).

2. Inhibitor field: nodes emit inhibitor proportional to their weight
   mass. Inhibitor diffuses spatially and decays. Via DIFFERENCE-
   DEPENDENT coupling, inhibitor pushes eta DOWN — suppressing learning
   where consolidated assemblages emit strongly. The coupling is
   proportional to the difference between a node's eta and its spatial
   neighbors' mean eta, amplifying pre-existing eta heterogeneity.

The combination creates a Turing instability: Hebbian reinforcement is
the short-range activator, inhibitor diffusion is the long-range
inhibitor. The variable that differentiates is eta — the learning rule
itself — not the weights directly.
"""

import numpy as np
from .multifield import MultiField


class MetaplasticField(MultiField):
    """MultiField with per-node metaplasticity and inhibitor communication.

    Parameters (beyond MultiField)
    ----------
    meta_strength : float
        How strongly activity deviation from target adjusts eta.
        0 = no metaplasticity (reduces to MultiField).
    target_activity : float
        Activity level that leaves eta unchanged. Default 0.15.
    eta_min, eta_max : float
        Bounds on per-node learning rate.
    inhibitor_diffusion : float
        Discrete Laplacian coefficient for inhibitor spread.
        Capped at 0.20 for CFL stability.
    inhibitor_decay : float
        Fraction of inhibitor removed each step. Default 0.10.
    inhibitor_coupling : float
        How strongly inhibitor suppresses eta (difference-dependent).
        0 = no communication.
    inhibitor_emission_rate : float
        Scale factor for weight-mass → inhibitor emission.
    use_local_target : bool
        If True, target_activity is replaced by each node's spatial
        neighbors' mean activity (local homeostasis). Default True.
    use_difference_coupling : bool
        If True, inhibitor coupling is difference-dependent (amplifies
        eta heterogeneity). If False, uses original absolute coupling.
        Default True.
    """

    def __init__(self, meta_strength=0.0, target_activity=0.15,
                 eta_min=0.005, eta_max=0.20,
                 inhibitor_diffusion=0.05, inhibitor_decay=0.10,
                 inhibitor_coupling=0.0, inhibitor_emission_rate=0.01,
                 use_local_target=True, use_difference_coupling=True,
                 target_radius=1, use_soft_bounds=False,
                 ema_rate=0.05,
                 **kwargs):
        super().__init__(**kwargs)
        self.ema_rate = ema_rate

        self.meta_strength = meta_strength
        self.target_activity = target_activity
        self.eta_min = eta_min
        self.eta_max = eta_max
        self.inhibitor_diffusion = min(inhibitor_diffusion, 0.20)
        self.inhibitor_decay = inhibitor_decay
        self.inhibitor_coupling = inhibitor_coupling
        self.inhibitor_emission_rate = inhibitor_emission_rate
        self.use_local_target = use_local_target
        self.use_difference_coupling = use_difference_coupling
        self.target_radius = target_radius
        self.use_soft_bounds = use_soft_bounds

        # Per-node learning rates, initialized to global eta
        self.node_eta = np.full(self.n_nodes, self.eta, dtype=np.float64)

        # Inhibitor field on the 2D grid
        self.inhibitor = np.zeros(self.n_nodes, dtype=np.float64)

        # Precompute 2D grid neighbor indices for Laplacian diffusion (1-hop)
        self._neighbors = self._build_grid_neighbors()
        # Precompute extended neighborhood for local target (variable radius)
        self._target_neighbors = self._build_grid_neighbors_radius(target_radius)

    def _build_grid_neighbors(self):
        """Build von Neumann neighborhood (4-connected) for each grid cell."""
        neighbors = []
        gs = self.grid_size
        for idx in range(self.n_nodes):
            row = idx // gs
            col = idx % gs
            nbrs = []
            if row > 0:
                nbrs.append((row - 1) * gs + col)
            if row < gs - 1:
                nbrs.append((row + 1) * gs + col)
            if col > 0:
                nbrs.append(row * gs + (col - 1))
            if col < gs - 1:
                nbrs.append(row * gs + (col + 1))
            neighbors.append(nbrs)
        return neighbors

    def _build_grid_neighbors_radius(self, radius):
        """Build neighborhood for each grid cell within given Manhattan radius."""
        if radius <= 0:
            return [[] for _ in range(self.n_nodes)]
        if radius == 1:
            return self._neighbors  # reuse 1-hop
        neighbors = []
        gs = self.grid_size
        for idx in range(self.n_nodes):
            row = idx // gs
            col = idx % gs
            nbrs = []
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    if dr == 0 and dc == 0:
                        continue
                    if abs(dr) + abs(dc) > radius:
                        continue
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < gs and 0 <= nc < gs:
                        nbrs.append(nr * gs + nc)
            neighbors.append(nbrs)
        return neighbors

    def _bound_eta(self):
        """Apply bounds to node_eta — hard clip or soft sigmoid."""
        if self.use_soft_bounds:
            mid = (self.eta_min + self.eta_max) / 2
            spread = (self.eta_max - self.eta_min) / 2
            self.node_eta = mid + spread * np.tanh((self.node_eta - mid) / spread)
        else:
            np.clip(self.node_eta, self.eta_min, self.eta_max, out=self.node_eta)

    def _compute_node_weight_mass(self):
        """Total absolute weight mass emanating from each node."""
        mass = np.zeros(self.n_nodes)
        for (i, j), w in self.weights.items():
            mass[i] += abs(w)
        return mass

    def _diffuse_inhibitor(self):
        """Discrete Laplacian diffusion of inhibitor field."""
        new_inhibitor = self.inhibitor.copy()
        coeff = self.inhibitor_diffusion
        for idx in range(self.n_nodes):
            nbrs = self._neighbors[idx]
            if nbrs:
                laplacian = sum(self.inhibitor[n] for n in nbrs) - len(nbrs) * self.inhibitor[idx]
                new_inhibitor[idx] += coeff * laplacian
        # Ensure non-negative
        np.maximum(new_inhibitor, 0.0, out=new_inhibitor)
        self.inhibitor = new_inhibitor

    def step(self):
        """One step of metaplastic field dynamics.

        Extends MultiField.step() with:
        1. Metaplastic eta adjustment (after activity update)
        2. Inhibitor emission, diffusion, decay
        3. Inhibitor-eta coupling
        4. Per-edge eta in Hebbian update
        """
        self.step_count += 1

        # 1. Inject spatially varying noise from hotspots
        noise = self.rng.uniform(-1, 1, self.n_nodes) * self.noise_profile
        self.activations += noise

        # 2. Propagate through connections
        new_input = np.zeros(self.n_nodes)
        in_degree = np.zeros(self.n_nodes)

        for (i, j), w in self.weights.items():
            new_input[j] += w * self.activations[i]
            in_degree[j] += 1

        scale = np.where(in_degree > 0, np.sqrt(np.maximum(in_degree, 1)), 1.0)

        self.activations = np.tanh(
            0.5 * self.activations + new_input / scale
        )

        # 3. Hebbian update with per-edge eta (average of endpoint etas)
        for (i, j) in list(self.weights.keys()):
            eta_ij = 0.5 * (self.node_eta[i] + self.node_eta[j])
            self.weights[(i, j)] += eta_ij * self.activations[i] * self.activations[j]
            self.weights[(i, j)] *= (1.0 - self.lam)
            self.weights[(i, j)] = np.clip(self.weights[(i, j)], -self.w_max, self.w_max)

        # 4. Strictly local encounters
        for _ in range(self.encounter_rate):
            i, j = self._local_encounter_pair()
            if i != j and (i, j) not in self.weights:
                self.weights[(i, j)] = 0.0
                self.edges_created += 1

        # 5. Prune dead connections
        dead = [k for k, w in self.weights.items() if abs(w) < self.prune_threshold]
        for k in dead:
            del self.weights[k]
            self.edges_pruned += 1

        # 6. Update activity history (EMA)
        r = self.ema_rate
        self._activity_history = (1.0 - r) * self._activity_history + r * np.abs(self.activations)

        # 7. Metaplastic eta adjustment
        if self.meta_strength > 0:
            if self.use_local_target:
                # Local target: each node's target = mean activity of neighborhood
                local_target = np.zeros(self.n_nodes)
                for idx in range(self.n_nodes):
                    nbrs = self._target_neighbors[idx]
                    if nbrs:
                        local_target[idx] = np.mean(self._activity_history[nbrs])
                    else:
                        local_target[idx] = self.target_activity
                eta_delta = -self.meta_strength * (self._activity_history - local_target)
            else:
                # Original global target
                eta_delta = -self.meta_strength * (self._activity_history - self.target_activity)
            self.node_eta += eta_delta
            self._bound_eta()

        # 8. Inhibitor dynamics
        if self.inhibitor_coupling > 0 or self.meta_strength > 0:
            # Emission: proportional to weight mass
            weight_mass = self._compute_node_weight_mass()
            self.inhibitor += self.inhibitor_emission_rate * weight_mass

            # Diffusion
            self._diffuse_inhibitor()

            # Decay
            self.inhibitor *= (1.0 - self.inhibitor_decay)

            # Coupling: inhibitor SUPPRESSES eta (sign reversed from v1)
            if self.inhibitor_coupling > 0:
                if self.use_difference_coupling:
                    # Difference-dependent: amplifies eta heterogeneity
                    # Nodes with eta above local mean are pushed further up,
                    # nodes below are pushed further down, scaled by inhibitor
                    mean_eta_local = np.zeros(self.n_nodes)
                    for idx in range(self.n_nodes):
                        nbrs = self._neighbors[idx]
                        if nbrs:
                            mean_eta_local[idx] = np.mean(self.node_eta[nbrs])
                        else:
                            mean_eta_local[idx] = self.node_eta[idx]
                    eta_diff = self.node_eta - mean_eta_local
                    self.node_eta -= self.inhibitor_coupling * self.inhibitor * (1.0 - eta_diff)
                else:
                    # Original absolute coupling (but sign-reversed: DOWN)
                    self.node_eta -= self.inhibitor_coupling * self.inhibitor
                self._bound_eta()

    def census(self):
        """Extended census with metaplastic metrics."""
        base = super().census()

        # Add metaplastic fields
        assemblages = self.find_assemblages()

        # Per-assemblage mean eta
        asm_etas = []
        for nodes in assemblages:
            node_list = sorted(nodes)
            asm_etas.append(float(np.mean(self.node_eta[node_list])))

        base["mean_eta"] = float(np.mean(self.node_eta))
        base["eta_std"] = float(np.std(self.node_eta))
        base["eta_range"] = float(np.max(self.node_eta) - np.min(self.node_eta))
        base["mean_inhibitor"] = float(np.mean(self.inhibitor))
        base["max_inhibitor"] = float(np.max(self.inhibitor))
        base["assemblage_etas"] = asm_etas

        return base
