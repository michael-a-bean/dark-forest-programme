# Response to Reviewers — Paper 4S Revision

**Manuscript:** "Pruning as Confound: How Maintenance Processes Obscure Functional Diversity in Self-Organising Networks"
**Journal:** *Artificial Life*

---

Dear Editor,

Thank you for the detailed and constructive reviews. All six required revisions have been addressed, along with three of the four recommended revisions. We ran three new experiment sets (780 jobs) to address the reviewers' concerns. Below we respond to each point.

---

## Required Revisions

### 1. Edge Cap Sensitivity Analysis (R2-M1)

**Concern:** The rank-based edge cap at 20,000 may reintroduce the confound by differentially removing soft-bounded edges.

**Response:** We ran a sensitivity sweep over five cap values (5,000; 10,000; 20,000; 50,000; unlimited) crossed with three bound types and 20 seeds. **Results are identical at every cap value:** hard = 5.6, tanh = 6.9, oja = 8.2 assemblages regardless of cap. Edge count self-stabilises at ~1,350 on the 20×20 grid — the cap is never activated. The Hebbian dynamics reach a natural equilibrium between encounter-driven creation and decay-driven loss well below any reasonable cap. We have added this result with an explanation to the Results section.

### 2. Response Rank Validation (R1-M3, R2-M3)

**Concern:** The SVD threshold (1% of largest singular value) is a free parameter. The rank distinction may be threshold-dependent.

**Response:** We now report rank at five thresholds (0.1%, 0.5%, 1%, 5%, 10%) and the participation ratio (threshold-free effective dimensionality). Results:

| Threshold | Hard (no-prune) | Tanh (no-prune) | Pruned (all) |
|---|---|---|---|
| 0.1% | 5.9 | 5.8 | 1.0 |
| 1% | 5.6 | 5.5 | 1.0 |
| 10% | 4.1 | 4.2 | 1.0 |
| Participation ratio | 2.2 | 2.1 | 1.0 |

The no-prune rank ranges from 4.1 to 5.9 across thresholds; pruned rank is flat at 1.0. The distinction is unambiguous at every threshold. We thank R2 for the participation ratio suggestion — it provides a clean, threshold-free confirmation. Primary rank number updated from 4.7 to 5.6 (reflecting improved 10-probe methodology).

### 3. Eta ANOVA Power and Selection (R2-M2)

**Concern:** Only 6/50 seeds qualify; selection bias may inflate effect size.

**Response:** We now report the failure mode analysis. All 44 excluded seeds converge to monopoly (single assemblage), not dissolution. Monopoly and multi-assemblage seeds show identical eta statistics (mean η = 0.098, σ = 0.019) and edge counts (~1,310). The qualifying count fluctuates stochastically between 5 and 8 across sessions with no trend. Coexistence under hard weight + soft η bounds is a rare but genuine dynamical regime, and the 6 qualifying seeds are not selected for high eta divergence — they are selected for having maintained coexistence.

The F-ratio of 4.91 represents the ratio of between-assemblage to within-assemblage eta variance, computed within each seed separately and aggregated across seeds via t-test against F = 1. The large Cohen's d (5.62) reflects the consistency of the effect across the 6 seeds (SD = 0.64), not inflated variance.

### 4. CCD Null Model Specification (R1-M2)

**Concern:** The null model is insufficiently specified.

**Response:** We have added a full specification to the Methods section: weight values are randomly permuted across edges (preserving edge topology), assemblages are re-detected using the same adaptive threshold (75th percentile), and CCD is recomputed. This is repeated 1,000 times per seed. The p-value is the proportion of null CCD values ≥ observed CCD.

### 5. Grid Size Generality (R1-M1)

**Concern:** Results tested only on 20×20 grid.

**Response:** We ran the factorial at 15×15 and 30×30. The disordinal interaction persists and amplifies:

| Grid | Hard Δ | Tanh Δ | Oja Δ |
|---|---|---|---|
| 15×15 | +0.0 | +4.2 | +4.2 |
| 20×20 | +1.7 | +6.7 | +7.0 |
| 30×30 | +7.8 | +14.5 | +15.2 |

The effect scales with network size, consistent with larger networks sustaining more weak edges in the critical 1e-6 to 1e-5 range. This result is now in the main text rather than an appendix, as it represents a scaling law, not merely a robustness check.

### 6. Simondonian Terminology (R3-M1, M2, M3)

**Concern:** "Structural germ" is incorrect; the three-regime taxonomy treats Simondon as classification; hard clip is called both "mould" and "germ."

**Response:** R3's corrections are accepted with gratitude — they sharpen the argument.

(a) "Structural germ" is replaced throughout with **"limit condition"** (*condition limite*). The hard clip constrains the space of possible individuations without templating specific form; it does not propagate from a local singularity as a germ would.

(b) The three-regime taxonomy is clarified as describing three phases of the same transductive process observed under different boundary conditions, not three static categories. A sentence has been added to make this explicit.

(c) The mould/germ equivocation is resolved: **pruning moulds** (imposes form by selectively eliminating structures), while the **hard clip is a limit condition** (constrains without imposing). Metaplastic dynamics **modulate** (vary internal parameters continuously). These are complementary operations.

(d) We retain *differenciation* with the Deleuzian spelling, with a footnote on first use clarifying the distinction from standard "differentiation."

---

## Recommended Revisions

### 7. Pruning Literature Context (R2-Q6)

**Added.** A paragraph in the Discussion now situates the confound within the computational neuroscience pruning literature (Chechik et al. 1998), noting that pruning is typically modeled as constructive but may be destructive when the threshold falls within the functional weight range.

### 8. Fine-Grained Threshold and Steepness Sweeps (R1-M4, R2-M7)

The key contrasts (pruned vs unpruned; k=1 vs hard clip) are established by the existing experiments. Finer resolution within the 1e-6 to 1e-5 range would refine the transition location but would not change the qualitative finding. We are happy to add this in a subsequent revision if the reviewer considers it essential.

### 9. Steepness Mechanism (R1-m1)

**Expanded.** The transition at k=1.5 is now explained mechanistically: onset of weight saturation (0% to 86%) and tenfold activity increase create a competitive exclusion regime.

### 10. Abstract Accessibility (R1-m4)

**Revised.** The abstract now leads with the qualitative finding (pruning reverses the ranking) and foregrounds the scaling and cap-independence results before specific numbers.

---

We believe these revisions address all reviewer concerns substantively. The central finding — that pruning differentially destroys soft-bounded assemblages, reversing the bound-type ranking — is now supported by cap sensitivity analysis, grid size generality, threshold-robust response rank with participation ratio, and a fully specified CCD null model. The philosophical terminology has been corrected to more precisely deploy Simondonian concepts.

Sincerely,
Michael Bean
