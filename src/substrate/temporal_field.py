"""Temporal Field — MultiField with config switching and anti-Hebbian decorrelation.

Extends MultiField with two mechanisms for investigating differentiation:
1. Temporal environmental variation: hotspot configs switch on a fixed period
2. Anti-Hebbian lateral connections: weaken cross-assemblage co-activation
"""

import numpy as np
from .multifield import MultiField


class TemporalField(MultiField):
    """MultiField with temporal config switching and anti-Hebbian decorrelation.

    Parameters
    ----------
    hotspot_configs : list of list of tuples
        Each config is a list of (x, y) positions for hotspots.
        Configs are cycled through every switch_period steps.
    switch_period : int
        Steps between config switches.
    anti_hebbian_strength : float
        Decorrelation force between assemblages (default 0.0 = off).
    membership_refresh : int
        Steps between assemblage re-detection for anti-Hebbian (default 50).
    **kwargs : passed to MultiField
    """

    def __init__(self, hotspot_configs, switch_period=100,
                 anti_hebbian_strength=0.0, membership_refresh=50,
                 inject_cross_edges=0,
                 inject_init_weight=0.0,
                 **kwargs):
        # Use first config's hotspot count and positions
        self._hotspot_configs = hotspot_configs
        self._config_index = 0
        self.switch_period = switch_period
        self.anti_hebbian_strength = anti_hebbian_strength
        self.membership_refresh = membership_refresh
        self.inject_cross_edges = inject_cross_edges
        self.inject_init_weight = inject_init_weight

        # Initialize with first config
        kwargs['n_hotspots'] = len(hotspot_configs[0])
        super().__init__(**kwargs)

        # Override hotspots with first config
        self.hotspots = list(hotspot_configs[0])
        self.noise_profile = self._compute_noise_profile()

        # Assemblage cache for anti-Hebbian
        self._cached_assemblages = []
        self._last_membership_step = 0

    def _switch_config(self):
        """Switch to next hotspot configuration."""
        self._config_index = (self._config_index + 1) % len(self._hotspot_configs)
        self.hotspots = list(self._hotspot_configs[self._config_index])
        self.noise_profile = self._compute_noise_profile()

    def _refresh_assemblages(self):
        """Re-detect assemblages for anti-Hebbian targeting."""
        self._cached_assemblages = self.find_assemblages()
        self._last_membership_step = self.step_count

    def _inject_cross_assemblage_edges(self):
        """Inject random edges between different assemblages.

        Maintains the structural conditions for anti-Hebbian to operate
        by ensuring cross-assemblage edges persist.
        """
        if not self._cached_assemblages or len(self._cached_assemblages) < 2:
            return

        all_nodes = [list(nodes) for nodes in self._cached_assemblages]
        n_asm = len(all_nodes)
        injected = 0

        max_attempts = self.inject_cross_edges * 20
        attempts = 0
        while injected < self.inject_cross_edges and attempts < max_attempts:
            attempts += 1
            # Pick two different assemblages
            a1 = self.rng.integers(0, n_asm)
            a2 = self.rng.integers(0, n_asm)
            if a1 == a2:
                continue
            i = self.rng.choice(all_nodes[a1])
            j = self.rng.choice(all_nodes[a2])
            if i != j and (i, j) not in self.weights:
                self.weights[(i, j)] = self.inject_init_weight
                self.edges_created += 1
                injected += 1

    def _apply_anti_hebbian(self):
        """Weaken connections between co-active nodes in different assemblages.

        For each pair of assemblages, find edges that connect them and
        apply a decorrelation update: if both endpoints are active with
        the same sign, weaken the connection.
        """
        if not self._cached_assemblages or len(self._cached_assemblages) < 2:
            return

        # Build node-to-assemblage mapping
        node_to_asm = {}
        for asm_idx, nodes in enumerate(self._cached_assemblages):
            for node in nodes:
                node_to_asm[node] = asm_idx

        # Apply anti-Hebbian to cross-assemblage edges
        for (i, j) in list(self.weights.keys()):
            asm_i = node_to_asm.get(i, -1)
            asm_j = node_to_asm.get(j, -1)

            # Only apply between different assemblages (both must be assigned)
            if asm_i >= 0 and asm_j >= 0 and asm_i != asm_j:
                # Anti-Hebbian: weaken when co-active
                co_activation = self.activations[i] * self.activations[j]
                self.weights[(i, j)] -= self.anti_hebbian_strength * co_activation
                self.weights[(i, j)] = np.clip(
                    self.weights[(i, j)], -self.w_max, self.w_max
                )

    def step(self):
        """One step of temporal field dynamics."""
        self.step_count += 1

        # Config switching
        if self.step_count % self.switch_period == 0:
            self._switch_config()

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

        # 3. Hebbian update
        for (i, j) in list(self.weights.keys()):
            self.weights[(i, j)] += self.eta * self.activations[i] * self.activations[j]
            self.weights[(i, j)] *= (1.0 - self.lam)
            self.weights[(i, j)] = np.clip(self.weights[(i, j)], -self.w_max, self.w_max)

        # 4. Anti-Hebbian decorrelation + edge injection
        if self.anti_hebbian_strength > 0 or self.inject_cross_edges > 0:
            # Refresh assemblage membership periodically
            if (self.step_count - self._last_membership_step) >= self.membership_refresh:
                self._refresh_assemblages()
            if self.anti_hebbian_strength > 0:
                self._apply_anti_hebbian()
            if self.inject_cross_edges > 0:
                self._inject_cross_assemblage_edges()

        # 5. Strictly local encounters
        for _ in range(self.encounter_rate):
            i, j = self._local_encounter_pair()
            if i != j and (i, j) not in self.weights:
                self.weights[(i, j)] = 0.0
                self.edges_created += 1

        # 6. Prune dead connections
        dead = [k for k, w in self.weights.items() if abs(w) < self.prune_threshold]
        for k in dead:
            del self.weights[k]
            self.edges_pruned += 1

        # 7. Update activity history
        self._activity_history = 0.95 * self._activity_history + 0.05 * np.abs(self.activations)
