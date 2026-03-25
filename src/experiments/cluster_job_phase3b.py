#!/usr/bin/env python3
"""Phase 3b: Okafor's mandatory corrections.

Three experiments:
  R2: Spatially-deconfounded response probes (uniform random stimuli)
  S:  Steepness eta snapshots at k=2-5 (explain non-monotonicity)
  E2: Extended eta ANOVA with more seeds for hard+soft eta (n=50)

Usage:
    ray job submit --address http://192.168.1.11:8265 \
        --working-dir . \
        --runtime-env-json '{"pip": ["numpy", "pyarrow", "scikit-learn", "scipy"], "excludes": ["data/", "papers/", ".git/", ".pytest_cache/"]}' \
        --no-wait \
        -- python3 -m src.cluster_job_phase3b
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
# Exp R2: Deconfounded response probes (uniform random stimuli)
# ============================================================

@ray.remote
def run_deconfounded_probe_job(condition, seed, params):
    """Response-profile with spatially UNIFORM probes (no Gaussian structure)."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance
    from scipy.spatial.distance import jensenshannon

    exp_name = "expR2_deconfounded_probes"
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

    # Run to steady state
    for session in range(200):
        for _ in range(300):
            mf.step()
        if not prune_on and len(mf.weights) > max_edges:
            sorted_edges = sorted(mf.weights.items(), key=lambda x: abs(x[1]))
            for k, _ in sorted_edges[:len(mf.weights) - max_edges]:
                del mf.weights[k]

    asm = mf.find_assemblages()
    n_asm = len(asm)
    baseline_ccd = centroid_cosine_distance(mf.weights, asm, mf.n_nodes)
    baseline_mod = weight_modularity(mf.weights, asm)

    if n_asm < 2:
        row = {
            "experiment": exp_name, "condition": condition, "seed": seed,
            "bound_type": params["bound_type"], "prune_on": prune_on,
            "n_assemblages": n_asm, "n_edges": len(mf.weights),
            "mean_weight": float(np.mean(np.abs(list(mf.weights.values())))) if mf.weights else 0,
            "baseline_ccd": baseline_ccd, "baseline_modularity": baseline_mod,
            "uniform_mean_js": None, "uniform_max_js": None,
            "uniform_response_rank": None,
            "gaussian_mean_js": None, "gaussian_max_js": None,
            "gaussian_response_rank": None,
            "n_probes": 0,
        }
        os.makedirs(job_dir, exist_ok=True)
        pq.write_table(pa.Table.from_pylist([row]), job_file)
        return row

    saved_activations = mf.activations.copy()
    saved_weights = dict(mf.weights)
    probe_rng = np.random.default_rng(seed + 888888)
    n_probes = 10

    def run_probes(stimulus_fn):
        """Run probes and return (mean_js, max_js, response_rank)."""
        responses = []  # (n_probes, n_asm)
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
        shifted = rm - rm.min(axis=1, keepdims=True) + 1e-8
        probs = shifted / shifted.sum(axis=1, keepdims=True)

        js_divs = []
        for i in range(n_asm):
            for j in range(i + 1, n_asm):
                js = jensenshannon(probs[i], probs[j])
                if np.isfinite(js):
                    js_divs.append(js)

        if rm.shape[0] >= 2:
            U, s, Vt = np.linalg.svd(rm - rm.mean(axis=0), full_matrices=False)
            s_norm = s**2 / np.sum(s**2) if np.sum(s**2) > 0 else s
            eff_rank = float(1.0 / np.sum(s_norm**2)) if np.sum(s_norm**2) > 0 else 0
        else:
            eff_rank = 0

        return (
            float(np.mean(js_divs)) if js_divs else 0,
            float(np.max(js_divs)) if js_divs else 0,
            eff_rank,
        )

    # Uniform random probes (spatially deconfounded)
    def uniform_stimulus():
        return probe_rng.uniform(-0.3, 0.3, mf.n_nodes)

    # Gaussian probes (original, spatially structured)
    def gaussian_stimulus():
        cx, cy = probe_rng.uniform(0.1, 0.9, 2)
        d = np.sqrt((mf.pos_x - cx)**2 + (mf.pos_y - cy)**2)
        return 0.5 * np.exp(-d**2 / (2 * 0.1**2))

    u_js, u_js_max, u_rank = run_probes(uniform_stimulus)
    g_js, g_js_max, g_rank = run_probes(gaussian_stimulus)

    row = {
        "experiment": exp_name, "condition": condition, "seed": seed,
        "bound_type": params["bound_type"], "prune_on": prune_on,
        "n_assemblages": n_asm, "n_edges": len(saved_weights),
        "mean_weight": float(np.mean(np.abs(list(saved_weights.values())))) if saved_weights else 0,
        "baseline_ccd": baseline_ccd, "baseline_modularity": baseline_mod,
        "uniform_mean_js": u_js, "uniform_max_js": u_js_max,
        "uniform_response_rank": u_rank,
        "gaussian_mean_js": g_js, "gaussian_max_js": g_js_max,
        "gaussian_response_rank": g_rank,
        "n_probes": n_probes,
    }

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist([row]), job_file)
    return row


# ============================================================
# Exp S: Steepness eta snapshots (k=2-5, explain non-monotonicity)
# ============================================================

@ray.remote
def run_steepness_eta_job(condition, seed, params):
    """Steepness sweep with eta distribution snapshots at key sessions."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.multifield import MultiField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "expS_steepness_eta"
    job_dir = os.path.join(NFS_DATA_DIR, exp_name, "jobs")
    job_file = os.path.join(job_dir, f"{condition}_seed{seed:04d}.parquet")
    if os.path.exists(job_file):
        return {"skipped": True}

    steepness = params["steepness"]
    max_edges = 20000

    class SteepMultiField(MultiField):
        def __init__(self, steepness_k, **kwargs):
            super().__init__(bound_type="hard", **kwargs)
            self.steepness_k = steepness_k

        def step(self):
            self.step_count += 1
            noise = self.rng.uniform(-1, 1, self.n_nodes) * self.noise_profile
            self.activations += noise

            new_input = np.zeros(self.n_nodes)
            in_degree = np.zeros(self.n_nodes)
            for (i, j), w in self.weights.items():
                new_input[j] += w * self.activations[i]
                in_degree[j] += 1
            scale = np.where(in_degree > 0, np.sqrt(np.maximum(in_degree, 1)), 1.0)
            self.activations = np.tanh(0.5 * self.activations + new_input / scale)

            k = self.steepness_k
            for (i, j) in list(self.weights.keys()):
                self.weights[(i, j)] += self.eta * self.activations[i] * self.activations[j]
                self.weights[(i, j)] *= (1.0 - self.lam)
                w = self.weights[(i, j)]
                self.weights[(i, j)] = self.w_max * np.tanh(k * w / self.w_max)

            for _ in range(self.encounter_rate):
                i, j = self._local_encounter_pair()
                if i != j and (i, j) not in self.weights:
                    self.weights[(i, j)] = 0.0
                    self.edges_created += 1

            dead = [key for key, w in self.weights.items() if abs(w) < 1e-8]
            for key in dead:
                del self.weights[key]
                self.edges_pruned += 1

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
        prune_threshold=1e-8,
        seed=seed,
    )

    rows = []
    for session in range(1, 101):
        for _ in range(300):
            mf.step()

        if len(mf.weights) > max_edges:
            sorted_edges = sorted(mf.weights.items(), key=lambda x: abs(x[1]))
            for k_e, _ in sorted_edges[:len(mf.weights) - max_edges]:
                del mf.weights[k_e]

        asm = mf.find_assemblages()
        c = mf.census()

        # Weight distribution stats
        w_arr = np.abs(list(mf.weights.values())) if mf.weights else [0]

        row = {
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "steepness": float(steepness),
            "n_assemblages": len(asm),
            "n_edges": c["n_edges"],
            "mean_weight": c["mean_weight"],
            "max_weight": c["max_weight"],
            "modularity": weight_modularity(mf.weights, asm),
            "centroid_cosine_distance": centroid_cosine_distance(mf.weights, asm, mf.n_nodes),
            # Weight distribution
            "weight_std": float(np.std(w_arr)),
            "weight_p25": float(np.percentile(w_arr, 25)),
            "weight_p75": float(np.percentile(w_arr, 75)),
            "pct_saturated": float(np.mean(np.array(w_arr) > 0.95)),
            # Activity distribution
            "act_mean": float(np.mean(np.abs(mf.activations))),
            "act_std": float(np.std(mf.activations)),
            # Energy
            "mean_energy": c["mean_energy"],
        }

        # Snapshot weight histogram at key sessions
        if session in {10, 25, 50, 75, 100}:
            # Bin weights into 10 bins from 0 to 1
            hist, _ = np.histogram(w_arr, bins=10, range=(0, 1))
            for i, count in enumerate(hist):
                row[f"whist_bin{i}"] = int(count)

        rows.append(row)

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


# ============================================================
# Exp E2: Extended eta ANOVA — more seeds for hard+soft eta
# ============================================================

@ray.remote
def run_eta_extended_job(condition, seed, params):
    """MetaplasticField with eta snapshots — extended seeds for hard+soft eta."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from src.substrate.metaplastic_field import MetaplasticField
    from src.metrics.modularity import weight_modularity
    from src.metrics.centroid_distance import centroid_cosine_distance

    exp_name = "expE2_eta_extended"
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
    for session in range(1, 301):  # 300 sessions for more stable estimates
        for _ in range(300):
            mf.step()

        asm = mf.find_assemblages()

        row = {
            "experiment": exp_name,
            "condition": condition,
            "seed": seed,
            "session": session,
            "weight_bound_type": params["weight_bound_type"],
            "eta_bound_type": "soft" if params["use_soft_eta_bounds"] else "hard",
            "n_assemblages": len(asm),
            "n_edges": len(mf.weights),
            "eta_mean": float(np.mean(mf.node_eta)),
            "eta_std": float(np.std(mf.node_eta)),
            "pct_eta_at_min": float(np.mean(mf.node_eta <= params["eta_min"] + 1e-6)),
            "pct_eta_at_max": float(np.mean(mf.node_eta >= params["eta_max"] - 1e-6)),
        }

        if len(asm) >= 2:
            asm_means = [float(np.mean(mf.node_eta[list(nodes)])) for nodes in asm]
            within_vars = [float(np.var(mf.node_eta[list(nodes)])) for nodes in asm]
            row["eta_between_var"] = float(np.var(asm_means))
            row["eta_within_var"] = float(np.mean(within_vars))
            row["eta_f_ratio"] = float(np.var(asm_means) / max(np.mean(within_vars), 1e-12))
        else:
            row["eta_between_var"] = None
            row["eta_within_var"] = None
            row["eta_f_ratio"] = None

        # Save eta snapshot at key sessions
        if session in {100, 200, 300}:
            row["eta_snapshot"] = ",".join(f"{e:.6f}" for e in mf.node_eta)
        else:
            row["eta_snapshot"] = None

        rows.append(row)

    os.makedirs(job_dir, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), job_file)
    return {"n_rows": len(rows)}


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
                    'seed', 'n_assemblages', 'n_edges', 'n_probes', 'session',
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

    # ---- Exp R2: Deconfounded probes (240 jobs) ----
    print(f"\n{'='*60}")
    print("Exp R2: Deconfounded response probes (240 jobs)")
    print(f"{'='*60}")
    futures_R2 = []
    for bt in BOUND_TYPES:
        for prune_on in [True, False]:
            tag = "pruned" if prune_on else "noprune"
            for seed in range(30):
                condition = f"{bt}_{tag}"
                params = dict(BASE_PARAMS)
                params["bound_type"] = bt
                params["prune_on"] = prune_on
                futures_R2.append(run_deconfounded_probe_job.remote(condition, seed, params))
    _wait_all(futures_R2, "Exp R2")
    merge_and_copy("expR2_deconfounded_probes")

    # ---- Exp S: Steepness eta snapshots (160 jobs) ----
    # k=1, 2, 3, 5, 10, 50, plus hard clip baseline via standard MultiField
    print(f"\n{'='*60}")
    print("Exp S: Steepness eta snapshots (160 jobs)")
    print(f"{'='*60}")
    steepness_values = [1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0]
    futures_S = []
    for k in steepness_values:
        for seed in range(20):
            condition = f"k{k:.1f}_loc0.10"
            params = dict(BASE_PARAMS)
            params["steepness"] = k
            futures_S.append(run_steepness_eta_job.remote(condition, seed, params))
    _wait_all(futures_S, "Exp S")
    merge_and_copy("expS_steepness_eta")

    # ---- Exp E2: Extended eta ANOVA (50 seeds, hard+soft eta only) ----
    print(f"\n{'='*60}")
    print("Exp E2: Extended eta ANOVA — hard+soft eta, 50 seeds, 300 sessions (50 jobs)")
    print(f"{'='*60}")
    futures_E2 = []
    for seed in range(50):
        condition = "whard_soft_eta"
        params = dict(BASE_PARAMS)
        params["weight_bound_type"] = "hard"
        params["use_soft_eta_bounds"] = True
        params["meta_strength"] = 0.005
        params["inhibitor_coupling"] = 0.0
        futures_E2.append(run_eta_extended_job.remote(condition, seed, params))
    _wait_all(futures_E2, "Exp E2")
    merge_and_copy("expE2_eta_extended")

    elapsed = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"ALL PHASE 3b COMPLETE in {elapsed:.0f}s ({elapsed/3600:.1f}h)")
    print(f"{'='*60}")
    print("  expR2_deconfounded_probes — uniform vs Gaussian probes")
    print("  expS_steepness_eta       — weight distributions at k=1-50")
    print("  expE2_eta_extended       — hard+soft eta with n=50, 300 sessions")


if __name__ == "__main__":
    main()
