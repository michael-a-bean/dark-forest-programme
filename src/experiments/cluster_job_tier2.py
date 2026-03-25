#!/usr/bin/env python3
"""Tier 2 experiments for Paper 4 revision.

Submitted via `ray job submit` to the cluster. Runs on cluster Python (3.12).
Designed to persist independently of the submitting machine.

Experiments:
  exp13_bound_factorial: Full {hard,soft} x {baseline,global,local} factorial
                         for functional probe. Fills gaps in Exp 12.
                         2 new conditions x 20 seeds = 40 jobs.

  exp14_null_model:      Null model for response_diversity. Permute eta values
                         across assemblages at final session, recompute metric.
                         Uses local_target condition from Exp 12 as base.
                         1000 permutations x 20 seeds = computed post-hoc, not
                         a simulation experiment. Runs as analysis on existing data.

  exp15_dynamics_compare: Record per-session weight distributions and eta
                         trajectories for hard vs soft eta bounds at coup=0.
                         Diagnoses WHY soft bounds reduce CCD.
                         2 conditions x 20 seeds = 40 jobs, 200 sessions.
                         Records additional columns: weight_std, weight_max,
                         eta_skew, pct_eta_at_bound.
"""

import argparse
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


@ray.remote
def run_job(experiment_name, condition, seed, params, output_dir):
    """Run one metaplastic simulation on a Ray worker."""
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
    )

    rows = []
    for session in range(1, params["n_sessions"] + 1):
        for _ in range(params["n_steps"]):
            mf.step()

        asm = mf.find_assemblages()
        c = mf.census()
        eta_div = eta_divergence(mf.node_eta, asm)

        # Functional probe: response diversity
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

        # Extended diagnostics for dynamics comparison
        w_vals = np.array(list(mf.weights.values())) if mf.weights else np.array([0.0])
        eta_vals = mf.node_eta

        # Percentage of eta values at bounds (within 1% of min or max)
        eta_range = mf.eta_max - mf.eta_min
        at_min = np.sum(eta_vals < mf.eta_min + 0.01 * eta_range)
        at_max = np.sum(eta_vals > mf.eta_max - 0.01 * eta_range)
        pct_at_bound = float(at_min + at_max) / len(eta_vals)

        from scipy.stats import skew as scipy_skew
        eta_skew = float(scipy_skew(eta_vals)) if len(eta_vals) > 2 else 0.0

        rows.append({
            "experiment": experiment_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "total_steps": mf.step_count,
            "n_edges": len(mf.weights),
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
            "eta_divergence": eta_div,
            "n_assemblages": len(asm),
            "largest_assemblage": sorted([len(a) for a in asm], reverse=True)[0] if asm else 0,
            "mean_energy": c["mean_energy"],
            "mean_weight": c["mean_weight"],
            "mean_eta": c["mean_eta"],
            "eta_std": c["eta_std"],
            "eta_range": c["eta_range"],
            "mean_inhibitor": c["mean_inhibitor"],
            "max_inhibitor": c["max_inhibitor"],
            "locality": float(params["locality"]),
            "meta_strength": float(params["meta_strength"]),
            "inhibitor_diffusion": float(params["inhibitor_diffusion"]),
            "inhibitor_coupling": float(params["inhibitor_coupling"]),
            "inhibitor_decay": float(params["inhibitor_decay"]),
            "grid_size": int(params["grid_size"]),
            "target_radius": int(params.get("target_radius", 1)),
            "coupling_switch_session": 0,
            "perturb_session": 0,
            "perturb_fraction": 0.0,
            "use_soft_bounds": int(params.get("use_soft_bounds", False)),
            "response_diversity": response_div,
            # Extended diagnostics
            "weight_std": float(np.std(w_vals)),
            "weight_max": float(np.max(np.abs(w_vals))),
            "eta_skew": eta_skew,
            "pct_eta_at_bound": pct_at_bound,
        })

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"condition": condition, "seed": seed, "n_rows": len(rows)}


def merge_job_files(experiment_name, output_dir):
    import pyarrow.parquet as pq
    import pyarrow as pa

    job_dir = os.path.join(output_dir, experiment_name, "jobs")
    if not os.path.isdir(job_dir):
        print(f"  No jobs directory for {experiment_name}")
        return
    tables = [pq.read_table(os.path.join(job_dir, f))
              for f in sorted(os.listdir(job_dir)) if f.endswith(".parquet")]
    if not tables:
        print(f"  No job files for {experiment_name}")
        return
    merged = pa.concat_tables(tables, promote_options="default")
    path = os.path.join(output_dir, experiment_name, "session_metrics.parquet")
    pq.write_table(merged, path)
    print(f"  Merged {len(tables)} files -> {len(merged)} rows -> {path}")


def build_exp13_bound_factorial(n_seeds=20):
    """Exp 13: Complete the bound-type factorial for functional probe.
    Fills gaps in Exp 12: adds baseline_soft and global_soft conditions.
    Plus reruns all 4 original conditions for consistency with extended metrics.
    6 conditions x 20 seeds = 120 jobs.
    """
    conditions = [
        ("baseline_hard", {"meta_strength": 0.0, "use_local_target": False, "use_soft_bounds": False}),
        ("baseline_soft", {"meta_strength": 0.0, "use_local_target": False, "use_soft_bounds": True}),
        ("global_hard", {"meta_strength": 0.05, "use_local_target": False, "use_soft_bounds": False}),
        ("global_soft", {"meta_strength": 0.05, "use_local_target": False, "use_soft_bounds": True}),
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
            jobs.append(("exp13_bound_factorial", cond_name, seed, params))
    return "exp13_bound_factorial", jobs


def build_exp15_dynamics_compare(n_seeds=20):
    """Exp 15: Detailed dynamics comparison hard vs soft eta bounds.
    Records extended metrics to diagnose WHY soft bounds reduce CCD.
    2 conditions x 20 seeds = 40 jobs.
    """
    jobs = []
    for soft in [False, True]:
        label = "soft" if soft else "hard"
        for seed in range(n_seeds):
            params = dict(BASE_PARAMS)
            params["locality"] = 0.10
            params["meta_strength"] = 0.05
            params["inhibitor_coupling"] = 0.0
            params["use_local_target"] = True
            params["use_soft_bounds"] = soft
            jobs.append(("exp15_dynamics_compare", f"eta_{label}", seed, params))
    return "exp15_dynamics_compare", jobs


BUILDERS = {
    "exp13": build_exp13_bound_factorial,
    "exp15": build_exp15_dynamics_compare,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiments", nargs="+", default=["exp13", "exp15"])
    parser.add_argument("--seeds", type=int, default=20)
    args = parser.parse_args()

    ray.init()
    resources = ray.cluster_resources()
    print(f"Cluster: {resources.get('CPU', 0):.0f} CPUs")
    print(f"Experiments: {args.experiments}")

    for exp_name in args.experiments:
        builder = BUILDERS[exp_name]
        name, jobs = builder(args.seeds)

        job_dir = os.path.join(NFS_DATA_DIR, name, "jobs")
        already_done = 0
        if os.path.isdir(job_dir):
            already_done = len([f for f in os.listdir(job_dir) if f.endswith(".parquet")])

        print(f"\n{'=' * 60}")
        print(f"  {name}: {len(jobs)} total, {already_done} done, {len(jobs) - already_done} remaining")
        print(f"{'=' * 60}", flush=True)

        t0 = time.time()
        futures = [run_job.remote(*job, NFS_DATA_DIR) for job in jobs]

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
            print(f"  {done}/{total} ({elapsed:.0f}s, ~{remaining:.0f}s left, {skipped} skipped)", flush=True)

        elapsed = time.time() - t0
        print(f"  {name} completed in {elapsed:.0f}s ({elapsed / 60:.1f}m)")
        merge_job_files(name, NFS_DATA_DIR)

    print(f"\n{'=' * 60}\n  All experiments done.\n{'=' * 60}")


if __name__ == "__main__":
    main()
