#!/usr/bin/env python3
"""Phase 1A: Steepness sweep WITHOUT pruning + no-prune baselines.

Combined cluster job:
  - Exp 7b: Steepness sweep with pruning disabled (re-run of Exp 7)
  - Exp 2b: Hard clip baseline without pruning at locality=0.10 (for comparison)

Total: (7 steepness + 4 bound_types) × 20 seeds = 220 jobs

Usage:
    ray job submit --address http://192.168.1.11:8265 \
        --working-dir . \
        --runtime-env-json '{"pip": ["numpy", "pyarrow", "scikit-learn"], "excludes": ["data/", "papers/", ".git/", ".pytest_cache/"]}' \
        --no-wait \
        -- python3 -m src.cluster_job_phase1
"""

import os
import time

import ray
import numpy as np

NFS_DATA_DIR = "/mnt/cluster/experiments/dark-forest-bounds/data"

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
    "n_sessions": 100,
    "n_steps": 300,
}


# ============================================================
# Exp 7b: Steepness sweep without pruning
# ============================================================

@ray.remote
def run_steepness_noprune_job(condition, seed, params):
    """Steepness sweep with pruning disabled (max_edges cap instead)."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "exp7b_steepness_noprune"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    steepness = params["steepness"]
    max_edges = params.get("max_edges", 20000)

    class SteepMultiField(MultiField):
        def __init__(self, steepness_k, **kwargs):
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
                self.weights[(i, j)] = self.w_max * np.tanh(k * w / self.w_max)

            # 4. Local encounters
            for _ in range(self.encounter_rate):
                i, j = self._local_encounter_pair()
                if i != j and (i, j) not in self.weights:
                    self.weights[(i, j)] = 0.0
                    self.edges_created += 1

            # 5. NO pruning — use prune_threshold=1e-8 (near-zero)
            dead = [key for key, w in self.weights.items() if abs(w) < 1e-8]
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
        prune_threshold=1e-8,  # effectively disabled
        seed=seed,
    )

    rows = []
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

        # Cap edges per session (rank-based, not threshold-based)
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
# Exp 2b: All bound types without pruning at loc=0.10
# (provides clean baselines for comparison with steepness sweep)
# ============================================================

@ray.remote
def run_baseline_noprune_job(condition, seed, params):
    """Standard MultiField with pruning disabled."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "exp2b_baseline_noprune"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    max_edges = params.get("max_edges", 20000)

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
        prune_threshold=1e-8,
        bound_type=params["bound_type"],
        seed=seed,
    )

    rows = []
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

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
        out = os.path.join(NFS_DATA_DIR, experiment_name, "session_metrics.parquet")
        pq.write_table(merged, out)
        # Also copy locally
        local_dir = os.path.join(os.path.expanduser("~"), "research", "dark-forest-bounds", "data", experiment_name)
        os.makedirs(local_dir, exist_ok=True)
        pq.write_table(merged, os.path.join(local_dir, "session_metrics.parquet"))
        print(f"  {experiment_name}: {len(tables)} files -> {len(merged)} rows")


# ============================================================
# Main
# ============================================================

def main():
    ray.init()
    resources = ray.cluster_resources()
    print(f"Cluster: {resources.get('CPU', 0):.0f} CPUs")

    # ---- Exp 7b: Steepness sweep without pruning ----
    steepness_values = [1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0]
    n_seeds = 20
    print(f"\n=== Exp 7b: Steepness no-prune ({len(steepness_values)*n_seeds} jobs) ===")
    futures_7b = []
    for k in steepness_values:
        for seed in range(n_seeds):
            condition = f"k{k:.1f}_loc0.10"
            params = dict(BASE_PARAMS)
            params["steepness"] = k
            params["max_edges"] = 20000
            futures_7b.append(run_steepness_noprune_job.remote(condition, seed, params))

    # ---- Exp 2b: Baseline no-prune for all bound types ----
    bound_types = ["hard", "tanh", "sigmoid", "oja"]
    print(f"=== Exp 2b: Baseline no-prune ({len(bound_types)*n_seeds} jobs) ===")
    futures_2b = []
    for bt in bound_types:
        for seed in range(n_seeds):
            condition = f"{bt}_loc0.10"
            params = dict(BASE_PARAMS)
            params["bound_type"] = bt
            params["max_edges"] = 20000
            futures_2b.append(run_baseline_noprune_job.remote(condition, seed, params))

    # Track
    all_futures = futures_7b + futures_2b
    total = len(all_futures)
    print(f"\nTotal: {total} jobs submitted")

    done = 0
    t0 = time.time()
    remaining = list(all_futures)
    while remaining:
        ready, remaining = ray.wait(remaining,
                                     num_returns=min(50, len(remaining)),
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
    for exp in ["exp7b_steepness_noprune", "exp2b_baseline_noprune"]:
        merge_job_files(exp)

    print("\nPhase 1A complete.")


if __name__ == "__main__":
    main()
