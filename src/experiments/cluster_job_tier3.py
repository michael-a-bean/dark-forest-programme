#!/usr/bin/env python3
"""Tier 3 experiments for Paper 4 revision — knowledge-complete analysis.

Submitted via `ray job submit`. Persists on cluster independently.

Experiments:
  exp16_eta_dump:       Save full per-node eta arrays at key sessions.
                        For histogram figures showing bimodal vs unimodal.
                        2 conditions × 5 seeds × snapshots at sessions [1,10,50,100,200].

  exp17_response_matrix: Perturbation-response matrix — genuinely independent
                        functional probe. After 200 sessions, apply K=5
                        structured input patterns, measure per-assemblage responses.
                        Rank of response matrix > 1 = genuinely functional.
                        4 conditions × 20 seeds.

  exp18_ema_sensitivity: Does differentiation depend on homeostatic timescale?
                        3 EMA rates × 20 seeds.

  exp19_transplant:     DeLanda exteriority test. After differentiation,
                        swap two assemblages' spatial positions. Do they
                        retain functional identity or re-adapt?
                        2 conditions × 20 seeds.
"""

import argparse
import json
import os
import sys
import time

import ray
import numpy as np

NFS_DATA_DIR = "/mnt/cluster/experiments/dark-forest-metaplastic/data"

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
    """Construct a MetaplasticField from params dict."""
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


# ─── Exp 16: Per-node eta dump ──────────────────────────────────────────

@ray.remote
def run_exp16(condition, seed, params, output_dir):
    """Save per-node eta arrays at snapshot sessions for histogram figures."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    job_dir = os.path.join(output_dir, "exp16_eta_dump", "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"condition": condition, "seed": seed, "skipped": True}

    mf = make_field(params, seed)
    snapshot_sessions = {1, 10, 50, 100, 200}

    rows = []
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

        if session in snapshot_sessions:
            asm = mf.find_assemblages()
            # Store per-node eta as JSON array
            eta_list = mf.node_eta.tolist()
            activity_list = mf._activity_history.tolist()

            # Tag each node with assemblage membership (-1 = no assemblage)
            membership = [-1] * mf.n_nodes
            for asm_idx, nodes in enumerate(asm):
                for n in nodes:
                    membership[n] = asm_idx

            rows.append({
                "condition": condition,
                "seed": seed,
                "session": session,
                "n_nodes": mf.n_nodes,
                "n_assemblages": len(asm),
                "eta_values": json.dumps(eta_list),
                "activity_values": json.dumps(activity_list),
                "membership": json.dumps(membership),
                "mean_eta": float(np.mean(mf.node_eta)),
                "eta_std": float(np.std(mf.node_eta)),
            })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"condition": condition, "seed": seed, "n_rows": len(rows)}


# ─── Exp 17: Perturbation-response matrix ───────────────────────────────

@ray.remote
def run_exp17(condition, seed, params, output_dir):
    """After training, probe with K structured inputs, measure per-assemblage response."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from src.metrics.eta_divergence import eta_divergence

    job_dir = os.path.join(output_dir, "exp17_response_matrix", "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"condition": condition, "seed": seed, "skipped": True}

    mf = make_field(params, seed)

    # Phase 1: Train for 200 sessions
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

    # Record post-training state
    asm = mf.find_assemblages()
    ccd = centroid_cosine_distance(mf.weights, asm, mf.n_nodes)
    eta_div = eta_divergence(mf.node_eta, asm)

    if len(asm) < 2:
        # Can't probe if <2 assemblages
        rows = [{
            "condition": condition, "seed": seed,
            "n_assemblages": len(asm), "ccd": ccd, "eta_divergence": eta_div,
            "response_rank": 0, "response_matrix_json": "[]",
            "mean_response_diversity": 0.0,
        }]
        os.makedirs(job_dir, exist_ok=True)
        pq.write_table(pa.Table.from_pylist(rows), job_file)
        return {"condition": condition, "seed": seed, "n_rows": 1}

    # Phase 2: Probe with K=5 structured input patterns
    # Save weights and eta for restoration
    saved_weights = dict(mf.weights)
    saved_eta = mf.node_eta.copy()
    saved_activations = mf.activations.copy()
    saved_activity_history = mf._activity_history.copy()

    probe_rng = np.random.default_rng(seed + 77777)
    K = 5
    probe_steps = 50  # steps per probe (enough to measure response)

    # Generate K different structured input patterns
    # Each pattern activates a different spatial quadrant
    gs = mf.grid_size
    patterns = []
    # Pattern 0: top-left quadrant
    # Pattern 1: top-right
    # Pattern 2: bottom-left
    # Pattern 3: bottom-right
    # Pattern 4: center ring
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

    # For each pattern, inject it and measure per-assemblage mean response
    # response_matrix[k][a] = mean activation of assemblage a under pattern k
    response_matrix = np.zeros((K, len(asm)))

    for k, pattern in enumerate(patterns):
        # Reset to post-training state
        mf.weights = dict(saved_weights)
        mf.node_eta = saved_eta.copy()
        mf.activations = saved_activations.copy()
        mf._activity_history = saved_activity_history.copy()

        # Inject pattern for probe_steps (no learning — just propagation)
        for step in range(probe_steps):
            # Add pattern as external input
            mf.activations += pattern * 0.1  # gentle injection
            # Propagate (but don't learn — just measure response)
            new_input = np.zeros(mf.n_nodes)
            in_degree = np.zeros(mf.n_nodes)
            for (i, j), w in mf.weights.items():
                new_input[j] += w * mf.activations[i]
                in_degree[j] += 1
            scale = np.where(in_degree > 0, np.sqrt(np.maximum(in_degree, 1)), 1.0)
            mf.activations = np.tanh(0.5 * mf.activations + new_input / scale)

        # Measure per-assemblage mean activation
        for a_idx, nodes in enumerate(asm):
            node_list = sorted(nodes)
            response_matrix[k, a_idx] = float(np.mean(np.abs(mf.activations[node_list])))

    # Compute rank of response matrix (SVD)
    U, S, Vt = np.linalg.svd(response_matrix, full_matrices=False)
    # Effective rank: number of singular values > 1% of largest
    threshold = 0.01 * S[0] if S[0] > 0 else 1e-10
    effective_rank = int(np.sum(S > threshold))

    # Per-pattern response diversity (std across assemblages)
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
    }]

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"condition": condition, "seed": seed, "n_rows": 1}


# ─── Exp 18: EMA sensitivity ────────────────────────────────────────────

@ray.remote
def run_exp18(condition, seed, params, output_dir):
    """Test differentiation under different EMA rates."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from src.metrics.eta_divergence import eta_divergence

    job_dir = os.path.join(output_dir, "exp18_ema_sensitivity", "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"condition": condition, "seed": seed, "skipped": True}

    mf = make_field(params, seed)

    rows = []
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

        asm = mf.find_assemblages()
        c = mf.census()
        eta_div = eta_divergence(mf.node_eta, asm)

        # Response diversity
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
            "experiment": "exp18_ema_sensitivity",
            "condition": condition,
            "seed": seed,
            "session": session,
            "total_steps": mf.step_count,
            "n_edges": len(mf.weights),
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
            "eta_divergence": eta_div,
            "n_assemblages": len(asm),
            "mean_eta": c["mean_eta"],
            "eta_std": c["eta_std"],
            "response_diversity": response_div,
            "ema_rate": float(params["ema_rate"]),
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"condition": condition, "seed": seed, "n_rows": len(rows)}


# ─── Exp 19: Transplant test (DeLanda exteriority) ──────────────────────

@ray.remote
def run_exp19(condition, seed, params, output_dir):
    """After differentiation, swap two assemblages' grid positions.
    Test whether assemblages retain functional identity or re-adapt.
    """
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.metrics.centroid_distance import centroid_cosine_distance
    from src.metrics.eta_divergence import eta_divergence

    job_dir = os.path.join(output_dir, "exp19_transplant", "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"condition": condition, "seed": seed, "skipped": True}

    mf = make_field(params, seed)
    transplant_session = 100
    do_transplant = condition == "transplant"

    rows = []
    pre_transplant_gains = None

    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

        asm = mf.find_assemblages()

        # Compute per-assemblage gains for identity tracking
        gains = []
        if len(asm) >= 2:
            for nodes in asm:
                node_list = sorted(nodes)
                asm_eta = np.mean(mf.node_eta[node_list])
                internal_w = [abs(mf.weights[(i, j)]) for i in node_list
                              for j in node_list if (i, j) in mf.weights]
                asm_gain = asm_eta * (np.mean(internal_w) if internal_w else 0)
                gains.append(asm_gain)

        # At transplant session, swap the two largest assemblages' node properties
        if session == transplant_session and do_transplant and len(asm) >= 2:
            pre_transplant_gains = gains.copy()
            # Sort by size, take two largest
            sorted_asm = sorted(asm, key=len, reverse=True)
            asm_a = sorted(sorted_asm[0])
            asm_b = sorted(sorted_asm[1])

            # Swap eta values between the two assemblages
            min_len = min(len(asm_a), len(asm_b))
            eta_a = mf.node_eta[asm_a[:min_len]].copy()
            eta_b = mf.node_eta[asm_b[:min_len]].copy()
            mf.node_eta[asm_a[:min_len]] = eta_b
            mf.node_eta[asm_b[:min_len]] = eta_a

            # Swap activity histories too
            act_a = mf._activity_history[asm_a[:min_len]].copy()
            act_b = mf._activity_history[asm_b[:min_len]].copy()
            mf._activity_history[asm_a[:min_len]] = act_b
            mf._activity_history[asm_b[:min_len]] = act_a

        elif session == transplant_session and not do_transplant:
            pre_transplant_gains = gains.copy()

        # Track gain correlation with pre-transplant values
        gain_correlation = 0.0
        if pre_transplant_gains and len(gains) >= 2 and len(pre_transplant_gains) >= 2:
            # Correlation between sorted gains (order-invariant identity measure)
            min_g = min(len(gains), len(pre_transplant_gains))
            g_now = sorted(gains[:min_g])
            g_pre = sorted(pre_transplant_gains[:min_g])
            if np.std(g_now) > 0 and np.std(g_pre) > 0:
                gain_correlation = float(np.corrcoef(g_now, g_pre)[0, 1])

        ccd = centroid_cosine_distance(mf.weights, asm, mf.n_nodes)
        eta_div = eta_divergence(mf.node_eta, asm)

        rows.append({
            "experiment": "exp19_transplant",
            "condition": condition,
            "seed": seed,
            "session": session,
            "centroid_cosine_distance": ccd,
            "eta_divergence": eta_div,
            "n_assemblages": len(asm),
            "response_diversity": float(np.std(gains)) if len(gains) >= 2 else 0.0,
            "gain_correlation": gain_correlation,
            "transplant_session": transplant_session,
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"condition": condition, "seed": seed, "n_rows": len(rows)}


# ─── Job builders ────────────────────────────────────────────────────────

def build_exp16(n_seeds=5):
    """2 conditions × 5 seeds = 10 jobs (small, for histograms)."""
    jobs = []
    for soft in [False, True]:
        label = "soft" if soft else "hard"
        for seed in range(n_seeds):
            params = dict(BASE_PARAMS)
            params["meta_strength"] = 0.05
            params["use_local_target"] = True
            params["use_soft_bounds"] = soft
            jobs.append((f"eta_{label}", seed, params))
    return jobs


def build_exp17(n_seeds=20):
    """4 conditions × 20 seeds = 80 jobs."""
    conditions = [
        ("baseline", {"meta_strength": 0.0, "use_local_target": False, "use_soft_bounds": False}),
        ("global_target", {"meta_strength": 0.05, "use_local_target": False, "use_soft_bounds": False}),
        ("local_hard", {"meta_strength": 0.05, "use_local_target": True, "use_soft_bounds": False}),
        ("local_soft", {"meta_strength": 0.05, "use_local_target": True, "use_soft_bounds": True}),
    ]
    jobs = []
    for cond_name, overrides in conditions:
        for seed in range(n_seeds):
            params = dict(BASE_PARAMS)
            params["locality"] = 0.10
            params["inhibitor_coupling"] = 0.0
            params.update(overrides)
            jobs.append((cond_name, seed, params))
    return jobs


def build_exp18(n_seeds=20):
    """3 EMA rates × 20 seeds = 60 jobs."""
    ema_rates = [0.10, 0.05, 0.01]  # fast, default, slow
    jobs = []
    for ema in ema_rates:
        label = f"ema{ema:.2f}"
        for seed in range(n_seeds):
            params = dict(BASE_PARAMS)
            params["meta_strength"] = 0.05
            params["use_local_target"] = True
            params["inhibitor_coupling"] = 0.0
            params["ema_rate"] = ema
            jobs.append((label, seed, params))
    return jobs


def build_exp19(n_seeds=20):
    """2 conditions × 20 seeds = 40 jobs."""
    jobs = []
    for cond in ["control", "transplant"]:
        for seed in range(n_seeds):
            params = dict(BASE_PARAMS)
            params["meta_strength"] = 0.05
            params["use_local_target"] = True
            params["inhibitor_coupling"] = 0.0
            jobs.append((cond, seed, params))
    return jobs


def merge_job_files(experiment_name, output_dir):
    import pyarrow.parquet as pq
    import pyarrow as pa
    job_dir = os.path.join(output_dir, experiment_name, "jobs")
    if not os.path.isdir(job_dir):
        print(f"  No jobs dir for {experiment_name}")
        return
    tables = [pq.read_table(os.path.join(job_dir, f))
              for f in sorted(os.listdir(job_dir)) if f.endswith(".parquet")]
    if not tables:
        return
    merged = pa.concat_tables(tables, promote_options="default")
    pq.write_table(merged, os.path.join(output_dir, experiment_name, "session_metrics.parquet"))
    print(f"  Merged {len(tables)} -> {len(merged)} rows")


# ─── Dispatch ────────────────────────────────────────────────────────────

EXPERIMENTS = {
    "exp16": ("exp16_eta_dump", build_exp16, run_exp16),
    "exp17": ("exp17_response_matrix", build_exp17, run_exp17),
    "exp18": ("exp18_ema_sensitivity", build_exp18, run_exp18),
    "exp19": ("exp19_transplant", build_exp19, run_exp19),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiments", nargs="+",
                        default=["exp16", "exp17", "exp18", "exp19"])
    args = parser.parse_args()

    ray.init()
    print(f"Cluster: {ray.cluster_resources().get('CPU', 0):.0f} CPUs")
    print(f"Experiments: {args.experiments}")

    for exp_key in args.experiments:
        exp_name, builder, runner = EXPERIMENTS[exp_key]
        jobs = builder()

        job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
        already = len([f for f in os.listdir(job_dir) if f.endswith(".parquet")]) if os.path.isdir(job_dir) else 0

        print(f"\n{'=' * 60}")
        print(f"  {exp_name}: {len(jobs)} total, {already} done")
        print(f"{'=' * 60}", flush=True)

        t0 = time.time()
        futures = [runner.remote(cond, seed, params, NFS_DATA_DIR)
                   for cond, seed, params in jobs]

        done = 0
        total = len(futures)
        while futures:
            ready, futures = ray.wait(futures, num_returns=min(50, len(futures)), timeout=60)
            results = ray.get(ready)
            done += len(results)
            elapsed = time.time() - t0
            skipped = sum(1 for r in results if r.get("skipped", False))
            print(f"  {done}/{total} ({elapsed:.0f}s, {skipped} skipped)", flush=True)

        print(f"  {exp_name} done in {time.time() - t0:.0f}s")
        merge_job_files(exp_name, NFS_DATA_DIR)

    print(f"\n{'=' * 60}\n  All done.\n{'=' * 60}")


if __name__ == "__main__":
    main()
