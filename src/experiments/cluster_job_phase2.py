#!/usr/bin/env python3
"""Phase 2+3: Full experiment battery for Paper 4S revision.

Runs autonomously on the cluster (no laptop needed).

Experiments:
  F:  2×2 factorial — pruning on/off × 4 bound types, n=30, loc=0.10
  B:  Pruning threshold sweep — {1e-6, 1e-5, 1e-4, 1e-3, 1e-2} × 4 bounds × 20 seeds
  E:  Eta distribution snapshots — MetaplasticField with node_eta saved per session
  R:  Response-profile divergence — stimulus-response protocol for functional differentiation

Total: ~1340 jobs, estimated ~6-8 hours on 36 CPUs.

Usage:
    ray job submit --address http://192.168.1.11:8265 \
        --working-dir . \
        --runtime-env-json '{"pip": ["numpy", "pyarrow", "scikit-learn"], "excludes": ["data/", "papers/", ".git/", ".pytest_cache/"]}' \
        --no-wait \
        -- python3 -m src.cluster_job_phase2
"""

import os
import time

import ray
import numpy as np

NFS_DATA_DIR = "/mnt/cluster/experiments/dark-forest-bounds/data"
LOCAL_DATA_DIR = os.path.expanduser("~/research/dark-forest-bounds/data")

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
# Exp F: 2×2 factorial — pruning on/off × bound type
# ============================================================

@ray.remote
def run_factorial_job(condition, seed, params):
    """2x2 factorial: pruning × bound type."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "expF_factorial"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    prune_on = params["prune_on"]
    prune_threshold = 1e-4 if prune_on else 1e-8
    max_edges = 5000 if prune_on else 20000

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
            "total_steps": mf.step_count,
            "bound_type": params["bound_type"],
            "prune_on": prune_on,
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
# Exp B: Pruning threshold sweep
# ============================================================

@ray.remote
def run_prune_sweep_job(condition, seed, params):
    """Sweep pruning threshold to characterise the confound."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "expB_prune_sweep"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    pt = params["prune_threshold_value"]
    # For very low thresholds, cap edges to prevent memory explosion
    max_edges = 20000 if pt < 1e-4 else 5000

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
        prune_threshold=pt,
        bound_type=params["bound_type"],
        seed=seed,
    )

    rows = []
    for session in range(1, 101):
        for _ in range(300):
            mf.step()

        if len(mf.weights) > max_edges:
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
            "total_steps": mf.step_count,
            "bound_type": params["bound_type"],
            "prune_threshold": pt,
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
# Exp E: Eta distribution snapshots (MetaplasticField)
# Saves per-node eta at final session for between/within
# assemblage variance analysis.
# ============================================================

@ray.remote
def run_eta_snapshot_job(condition, seed, params):
    """MetaplasticField run saving eta snapshots for variance analysis."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.metaplastic_field import MetaplasticField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "expE_eta_snapshots"
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

    rows = []
    snapshot_sessions = {50, 100, 150, 200}  # Save eta snapshots at these

    for session in range(1, 201):
        for _ in range(300):
            mf.step()

        asm = mf.find_assemblages()
        c = mf.census()

        row = {
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "total_steps": mf.step_count,
            "weight_bound_type": params["weight_bound_type"],
            "eta_bound_type": "soft" if params["use_soft_eta_bounds"] else "hard",
            "meta_strength": params["meta_strength"],
            "inhibitor_coupling": params["inhibitor_coupling"],
            "n_edges": c["n_edges"],
            "mean_weight": c["mean_weight"],
            "n_assemblages": len(asm),
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
        }

        # Eta distribution stats
        row["eta_mean"] = float(np.mean(mf.node_eta))
        row["eta_std"] = float(np.std(mf.node_eta))
        row["eta_min_val"] = float(np.min(mf.node_eta))
        row["eta_max_val"] = float(np.max(mf.node_eta))
        row["pct_eta_at_min"] = float(np.mean(mf.node_eta <= params["eta_min"] + 1e-6))
        row["pct_eta_at_max"] = float(np.mean(mf.node_eta >= params["eta_max"] - 1e-6))

        # Between- vs within-assemblage eta variance
        if len(asm) >= 2 and session in snapshot_sessions:
            asm_means = []
            within_vars = []
            for nodes in asm:
                node_list = list(nodes)
                etas = mf.node_eta[node_list]
                asm_means.append(np.mean(etas))
                within_vars.append(np.var(etas))
            row["eta_between_var"] = float(np.var(asm_means))
            row["eta_within_var"] = float(np.mean(within_vars))
            row["eta_f_ratio"] = float(np.var(asm_means) / max(np.mean(within_vars), 1e-12))
            # Serialize eta snapshot as comma-separated string (compact)
            row["eta_snapshot"] = ",".join(f"{e:.6f}" for e in mf.node_eta)
        else:
            row["eta_between_var"] = None
            row["eta_within_var"] = None
            row["eta_f_ratio"] = None
            row["eta_snapshot"] = None

        rows.append(row)

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


# ============================================================
# Exp R: Response-profile divergence
# Run simulation to steady state, then probe each assemblage
# with standardized stimuli and measure response diversity.
# ============================================================

@ray.remote
def run_response_profile_job(condition, seed, params):
    """Functional differentiation via stimulus-response divergence."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from scipy.spatial.distance import jensenshannon

    exp_name = "expR_response_profile"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    prune_on = params["prune_on"]
    prune_threshold = 1e-4 if prune_on else 1e-8
    max_edges = 5000 if prune_on else 20000

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
        prune_threshold=prune_threshold,
        bound_type=params["bound_type"],
        seed=seed,
    )

    # Phase 1: Run to steady state (200 sessions)
    for session in range(200):
        for _ in range(300):
            mf.step()
        if not prune_on and len(mf.weights) > max_edges:
            sorted_edges = sorted(mf.weights.items(), key=lambda x: abs(x[1]))
            for k, _ in sorted_edges[:len(mf.weights) - max_edges]:
                del mf.weights[k]

    # Record baseline state
    asm = mf.find_assemblages()
    n_asm = len(asm)
    baseline_ccd = centroid_cosine_distance(mf.weights, asm, mf.n_nodes)
    baseline_mod = weight_modularity(mf.weights, asm)

    if n_asm < 2:
        # Can't measure divergence with <2 assemblages
        row = {
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "bound_type": params["bound_type"],
            "prune_on": prune_on,
            "n_assemblages": n_asm,
            "n_edges": len(mf.weights),
            "mean_weight": float(np.mean(np.abs(list(mf.weights.values())))) if mf.weights else 0,
            "baseline_ccd": baseline_ccd,
            "baseline_modularity": baseline_mod,
            "mean_js_divergence": None,
            "max_js_divergence": None,
            "response_rank": None,
            "response_dimensionality": None,
            "n_probes": 0,
        }
        os.makedirs(job_dir, exist_ok=True)
        pq.write_table(pa.Table.from_pylist([row]), job_file)
        return row

    # Phase 2: Probe each assemblage with standardized stimuli
    # Save current state for reset between probes
    saved_activations = mf.activations.copy()
    saved_weights = dict(mf.weights)

    n_probes = 5  # different stimulus patterns
    probe_rng = np.random.default_rng(seed + 999999)

    # Generate probe stimuli: Gaussian bumps at different positions
    probe_responses = []  # shape: (n_probes, n_asm, n_nodes)

    for probe_idx in range(n_probes):
        # Random stimulus location
        cx = probe_rng.uniform(0.1, 0.9)
        cy = probe_rng.uniform(0.1, 0.9)
        stimulus_strength = 0.5

        # Reset state
        mf.activations = saved_activations.copy()
        mf.weights = dict(saved_weights)

        # Inject stimulus: Gaussian centered at (cx, cy)
        distances = np.sqrt((mf.pos_x - cx)**2 + (mf.pos_y - cy)**2)
        stimulus = stimulus_strength * np.exp(-distances**2 / (2 * 0.1**2))
        mf.activations += stimulus

        # Propagate for 10 steps (short-term response)
        for _ in range(10):
            # Propagate only, no learning or encounters
            new_input = np.zeros(mf.n_nodes)
            in_degree = np.zeros(mf.n_nodes)
            for (i, j), w in mf.weights.items():
                new_input[j] += w * mf.activations[i]
                in_degree[j] += 1
            scale = np.where(in_degree > 0, np.sqrt(np.maximum(in_degree, 1)), 1.0)
            mf.activations = np.tanh(0.5 * mf.activations + new_input / scale)

        # Record response per assemblage (mean activation of member nodes)
        asm_responses = []
        for nodes in asm:
            node_list = list(nodes)
            asm_responses.append(float(np.mean(mf.activations[node_list])))
        probe_responses.append(asm_responses)

    # Phase 3: Compute response-profile divergence
    # Build response matrix: (n_asm × n_probes)
    response_matrix = np.array(probe_responses).T  # (n_asm, n_probes)

    # Normalize rows to probability distributions for JS divergence
    # Shift to positive, then normalize
    response_shifted = response_matrix - response_matrix.min(axis=1, keepdims=True) + 1e-8
    response_probs = response_shifted / response_shifted.sum(axis=1, keepdims=True)

    # Pairwise JS divergence between assemblages
    js_divs = []
    for i in range(n_asm):
        for j in range(i + 1, n_asm):
            js = jensenshannon(response_probs[i], response_probs[j])
            if np.isfinite(js):
                js_divs.append(js)

    # Response dimensionality via SVD
    if response_matrix.shape[0] >= 2:
        U, s, Vt = np.linalg.svd(response_matrix - response_matrix.mean(axis=0), full_matrices=False)
        # Effective rank (participation ratio of singular values)
        s_norm = s**2 / np.sum(s**2) if np.sum(s**2) > 0 else s
        eff_rank = float(1.0 / np.sum(s_norm**2)) if np.sum(s_norm**2) > 0 else 0
    else:
        eff_rank = 0

    row = {
        "experiment": exp_name,
        "condition": condition,
        "seed": seed,
        "bound_type": params["bound_type"],
        "prune_on": prune_on,
        "n_assemblages": n_asm,
        "n_edges": len(saved_weights),
        "mean_weight": float(np.mean(np.abs(list(saved_weights.values())))) if saved_weights else 0,
        "baseline_ccd": baseline_ccd,
        "baseline_modularity": baseline_mod,
        "mean_js_divergence": float(np.mean(js_divs)) if js_divs else 0,
        "max_js_divergence": float(np.max(js_divs)) if js_divs else 0,
        "response_rank": eff_rank,
        "response_dimensionality": float(np.linalg.matrix_rank(response_matrix, tol=0.01)) if response_matrix.shape[0] >= 2 else 0,
        "n_probes": n_probes,
    }

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist([row]), job_file)
    return row


# ============================================================
# Merge helper
# ============================================================

def merge_and_copy(experiment_name):
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
        nfs_out = os.path.join(NFS_DATA_DIR, experiment_name, "session_metrics.parquet")
        pq.write_table(merged, nfs_out)
        local_dir = os.path.join(LOCAL_DATA_DIR, experiment_name)
        os.makedirs(local_dir, exist_ok=True)
        pq.write_table(merged, os.path.join(local_dir, "session_metrics.parquet"))
        print(f"  {experiment_name}: {len(tables)} files -> {len(merged)} rows")


# ============================================================
# Main — runs all experiments sequentially by phase
# ============================================================

def main():
    ray.init()
    resources = ray.cluster_resources()
    cpus = resources.get("CPU", 0)
    print(f"Cluster: {cpus:.0f} CPUs")
    print(f"NFS: {NFS_DATA_DIR}")
    t_start = time.time()

    # ================================================================
    # PHASE 2a: Exp F — 2×2 factorial (pruning × bound type)
    # 2 prune conditions × 4 bound types × 30 seeds = 240 jobs
    # ================================================================
    print(f"\n{'='*60}")
    print("PHASE 2a: Exp F — 2×2 factorial (240 jobs, 200 sessions each)")
    print(f"{'='*60}")
    futures_F = []
    for bt in BOUND_TYPES:
        for prune_on in [True, False]:
            prune_tag = "pruned" if prune_on else "noprune"
            for seed in range(30):
                condition = f"{bt}_{prune_tag}"
                params = dict(BASE_PARAMS)
                params["bound_type"] = bt
                params["prune_on"] = prune_on
                futures_F.append(run_factorial_job.remote(condition, seed, params))

    done = _wait_all(futures_F, "Exp F")
    merge_and_copy("expF_factorial")

    # ================================================================
    # PHASE 2b: Exp B — Pruning threshold sweep
    # 5 thresholds × 4 bound types × 20 seeds = 400 jobs
    # ================================================================
    print(f"\n{'='*60}")
    print("PHASE 2b: Exp B — Pruning threshold sweep (400 jobs, 100 sessions)")
    print(f"{'='*60}")
    prune_thresholds = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
    futures_B = []
    for bt in BOUND_TYPES:
        for pt in prune_thresholds:
            for seed in range(20):
                condition = f"{bt}_pt{pt:.0e}"
                params = dict(BASE_PARAMS)
                params["bound_type"] = bt
                params["prune_threshold_value"] = pt
                futures_B.append(run_prune_sweep_job.remote(condition, seed, params))

    done = _wait_all(futures_B, "Exp B")
    merge_and_copy("expB_prune_sweep")

    # ================================================================
    # PHASE 2c: Exp E — Eta distribution snapshots
    # 4 weight bounds × 2 eta bounds × 20 seeds = 160 jobs
    # ================================================================
    print(f"\n{'='*60}")
    print("PHASE 2c: Exp E — Eta snapshots (160 jobs, 200 sessions)")
    print(f"{'='*60}")
    futures_E = []
    for wbt in BOUND_TYPES:
        for soft_eta in [False, True]:
            eta_tag = "soft_eta" if soft_eta else "hard_eta"
            for seed in range(20):
                condition = f"w{wbt}_{eta_tag}"
                params = dict(BASE_PARAMS)
                params["weight_bound_type"] = wbt
                params["use_soft_eta_bounds"] = soft_eta
                params["meta_strength"] = 0.005
                params["inhibitor_coupling"] = 0.0
                futures_E.append(run_eta_snapshot_job.remote(condition, seed, params))

    done = _wait_all(futures_E, "Exp E")
    merge_and_copy("expE_eta_snapshots")

    # ================================================================
    # PHASE 3: Exp R — Response-profile divergence
    # 4 bound types × 2 prune × 30 seeds = 240 jobs
    # ================================================================
    print(f"\n{'='*60}")
    print("PHASE 3: Exp R — Response profiles (240 jobs, 200 sessions + probes)")
    print(f"{'='*60}")
    futures_R = []
    for bt in BOUND_TYPES:
        for prune_on in [True, False]:
            prune_tag = "pruned" if prune_on else "noprune"
            for seed in range(30):
                condition = f"{bt}_{prune_tag}"
                params = dict(BASE_PARAMS)
                params["bound_type"] = bt
                params["prune_on"] = prune_on
                futures_R.append(run_response_profile_job.remote(condition, seed, params))

    done = _wait_all(futures_R, "Exp R")
    merge_and_copy("expR_response_profile")

    # ================================================================
    # Summary
    # ================================================================
    elapsed = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"ALL PHASES COMPLETE in {elapsed:.0f}s ({elapsed/3600:.1f}h)")
    print(f"{'='*60}")
    print("Experiments completed:")
    print("  expF_factorial          — 2×2 pruning × bound type")
    print("  expB_prune_sweep        — pruning threshold characterisation")
    print("  expE_eta_snapshots      — eta distribution for variance analysis")
    print("  expR_response_profile   — functional differentiation metric")
    print(f"\nData on NFS: {NFS_DATA_DIR}")
    print(f"Data copied to: {LOCAL_DATA_DIR}")


def _wait_all(futures, label):
    """Wait for all futures with progress reporting."""
    total = len(futures)
    done = 0
    t0 = time.time()
    remaining = list(futures)
    while remaining:
        ready, remaining = ray.wait(remaining,
                                     num_returns=min(50, len(remaining)),
                                     timeout=60)
        results = ray.get(ready)
        done += len(results)
        elapsed = time.time() - t0
        rate = done / elapsed if elapsed > 0 else 0
        est = (total - done) / rate if rate > 0 else 0
        print(f"  [{label}] {done}/{total} ({elapsed:.0f}s, ~{est:.0f}s left)", flush=True)
    elapsed = time.time() - t0
    print(f"  [{label}] Complete: {total} jobs in {elapsed:.0f}s ({elapsed/60:.1f}m)")
    return done


if __name__ == "__main__":
    main()
