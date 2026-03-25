#!/usr/bin/env python3
"""Paper 4S Revision Experiments — Addressing Reviewer Concerns.

Three experiment groups:

  Rev1: Edge cap sensitivity sweep (R2-M1, Editor #1)
        4 cap values × 3 bound types × 2 prune conditions × 20 seeds = 480 jobs
        Tests whether disordinal interaction is cap-dependent.

  Rev2: Grid size generality (R1-M1, Editor #5)
        2 grid sizes (15×15, 30×30) × 3 bounds × 2 prune × 20 seeds = 240 jobs
        Shows interaction persists across network scales.

  Rev3: Response rank with participation ratio + full SVD spectra (R1-M3, R2-M3, Editor #2)
        3 bounds × 2 prune × 30 seeds = 180 jobs
        Saves full singular value spectra for scree plots + computes participation ratio.

Total: 900 jobs, estimated ~8-10 hours on 36 CPUs.

Usage:
    cd ~/research/dark-forest-bounds
    ray job submit --address http://192.168.1.11:8265 \
        --working-dir . \
        --runtime-env-json '{"pip": ["numpy", "pyarrow", "scikit-learn", "scipy"], "excludes": ["data/", "papers/", ".git/", ".pytest_cache/"]}' \
        --no-wait \
        -- python3 -m src.cluster_job_revision
"""

import json
import os
import time

import ray
import numpy as np

NFS_DATA_DIR = "/mnt/cluster/experiments/dark-forest-bounds/data"
LOCAL_DATA_DIR = os.path.expanduser("~/research/dark-forest-bounds/data")

# Drop sigmoid per committee decision
BOUND_TYPES = ["hard", "tanh", "oja"]

BASE_PARAMS = {
    "n_hotspots": 3,
    "hotspot_energy": 0.3,
    "hotspot_radius": 0.2,
    "base_noise": 0.02,
    "eta": 0.05,
    "lam": 0.002,
    "w_max": 1.0,
    "encounter_rate": 20,
    "locality": 0.10,
}


# ============================================================
# Rev1: Edge cap sensitivity sweep
# ============================================================

@ray.remote
def run_cap_sweep_job(condition, seed, params):
    """Test whether results depend on max_edges cap value."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "rev1_cap_sweep"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    prune_on = params["prune_on"]
    prune_threshold = 1e-4 if prune_on else 1e-8
    max_edges = params["max_edges"]  # The variable under test
    grid_size = params.get("grid_size", 20)

    mf = MultiField(
        grid_size=grid_size,
        n_hotspots=params["n_hotspots"],
        hotspot_energy=params["hotspot_energy"],
        hotspot_radius=params.get("hotspot_radius", 0.2),
        base_noise=params.get("base_noise", 0.02),
        eta=params["eta"],
        lam=params["lam"],
        w_max=params["w_max"],
        encounter_rate=params["encounter_rate"],
        locality=params["locality"],
        prune_threshold=prune_threshold,
        bound_type=params["bound_type"],
        seed=seed,
    )

    rows = []
    for session in range(1, 201):
        for _ in range(300):
            mf.step()

        # Apply cap only when pruning is off and cap is not "unlimited"
        if not prune_on and max_edges > 0 and len(mf.weights) > max_edges:
            sorted_edges = sorted(mf.weights.items(), key=lambda x: abs(x[1]))
            for k, _ in sorted_edges[:len(mf.weights) - max_edges]:
                del mf.weights[k]

        asm = mf.find_assemblages()
        c = mf.census()

        rows.append({
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "bound_type": params["bound_type"],
            "prune_on": prune_on,
            "max_edges": max_edges,
            "grid_size": grid_size,
            "n_edges": c["n_edges"],
            "mean_weight": c["mean_weight"],
            "max_weight": c["max_weight"],
            "n_assemblages": len(asm),
            "largest_assemblage": c["assemblage_sizes"][0] if c["assemblage_sizes"] else 0,
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


# ============================================================
# Rev2: Grid size generality
# ============================================================

@ray.remote
def run_grid_size_job(condition, seed, params):
    """Test disordinal interaction at different grid sizes."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "rev2_grid_size"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    prune_on = params["prune_on"]
    grid_size = params["grid_size"]
    prune_threshold = 1e-4 if prune_on else 1e-8
    # Scale max_edges with grid size: 20×20=400 nodes → 20k cap; scale proportionally
    n_nodes = grid_size * grid_size
    max_edges = int(20000 * (n_nodes / 400))

    mf = MultiField(
        grid_size=grid_size,
        n_hotspots=params["n_hotspots"],
        hotspot_energy=params["hotspot_energy"],
        hotspot_radius=params.get("hotspot_radius", 0.2),
        base_noise=params.get("base_noise", 0.02),
        eta=params["eta"],
        lam=params["lam"],
        w_max=params["w_max"],
        encounter_rate=params["encounter_rate"],
        locality=params["locality"],
        prune_threshold=prune_threshold,
        bound_type=params["bound_type"],
        seed=seed,
    )

    rows = []
    for session in range(1, 201):
        for _ in range(300):
            mf.step()

        if not prune_on and len(mf.weights) > max_edges:
            sorted_edges = sorted(mf.weights.items(), key=lambda x: abs(x[1]))
            for k, _ in sorted_edges[:len(mf.weights) - max_edges]:
                del mf.weights[k]

        asm = mf.find_assemblages()
        c = mf.census()

        rows.append({
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "bound_type": params["bound_type"],
            "prune_on": prune_on,
            "grid_size": grid_size,
            "n_edges": c["n_edges"],
            "mean_weight": c["mean_weight"],
            "n_assemblages": len(asm),
            "largest_assemblage": c["assemblage_sizes"][0] if c["assemblage_sizes"] else 0,
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


# ============================================================
# Rev3: Response rank with full SVD spectra + participation ratio
# ============================================================

@ray.remote
def run_rank_validation_job(condition, seed, params):
    """Full SVD analysis: scree plots, threshold sweep, participation ratio."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from scipy.spatial.distance import jensenshannon

    exp_name = "rev3_rank_validation"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    prune_on = params["prune_on"]
    prune_threshold = 1e-4 if prune_on else 1e-8
    max_edges = 5000 if prune_on else 20000

    mf = MultiField(
        grid_size=params.get("grid_size", 20),
        n_hotspots=params["n_hotspots"],
        hotspot_energy=params["hotspot_energy"],
        hotspot_radius=params.get("hotspot_radius", 0.2),
        base_noise=params.get("base_noise", 0.02),
        eta=params["eta"],
        lam=params["lam"],
        w_max=params["w_max"],
        encounter_rate=params["encounter_rate"],
        locality=params["locality"],
        prune_threshold=prune_threshold,
        bound_type=params["bound_type"],
        seed=seed,
    )

    # Train 200 sessions
    for session in range(200):
        for _ in range(300):
            mf.step()
        if not prune_on and len(mf.weights) > max_edges:
            sorted_edges = sorted(mf.weights.items(), key=lambda x: abs(x[1]))
            for k, _ in sorted_edges[:len(mf.weights) - max_edges]:
                del mf.weights[k]

    asm = mf.find_assemblages()
    n_asm = len(asm)
    ccd = centroid_cosine_distance(mf.weights, asm, mf.n_nodes)

    if n_asm < 2:
        row = {
            "experiment": exp_name, "condition": condition, "seed": seed,
            "bound_type": params["bound_type"], "prune_on": prune_on,
            "n_assemblages": n_asm, "n_edges": len(mf.weights),
            "mean_weight": float(np.mean(np.abs(list(mf.weights.values())))) if mf.weights else 0,
            "ccd": ccd,
            "singular_values_json": "[]",
            "rank_at_001": 0, "rank_at_005": 0, "rank_at_01": 0,
            "rank_at_05": 0, "rank_at_10": 0,
            "participation_ratio": 0.0,
            "uniform_rank_at_01": 0, "uniform_participation_ratio": 0.0,
            "uniform_singular_values_json": "[]",
            "n_probes": 0,
        }
        os.makedirs(job_dir, exist_ok=True)
        pq.write_table(pa.Table.from_pylist([row]), job_file)
        return row

    saved_activations = mf.activations.copy()
    saved_weights = dict(mf.weights)
    probe_rng = np.random.default_rng(seed + 777777)

    def run_probes_svd(stimulus_fn, n_probes=10):
        """Run probes, return full SVD analysis."""
        responses = []
        for _ in range(n_probes):
            mf.activations = saved_activations.copy()
            mf.weights = dict(saved_weights)
            stimulus = stimulus_fn()
            mf.activations += stimulus
            for __ in range(10):
                new_input = np.zeros(mf.n_nodes)
                in_degree = np.zeros(mf.n_nodes)
                for (i, j), w in mf.weights.items():
                    new_input[j] += w * mf.activations[i]
                    in_degree[j] += 1
                scale = np.where(in_degree > 0, np.sqrt(np.maximum(in_degree, 1)), 1.0)
                mf.activations = np.tanh(0.5 * mf.activations + new_input / scale)
            asm_resp = [float(np.mean(mf.activations[list(nodes)])) for nodes in asm]
            responses.append(asm_resp)

        rm = np.array(responses).T  # (n_asm, n_probes)
        U, S, Vt = np.linalg.svd(rm - rm.mean(axis=0), full_matrices=False)

        # Rank at multiple thresholds
        ranks = {}
        for pct in [0.001, 0.005, 0.01, 0.05, 0.10]:
            thresh = pct * S[0] if S[0] > 0 else 1e-10
            ranks[pct] = int(np.sum(S > thresh))

        # Participation ratio (threshold-free effective dimensionality)
        s_sq = S**2
        total = np.sum(s_sq)
        if total > 0:
            p = s_sq / total
            participation_ratio = float(1.0 / np.sum(p**2))
        else:
            participation_ratio = 0.0

        return S, ranks, participation_ratio

    # Gaussian probes (structured)
    def gaussian_stimulus():
        cx, cy = probe_rng.uniform(0.1, 0.9, 2)
        d = np.sqrt((mf.pos_x - cx)**2 + (mf.pos_y - cy)**2)
        return 0.5 * np.exp(-d**2 / (2 * 0.1**2))

    # Uniform probes (deconfounded)
    def uniform_stimulus():
        return probe_rng.uniform(-0.3, 0.3, mf.n_nodes)

    S_gauss, ranks_gauss, pr_gauss = run_probes_svd(gaussian_stimulus, n_probes=10)
    S_uniform, ranks_uniform, pr_uniform = run_probes_svd(uniform_stimulus, n_probes=10)

    row = {
        "experiment": exp_name, "condition": condition, "seed": seed,
        "bound_type": params["bound_type"], "prune_on": prune_on,
        "n_assemblages": n_asm, "n_edges": len(saved_weights),
        "mean_weight": float(np.mean(np.abs(list(saved_weights.values())))) if saved_weights else 0,
        "ccd": ccd,
        # Gaussian probes
        "singular_values_json": json.dumps(S_gauss.tolist()),
        "rank_at_001": ranks_gauss[0.001],
        "rank_at_005": ranks_gauss[0.005],
        "rank_at_01": ranks_gauss[0.01],
        "rank_at_05": ranks_gauss[0.05],
        "rank_at_10": ranks_gauss[0.10],
        "participation_ratio": pr_gauss,
        # Uniform probes
        "uniform_singular_values_json": json.dumps(S_uniform.tolist()),
        "uniform_rank_at_01": ranks_uniform[0.01],
        "uniform_participation_ratio": pr_uniform,
        "n_probes": 10,
    }

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist([row]), job_file)
    return row


# ============================================================
# Merge + copy
# ============================================================

def merge_and_copy(experiment_name):
    import pyarrow as pa
    import pyarrow.parquet as pq
    job_dir = os.path.join(NFS_DATA_DIR, experiment_name, "jobs")
    if not os.path.isdir(job_dir):
        print(f"  No jobs for {experiment_name}")
        return
    tables = []
    for f in sorted(os.listdir(job_dir)):
        if f.endswith(".parquet"):
            t = pq.read_table(os.path.join(job_dir, f))
            for i, field in enumerate(t.schema):
                if field.type == pa.int64() and field.name not in (
                    'seed', 'n_assemblages', 'n_edges', 'session', 'grid_size',
                    'max_edges', 'largest_assemblage', 'n_probes',
                    'rank_at_001', 'rank_at_005', 'rank_at_01', 'rank_at_05',
                    'rank_at_10', 'uniform_rank_at_01',
                ):
                    t = t.set_column(i, field.name, t.column(i).cast(pa.float64()))
            tables.append(t)
    if tables:
        merged = pa.concat_tables(tables, promote_options="default")
        pq.write_table(merged, os.path.join(NFS_DATA_DIR, experiment_name, "session_metrics.parquet"))
        local_dir = os.path.join(LOCAL_DATA_DIR, experiment_name)
        os.makedirs(local_dir, exist_ok=True)
        pq.write_table(merged, os.path.join(local_dir, "session_metrics.parquet"))
        print(f"  {experiment_name}: {len(tables)} files -> {len(merged)} rows")


def _wait_all(futures, label):
    total = len(futures)
    done = 0
    t0 = time.time()
    remaining = list(futures)
    while remaining:
        ready, remaining = ray.wait(remaining, num_returns=min(50, len(remaining)), timeout=60)
        results = ray.get(ready)
        done += len(results)
        elapsed = time.time() - t0
        rate = done / elapsed if elapsed > 0 else 0
        est = (total - done) / rate if rate > 0 else 0
        print(f"  [{label}] {done}/{total} ({elapsed:.0f}s, ~{est:.0f}s left)", flush=True)
    elapsed = time.time() - t0
    print(f"  [{label}] Complete: {total} jobs in {elapsed:.0f}s ({elapsed/60:.1f}m)")


# ============================================================
# Main
# ============================================================

def main():
    ray.init()
    resources = ray.cluster_resources()
    print(f"Cluster: {resources.get('CPU', 0):.0f} CPUs")
    t_start = time.time()
    n_seeds = 20

    # ================================================================
    # Rev1: Edge cap sensitivity (R2's critical concern)
    # 4 cap values × 3 bounds × no-prune only × 20 seeds = 240 jobs
    # Also: pruned baseline (cap irrelevant) × 3 bounds × 20 = 60 jobs
    # Plus: unlimited (cap=0) × 3 bounds × 20 = 60 jobs
    # Total: 360 jobs
    # ================================================================
    print(f"\n{'='*60}")
    print("Rev1: Edge cap sensitivity sweep (360 jobs, 200 sessions)")
    print(f"{'='*60}")

    cap_values = [5000, 10000, 20000, 50000]  # 0 = unlimited handled separately
    futures_rev1 = []

    # Pruned baseline (cap irrelevant)
    for bt in BOUND_TYPES:
        for seed in range(n_seeds):
            condition = f"{bt}_pruned_cap0"
            params = dict(BASE_PARAMS)
            params["grid_size"] = 20
            params["bound_type"] = bt
            params["prune_on"] = True
            params["max_edges"] = 0  # irrelevant when pruning is on
            futures_rev1.append(run_cap_sweep_job.remote(condition, seed, params))

    # No-prune with varying caps
    for cap in cap_values:
        for bt in BOUND_TYPES:
            for seed in range(n_seeds):
                condition = f"{bt}_noprune_cap{cap}"
                params = dict(BASE_PARAMS)
                params["grid_size"] = 20
                params["bound_type"] = bt
                params["prune_on"] = False
                params["max_edges"] = cap
                futures_rev1.append(run_cap_sweep_job.remote(condition, seed, params))

    # Unlimited (no cap at all) — max_edges=0 signals no capping
    for bt in BOUND_TYPES:
        for seed in range(n_seeds):
            condition = f"{bt}_noprune_unlimited"
            params = dict(BASE_PARAMS)
            params["grid_size"] = 20
            params["bound_type"] = bt
            params["prune_on"] = False
            params["max_edges"] = 0  # 0 = no cap
            futures_rev1.append(run_cap_sweep_job.remote(condition, seed, params))

    _wait_all(futures_rev1, "Rev1")
    merge_and_copy("rev1_cap_sweep")

    # ================================================================
    # Rev2: Grid size generality (15×15 and 30×30)
    # 2 sizes × 3 bounds × 2 prune × 20 seeds = 240 jobs
    # ================================================================
    print(f"\n{'='*60}")
    print("Rev2: Grid size generality (240 jobs, 200 sessions)")
    print(f"{'='*60}")

    futures_rev2 = []
    for gs in [15, 30]:
        for bt in BOUND_TYPES:
            for prune_on in [True, False]:
                tag = "pruned" if prune_on else "noprune"
                for seed in range(n_seeds):
                    condition = f"{bt}_{tag}_gs{gs}"
                    params = dict(BASE_PARAMS)
                    params["grid_size"] = gs
                    params["bound_type"] = bt
                    params["prune_on"] = prune_on
                    futures_rev2.append(run_grid_size_job.remote(condition, seed, params))

    _wait_all(futures_rev2, "Rev2")
    merge_and_copy("rev2_grid_size")

    # ================================================================
    # Rev3: Response rank validation (full SVD + participation ratio)
    # 3 bounds × 2 prune × 30 seeds = 180 jobs
    # ================================================================
    print(f"\n{'='*60}")
    print("Rev3: Response rank validation (180 jobs, 200 sessions + probes)")
    print(f"{'='*60}")

    futures_rev3 = []
    for bt in BOUND_TYPES:
        for prune_on in [True, False]:
            tag = "pruned" if prune_on else "noprune"
            for seed in range(30):
                condition = f"{bt}_{tag}"
                params = dict(BASE_PARAMS)
                params["grid_size"] = 20
                params["bound_type"] = bt
                params["prune_on"] = prune_on
                futures_rev3.append(run_rank_validation_job.remote(condition, seed, params))

    _wait_all(futures_rev3, "Rev3")
    merge_and_copy("rev3_rank_validation")

    # ================================================================
    # Summary
    # ================================================================
    elapsed = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"ALL REVISION EXPERIMENTS COMPLETE in {elapsed:.0f}s ({elapsed/3600:.1f}h)")
    print(f"{'='*60}")
    print("  rev1_cap_sweep       — edge cap sensitivity (5k/10k/20k/50k/unlimited)")
    print("  rev2_grid_size       — generality (15×15, 30×30)")
    print("  rev3_rank_validation — SVD spectra, threshold sweep, participation ratio")


if __name__ == "__main__":
    main()
