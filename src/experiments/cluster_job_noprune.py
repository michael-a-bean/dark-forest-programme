#!/usr/bin/env python3
"""No-pruning replications of Paper 4 key experiments for Paper 4S.

Committee requirement: re-run Exp 5, 12, 17 without pruning to demonstrate
that functional differentiation findings survive the pruning confound.

Experiments:
  exp5np:  Corrective mechanism — reduced sweep (3 meta × 3 coupling = 9 conditions)
           focusing on the parameter range where differentiation was strongest.
  exp12np: Functional probe — all 4 conditions, identical to original.
  exp17np: Response matrix — all 4 conditions, identical to original.

Total: (9 + 4 + 4) × 20 seeds = 340 jobs

Usage:
    cd ~/research/dark-forest-metaplastic
    ray job submit --address http://192.168.1.11:8265 \
        --working-dir . \
        --runtime-env-json '{"pip": ["numpy", "pyarrow", "scikit-learn"], "excludes": ["data/", "papers/", ".git/", ".pytest_cache/"]}' \
        --no-wait \
        -- python3 -m src.cluster_job_noprune
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
    "prune_threshold": 1e-8,  # Effectively disabled
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
    "max_edges": 20000,
}


def make_field(params, seed):
    """Construct MetaplasticField with no-pruning parameters."""
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


def cap_edges(mf, max_edges):
    """Rank-based edge capping (not threshold pruning)."""
    if len(mf.weights) > max_edges:
        sorted_edges = sorted(mf.weights.items(), key=lambda x: abs(x[1]))
        for k, _ in sorted_edges[:len(mf.weights) - max_edges]:
            del mf.weights[k]


# ============================================================
# Exp 5np: Corrective mechanism without pruning (reduced sweep)
# ============================================================

@ray.remote
def run_exp5np(condition, seed, params):
    """Exp 5 corrective without pruning."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from src.metrics.eta_divergence import eta_divergence

    exp_name = "exp5np_corrective_noprune"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    mf = make_field(params, seed)
    max_edges = params.get("max_edges", 20000)

    rows = []
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()
        cap_edges(mf, max_edges)

        asm = mf.find_assemblages()
        eta_div = eta_divergence(mf.node_eta, asm)

        response_div = 0.0
        if len(asm) >= 2:
            gains = []
            for nodes in asm:
                node_list = sorted(nodes)
                asm_eta = np.mean(mf.node_eta[node_list])
                internal_w = [abs(mf.weights[(i, j)]) for i in node_list
                              for j in node_list if (i, j) in mf.weights]
                asm_gain = asm_eta * (np.mean(internal_w) if internal_w else 0)
                gains.append(asm_gain)
            response_div = float(np.std(gains)) if len(gains) >= 2 else 0.0

        rows.append({
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "total_steps": mf.step_count,
            "n_edges": len(mf.weights),
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
            "eta_divergence": eta_div,
            "n_assemblages": len(asm),
            "mean_weight": float(np.mean(np.abs(list(mf.weights.values())))) if mf.weights else 0,
            "mean_eta": float(np.mean(mf.node_eta)),
            "eta_std": float(np.std(mf.node_eta)),
            "response_diversity": response_div,
            "meta_strength": float(params["meta_strength"]),
            "inhibitor_coupling": float(params["inhibitor_coupling"]),
            "locality": float(params["locality"]),
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


# ============================================================
# Exp 12np: Functional probe without pruning
# ============================================================

@ray.remote
def run_exp12np(condition, seed, params):
    """Exp 12 functional probe without pruning."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from src.metrics.eta_divergence import eta_divergence

    exp_name = "exp12np_functional_noprune"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    mf = make_field(params, seed)
    max_edges = params.get("max_edges", 20000)

    rows = []
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()
        cap_edges(mf, max_edges)

        asm = mf.find_assemblages()
        eta_div = eta_divergence(mf.node_eta, asm)

        response_div = 0.0
        if len(asm) >= 2:
            gains = []
            for nodes in asm:
                node_list = sorted(nodes)
                asm_eta = np.mean(mf.node_eta[node_list])
                internal_w = [abs(mf.weights[(i, j)]) for i in node_list
                              for j in node_list if (i, j) in mf.weights]
                asm_gain = asm_eta * (np.mean(internal_w) if internal_w else 0)
                gains.append(asm_gain)
            response_div = float(np.std(gains)) if len(gains) >= 2 else 0.0

        rows.append({
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "total_steps": mf.step_count,
            "n_edges": len(mf.weights),
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
            "eta_divergence": eta_div,
            "n_assemblages": len(asm),
            "mean_weight": float(np.mean(np.abs(list(mf.weights.values())))) if mf.weights else 0,
            "mean_eta": float(np.mean(mf.node_eta)),
            "eta_std": float(np.std(mf.node_eta)),
            "response_diversity": response_div,
            "meta_strength": float(params["meta_strength"]),
            "inhibitor_coupling": float(params["inhibitor_coupling"]),
            "locality": float(params["locality"]),
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


# ============================================================
# Exp 17np: Response matrix without pruning
# ============================================================

@ray.remote
def run_exp17np(condition, seed, params):
    """Exp 17 perturbation-response matrix without pruning."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.metrics.centroid_distance import centroid_cosine_distance
    from src.metrics.eta_divergence import eta_divergence

    exp_name = "exp17np_response_noprune"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    mf = make_field(params, seed)
    max_edges = params.get("max_edges", 20000)

    # Phase 1: Train for 200 sessions (with edge capping, no threshold pruning)
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()
        cap_edges(mf, max_edges)

    # Record post-training state
    asm = mf.find_assemblages()
    ccd = centroid_cosine_distance(mf.weights, asm, mf.n_nodes)
    eta_div = eta_divergence(mf.node_eta, asm)

    if len(asm) < 2:
        rows = [{
            "condition": condition, "seed": seed,
            "n_assemblages": len(asm), "ccd": ccd, "eta_divergence": eta_div,
            "response_rank": 0, "response_matrix_json": "[]",
            "mean_response_diversity": 0.0, "n_edges": len(mf.weights),
            "mean_weight": float(np.mean(np.abs(list(mf.weights.values())))) if mf.weights else 0,
        }]
        os.makedirs(job_dir, exist_ok=True)
        pq.write_table(pa.Table.from_pylist(rows), job_file)
        return {"n_rows": 1}

    # Phase 2: Probe with K=5 structured input patterns
    saved_weights = dict(mf.weights)
    saved_eta = mf.node_eta.copy()
    saved_activations = mf.activations.copy()
    saved_activity_history = mf._activity_history.copy()

    K = 5
    probe_steps = 50
    gs = mf.grid_size

    # Generate patterns (quadrants + center ring)
    patterns = []
    for k in range(K):
        pattern = np.zeros(mf.n_nodes)
        for idx in range(mf.n_nodes):
            row, col = idx // gs, idx % gs
            r_norm, c_norm = row / gs, col / gs
            if k == 0 and r_norm < 0.5 and c_norm < 0.5:
                pattern[idx] = 0.5
            elif k == 1 and r_norm < 0.5 and c_norm >= 0.5:
                pattern[idx] = 0.5
            elif k == 2 and r_norm >= 0.5 and c_norm < 0.5:
                pattern[idx] = 0.5
            elif k == 3 and r_norm >= 0.5 and c_norm >= 0.5:
                pattern[idx] = 0.5
            elif k == 4 and 0.3 <= r_norm <= 0.7 and 0.3 <= c_norm <= 0.7:
                pattern[idx] = 0.5
        patterns.append(pattern)

    response_matrix = np.zeros((K, len(asm)))

    for k, pattern in enumerate(patterns):
        mf.weights = dict(saved_weights)
        mf.node_eta = saved_eta.copy()
        mf.activations = saved_activations.copy()
        mf._activity_history = saved_activity_history.copy()

        for step in range(probe_steps):
            mf.activations += pattern * 0.1
            new_input = np.zeros(mf.n_nodes)
            in_degree = np.zeros(mf.n_nodes)
            for (i, j), w in mf.weights.items():
                new_input[j] += w * mf.activations[i]
                in_degree[j] += 1
            scale = np.where(in_degree > 0, np.sqrt(np.maximum(in_degree, 1)), 1.0)
            mf.activations = np.tanh(0.5 * mf.activations + new_input / scale)

        for a_idx, nodes in enumerate(asm):
            node_list = sorted(nodes)
            response_matrix[k, a_idx] = float(np.mean(np.abs(mf.activations[node_list])))

    # SVD for effective rank
    U, S, Vt = np.linalg.svd(response_matrix, full_matrices=False)
    threshold = 0.01 * S[0] if S[0] > 0 else 1e-10
    effective_rank = int(np.sum(S > threshold))

    per_pattern_div = [float(np.std(response_matrix[k, :])) for k in range(K)]
    mean_response_div = float(np.mean(per_pattern_div))

    rows = [{
        "condition": condition,
        "seed": seed,
        "n_assemblages": len(asm),
        "ccd": ccd,
        "eta_divergence": eta_div,
        "response_rank": effective_rank,
        "singular_values": json.dumps(S.tolist()),
        "response_matrix_json": json.dumps(response_matrix.tolist()),
        "mean_response_diversity": mean_response_div,
        "per_pattern_diversity": json.dumps(per_pattern_div),
        "n_edges": len(saved_weights),
        "mean_weight": float(np.mean(np.abs(list(saved_weights.values())))) if saved_weights else 0,
    }]

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": 1}


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
    tables = []
    for f in sorted(os.listdir(job_dir)):
        if f.endswith(".parquet"):
            t = pq.read_table(os.path.join(job_dir, f))
            for i, field in enumerate(t.schema):
                if field.type == pa.int64() and field.name not in (
                    'seed', 'n_assemblages', 'n_edges', 'session', 'response_rank',
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

    # ---- Exp 5np: Corrective no-prune (reduced sweep) ----
    # Focus on parameter range where differentiation was strongest:
    # meta_strength in {0.005, 0.01, 0.05} × coupling in {0, 0.005, 0.01}
    print(f"\n{'='*60}")
    print("Exp 5np: Corrective no-prune (9 conditions × 20 seeds = 180 jobs)")
    print(f"{'='*60}")
    meta_strengths = [0.005, 0.01, 0.05]
    couplings = [0, 0.005, 0.01]
    futures_5 = []
    for ms in meta_strengths:
        for coup in couplings:
            for seed in range(n_seeds):
                condition = f"ms{ms:.4f}_coup{coup:.4f}"
                params = dict(BASE_PARAMS)
                params["meta_strength"] = ms
                params["inhibitor_coupling"] = coup
                params["use_local_target"] = True
                params["use_difference_coupling"] = True
                futures_5.append(run_exp5np.remote(condition, seed, params))
    _wait_all(futures_5, "Exp 5np")
    merge_and_copy("exp5np_corrective_noprune")

    # ---- Exp 12np: Functional probe no-prune ----
    print(f"\n{'='*60}")
    print("Exp 12np: Functional probe no-prune (4 conditions × 20 seeds = 80 jobs)")
    print(f"{'='*60}")
    conditions_12 = [
        ("baseline", {"meta_strength": 0.0, "use_local_target": False, "use_soft_bounds": False}),
        ("global_target", {"meta_strength": 0.05, "use_local_target": False, "use_soft_bounds": False}),
        ("local_target", {"meta_strength": 0.05, "use_local_target": True, "use_soft_bounds": False}),
        ("local_soft", {"meta_strength": 0.05, "use_local_target": True, "use_soft_bounds": True}),
    ]
    futures_12 = []
    for cond_name, overrides in conditions_12:
        for seed in range(n_seeds):
            params = dict(BASE_PARAMS)
            params["inhibitor_coupling"] = 0.0
            params.update(overrides)
            futures_12.append(run_exp12np.remote(cond_name, seed, params))
    _wait_all(futures_12, "Exp 12np")
    merge_and_copy("exp12np_functional_noprune")

    # ---- Exp 17np: Response matrix no-prune ----
    print(f"\n{'='*60}")
    print("Exp 17np: Response matrix no-prune (4 conditions × 20 seeds = 80 jobs)")
    print(f"{'='*60}")
    conditions_17 = [
        ("baseline", {"meta_strength": 0.0, "use_local_target": False, "use_soft_bounds": False}),
        ("global_target", {"meta_strength": 0.05, "use_local_target": False, "use_soft_bounds": False}),
        ("local_hard", {"meta_strength": 0.05, "use_local_target": True, "use_soft_bounds": False}),
        ("local_soft", {"meta_strength": 0.05, "use_local_target": True, "use_soft_bounds": True}),
    ]
    futures_17 = []
    for cond_name, overrides in conditions_17:
        for seed in range(n_seeds):
            params = dict(BASE_PARAMS)
            params["inhibitor_coupling"] = 0.0
            params.update(overrides)
            futures_17.append(run_exp17np.remote(cond_name, seed, params))
    _wait_all(futures_17, "Exp 17np")
    merge_and_copy("exp17np_response_noprune")

    elapsed = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"ALL NO-PRUNING REPLICATIONS COMPLETE in {elapsed:.0f}s ({elapsed/3600:.1f}h)")
    print(f"{'='*60}")
    print("  exp5np_corrective_noprune  — corrective mechanism (reduced sweep)")
    print("  exp12np_functional_noprune — functional probe (4 conditions)")
    print("  exp17np_response_noprune   — response matrix (4 conditions)")


if __name__ == "__main__":
    main()
