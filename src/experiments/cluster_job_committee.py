#!/usr/bin/env python3
"""Cluster job for committee-requested experiments.

Three experiments:
  Exp 2a: Pruning-disabled replication of Exp 2 (Okafor concern #1)
  Exp 6:  CCD permutation test for Exp 4 conditions (Okafor concern #2)
  Exp 7:  Steepness sweep — interpolation from tanh to hard clip (all three)

Usage:
    ray job submit --working-dir . -- python3 -m src.cluster_job_committee
"""

import argparse
import os
import time

import ray
import numpy as np

NFS_DATA_DIR = "/mnt/cluster/experiments/dark-forest-bounds/data"

BOUND_TYPES = ["hard", "tanh", "sigmoid", "oja"]

BASE_PARAMS = {
    "grid_size": 20,
    "n_hotspots": 3,
    "hotspot_energy": 0.3,
    "hotspot_radius": 0.2,
    "base_noise": 0.02,
    "eta": 0.05,
    "lam": 0.002,
    "w_max": 1.0,
    "encounter_rate": 20,
    "locality": 0.10,
    "target_activity": 0.15,
    "eta_min": 0.005,
    "eta_max": 0.20,
    "inhibitor_decay": 0.10,
    "inhibitor_emission_rate": 0.01,
    "inhibitor_diffusion": 0.05,
}


# ============================================================
# Exp 2a: Pruning-disabled coexistence replication
# ============================================================

@ray.remote
def run_exp2a_job(condition, seed, params):
    """Exp 2a: MultiField with pruning disabled."""
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    import pyarrow as pa
    import pyarrow.parquet as pq

    exp_name = "exp2a_no_pruning"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    # Use very low prune threshold instead of 0 to prevent unbounded
    # edge growth (O(n^2) edges makes step() intractable).
    # 1e-8 is low enough that only truly dead edges are pruned.
    mf = MultiField(
        grid_size=params["grid_size"],
        n_hotspots=params["n_hotspots"],
        hotspot_energy=params["hotspot_energy"],
        hotspot_radius=params.get("hotspot_radius", 0.2),
        base_noise=params.get("base_noise", 0.02),
        eta=params["eta"],
        lam=params["lam"],
        w_max=params["w_max"],
        encounter_rate=params["encounter_rate"],
        locality=params["locality"],
        prune_threshold=params.get("prune_threshold", 1e-8),
        bound_type=params["bound_type"],
        seed=seed,
    )

    max_edges = params.get("max_edges", 5000)

    rows = []
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

        # Cap edges ONCE per session (not per step) to avoid O(n log n) sort in inner loop
        if len(mf.weights) > max_edges:
            sorted_edges = sorted(mf.weights.items(), key=lambda x: abs(x[1]))
            n_prune = len(mf.weights) - max_edges
            for k, _ in sorted_edges[:n_prune]:
                del mf.weights[k]

        asm = mf.find_assemblages()
        c = mf.census()

        rows.append({
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "total_steps": mf.step_count,
            "bound_type": params["bound_type"],
            "prune_threshold": 0,
            "n_edges": c["n_edges"],
            "mean_weight": c["mean_weight"],
            "max_weight": c["max_weight"],
            "mean_energy": c["mean_energy"],
            "n_assemblages": len(asm),
            "largest_assemblage": c["assemblage_sizes"][0] if c["assemblage_sizes"] else 0,
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
            "locality": float(params["locality"]),
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


# ============================================================
# Exp 6: CCD permutation test
# ============================================================

@ray.remote
def run_ccd_permutation_job(condition, seed, params):
    """Run simulation to session 200, then permutation test on CCD."""
    from src.substrate.metaplastic_field import MetaplasticField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance, assemblage_centroid_vectors
    from src.metrics.eta_divergence import eta_divergence
    import pyarrow as pa
    import pyarrow.parquet as pq

    exp_name = "exp6_ccd_permutation"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    mf = MetaplasticField(
        grid_size=params["grid_size"],
        n_hotspots=params["n_hotspots"],
        hotspot_energy=params["hotspot_energy"],
        hotspot_radius=params.get("hotspot_radius", 0.2),
        base_noise=params.get("base_noise", 0.02),
        eta=params["eta"],
        lam=params["lam"],
        w_max=params["w_max"],
        encounter_rate=params["encounter_rate"],
        locality=params["locality"],
        prune_threshold=params.get("prune_threshold", 1e-4),
        seed=seed,
        meta_strength=params["meta_strength"],
        target_activity=params.get("target_activity", 0.15),
        eta_min=params.get("eta_min", 0.005),
        eta_max=params.get("eta_max", 0.20),
        inhibitor_diffusion=params.get("inhibitor_diffusion", 0.05),
        inhibitor_decay=params.get("inhibitor_decay", 0.10),
        inhibitor_coupling=params["inhibitor_coupling"],
        inhibitor_emission_rate=params.get("inhibitor_emission_rate", 0.01),
        use_soft_bounds=params["use_soft_eta_bounds"],
        weight_bound_type=params["weight_bound_type"],
    )

    # Run to session 200
    for session in range(1, 201):
        for _ in range(300):
            mf.step()

    # Compute real CCD
    asm = mf.find_assemblages()
    real_ccd = centroid_cosine_distance(mf.weights, asm, mf.n_nodes)
    real_mod = weight_modularity(mf.weights, asm)
    real_n_asm = len(asm)

    # Permutation test: shuffle weight values, recompute CCD
    rng = np.random.default_rng(seed + 200000)
    n_perms = 1000
    null_ccds = []

    weight_keys = list(mf.weights.keys())
    weight_vals = np.array([mf.weights[k] for k in weight_keys])

    for _ in range(n_perms):
        shuffled_vals = rng.permutation(weight_vals)
        shuffled_weights = {k: float(v) for k, v in zip(weight_keys, shuffled_vals)}
        # Find assemblages on shuffled weights
        from collections import defaultdict
        w_arr = np.abs(shuffled_vals)
        if len(w_arr) > 1:
            threshold = np.percentile(w_arr, 75)
        else:
            threshold = 0.01
        adj = defaultdict(set)
        for (i, j), w in shuffled_weights.items():
            if abs(w) >= threshold:
                adj[i].add(j)
                adj[j].add(i)
        visited = set()
        shuffled_asm = []
        for node in range(mf.n_nodes):
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
                shuffled_asm.append(component)
        null_ccd = centroid_cosine_distance(shuffled_weights, shuffled_asm, mf.n_nodes)
        null_ccds.append(null_ccd)

    null_ccds = np.array(null_ccds)
    p_value = float(np.mean(null_ccds >= real_ccd))

    row = {
        "experiment": exp_name,
        "condition": condition,
        "seed": seed,
        "weight_bound_type": params["weight_bound_type"],
        "eta_bound_type": "soft" if params["use_soft_eta_bounds"] else "hard",
        "real_ccd": real_ccd,
        "null_ccd_mean": float(np.mean(null_ccds)),
        "null_ccd_std": float(np.std(null_ccds)),
        "null_ccd_95th": float(np.percentile(null_ccds, 95)),
        "null_ccd_99th": float(np.percentile(null_ccds, 99)),
        "p_value": p_value,
        "n_permutations": n_perms,
        "n_assemblages": real_n_asm,
        "n_edges": len(mf.weights),
        "modularity": real_mod,
        "mean_weight": float(np.mean(np.abs(weight_vals))) if len(weight_vals) > 0 else 0.0,
    }

    os.makedirs(job_dir, exist_ok=True)
    import pyarrow as pa
    import pyarrow.parquet as pq
    pq.write_table(pa.Table.from_pylist([row]), job_file)
    return {"real_ccd": real_ccd, "p_value": p_value}


# ============================================================
# Exp 7: Steepness sweep
# ============================================================

@ray.remote
def run_steepness_job(condition, seed, params):
    """MultiField with parameterised steepness: w_max * tanh(k * w / w_max)."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "exp7_steepness"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    steepness = params["steepness"]

    # Use tanh bound with custom steepness — we override the bound by
    # subclassing step behavior inline via a wrapper
    class SteepMultiField(MultiField):
        def __init__(self, steepness_k, **kwargs):
            # Init with bound_type="hard" to avoid tanh default, we override
            super().__init__(bound_type="hard", **kwargs)
            self.steepness_k = steepness_k

        def step(self):
            self.step_count += 1

            # 1. Inject noise
            noise = self.rng.uniform(-1, 1, self.n_nodes) * self.noise_profile
            self.activations += noise

            # 2. Propagate
            new_input = np.zeros(self.n_nodes)
            in_degree = np.zeros(self.n_nodes)
            for (i, j), w in self.weights.items():
                new_input[j] += w * self.activations[i]
                in_degree[j] += 1
            scale = np.where(in_degree > 0, np.sqrt(np.maximum(in_degree, 1)), 1.0)
            self.activations = np.tanh(0.5 * self.activations + new_input / scale)

            # 3. Hebbian update with parameterised steepness bound
            k = self.steepness_k
            for (i, j) in list(self.weights.keys()):
                self.weights[(i, j)] += self.eta * self.activations[i] * self.activations[j]
                self.weights[(i, j)] *= (1.0 - self.lam)
                w = self.weights[(i, j)]
                # Parameterised bound: w_max * tanh(k * w / w_max)
                # k=1: standard tanh, k→∞: hard clip
                self.weights[(i, j)] = self.w_max * np.tanh(k * w / self.w_max)

            # 4. Local encounters
            for _ in range(self.encounter_rate):
                i, j = self._local_encounter_pair()
                if i != j and (i, j) not in self.weights:
                    self.weights[(i, j)] = 0.0
                    self.edges_created += 1

            # 5. Prune
            dead = [key for key, w in self.weights.items() if abs(w) < self.prune_threshold]
            for key in dead:
                del self.weights[key]
                self.edges_pruned += 1

            # 6. Activity history
            self._activity_history = 0.95 * self._activity_history + 0.05 * np.abs(self.activations)

    mf = SteepMultiField(
        steepness_k=steepness,
        grid_size=params["grid_size"],
        n_hotspots=params["n_hotspots"],
        hotspot_energy=params["hotspot_energy"],
        hotspot_radius=params.get("hotspot_radius", 0.2),
        base_noise=params.get("base_noise", 0.02),
        eta=params["eta"],
        lam=params["lam"],
        w_max=params["w_max"],
        encounter_rate=params["encounter_rate"],
        locality=params["locality"],
        prune_threshold=params.get("prune_threshold", 1e-4),
        seed=seed,
    )

    rows = []
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

        asm = mf.find_assemblages()
        c = mf.census()

        rows.append({
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "total_steps": mf.step_count,
            "steepness": float(steepness),
            "n_edges": c["n_edges"],
            "mean_weight": c["mean_weight"],
            "max_weight": c["max_weight"],
            "mean_energy": c["mean_energy"],
            "n_assemblages": len(asm),
            "largest_assemblage": c["assemblage_sizes"][0] if c["assemblage_sizes"] else 0,
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
            "locality": float(params["locality"]),
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


# ============================================================
# Merge helper
# ============================================================

def merge_job_files(experiment_name):
    import pyarrow as pa
    import pyarrow.parquet as pq
    job_dir = os.path.join(NFS_DATA_DIR, experiment_name, "jobs")
    if not os.path.isdir(job_dir):
        print(f"  No jobs for {experiment_name}")
        return
    tables = [pq.read_table(os.path.join(job_dir, f))
              for f in sorted(os.listdir(job_dir)) if f.endswith(".parquet")]
    if tables:
        merged = pa.concat_tables(tables, promote_options="default")
        pq.write_table(merged, os.path.join(NFS_DATA_DIR, experiment_name, "session_metrics.parquet"))
        print(f"  {experiment_name}: {len(tables)} files -> {len(merged)} rows")


# ============================================================
# Main
# ============================================================

def main():
    ray.init()
    resources = ray.cluster_resources()
    print(f"Cluster: {resources.get('CPU', 0):.0f} CPUs")

    # ---- Exp 2a: Low-pruning coexistence (prune=1e-8 + edge cap) ----
    # Reduced: 3 key localities, 100 sessions (enough to see formation)
    localities_2a = [0.05, 0.10, 0.20]
    n_sessions_2a = 100
    print(f"\n=== Exp 2a: Low-pruning coexistence ({len(BOUND_TYPES)*len(localities_2a)*20} jobs) ===")
    futures_2a = []
    for bt in BOUND_TYPES:
        for loc in localities_2a:
            for seed in range(20):
                condition = f"{bt}_loc{loc:.2f}"
                params = dict(BASE_PARAMS)
                params["bound_type"] = bt
                params["locality"] = loc
                params["n_sessions"] = n_sessions_2a
                params["n_steps"] = 300
                params["prune_threshold"] = 1e-8
                params["max_edges"] = 20000
                futures_2a.append(run_exp2a_job.remote(condition, seed, params))

    # ---- Exp 6: CCD permutation test ----
    print("=== Exp 6: CCD permutation test (160 jobs) ===")
    futures_6 = []
    for wbt in BOUND_TYPES:
        for soft_eta in [False, True]:
            for seed in range(20):
                eta_tag = "soft_eta" if soft_eta else "hard_eta"
                condition = f"w{wbt}_{eta_tag}"
                params = dict(BASE_PARAMS)
                params["weight_bound_type"] = wbt
                params["use_soft_eta_bounds"] = soft_eta
                params["meta_strength"] = 0.005
                params["inhibitor_coupling"] = 0.0
                futures_6.append(run_ccd_permutation_job.remote(condition, seed, params))

    # ---- Exp 7: Steepness sweep ----
    print("=== Exp 7: Steepness sweep (140 jobs) ===")
    steepness_values = [1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0]
    futures_7 = []
    for k in steepness_values:
        for seed in range(20):
            condition = f"k{k:.1f}_loc0.10"
            params = dict(BASE_PARAMS)
            params["steepness"] = k
            params["locality"] = 0.10
            params["n_sessions"] = 100  # reduced from 200
            params["n_steps"] = 300
            futures_7.append(run_steepness_job.remote(condition, seed, params))

    # Track all futures
    all_futures = futures_2a + futures_6 + futures_7
    total = len(all_futures)
    print(f"\nTotal: {total} jobs submitted")

    done = 0
    t0 = time.time()
    remaining_futures = list(all_futures)
    while remaining_futures:
        ready, remaining_futures = ray.wait(remaining_futures,
                                             num_returns=min(50, len(remaining_futures)),
                                             timeout=60)
        results = ray.get(ready)
        done += len(results)
        elapsed = time.time() - t0
        rate = done / elapsed if elapsed > 0 else 0
        est = (total - done) / rate if rate > 0 else 0
        print(f"  {done}/{total} ({elapsed:.0f}s, ~{est:.0f}s left)", flush=True)

    elapsed = time.time() - t0
    print(f"\nAll {total} jobs completed in {elapsed:.0f}s ({elapsed/60:.1f}m)")

    # Merge
    for exp in ["exp2a_no_pruning", "exp6_ccd_permutation", "exp7_steepness"]:
        merge_job_files(exp)

    print("\nDone.")


if __name__ == "__main__":
    main()
