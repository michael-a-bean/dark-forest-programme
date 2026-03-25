#!/usr/bin/env python3
"""Self-contained cluster job script for Paper 4S weight bounds experiments.

Submitted via `ray job submit`. Runs on the cluster's Python.
Uses Ray tasks for parallelism across cluster nodes.
Output goes to NFS, then merged.

Usage:
    ray job submit --working-dir . -- python -m src.cluster_job --experiments exp1 exp2 exp3 exp4 exp5
    ray job submit --working-dir . -- python -m src.cluster_job --experiments exp1  # single experiment
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
    "prune_threshold": 1e-4,
    "locality": 0.10,
    # Metaplastic defaults
    "target_activity": 0.15,
    "eta_min": 0.005,
    "eta_max": 0.20,
    "inhibitor_decay": 0.10,
    "inhibitor_emission_rate": 0.01,
    "inhibitor_diffusion": 0.05,
}


# ============================================================
# Ray remote workers
# ============================================================

@ray.remote
def run_network_job(experiment_name, condition, seed, params, output_dir):
    """Run one Network experiment (Exp 1, Exp 5 network) on a Ray worker."""
    from src.network import Network
    import pyarrow as pa
    import pyarrow.parquet as pq

    job_dir = os.path.join(output_dir, experiment_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"condition": condition, "seed": seed, "skipped": True}

    net = Network(
        n_nodes=params["n_nodes"],
        eta=params["eta"],
        lam=params["lam"],
        w_max=params["w_max"],
        bound_type=params["bound_type"],
        seed=seed,
    )

    rng = np.random.default_rng(seed + 100000)
    noise_scale = params.get("noise_scale", 0.3)

    rows = []
    prev_weights = None
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            input_vec = rng.normal(0, noise_scale, params["n_nodes"])
            net.step_and_learn(input_vec)

        w = net.weights
        w_flat = w.flatten()

        row = {
            "experiment": experiment_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "total_steps": session * params["n_steps"],
            "bound_type": params["bound_type"],
            "weight_mean": float(np.mean(w_flat)),
            "weight_std": float(np.std(w_flat)),
            "weight_mean_abs": float(np.mean(np.abs(w_flat))),
            "weight_max": float(np.max(np.abs(w_flat))),
            "saturation": float(np.mean(np.abs(w_flat) > 0.99 * params["w_max"])),
            "mean_activation": float(np.mean(np.abs(net.activations))),
            "eta": params["eta"],
            "lam": params["lam"],
        }

        if prev_weights is not None:
            row["drift"] = float(np.linalg.norm(w - prev_weights, "fro"))
        else:
            row["drift"] = None

        rows.append(row)
        prev_weights = w.copy()

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"condition": condition, "seed": seed, "n_rows": len(rows)}


@ray.remote
def run_multifield_job(experiment_name, condition, seed, params, output_dir):
    """Run one MultiField experiment (Exp 2, 3, 5) on a Ray worker."""
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    import pyarrow as pa
    import pyarrow.parquet as pq

    job_dir = os.path.join(output_dir, experiment_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"condition": condition, "seed": seed, "skipped": True}

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
        prune_threshold=params.get("prune_threshold", 1e-4),
        bound_type=params["bound_type"],
        seed=seed,
    )

    rows = []
    save_sessions = params.get("save_weight_sessions", [])
    weight_snapshot_rows = []

    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

        asm = mf.find_assemblages()
        c = mf.census()

        row = {
            "experiment": experiment_name,
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
        }

        # Exp 3 injection tracking
        if "inject_session" in params and session == params["inject_session"]:
            if len(asm) >= 2:
                nodes_a = sorted(asm[0])
                nodes_b = sorted(asm[1])
                for _ in range(params.get("n_inject", 10)):
                    ni = nodes_a[mf.rng.integers(0, len(nodes_a))]
                    nj = nodes_b[mf.rng.integers(0, len(nodes_b))]
                    if (ni, nj) not in mf.weights:
                        mf.weights[(ni, nj)] = 0.3
                        mf.edges_created += 1
            row["injection_event"] = True
        else:
            row["injection_event"] = False

        # Cross-assemblage edge count
        if len(asm) >= 2:
            node_to_asm = {}
            for ai, nodes in enumerate(asm):
                for n in nodes:
                    node_to_asm[n] = ai
            cross_edges = sum(1 for (i, j) in mf.weights
                              if node_to_asm.get(i, -1) != node_to_asm.get(j, -1)
                              and node_to_asm.get(i, -1) >= 0
                              and node_to_asm.get(j, -1) >= 0)
            row["cross_assemblage_edges"] = cross_edges
        else:
            row["cross_assemblage_edges"] = 0

        rows.append(row)

        # Save weight snapshots for Exp 5
        if session in save_sessions:
            w_arr = np.array(list(mf.weights.values()))
            for wi, wv in enumerate(w_arr):
                weight_snapshot_rows.append({
                    "experiment": experiment_name,
                    "condition": condition,
                    "seed": seed,
                    "session": session,
                    "bound_type": params["bound_type"],
                    "weight_idx": wi,
                    "weight": float(wv),
                })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)

    if weight_snapshot_rows:
        snap_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}_weights.parquet")
        pq.write_table(pa.Table.from_pylist(weight_snapshot_rows), snap_file)

    return {"condition": condition, "seed": seed, "n_rows": len(rows)}


@ray.remote
def run_metaplastic_job(experiment_name, condition, seed, params, output_dir):
    """Run one MetaplasticField experiment (Exp 4, Exp 5 metaplastic) on a Ray worker."""
    from src.substrate.metaplastic_field import MetaplasticField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from src.metrics.eta_divergence import eta_divergence
    import pyarrow as pa
    import pyarrow.parquet as pq

    job_dir = os.path.join(output_dir, experiment_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"condition": condition, "seed": seed, "skipped": True}

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
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

        asm = mf.find_assemblages()
        c = mf.census()
        sizes = sorted([len(a) for a in asm], reverse=True)

        pct_eta_at_min = float(np.mean(mf.node_eta <= mf.eta_min + 1e-6))
        pct_eta_at_max = float(np.mean(mf.node_eta >= mf.eta_max - 1e-6))

        rows.append({
            "experiment": experiment_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "total_steps": mf.step_count,
            "weight_bound_type": params["weight_bound_type"],
            "eta_bound_type": "soft" if params["use_soft_eta_bounds"] else "hard",
            "n_edges": len(mf.weights),
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
            "eta_divergence": eta_divergence(mf.node_eta, asm),
            "n_assemblages": len(asm),
            "largest_assemblage": sizes[0] if sizes else 0,
            "mean_energy": c["mean_energy"],
            "mean_weight": c["mean_weight"],
            "max_weight": c["max_weight"],
            "mean_eta": c["mean_eta"],
            "eta_std": c["eta_std"],
            "eta_range": c["eta_range"],
            "mean_inhibitor": c["mean_inhibitor"],
            "pct_eta_at_min": pct_eta_at_min,
            "pct_eta_at_max": pct_eta_at_max,
            "pct_eta_at_bound": pct_eta_at_min + pct_eta_at_max,
            "meta_strength": float(params["meta_strength"]),
            "inhibitor_coupling": float(params["inhibitor_coupling"]),
            "locality": float(params["locality"]),
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"condition": condition, "seed": seed, "n_rows": len(rows)}


# ============================================================
# Experiment builders
# ============================================================

def build_exp1_regime(n_seeds=20):
    """Exp 1: Three-regime structure. 4 bounds x 8 eta/lam x 20 seeds = 640."""
    eta_lam_combos = [
        (0.005, 0.002), (0.01, 0.002), (0.02, 0.002), (0.05, 0.002),
        (0.02, 0.0005), (0.02, 0.001), (0.02, 0.005), (0.02, 0.01),
    ]
    jobs = []
    for bt in BOUND_TYPES:
        for eta, lam in eta_lam_combos:
            for seed in range(n_seeds):
                condition = f"{bt}_eta{eta:.3f}_lam{lam:.4f}"
                jobs.append(("exp1_regime", condition, seed, {
                    "n_nodes": 64, "eta": eta, "lam": lam, "w_max": 1.0,
                    "bound_type": bt, "n_sessions": 20, "n_steps": 1000,
                    "noise_scale": 5.0,
                }))
    return "exp1_regime", jobs, "network"


def build_exp2_coexistence(n_seeds=20):
    """Exp 2: Coexistence/monopoly. 4 bounds x 7 localities x 20 seeds = 560."""
    localities = [0.05, 0.08, 0.10, 0.15, 0.20, 0.30, 0.50]
    jobs = []
    for bt in BOUND_TYPES:
        for loc in localities:
            for seed in range(n_seeds):
                condition = f"{bt}_loc{loc:.2f}"
                params = dict(BASE_PARAMS)
                params["bound_type"] = bt
                params["locality"] = loc
                params["n_sessions"] = 200
                params["n_steps"] = 300
                jobs.append(("exp2_coexistence", condition, seed, params))
    return "exp2_coexistence", jobs, "multifield"


def build_exp3_self_sealing(n_seeds=20):
    """Exp 3: Self-sealing. 4 bounds x 2 conditions x 20 seeds = 160."""
    jobs = []
    for bt in BOUND_TYPES:
        for inject in [False, True]:
            for seed in range(n_seeds):
                tag = "inject" if inject else "control"
                condition = f"{bt}_{tag}"
                params = dict(BASE_PARAMS)
                params["bound_type"] = bt
                params["locality"] = 0.10
                params["n_sessions"] = 200
                params["n_steps"] = 300
                if inject:
                    params["inject_session"] = 100
                    params["n_inject"] = 10
                jobs.append(("exp3_self_sealing", condition, seed, params))
    return "exp3_self_sealing", jobs, "multifield"


def build_exp4_continuous(n_seeds=20):
    """Exp 4: Fully continuous. 4 weight bounds x 2 eta bounds x 20 seeds = 160."""
    jobs = []
    for wbt in BOUND_TYPES:
        for soft_eta in [False, True]:
            for seed in range(n_seeds):
                eta_tag = "soft_eta" if soft_eta else "hard_eta"
                condition = f"w{wbt}_{eta_tag}"
                params = dict(BASE_PARAMS)
                params["weight_bound_type"] = wbt
                params["use_soft_eta_bounds"] = soft_eta
                params["meta_strength"] = 0.005
                params["inhibitor_coupling"] = 0.0
                params["n_sessions"] = 200
                params["n_steps"] = 300
                jobs.append(("exp4_continuous", condition, seed, params))
    return "exp4_continuous", jobs, "metaplastic"


def build_exp5_distributions(n_seeds=5):
    """Exp 5: Weight distributions. 4 bounds x 3 substrates x 5 seeds = 60."""
    save_sessions = [1, 10, 50, 100, 200]
    all_jobs = []

    for bt in BOUND_TYPES:
        for seed in range(n_seeds):
            # Network
            all_jobs.append(("exp5_dist_network", f"{bt}_network", seed, {
                "n_nodes": 64, "eta": 0.02, "lam": 0.002, "w_max": 1.0,
                "bound_type": bt, "n_sessions": 200, "n_steps": 300,
            }, "network"))

            # MultiField
            params = dict(BASE_PARAMS)
            params["bound_type"] = bt
            params["n_sessions"] = 200
            params["n_steps"] = 300
            params["save_weight_sessions"] = save_sessions
            all_jobs.append(("exp5_dist_multifield", f"{bt}_multifield", seed,
                             params, "multifield"))

            # MetaplasticField
            params_m = dict(BASE_PARAMS)
            params_m["weight_bound_type"] = bt
            params_m["use_soft_eta_bounds"] = False
            params_m["meta_strength"] = 0.005
            params_m["inhibitor_coupling"] = 0.0
            params_m["n_sessions"] = 200
            params_m["n_steps"] = 300
            all_jobs.append(("exp5_dist_metaplastic", f"{bt}_metaplastic", seed,
                             params_m, "metaplastic"))

    return all_jobs


# ============================================================
# Merge helper
# ============================================================

def merge_job_files(experiment_name, output_dir):
    """Merge per-job parquet files into one."""
    import pyarrow.parquet as pq
    import pyarrow as pa

    job_dir = os.path.join(output_dir, experiment_name, "jobs")
    if not os.path.isdir(job_dir):
        print(f"  No jobs directory for {experiment_name}")
        return

    tables = []
    weight_tables = []
    for f in sorted(os.listdir(job_dir)):
        if f.endswith("_weights.parquet"):
            weight_tables.append(pq.read_table(os.path.join(job_dir, f)))
        elif f.endswith(".parquet"):
            tables.append(pq.read_table(os.path.join(job_dir, f)))

    if tables:
        merged = pa.concat_tables(tables, promote_options="default")
        path = os.path.join(output_dir, experiment_name, "session_metrics.parquet")
        pq.write_table(merged, path)
        print(f"  Merged {len(tables)} files -> {len(merged)} rows -> {path}")

    if weight_tables:
        merged_w = pa.concat_tables(weight_tables, promote_options="default")
        path = os.path.join(output_dir, experiment_name, "weight_snapshots.parquet")
        pq.write_table(merged_w, path)
        print(f"  Merged {len(weight_tables)} weight files -> {len(merged_w)} rows")


# ============================================================
# Dispatch and progress
# ============================================================

WORKER_MAP = {
    "network": run_network_job,
    "multifield": run_multifield_job,
    "metaplastic": run_metaplastic_job,
}


def submit_and_track(exp_name, jobs, worker_type, output_dir):
    """Submit all jobs as Ray tasks and track progress."""
    worker_fn = WORKER_MAP[worker_type]

    # Check resume
    job_dir = os.path.join(output_dir, exp_name, "jobs")
    already_done = 0
    if os.path.isdir(job_dir):
        already_done = len([f for f in os.listdir(job_dir)
                            if f.endswith(".parquet") and not f.endswith("_weights.parquet")])

    print(f"\n{'='*60}")
    print(f"  {exp_name}: {len(jobs)} total, {already_done} done, {len(jobs) - already_done} remaining")
    print(f"{'='*60}", flush=True)

    t0 = time.time()

    # Submit all as Ray tasks
    futures = [worker_fn.remote(*job, output_dir) for job in jobs]

    # Collect with progress
    done = 0
    total = len(futures)
    while futures:
        ready, futures = ray.wait(futures, num_returns=min(50, len(futures)), timeout=60)
        results = ray.get(ready)
        done += len(results)
        elapsed = time.time() - t0
        rate = done / elapsed if elapsed > 0 else 0
        remaining = (total - done) / rate if rate > 0 else 0
        skipped = sum(1 for r in results if r.get("skipped", False))
        print(f"  {done}/{total} ({elapsed:.0f}s, ~{remaining:.0f}s left"
              f"{f', {skipped} skipped' if skipped else ''})", flush=True)

    elapsed = time.time() - t0
    print(f"  {exp_name} completed in {elapsed:.0f}s ({elapsed/60:.1f}m)")
    merge_job_files(exp_name, output_dir)


BUILDERS = {
    "exp1": build_exp1_regime,
    "exp2": build_exp2_coexistence,
    "exp3": build_exp3_self_sealing,
    "exp4": build_exp4_continuous,
}


def main():
    parser = argparse.ArgumentParser(description="Paper 4S cluster job runner")
    parser.add_argument("--experiments", nargs="+",
                        default=["exp1", "exp2", "exp3", "exp4", "exp5"])
    parser.add_argument("--seeds", type=int, default=20)
    args = parser.parse_args()

    ray.init()
    resources = ray.cluster_resources()
    n_cpus = resources.get("CPU", 0)
    n_nodes = sum(1 for k in resources if k.startswith("node:"))
    print(f"Cluster: {n_cpus:.0f} CPUs across {n_nodes} nodes")
    print(f"Experiments: {args.experiments}")

    for exp_key in args.experiments:
        if exp_key == "exp5":
            # Exp 5 has mixed substrate types
            all_jobs = build_exp5_distributions(n_seeds=min(args.seeds, 5))

            # Group by experiment name and worker type
            from collections import defaultdict
            grouped = defaultdict(lambda: ([], None))
            for job_tuple in all_jobs:
                exp_name, condition, seed, params, worker_type = job_tuple
                key = (exp_name, worker_type)
                if key not in grouped or grouped[key] == ([], None):
                    grouped[key] = ([], worker_type)
                grouped[key][0].append((exp_name, condition, seed, params))

            for (exp_name, worker_type), (jobs, wt) in grouped.items():
                submit_and_track(exp_name, jobs, wt, NFS_DATA_DIR)
        else:
            builder = BUILDERS[exp_key]
            exp_name, jobs, worker_type = builder(n_seeds=args.seeds)
            submit_and_track(exp_name, jobs, worker_type, NFS_DATA_DIR)

    print(f"\n{'='*60}\n  All experiments done.\n{'='*60}")


if __name__ == "__main__":
    main()
