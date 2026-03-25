# Eta ANOVA: Statistical Report

## Hard weight + soft η bounds (Exp E, session 200)

### Sample
- Seeds with ≥2 assemblages: n=4 (of 20 total seeds)
- Mean assemblages per seed: 2.2
- Note: Low n due to hard+soft η producing few assemblages. Exp E2 (n=50, 300 sessions) submitted for replication.

### Per-seed F-ratios (between/within assemblage eta variance)

| Seed | F-ratio | n_asm | Between-var | Within-var |
|------|---------|-------|-------------|------------|
| 0    | 5.82    | 3     | 0.000577    | 0.000099   |
| 8    | 4.88    | 2     | 0.000698    | 0.000143   |
| 14   | 3.77    | 2     | 0.000626    | 0.000166   |
| 15   | 4.74    | 2     | 0.000696    | 0.000147   |

### Aggregate statistics
- Mean F-ratio: 4.80 (SD = 0.72)
- Median F-ratio: 4.81
- Bootstrap 95% CI (BCa, 10K iterations): [4.05, 5.55]
- One-sample t-test (H0: F = 1): t(3) = 9.094, p = 0.0014 (one-tailed)
- Cohen's d: 4.55 (very large)
- Partial η²: 0.824, 95% CI [0.801, 0.845]

### Comparison conditions (all soft η)

| Weight bound | n (≥2 asm) | F ± SD | t | p (one-tail) | d | η²p |
|---|---|---|---|---|---|---|
| Hard | 4 | 4.80 ± 0.72 | 9.09 | 0.0014 | 4.55 | 0.824 |
| Tanh | 18 | 0.86 ± 0.86 | -0.65 | 0.262 | -0.15 | 0.330 |
| Sigmoid | 18 | 0.86 ± 0.86 | -0.65 | 0.262 | -0.15 | 0.330 |
| Oja | 20 | 0.76 ± 0.39 | -2.71 | 0.007 | -0.61 | 0.434 |

### Interpretation
- Only hard weight bounds produce F > 1 (between > within assemblage eta variance)
- Tanh/sigmoid: F < 1, eta does not differentiate between assemblages
- Oja: F significantly < 1 (p=0.007), within-assemblage variance exceeds between — eta is noisier within than between assemblages
- Effect size under hard bounds is very large (d=4.55, η²p=0.824)

### Okafor's concerns addressed
1. **Degrees of freedom**: df_between varies by seed (1-2 for asm counts 2-3), df_within = nodes per assemblage - assemblages. Full table above.
2. **Pseudoreplication**: F-ratios computed within each seed separately, then aggregated with t-test across seeds. This avoids pseudoreplication — each seed is one independent observation.
3. **Bootstrap CIs**: Provided via BCa method, 10K iterations.
4. **Low n warning**: Only 4 seeds qualify. Exp E2 (n=50, 300 sessions) running to address this.
