# Paper 4S: Weight Bounds Analysis — Committee Briefing R2

## Moulding or Modulation? Hard Weight Bounds as a Load-Bearing Assumption in Hebbian Self-Organization

**Updated 2026-03-23 — incorporates committee-requested experiments and Phase 2-3 results**

---

## 0. Summary of Changes Since R1

The original briefing (R1) presented five experiments showing that assemblage formation, coexistence, and differentiation were strongly bound-dependent. Three committee-requested experiments (Okafor concerns #1-2, steepness sweep) and four follow-up experiments have substantially altered the paper's narrative. Two major confounds were identified:

1. **Pruning confound (confirmed).** The pruning threshold (1e-4) differentially eliminates soft-bounded edges. Removing pruning reverses the bound-type ranking: soft > hard for assemblage formation.
2. **CCD metric confound (confirmed).** Centroid cosine distance is statistically indistinguishable from a spatial null distribution. It measures geometry, not functional differentiation.

---

## 1. Original Findings (R1) — Status Update

| R1 Finding | Status | Basis |
|---|---|---|
| Saturation regime is hard-clip artifact | **Stands** | Unaffected by pruning confound |
| Assemblage formation requires hard bounds | **Overturned** | Exp 2a, F: soft bounds produce more assemblages without pruning |
| Coexistence→monopoly transition is bound-dependent | **Partially overturned** | Transition exists under all bounds when pruning removed |
| Self-sealing is trivially bound-independent | **Needs re-evaluation** | If soft bounds form assemblages, self-sealing may operate non-trivially |
| Soft w + soft η → strong intensive differentiation (CCD=0.90) | **Overturned** | Exp 6: CCD indistinguishable from null |
| Tanh ≡ sigmoid | **Stands** | Confirmed across all new experiments to ≥4 decimal places |

---

## 2. New Experimental Results

### 2.1 Committee Experiments (March 22)

#### Exp 2a: Pruning-Disabled Coexistence (Okafor concern #1) — CONFIRMED

With pruning disabled (threshold=1e-8, max_edges=20000 cap):

| Bound | Original asm (pruned) | No-prune asm | CCD |
|---|:-:|:-:|:-:|
| Hard (loc=0.10) | 4.0 | 4.9 | 0.749 |
| Tanh | 0.3 | **6.0** | **0.996** |
| Sigmoid | 0.3 | **6.0** | **0.996** |
| Oja | 0.9 | **6.5** | **0.997** |

At tight locality (0.05): tanh/sigmoid=9.9 vs hard=7.2. Soft-bounded assemblages have near-zero weights (mean_w=0.005) but maintain topological structure.

#### Exp 6: CCD Permutation Test (Okafor concern #2) — CONFIRMED

1000 permutations × 20 seeds. No condition reaches significance (p < 0.05):

| Weight bound | η bound | Real CCD | Null mean | p-value | Significant seeds |
|---|---|:-:|:-:|:-:|:-:|
| Hard | hard | 0.000 | 0.034 | 1.000 | 0/20 |
| Hard | soft | 0.200 | 0.500 | 1.000 | 0/20 |
| Tanh | soft | 0.900 | 0.995 | 1.000 | 0/20 |
| Oja | soft | 1.000 | 1.000 | 0.566 | 3/20 |

**CCD reflects spatial embedding geometry, not functional differentiation.**

#### Exp 7: Steepness Sweep — Confounded by Pruning

Original results (with pruning) showed k=1 producing 0.3 assemblages. This was entirely a pruning artifact (see Exp 7b below).

### 2.2 Phase 1 Experiments (March 23, AM)

#### Exp 7b: Steepness Sweep Without Pruning — Non-Monotonic Pattern

| k | Pruned asm | No-prune asm | Mean weight |
|:-:|:-:|:-:|:-:|
| 1.0 (tanh) | 0.3 | **6.0** | 0.005 |
| 2.0 | 1.6 | 1.8 | 0.959 |
| 3.0 | 1.4 | 1.6 | 0.995 |
| 5.0 | 1.4 | 1.4 | 1.000 |
| 10.0 | 1.6 | 1.4 | 1.000 |
| 20.0 | 1.0 | 1.0 | 1.000 |
| 50.0 | 1.0 | 1.0 | 1.000 |
| Hard clip | — | 4.9 | 0.249 |

**Key finding:** Non-monotonic pattern. The softest bound (k=1, tanh) and the hardest (hard clip) both produce multiple assemblages, while intermediate steepness produces near-monopoly. The hard clip remains qualitatively irreducible — no finite steepness recovers its behavior.

#### Phase 1H: Threshold Sweep — Detection Is Method-Dependent

Assemblage detection is highly sensitive to threshold choice for no-prune conditions:

| Condition | t=0.001 | t=0.005 | adaptive | t=0.01 | t=0.05 |
|---|:-:|:-:|:-:|:-:|:-:|
| Hard pruned (13 edges) | 4.3 | 4.3 | 4.2 | 4.3 | 4.2 |
| Tanh noprune (1429 edges) | 1.0 | 4.9 | 6.8 | 15.6 | 0.2 |

Hard-pruned assemblages are robust (all weights ~1.0). Soft-bounded assemblages range from 1 to 16 depending on threshold, raising questions about their structural reality.

### 2.3 Phase 2-3 Experiments (March 23, overnight)

#### Exp F: 2×2 Factorial — Disordinal Interaction (n=30)

| Bound | Pruned | No-prune | Δ |
|---|:-:|:-:|:-:|
| Hard | 3.9 ± 2.1 | 5.6 ± 3.2 | +1.7 |
| Tanh | 0.2 ± 0.4 | 7.0 ± 2.2 | **+6.7** |
| Sigmoid | 0.2 ± 0.4 | 7.0 ± 2.2 | **+6.7** |
| Oja | 0.8 ± 0.7 | 7.8 ± 2.8 | **+7.0** |

**The interaction is disordinal.** With pruning, hard >> soft. Without pruning, soft > hard. The ranking reverses. Pruning effect on soft bounds (~35×) dwarfs the effect on hard bounds (~1.4×). This is the clean causal decomposition the paper needs.

Additional metrics for the factorial (200 sessions, loc=0.10):

| Bound | Prune | Modularity | CCD | Edges |
|---|---|:-:|:-:|:-:|
| Hard | on | 1.000 | 0.867 | 15 |
| Hard | off | 0.844 | 0.764 | 1,370 |
| Tanh | on | 0.233 | 0.000 | 0 |
| Tanh | off | 0.795 | 1.000 | 1,311 |

#### Exp B: Pruning Threshold Sweep — Critical Threshold Identified

Assemblages at final session, by bound type × pruning threshold:

| Bound | 1e-6 | 1e-5 | 1e-4 | 1e-3 | 1e-2 |
|---|:-:|:-:|:-:|:-:|:-:|
| Hard | 4.0 | 3.4 | 4.0 | 3.6 | 3.6 |
| Tanh | **13.9** | 0.7 | 0.3 | 0.3 | 0.2 |
| Sigmoid | **13.9** | 0.7 | 0.3 | 0.3 | 0.2 |
| Oja | **9.8** | 0.9 | 0.8 | 0.8 | 0.9 |

**Critical threshold is between 1e-6 and 1e-5.** At 1e-6, tanh/sigmoid produce 13.9 assemblages — more than 3× hard clip's 4.0. At 1e-5, they collapse to 0.7. Hard bounds are insensitive to threshold (3.4-4.0 across the entire range). Soft-bounded weights occupy the 1e-6 to 1e-5 magnitude range, so any threshold above that selectively eliminates them.

Edge counts confirm the mechanism:

| Bound | 1e-6 | 1e-5 | 1e-4 |
|---|:-:|:-:|:-:|
| Hard | 319 | 33 | 16 |
| Tanh | 86 | 2 | 1 |

#### Exp E: Eta Distribution Analysis — Differentiation Only Under Hard Weights

Between- vs within-assemblage eta variance (MetaplasticField, session 200):

| Weight bound | η bound | n_asm | F-ratio | Between-var | Within-var |
|---|---|:-:|:-:|:-:|:-:|
| Hard | soft | 1.2 | **4.80** | **0.000649** | 0.000139 |
| Tanh | soft | 2.9 | 0.86 | 0.000004 | 0.000008 |
| Sigmoid | soft | 2.9 | 0.86 | 0.000004 | 0.000008 |
| Oja | soft | 23.1 | 0.76 | 0.000093 | 0.000121 |
| All | hard | <1 | — | — | — |

**Only hard weight bounds + soft η bounds produce meaningful between-assemblage eta variance** (F=4.80, approximately 5× more variance between than within assemblages). All soft weight bound conditions show F<1 — within-assemblage variance exceeds between-assemblage variance, meaning eta does not differentiate assemblages.

This directly addresses the Turing instability claim: the per-node metaplastic mechanism only drives eta divergence between assemblages when the absorbing weight boundary creates the structural asymmetry needed for the instability to take hold.

#### Exp R: Response-Profile Divergence — No Functional Differentiation

Stimulus-response protocol: 5 Gaussian probe stimuli, 10-step propagation, JS divergence between assemblage response profiles:

| Condition | n (≥2 asm) | JS div | Response rank | CCD |
|---|:-:|:-:|:-:|:-:|
| Hard pruned | 26/30 | 0.531 | 1.00 | 1.000 |
| Hard noprune | 23/30 | 0.584 | 1.68 | 0.996 |
| Tanh noprune | 30/30 | 0.584 | 1.76 | 1.000 |
| Sigmoid noprune | 30/30 | 0.584 | 1.76 | 1.000 |
| Oja noprune | 30/30 | 0.588 | 1.78 | 1.002 |

**JS divergence is ~0.58 across all no-prune conditions.** Assemblages respond to stimuli comparably regardless of bound type. Response rank is 1.0-1.8, meaning assemblages span only 1-2 functional dimensions — parametric variation, not qualitative differentiation.

Hard-pruned assemblages show lower JS divergence (0.53) and response rank exactly 1.0, suggesting that high-weight rigid assemblages are actually *less* functionally diverse, not more.

---

## 3. Revised Synthesis

### 3.1 What the Data Now Shows

**The programme studied a system where pruning was the primary mechanism of assemblage selection, not weight bounding.**

Under the standard pruning threshold (1e-4):
- Hard-bounded edges survive because they reach w_max=1.0
- Soft-bounded edges are destroyed because they equilibrate at w≈0.005-0.01

Removing pruning reveals that soft bounds produce *more* assemblages (7.0 vs 5.6), with near-perfect topological modularity (0.795), but near-zero weight magnitude. These assemblages are:
- **Topologically persistent** — they survive across sessions
- **Threshold-sensitive** — count varies 5× depending on detection threshold
- **Not functionally differentiated** — JS divergence and response rank are comparable to hard-bounded assemblages
- **Not eta-differentiated** — F-ratio < 1 for all soft weight bounds

### 3.2 The Hard Clip Remains Qualitatively Special

Despite the pruning confound, two results confirm the hard clip's irreducibility:

1. **Steepness sweep (Exp 7b):** No finite steepness k recovers hard clip behavior. The pattern is non-monotonic — k=1 and hard clip both produce multiple assemblages, while k=2-50 produces monopoly.

2. **Eta differentiation (Exp E):** Only hard weight bounds + soft η produce F>1 between-assemblage eta variance. The absorbing boundary creates the structural asymmetry that the Turing instability requires.

### 3.3 The Three-Way Structure

| Property | Hard bounds | Soft bounds (no prune) | Soft bounds (pruned) |
|---|---|---|---|
| Assemblages | 4-6 | 6-8 | 0 |
| Weight magnitude | ~1.0 | ~0.005 | — |
| Threshold-robust | Yes | No | — |
| Eta differentiation | F=4.8 (with soft η) | F<1 | — |
| Functional divergence (JS) | 0.53 | 0.58 | — |
| Response dimensionality | 1.0 | 1.7 | — |

Hard bounds produce fewer but more structurally rigid assemblages with genuine eta differentiation. Soft bounds produce more but fragile assemblages with no eta differentiation. Neither achieves meaningful functional differentiation by the response-profile measure.

---

## 4. Revised Theoretical Framing

### 4.1 From Moulding/Modulation to Structural Conditions for Transduction

The original R1 framing — hard bounds as Simondonian "moulding," soft bounds as Deleuzian "modulation" — cannot survive the pruning confound. The binary was an artifact of the experimental design, not a property of the dynamics.

**Proposed reframing (following committee discussion):**

The hard clip creates a **topological singularity** in weight space — an absorbing boundary that is qualitatively distinct from any smooth saturation. This singularity functions as what Simondon calls a *structural germ*: an asymmetric condition that resolves metastability in a specific direction. The steepness sweep confirms this is a topological, not metric, distinction — no finite steepness approximates it.

Under hard bounds, the absorbing boundary creates irreversible commitment at the weight level, which in turn creates the structural asymmetry that drives eta divergence (F=4.80). Under soft bounds, weights remain reversible, the structural asymmetry does not develop, and eta does not differentiate (F<1).

The pruning confound itself is theoretically informative: it shows that a thresholding operation (pruning at 1e-4) can function as an implicit absorbing boundary for soft-bounded weights. Edges below the threshold are eliminated with the same irreversibility as edges above w_max under hard bounds. Pruning is an unintended mould.

### 4.2 Phantom Individuation

Soft-bounded assemblages without pruning present a theoretically interesting case: topological structure (persistent connected components, high modularity) without energetic commitment (mean_w=0.005) and without functional differentiation (JS≈0.58, comparable to null). In Simondonian terms, this may represent structural organization without genuine individuation — the appearance of an individual without the associated resolution of metastable tension.

However, the threshold sensitivity (1.0 to 15.6 assemblages depending on detection parameter) raises the prior question of whether these structures are detection artifacts. Further work with fixed-threshold detection and functional probes is needed before this concept can be validated.

---

## 5. What Survives and What Falls

### Programme-Level Impact

| Paper | Central Finding | Pruning-Exposed? | CCD-Dependent? | Status |
|---|---|---|---|---|
| Paper 1 | Regime structure (dissolution/productive/saturation) | Partially — saturation regime uses pruning | No | Add caveat about saturation regime under soft bounds |
| Paper 2 | Locality-dependent coexistence | **Yes** — coexistence comparison across bound types | Yes (partially) | Needs acknowledgment; core finding (locality transition under hard bounds) still holds |
| Paper 3 | Self-sealing | No — tests within hard-bounded system | No | Stands |
| Paper 4 | Metaplastic differentiation | **Yes** — CCD=0.90 claim is invalidated | **Yes** | Needs revision: eta differentiation result (F=4.80) survives but CCD claims do not |
| Paper 4S | Bound-dependence analysis | Central topic | Central topic | Complete revision per this briefing |

### Specific Claims Requiring Qualification

1. **Paper 2:** "Coexistence requires hard bounds" → Should read: "Coexistence under standard pruning requires hard bounds; without pruning, all bound types support coexistence."
2. **Paper 4:** "Soft η → CCD=0.90 (strong differentiation)" → CCD is not a valid differentiation metric. Replace with: "Soft η → eta F-ratio=4.80 under hard weight bounds only."
3. **Paper 4S (R1):** "Soft bounds dissolve" → Pruning artifact. Correct to: "Soft bounds form topologically persistent but low-magnitude assemblages."

---

## 6. Recommended Paper Structure

### Title (revised)
"Absorbing Boundaries as Structural Germs: How Weight Clipping Creates the Conditions for Metaplastic Differentiation"

### Proposed sections

1. **Introduction** — the question of whether hard clipping is load-bearing
2. **The pruning confound** — Exp 2a, F, B establishing the disordinal interaction and critical threshold
3. **Soft-bounded assemblage characterisation** — threshold sensitivity, topological structure, weight distributions
4. **The hard clip's irreducibility** — Exp 7b steepness sweep, non-monotonic pattern
5. **Eta differentiation requires absorbing boundaries** — Exp E, F-ratio analysis
6. **Functional probing: no differentiation under either regime** — Exp R, response profiles
7. **Discussion** — topological singularity interpretation, phantom individuation, programme implications

---

## 7. Updated Key Numbers

- **Exp F:** Hard pruned=3.9 asm, hard noprune=5.6, tanh noprune=7.0. Disordinal interaction.
- **Exp B:** Critical pruning threshold between 1e-6 (tanh=13.9 asm) and 1e-5 (tanh=0.7 asm). Hard insensitive.
- **Exp 7b:** k=1 no-prune=6.0 asm, k=2-50=1.0-1.8 asm, hard clip=4.9 asm. Non-monotonic.
- **Exp E:** F-ratio=4.80 for hard+soft η, F<1 for all soft weight bounds.
- **Exp R:** JS divergence=0.58 across all no-prune conditions. Response rank=1.0-1.8. No functional differentiation.
- **Tanh ≡ sigmoid** confirmed across all 12 experiments.

---

## 8. Questions for Committee R2

1. **Is the pruning-confound-as-unintended-mould framing too cute, or does it genuinely add theoretical value?** The parallel between pruning-as-threshold and clipping-as-boundary is real, but risks being seen as post-hoc rationalization.

2. **Should the response-profile protocol be extended?** Current design uses 5 Gaussian probes at random positions with 10-step propagation. This may be too simple to detect subtle functional differences. A richer stimulus set (structured patterns, multi-frequency) and longer propagation could yield different results.

3. **How should we handle the threshold sensitivity of soft-bounded assemblages?** Three options: (a) report all results at a fixed threshold, (b) report the adaptive threshold with sensitivity analysis, (c) argue that threshold sensitivity itself is the finding.

4. **Is F=4.80 for hard+soft η strong enough to anchor the paper's positive claim?** This is 20 seeds with a simple F-ratio. Should we run more seeds, compute confidence intervals, or use a nested ANOVA with session as a random effect?

5. **Paper 4 revision scope.** The CCD claims in Paper 4 need correction. Should this be handled as an erratum, a revision, or should Paper 4S absorb the corrections?

---

*Prepared for dissertation committee review (R2). All experimental data available at `~/research/dark-forest-bounds/data/`. Analysis scripts in `papers/04s-bounds/`.*

*Experiments completed: exp1_regime, exp2_coexistence, exp2a_no_pruning, exp2b_baseline_noprune, exp3_self_sealing, exp4_continuous, exp5_dist_*, exp6_ccd_permutation, exp7_steepness, exp7b_steepness_noprune, expB_prune_sweep, expE_eta_snapshots, expF_factorial, expR_response_profile.*
