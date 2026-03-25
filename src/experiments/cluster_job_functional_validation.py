#!/usr/bin/env python3
"""Functional validation: Exp 8 (critical period) and Exp 9 (perturbation)
with response rank as dependent variable.

Addresses R1 and R2 concerns that these key experiments were measured
only on CCD (now demoted to geometric metric).

Exp 8fv: Critical period with 10-probe response rank
  5 switch-points × 4 couplings × 20 seeds = 400 jobs
  200 training sessions + response probes at end

Exp 9fv: Perturbation resilience with 10-probe response rank
  4 perturbation levels × 20 seeds = 80 jobs
  200 sessions (perturb at session 100) + response probes at end

Total: 480 jobs

Usage:
    cd ~/research/dark-forest-metaplastic
    ray job submit --address http://192.168.1.11:8265 \
        --working-dir . \
        --runtime-env-json '{"pip": ["numpy", "pyarrow", "scikit-learn"], "excludes": ["data/", "papers/", ".git/", ".pytest_cache/"]}' \
        --no-wait \
        -- python3 -m src.cluster_job_functional_validation
"""

import json
import os
import time

import ray
import numpy as np

NFS_DATA_DIR = "/mnt/cluster/experiments/dark-forest-metaplastic/data"
LOCAL_DATA_DIR = os.path.expanduser("~/research/dark-forest-metaplastic/data")

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
    "prune_threshold": 1e-4,
    "n_sessions": 200,
    "n_steps": 300,
    "target_activity": 0.15,
    "eta_min": 0.005,
    "eta_max": 0.20,
    "inhibitor_decay": 0.10,
    "inhibitor_emission_rate": 0.01,
    "inhibitor_diffusion": 0.05,
    "inhibitor_coupling": 0.0,
    "meta_strength": 0.0,
    "locality": 0.10,
}


def make_field(params, seed):
    from src.substrate.metaplastic_field import MetaplasticField
    return MetaplasticField(
        grid_size=params["grid_size"],
        n_hotspots=params["n_hotspots"],
        hotspot_radius=params["hotspot_radius"],
        hotspot_energy=params["hotspot_energy"],
        base_noise=params["base_noise"],
        eta=params["eta"],
        lam=params["lam"],
        w_max=params["w_max"],
        encounter_rate=params["encounter_rate"],
        locality=params["locality"],
        prune_threshold=params["prune_threshold"],
        seed=seed,
        meta_strength=params["meta_strength"],
        target_activity=params["target_activity"],
        eta_min=params["eta_min"],
        eta_max=params["eta_max"],
        inhibitor_diffusion=params["inhibitor_diffusion"],
        inhibitor_decay=params["inhibitor_decay"],
        inhibitor_coupling=params["inhibitor_coupling"],
        inhibitor_emission_rate=params["inhibitor_emission_rate"],
        use_local_target=params.get("use_local_target", True),
        use_difference_coupling=params.get("use_difference_coupling", True),
        target_radius=params.get("target_radius", 1),
        use_soft_bounds=params.get("use_soft_bounds", False),
        ema_rate=params.get("ema_rate", 0.05),
    )


def probe_response_rank(mf, asm, seed_offset=0):
    """10-probe SVD response rank with participation ratio."""
    if len(asm) < 2:
        return {"response_rank": 0, "participation_ratio": 0.0,
                "singular_values_json": "[]", "mean_response_diversity": 0.0}

    saved_weights = dict(mf.weights)
    saved_eta = mf.node_eta.copy()
    saved_act = mf.activations.copy()
    saved_hist = mf._activity_history.copy()

    probe_rng = np.random.default_rng(seed_offset + 777777)
    K = 10
    gs = mf.grid_size
    response_matrix = np.zeros((K, len(asm)))

    for k in range(K):
        # Gaussian probe at random position
        cx, cy = probe_rng.uniform(0.1, 0.9, 2)
        mf.weights = dict(saved_weights)
        mf.node_eta = saved_eta.copy()
        mf.activations = saved_act.copy()
        mf._activity_history = saved_hist.copy()

        distances = np.sqrt((mf.pos_x - cx)**2 + (mf.pos_y - cy)**2)
        stimulus = 0.5 * np.exp(-distances**2 / (2 * 0.1**2))
        mf.activations += stimulus

        for _ in range(50):
            new_input = np.zeros(mf.n_nodes)
            in_degree = np.zeros(mf.n_nodes)
            for (i, j), w in mf.weights.items():
                new_input[j] += w * mf.activations[i]
                in_degree[j] += 1
            scale = np.where(in_degree > 0, np.sqrt(np.maximum(in_degree, 1)), 1.0)
            mf.activations = np.tanh(0.5 * mf.activations + new_input / scale)

        for a_idx, nodes in enumerate(asm):
            response_matrix[k, a_idx] = float(np.mean(np.abs(mf.activations[list(nodes)])))

    # Restore state
    mf.weights = saved_weights
    mf.node_eta = saved_eta
    mf.activations = saved_act
    mf._activity_history = saved_hist

    # SVD analysis
    U, S, Vt = np.linalg.svd(response_matrix, full_matrices=False)
    threshold = 0.01 * S[0] if S[0] > 0 else 1e-10
    effective_rank = int(np.sum(S > threshold))

    s_sq = S**2
    total = np.sum(s_sq)
    pr = float(total**2 / np.sum(s_sq**2)) if total > 0 else 0.0

    per_pattern_div = [float(np.std(response_matrix[k, :])) for k in range(K)]

    return {
        "response_rank": effective_rank,
        "participation_ratio": pr,
        "singular_values_json": json.dumps(S.tolist()),
        "mean_response_diversity": float(np.mean(per_pattern_div)),
    }


# ============================================================
# Exp 8fv: Critical period with response rank
# ============================================================

@ray.remote
def run_exp8fv(condition, seed, params):
    """Critical period with 10-probe response rank."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from src.metrics.eta_divergence import eta_divergence

    exp_name = "exp8fv_critical_period"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    mf = make_field(params, seed)
    coupling_switch = params.get("coupling_switch_session", 0)
    coupling_target = params.get("coupling_target", 0.0)
    if coupling_switch > 0:
        mf.inhibitor_coupling = 0.0

    rows = []
    # Record at key sessions: before switch, at switch, and after
    record_sessions = {1, 10, 25, 50, 75, 100, 150, 200}

    for session in range(1, 201):
        if coupling_switch > 0 and session == coupling_switch:
            mf.inhibitor_coupling = coupling_target

        for _ in range(300):
            mf.step()

        if session in record_sessions:
            asm = mf.find_assemblages()
            eta_div = eta_divergence(mf.node_eta, asm)

            # Response rank probe
            rank_data = probe_response_rank(mf, asm, seed_offset=seed)

            rows.append({
                "experiment": exp_name,
                "condition": condition,
                "seed": seed,
                "session": session,
                "coupling_switch_session": coupling_switch,
                "coupling_target": coupling_target,
                "n_assemblages": len(asm),
                "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
                "eta_divergence": eta_div,
                "modularity": weight_modularity(mf.weights, asm),
                "response_rank": rank_data["response_rank"],
                "participation_ratio": rank_data["participation_ratio"],
                "mean_response_diversity": rank_data["mean_response_diversity"],
                "n_edges": len(mf.weights),
                "mean_weight": float(np.mean(np.abs(list(mf.weights.values())))) if mf.weights else 0,
            })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


# ============================================================
# Exp 9fv: Perturbation resilience with response rank
# ============================================================

@ray.remote
def run_exp9fv(condition, seed, params):
    """Perturbation resilience with 10-probe response rank."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from src.metrics.eta_divergence import eta_divergence

    exp_name = "exp9fv_perturbation"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    mf = make_field(params, seed)
    perturb_session = params.get("perturb_session", 0)
    perturb_fraction = params.get("perturb_fraction", 0.0)
    perturb_rng = np.random.default_rng(seed + 99999)

    rows = []
    # Record before perturbation, at perturbation, and recovery
    record_sessions = {1, 50, 99, 100, 101, 110, 125, 150, 200}

    for session in range(1, 201):
        if perturb_session > 0 and session == perturb_session:
            n_perturb = int(mf.n_nodes * perturb_fraction)
            indices = perturb_rng.choice(mf.n_nodes, size=n_perturb, replace=False)
            mf.node_eta[indices] = perturb_rng.uniform(mf.eta_min, mf.eta_max, size=n_perturb)

        for _ in range(300):
            mf.step()

        if session in record_sessions:
            asm = mf.find_assemblages()
            eta_div = eta_divergence(mf.node_eta, asm)
            rank_data = probe_response_rank(mf, asm, seed_offset=seed)

            rows.append({
                "experiment": exp_name,
                "condition": condition,
                "seed": seed,
                "session": session,
                "perturb_session": perturb_session,
                "perturb_fraction": perturb_fraction,
                "n_assemblages": len(asm),
                "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
                "eta_divergence": eta_div,
                "modularity": weight_modularity(mf.weights, asm),
                "response_rank": rank_data["response_rank"],
                "participation_ratio": rank_data["participation_ratio"],
                "mean_response_diversity": rank_data["mean_response_diversity"],
                "n_edges": len(mf.weights),
                "mean_weight": float(np.mean(np.abs(list(mf.weights.values())))) if mf.weights else 0,
            })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


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
                    'seed', 'n_assemblages', 'n_edges', 'session',
                    'response_rank', 'coupling_switch_session', 'perturb_session',
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


def main():
    ray.init()
    resources = ray.cluster_resources()
    print(f"Cluster: {resources.get('CPU', 0):.0f} CPUs")
    t_start = time.time()

    # ---- Exp 8fv: Critical period with response rank ----
    print(f"\n{'='*60}")
    print("Exp 8fv: Critical period + response rank (400 jobs)")
    print(f"{'='*60}")
    switch_points = [0, 25, 50, 100, 150]
    couplings = [0.0005, 0.001, 0.005, 0.01]
    futures_8 = []
    for sp in switch_points:
        for coup in couplings:
            for seed in range(20):
                condition = f"switch{sp:03d}_coup{coup:.4f}"
                params = dict(BASE_PARAMS)
                params["meta_strength"] = 0.05
                params["inhibitor_diffusion"] = 0.05
                params["inhibitor_coupling"] = coup
                params["use_local_target"] = True
                params["coupling_switch_session"] = sp
                params["coupling_target"] = coup
                futures_8.append(run_exp8fv.remote(condition, seed, params))
    _wait_all(futures_8, "Exp 8fv")
    merge_and_copy("exp8fv_critical_period")

    # ---- Exp 9fv: Perturbation + response rank ----
    print(f"\n{'='*60}")
    print("Exp 9fv: Perturbation + response rank (80 jobs)")
    print(f"{'='*60}")
    fractions = [0.0, 0.10, 0.25, 0.50]
    futures_9 = []
    for frac in fractions:
        for seed in range(20):
            condition = f"perturb{frac:.2f}"
            params = dict(BASE_PARAMS)
            params["meta_strength"] = 0.05
            params["inhibitor_coupling"] = 0.0
            params["use_local_target"] = True
            params["perturb_session"] = 100 if frac > 0 else 0
            params["perturb_fraction"] = frac
            futures_9.append(run_exp9fv.remote(condition, seed, params))
    _wait_all(futures_9, "Exp 9fv")
    merge_and_copy("exp9fv_perturbation")

    elapsed = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"FUNCTIONAL VALIDATION COMPLETE in {elapsed:.0f}s ({elapsed/3600:.1f}h)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
