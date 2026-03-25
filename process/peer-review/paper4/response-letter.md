# Response to Reviewers — Paper 4

**Manuscript:** "Local Homeostasis Stabilises Differentiation in Hebbian Substrates"
**Journal:** *Artificial Life*

---

## Reviewer 1 (Computational ALife) — Minor Revision

### M1: Baseline matches metaplasticity on response rank

**Concern:** The baseline (no metaplasticity) achieves rank 5.6 without pruning — identical to the metaplastic condition. The title may overstate metaplasticity's contribution.

**Response:** This is an important observation that we now address more explicitly. Metaplasticity contributes: (a) eta divergence between assemblages (F=4.9, absent in the baseline), (b) increased assemblage count (10+ vs ~6), and (c) stabilisation of the differentiated state against stronger perturbations. The response rank parity reflects that the hard weight clip creates the structural scaffold for functional diversity; metaplasticity amplifies the number of differentiated units and adds a parametric dimension (eta variation) that the baseline lacks. We have clarified this distinction in the revised text.

### M2: CCD dominates figures despite demotion

**Concern:** Critical period (Exp 8) and perturbation (Exp 9) are measured exclusively on CCD.

**Response:** We ran functional validation experiments (Exp 8fv, 9fv) using 10-probe response rank. Results:

**Critical period (Exp 8fv):** Response rank shows the same critical period as CCD. Coupling from session 0: rank drops to 0.05. Coupling from session 50+: rank preserved at 0.85. Integrated into the revised text with a summary table.

**Perturbation (Exp 9fv):** Response rank at session 200 is 0.85 across all perturbation levels (0%, 10%, 25%, 50%), with no deflection at the perturbation event. Full recovery confirmed functionally.

### M3: 5-probe vs 10-probe confound

**Concern:** Rank increase from 2.4 to 5.6 may partly reflect doubling probe count.

**Response:** We now address this explicitly. Exp 17 (5 probes) gives rank 2.4, which is not ceiling-limited (ceiling = min(K,A) = 5). Paper 4S (10 probes) gives rank 5.6 without pruning. The increase reflects both: (a) removal of pruning (which destroyed weak exploratory connections), and (b) the larger probe space detecting additional functional dimensions. The participation ratio (threshold-free) gives 2.2 (Gaussian) to 3.2 (uniform), confirming genuine multidimensionality independent of probe count.

### Minor concerns

- m1 (Transplant): Acknowledged as a limitation.
- m2 (Three-regime table): Defined in Paper 4S; we add a forward reference.
- m3 (EMA range): Noted as future work; the one-order-of-magnitude result is sufficient for current claims.
- m4 (Non-sequential numbering): Explained in footnote; renumbering would break cross-references with Paper 4S.

---

## Reviewer 2 (Theoretical Neuroscience) — Major Revision

### M1: Response rank validation

**Concern:** SVD threshold (1%) not justified; rank sensitive to threshold choice.

**Response:** Paper 4S now reports rank at five thresholds (0.1% to 10%) and the participation ratio (threshold-free). No-prune rank ranges from 4.1 (10%) to 5.9 (0.1%); pruned rank is flat at 1.0. Participation ratio 2.1-3.3. The distinction is unambiguous at every threshold. We reference these results in the revised Paper 4 text.

### M2: Eta ANOVA — t-test on F-ratios is non-standard

**Concern:** F-ratios are right-skewed; t-test may inflate reliability.

**Response:** We add two robustness checks: (a) Shapiro-Wilk test confirms F-ratios pass normality (W=0.905, p=0.40); (b) Wilcoxon signed-rank test gives W=21, p=0.016 — concordant with the parametric t-test (p=0.000018). Both confirm the result. The large d=5.62 reflects the consistency across qualifying seeds (SD=0.64), not distributional inflation.

### M3: "Stabilises and amplifies" undermined by pruning

**Concern:** The local-hard condition produces 0 assemblages with pruning — mechanism is fragile to implementation detail.

**Response:** We qualify the claim as suggested: metaplasticity stabilises differentiation "provided the maintenance regime does not destroy the substrate on which it operates" (see Discussion, programme implications paragraph, and Paper 4S). The pruning sensitivity is itself a finding, not merely a caveat.

### M4: Critical period lacks functional validation

**Concern:** Does response rank show a critical period?

**Response:** Yes. Exp 8fv (400 jobs, 10-probe response rank) confirms: coupling from session 0 → rank 0.05; coupling from session 50+ → rank 0.85. Table integrated into the Results section.

### Minor concerns

- EMA citation: Acknowledged; mapping is approximate.
- Participation ratio: Now reported (2.2 Gaussian, 3.2 uniform).
- Transplant scope: Noted as limitation.
- Bootstrap replicates: Updated to 10,000 BCa throughout.

---

## Reviewer 3 (Philosophy) — Accept with minor revisions

### m1: Critical period needs more Simondonian work

**Response:** We add a sentence connecting the critical period to the three-regime taxonomy: the critical period marks the transition from structural to metaplastic individuation — the consolidation phase restructures the basin landscape, making subsequent coupling navigational rather than homogenising.

### m2: Moulding not pejorative

**Response:** Added: "Moulding is not pejorative in Simondon's framework — it is a legitimate operation, as in casting, that forecloses further individuation while producing stable form. Moulding is, in Simondon's analysis, a limit case of modulation — modulation frozen at its boundary values."

### m3: Exteriority admits degrees

**Response:** Revised: "DeLanda acknowledges that exteriority admits of degrees — components need not be fully detachable to possess some degree of external relations. The assemblages do resist perturbation (Exp 9), indicating partial exteriority. But the transplant shows that the identity-constituting relations are spatial, not intrinsic."

### m4: Differenciation footnote

**Response:** Footnote added at first use in abstract with full Deleuzian definition.

---

We believe these revisions address all reviewer concerns. The functional validation experiments (Exp 8fv, 9fv) confirm that the critical period and perturbation resilience are not CCD artifacts. The statistical robustness checks (Wilcoxon, Shapiro-Wilk) confirm the eta ANOVA. The philosophical terminology has been refined per R3's precise corrections.

Sincerely,
Michael Bean
