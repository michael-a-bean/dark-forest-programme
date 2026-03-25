"""Multi-Field Substrate — multiple energy sources in 2D space.

Extended from dark-forest-silica to support four weight bounding strategies:
  - hard: np.clip (Papers 1-4 baseline)
  - tanh: smooth saturation
  - sigmoid: smooth saturation (sharper transition)
  - oja: self-normalising Oja rule (replaces Hebbian update)
"""

import numpy as np
from collections import defaultdict

BOUND_TYPES = ("hard", "tanh", "sigmoid", "oja")


def _bound_weight_scalar(w, w_max, bound_type):
    """Apply weight bound to a single scalar value."""
    if bound_type == "hard":
        return np.clip(w, -w_max, w_max)
    elif bound_type == "tanh":
        return w_max * np.tanh(w / w_max)
    elif bound_type == "sigmoid":
        return 2.0 * w_max * (1.0 / (1.0 + np.exp(-2.0 * w / w_max))) - w_max
    return w  # oja — no explicit bound


class MultiField:
    """2D field of identical nodes with multiple energy hotspots."""

    def __init__(self, grid_size=20, n_hotspots=3, hotspot_radius=0.2,
                 hotspot_energy=0.3, base_noise=0.02, eta=0.05, lam=0.002,
                 w_max=1.0, encounter_rate=20, locality=0.15,
                 prune_threshold=1e-4, bound_type="hard", seed=None):

        if bound_type not in BOUND_TYPES:
            raise ValueError(f"bound_type must be one of {BOUND_TYPES}, got {bound_type!r}")

        self.grid_size = grid_size
        self.n_nodes = grid_size * grid_size
        self.eta = eta
        self.lam = lam
        self.w_max = w_max
        self.base_noise = base_noise
        self.hotspot_energy = hotspot_energy
        self.hotspot_radius = hotspot_radius
        self.encounter_rate = encounter_rate
        self.locality = locality
        self.prune_threshold = prune_threshold
        self.bound_type = bound_type
        self.rng = np.random.default_rng(seed)

        # 2D positions on [0,1] x [0,1]
        xs = np.linspace(0, 1, grid_size)
        ys = np.linspace(0, 1, grid_size)
        gx, gy = np.meshgrid(xs, ys)
        self.pos_x = gx.flatten()
        self.pos_y = gy.flatten()

        # Place hotspots
        self.hotspots = self._place_hotspots(n_hotspots)

        # Compute noise profile from hotspot distances
        self.noise_profile = self._compute_noise_profile()

        # Activations
        self.activations = self.rng.uniform(-0.1, 0.1, self.n_nodes) + 0.1 * self.noise_profile

        # Metrics
        self.step_count = 0
        self.edges_created = 0
        self.edges_pruned = 0

        # Sparse weights
        self.weights = {}
        self._init_local_connections()

        # Activity history
        self._activity_history = np.abs(self.activations.copy())

    def _place_hotspots(self, n):
        """Place hotspots spread across the field."""
        if n == 1:
            return [(0.5, 0.5)]
        elif n == 2:
            return [(0.25, 0.5), (0.75, 0.5)]
        elif n == 3:
            return [(0.2, 0.3), (0.8, 0.3), (0.5, 0.8)]
        elif n == 4:
            return [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)]
        else:
            return [(self.rng.uniform(0.1, 0.9), self.rng.uniform(0.1, 0.9))
                    for _ in range(n)]

    def _compute_noise_profile(self):
        """Compute per-node noise level based on distance to nearest hotspot."""
        profile = np.full(self.n_nodes, self.base_noise)
        for hx, hy in self.hotspots:
            dist = np.sqrt((self.pos_x - hx)**2 + (self.pos_y - hy)**2)
            contribution = self.hotspot_energy * np.exp(-dist**2 / (2 * self.hotspot_radius**2))
            profile += contribution
        return profile

    def _init_local_connections(self):
        """Create sparse initial connectivity biased toward spatial neighbors."""
        target = int(self.n_nodes * 4)
        created = 0
        while created < target:
            i = self.rng.integers(0, self.n_nodes)
            dx = self.rng.normal(0, self.locality)
            dy = self.rng.normal(0, self.locality)
            target_x = self.pos_x[i] + dx
            target_y = self.pos_y[i] + dy
            dists = (self.pos_x - target_x)**2 + (self.pos_y - target_y)**2
            j = np.argmin(dists)
            if i != j and (i, j) not in self.weights:
                self.weights[(i, j)] = self.rng.uniform(-0.3, 0.3)
                self.edges_created += 1
                created += 1

    def _local_encounter_pair(self):
        """Sample a pair of nearby nodes from a random spatial location."""
        loc_x = self.rng.uniform(0, 1)
        loc_y = self.rng.uniform(0, 1)

        dists = np.sqrt((self.pos_x - loc_x)**2 + (self.pos_y - loc_y)**2)
        proximity = np.exp(-dists**2 / (2 * self.locality**2))
        local_activity = self._activity_history + 0.001
        probs = proximity * local_activity
        total = probs.sum()
        if total < 1e-10:
            return self.rng.integers(0, self.n_nodes), self.rng.integers(0, self.n_nodes)
        probs /= total

        i = self.rng.choice(self.n_nodes, p=probs)

        probs2 = probs.copy()
        probs2[i] = 0
        total2 = probs2.sum()
        if total2 < 1e-10:
            j = self.rng.integers(0, self.n_nodes)
        else:
            probs2 /= total2
            j = self.rng.choice(self.n_nodes, p=probs2)

        return i, j

    def step(self):
        """One step of multi-field dynamics."""
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

        # 3. Hebbian update with configurable bound
        if self.bound_type == "oja":
            for (i, j) in list(self.weights.keys()):
                a_i = self.activations[i]
                a_j = self.activations[j]
                w = self.weights[(i, j)]
                # Oja: dw = eta * (a_i * a_j - a_j^2 * w)
                self.weights[(i, j)] = w + self.eta * (a_i * a_j - a_j**2 * w)
                self.weights[(i, j)] *= (1.0 - self.lam)
        else:
            for (i, j) in list(self.weights.keys()):
                self.weights[(i, j)] += self.eta * self.activations[i] * self.activations[j]
                self.weights[(i, j)] *= (1.0 - self.lam)
                self.weights[(i, j)] = _bound_weight_scalar(
                    self.weights[(i, j)], self.w_max, self.bound_type
                )

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

        # 6. Update activity history
        self._activity_history = 0.95 * self._activity_history + 0.05 * np.abs(self.activations)

    def find_assemblages(self, threshold=None):
        """Find connected components (assemblages) in the strong-edge subgraph."""
        if not self.weights:
            return []
        w_arr = np.array(list(self.weights.values()))
        if threshold is None:
            threshold = np.percentile(np.abs(w_arr), 75) if len(w_arr) > 1 else 0.01

        adj = defaultdict(set)
        for (i, j), w in self.weights.items():
            if abs(w) >= threshold:
                adj[i].add(j)
                adj[j].add(i)

        visited = set()
        assemblages = []
        for node in range(self.n_nodes):
            if node in visited or node not in adj:
                continue
            component = set()
            queue = [node]
            while queue:
                n = queue.pop(0)
                if n in visited:
                    continue
                visited.add(n)
                component.add(n)
                for neighbor in adj[n]:
                    if neighbor not in visited:
                        queue.append(neighbor)
            if len(component) > 1:
                assemblages.append(component)

        return assemblages

    def assemblage_census(self):
        """Detailed info about each assemblage."""
        assemblages = self.find_assemblages()
        infos = []
        for nodes in assemblages:
            node_list = sorted(nodes)
            cx = np.mean(self.pos_x[node_list])
            cy = np.mean(self.pos_y[node_list])
            energy = np.mean(np.abs(self.activations[node_list]))
            min_dist = float('inf')
            nearest_hotspot = -1
            for hi, (hx, hy) in enumerate(self.hotspots):
                d = np.sqrt((cx - hx)**2 + (cy - hy)**2)
                if d < min_dist:
                    min_dist = d
                    nearest_hotspot = hi
            infos.append({
                "size": len(nodes),
                "center": (float(cx), float(cy)),
                "energy": float(energy),
                "nearest_hotspot": nearest_hotspot,
                "hotspot_dist": float(min_dist),
            })
        return infos

    def census(self):
        """Full snapshot."""
        w_arr = np.array(list(self.weights.values())) if self.weights else np.array([0.0])
        assemblages = self.find_assemblages()
        a_census = self.assemblage_census()

        hotspot_activity = []
        for hx, hy in self.hotspots:
            dists = np.sqrt((self.pos_x - hx)**2 + (self.pos_y - hy)**2)
            nearby = dists < self.hotspot_radius * 2
            if nearby.any():
                hotspot_activity.append(float(np.mean(np.abs(self.activations[nearby]))))
            else:
                hotspot_activity.append(0.0)

        return {
            "step": self.step_count,
            "n_edges": len(self.weights),
            "mean_weight": float(np.mean(np.abs(w_arr))),
            "max_weight": float(np.max(np.abs(w_arr))),
            "mean_energy": float(np.mean(np.abs(self.activations))),
            "n_assemblages": len(assemblages),
            "assemblage_sizes": sorted([len(a) for a in assemblages], reverse=True),
            "assemblage_details": a_census,
            "hotspot_activity": hotspot_activity,
            "edges_created_total": self.edges_created,
            "edges_pruned_total": self.edges_pruned,
        }

    def weight_matrix_dense(self):
        W = np.zeros((self.n_nodes, self.n_nodes))
        for (i, j), w in self.weights.items():
            W[i, j] = w
        return W
