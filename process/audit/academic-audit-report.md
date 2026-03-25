# Academic Integrity Audit Report

**Programme:** The Dark Forest: Individuation, Coexistence, and Differentiation in Self-Organising Hebbian Networks
**Candidate:** Michael Bean
**Date:** 2026-03-25
**Auditor:** Automated Academic Integrity Coordinator

---

## Phase 1: Citation Verification

**Status: PASS with minor issues**

Eight key citations were verified against their bibliographic entries and the claims made about them.

### Verified citations

| Citation | Bib entry | Claim accuracy |
|---|---|---|
| Hooker et al. 2019 | Correct (arXiv:1911.05248) | Accurate: compressed networks disproportionately harm underrepresented classes |
| Tran et al. 2022 | Correct (NeurIPS 2022) | Accurate: disparate impact of pruning on model accuracy |
| Stringer et al. 2019 | Correct (Nature 571:361-365) | Accurate: 1/n eigenspectrum in visual cortex population responses |
| Adams et al. 2017 | Correct (Scientific Reports 7:997) | Acceptable: "demonstrated formally" is a fair paraphrase of their formal definitions approach |
| Achille et al. 2019 | Correct (ICLR 2019) | Accurate: critical learning periods emerge in deep networks |
| Maturana & Varela 1980 | Correct (D. Reidel, Dordrecht) | Accurate and appropriately qualified: "without claiming full autopoietic organisation" |
| Granovetter 1973 | Correct (AJS 78(6):1360-1380) | Accurate: weak ties carry disproportionate novel information |
| Scholl et al. 2021 | Bib has author error | Claim slightly overcharacterized |

### Issues found

1. **Scholl et al. 2021 author list error.** The bib entry in `dark-forest-bounds/papers/04s-bounds/references.bib` line 81 lists "Bhatt, Daniel H. and Bhatt, Daniel" -- this appears to be a duplication. The actual paper author list should be verified and corrected.

2. **Scholl et al. 2021 claim characterization.** Paper 4S states Scholl et al. "showed formally that information-theoretic pruning criteria reduce generative diversity in deep Boltzmann machines." The actual paper is about developmental pruning using local synaptic rules to optimize global network architecture. The general direction is correct but the specific framing ("reduce generative diversity in deep Boltzmann machines") may be more specific than the source supports. Recommend verifying this characterization against the original paper.

3. **Hooker 2019 venue.** Listed as arXiv preprint. This paper was later published more formally. Minor issue -- arXiv citation is acceptable.

---

## Phase 2: Code-Data Consistency

**Status: PASS**

All key numerical claims were verified against the parquet data files.

### expF_factorial (Paper 4S, disordinal interaction)

| Claim | Paper value | Data value | Match |
|---|---|---|---|
| Hard, pruned | 3.9 +/- 2.1 | 3.9 +/- 2.1 | Exact |
| Tanh, pruned | 0.2 +/- 0.4 | 0.2 +/- 0.4 | Exact |
| Hard, no-prune | 5.6 +/- 3.2 | 5.6 +/- 3.2 | Exact |
| Tanh, no-prune | 7.0 +/- 2.2 | 7.0 +/- 2.2 | Exact |
| Sigmoid == tanh | To 4+ d.p. | Confirmed identical | Exact |

### exp7b_steepness_noprune (Paper 4S, steepness sweep)

| Claim | Paper value | Data value | Match |
|---|---|---|---|
| k=1 (tanh) | 6.0 | 5.95 (rounds to 6.0) | Match |
| k>=2 | 1.0-1.8 monopoly | 1.0-1.75 | Match |
| Hard clip reference | 4.9 | 4.9 (from exp2b) | Exact |

### rev3_rank_validation (Paper 4S, response rank table)

All values match exactly when filtering for qualifying seeds (n_assemblages >= 2), which is the correct methodological approach:

| Threshold | Hard | Tanh | Oja |
|---|---|---|---|
| 0.1% | 5.9 / 5.9 | 5.8 / 5.8 | 6.4 / 6.4 |
| 1% | 5.6 / 5.6 | 5.5 / 5.5 | 5.8 / 5.8 |
| 5% | 4.8 / 4.8 | 4.8 / 4.8 | 5.1 / 5.1 |
| 10% | 4.1 / 4.1 | 4.2 / 4.2 | 4.5 / 4.5 |

(Format: paper / data)

### expE2_eta_extended (Paper 4S, eta F-ratio)

| Claim | Paper value | Data value | Match |
|---|---|---|---|
| Total seeds | 50 | 50 | Exact |
| Qualifying (>=2 asm) | 6 | 6 | Exact |
| Mean F-ratio | 4.91 | 4.91 | Exact |
| t-statistic | 13.77 | 13.77 | Exact |
| One-tailed p | 0.000018 | 0.000018 | Exact |
| Wilcoxon W | 21 | 21 | Exact |
| Wilcoxon p | 0.016 | 0.016 | Exact |

### exp8fv_critical_period

| Claim | Paper value | Data value | Match |
|---|---|---|---|
| Switch=0, coupling=0.01 | rank 0.05 | 0.05 | Exact |
| Switch=50, coupling=0.01 | rank 0.85 | 0.85 | Exact |

### Reproducibility chain verification

Three complete claim-to-data chains were traced:
1. **expF_factorial**: cluster_job_phase2.py -> MultiField(prune_threshold=1e-4/1e-8, bound_type=hard/tanh/oja/sigmoid) -> 200 sessions x 300 steps -> n_assemblages -> paper claims. Verified.
2. **expE2_eta_extended**: cluster_job_phase3b.py -> MetaplasticField(soft eta bounds, hard weight bounds) -> 300 sessions -> eta_f_ratio -> paper claims. Verified.
3. **rev3_rank_validation**: cluster_job_revision.py -> MultiField -> 200 sessions -> 10 Gaussian probes -> SVD -> rank at thresholds -> paper claims. Verified.

---

## Phase 3: Statistical Methods

**Status: PASS with one inconsistency**

### Reproduced statistics

| Test | Paper value | Reproduced | Match |
|---|---|---|---|
| Wilcoxon W | 21 | 21 | Exact |
| Wilcoxon p (one-tailed) | 0.016 | 0.016 | Exact |
| Cohen's d | 5.62 | 5.62 | Exact |
| t(5) | 13.77 | 13.77 | Exact |
| One-tailed p | 0.000018 | 0.000018 | Exact |

### Issues found

1. **Shapiro-Wilk p-value discrepancy.** Paper 4 reports Shapiro-Wilk normality p = 0.40. Reproduction from the 6 qualifying F-ratios [3.93, 5.88, 4.37, 5.08, 4.88, 5.35] gives W = 0.990, p = 0.99. The directional conclusion (normality not rejected) holds either way, but the reported value is incorrect. **Severity: Low** -- the wrong value is more conservative than the true value, and the parametric test (t-test) is well-justified either way.

2. **SD convention inconsistency.** Paper 4S reports SD = 0.64 (population SD, ddof=0) in the table but Cohen's d = 5.62 uses sample SD (ddof=1, SD=0.70). Both choices are individually defensible, but using different conventions in the same paragraph is an error. The paper should consistently use one convention. With ddof=1: SD=0.70, d=5.62. With ddof=0: SD=0.64, d=6.16. **Severity: Low** -- affects reported precision, not conclusions.

3. **Multiple comparisons.** Not an issue. The eta F-ratio analysis involves a single one-sample t-test (against F=1), with the Wilcoxon as a confirmatory non-parametric alternative. No correction needed.

---

## Phase 4: Internal Consistency

**Status: FAIL -- requires corrections before defence**

### Critical issue: dissertation-frame.qmd is outdated

The file `dark-forest-bounds/dissertation-frame.qmd` contains multiple inconsistencies with the final papers:

1. **"structural germ" vs "limit condition" (4 occurrences).**
   - Line 73: "structural germ in Simondon's sense"
   - Line 82: "propagates from a structural germ"
   - Line 83: "The hard clip boundary functions as this germ"
   - Line 176: "functions as a structural germ for the metaplastic instability"
   - Line 232: "structural germ that makes differenciation possible"

   Paper 4S explicitly distinguishes a structural germ (which templates form through propagation) from a limit condition (which constrains without imposing form) and classifies the hard clip as the latter. The dissertation-frame uses the wrong Simondonian category throughout.

2. **Response rank value "4.7" instead of "5.6" (2 occurrences).**
   - Line 72: "response rank 4.7 vs 2.4"
   - Line 152: "response rank 4.7"

   The final data from rev3_rank_validation confirms rank = 5.6 at the 1% threshold for qualifying seeds. The value 4.7 appears to be from an earlier analysis.

### No issues found

- No remaining "4.7" in the dissertation chapters (introduction.qmd, synthesis.qmd, conclusion.qmd) -- these all use "5.6" correctly.
- No "Enables" in titles -- all use "Stabilises."
- CCD is properly qualified in all papers and dissertation chapters.
- "differenciation" consistently defined and distinguished from "differentiation."

### Note on dissertation-frame.qmd vs dissertation chapters

The `dissertation-frame.qmd` appears to be a standalone summary document, possibly an earlier version. The actual dissertation chapters under `dissertation/chapters/` are internally consistent and use correct terminology. If the dissertation-frame.qmd is not part of the submitted dissertation, these issues are less critical. However, if it is the framing document that examiners will read, it must be corrected before defence.

---

## Phase 5: Philosophical Terms

**Status: PASS**

### Limit condition vs mould

The distinction is correctly maintained in Papers 4 and 4S and in the dissertation chapters:
- **Limit condition** (condition limite): the hard weight clip. Constrains the space of possible individuations without imposing specific form. Creates an absorbing boundary.
- **Mould** (moule): the pruning threshold. An external constraint that imposes form by selectively eliminating structures.

Paper 4S's footnote (lines 44-48 of the abstract) explicitly defines both terms and the distinction. This is philosophically sound.

### Differenciation

Properly defined in Paper 4's abstract (lines 24-29) and dissertation introduction (lines 109-117). The Deleuzian spelling is consistently used to mark the ontological concept vs the empirical measurement.

### Autopoiesis

Paper 4 (lines 978-986) correctly qualifies the connection: "without claiming full autopoietic organisation, which requires additional criteria including self-production of components." Cites Beer 2020 for the qualification and Thompson 2007 for the hierarchy of autonomy. The synthesis chapter mirrors this qualification. Appropriately hedged.

### Adams et al. characterization

Paper 4 says "demonstrated formally that only state-dependent update rules produce unbounded evolutionary dynamics." The synthesis says "proved formally." Adams et al. 2017 did provide formal definitions and derive conditions. "Demonstrated formally" is accurate; "proved formally" in the synthesis is slightly stronger but defensible given the paper's mathematical framework. Recommend softening to "demonstrated" or "showed" in the synthesis for safety.

---

## Phase 6: Reproducibility

**Status: PASS**

Three complete claim-to-data chains were traced through source code to data to paper claims:

1. **Factorial interaction (expF_factorial):** `cluster_job_phase2.py` line 58 -> `MultiField` with pruning on/off x bound type -> 200 sessions x 300 steps x 30 seeds -> `session_metrics.parquet` -> Paper 4S Fig. 2 values. All parameters match paper methods. Data matches claims exactly.

2. **Eta F-ratio (expE2_eta_extended):** `cluster_job_phase3b.py` line 333 -> `MetaplasticField` with soft eta bounds, hard weight bounds -> 300 sessions x 50 seeds -> `eta_f_ratio` computed as between/within variance -> Paper 4S claims. Code computes F-ratio correctly (line 399: `np.var(asm_means) / max(np.mean(within_vars), 1e-12)`). Data matches claims.

3. **Rank validation (rev3_rank_validation):** `cluster_job_revision.py` line 213 -> `MultiField` -> 200 sessions training -> 10 Gaussian probes -> SVD of response matrix -> rank at 5 thresholds + participation ratio -> Paper 4S rank table. Code implements probe injection and SVD correctly. Data matches claims.

All three chains are fully traceable from code to data to paper.

---

## Phase 7: Prose Quality

**Status: PASS with observations**

### Dissertation chapters (introduction, synthesis, conclusion)

The prose is clear, well-structured, and logically coherent. The argument builds systematically from Paper 1 through Paper 4S. Key strengths:

- The three-philosopher framework (Simondon/Deleuze/DeLanda) is deployed precisely, with each thinker assigned a specific analytical role.
- Negative results (Paper 3, CCD null, Turing failure) are positioned as essential contributions rather than failures.
- The "productive fracture" concept is well-defined and serves as an honest characterization of what the programme does and does not achieve.
- Cross-domain convergence claims (pruning in ML, ecology, immunology) are handled carefully, with the synthesis chapter noting convergence as evidence of domain-generality rather than redundancy.

### Observations (not blocking)

1. **Synthesis "proved formally" (line 44).** "Adams et al. (2017) proved formally that only state-dependent update rules produce unbounded evolution." Recommend softening to "demonstrated formally" or "showed formally" for philosophical precision.

2. **Conclusion broader implications section.** The neurodevelopmental, ML compression, and immune repertoire implications are speculative but appropriately framed as "the programme's framework could inform" rather than definitive claims. This is acceptable for a doctoral conclusion.

3. **Programme statistics table** (synthesis.qmd lines 139-147) reports "Papers published/accepted: 5" and "Venue: Artificial Life." If any papers are not yet published, this should be corrected to avoid misrepresentation.

---

## Summary of All Issues

### Must fix before defence (2 issues)

1. **dissertation-frame.qmd: "structural germ" -> "limit condition"** at lines 73, 82-83, 176, 232. The hard clip is a limit condition, not a structural germ. An examiner familiar with Simondon would catch this immediately.

2. **dissertation-frame.qmd: "4.7" -> "5.6"** at lines 72 and 152. The response rank value has been updated in the data and papers but not in this framing document.

### Should fix before defence (3 issues)

3. **Shapiro-Wilk p=0.40** in Paper 4 (line 763). The actual value is p=0.99. While directionally identical, an incorrect test statistic could attract scrutiny.

4. **SD convention mixing** in Paper 4S. The table reports population SD (0.64) while Cohen's d uses sample SD (0.70). Pick one convention and be consistent.

5. **Scholl et al. 2021 bib entry** has a duplicated author ("Bhatt, Daniel H. and Bhatt, Daniel"). Verify and correct the author list.

### Minor / optional (2 issues)

6. **Scholl et al. 2021 claim characterization.** Verify that the paper specifically discusses "generative diversity in deep Boltzmann machines."

7. **Synthesis "proved formally" -> "demonstrated formally"** for Adams et al. 2017 characterization.

---

## Overall Assessment

### READY FOR DEFENCE (with corrections)

The programme is methodologically sound, internally consistent across data and code, and philosophically rigorous. All key numerical claims are verified against the raw data. The code-to-data-to-paper chain is fully traceable. The statistical methods are appropriate and reproducible.

The two critical issues in the dissertation-frame.qmd (terminology and outdated numbers) must be fixed before submission, as they represent clear contradictions with the final papers that an informed examiner would identify. If the dissertation-frame.qmd is not part of the submitted dissertation, this risk is eliminated.

The remaining issues are minor and unlikely to affect the outcome of a defence, but correcting them before submission would strengthen the candidate's position against close statistical or bibliographic scrutiny.
