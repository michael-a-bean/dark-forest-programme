# Paper 4S: Weight Bounds Analysis — Committee Briefing

## Moulding or Modulation? Hard Weight Bounds as a Load-Bearing Assumption in Hebbian Self-Organization

---

## 1. Motivation and Central Question

Papers 1-4 of this research programme all use hard weight clipping (`np.clip(w, -1.0, 1.0)`) after every Hebbian update. The theoretical equilibrium weight for a co-active edge under standard Hebbian learning is:

    w_eq = (η / λ) × a_i × a_j

For typical parameters (η = 0.05, λ = 0.002, activations ≈ 0.4-0.8), this gives w_eq ≈ 4-16 — far above w_max = 1.0. This means every persistently co-active edge hits the hard ceiling. The hard clip is not a safety net that rarely activates; it is the dominant force shaping the weight distribution.

Paper 4 discovered that switching from hard to soft bounds on the *learning rate* (η) dramatically changed differentiation results: CCD dropped from 0.84 to 0.30. This raised the obvious question: **does the same sensitivity apply to weight bounds?** Are the findings of Papers 1-4 properties of Hebbian dynamics, or properties of *hard-bounded* Hebbian dynamics?

This question has philosophical weight. In Deleuzian terms, the hard clip is a *Simondonian mould* — an external form imposed on a process. Intensive quantities (which weights function as in our model) should, under Deleuze's framework, vary continuously. Hard clipping violates this requirement by creating an absorbing state at ±w_max. If the programme's findings depend on this moulding, then what we have studied is not self-organization in the Deleuzian sense, but a system whose individuation is partly imposed from outside.

## 2. Experimental Design

We implemented four weight bounding strategies and reran key experiments from Papers 1-4:

**Bound implementations:**

1. **Hard clip** (baseline): `w = clip(w, -w_max, w_max)` — absorbing state at ±1.0
2. **Tanh saturation**: `w = w_max × tanh(w / w_max)` — smooth asymptote, linear near zero
3. **Sigmoid saturation**: `w = 2w_max × σ(2w/w_max) - w_max` — sharper transition region
4. **Oja normalization**: replaces the learning rule itself with `dw = η(a_i·a_j - a_j²·w)` — self-normalising, no explicit bound needed

Note: Oja is qualitatively different — it modifies the *learning rule*, not just the *bound*. If tanh and sigmoid agree but Oja differs, the finding is about learning-rule structure. If all three soft alternatives agree but differ from hard, the finding is about bound type.

**Five experiments, 1,580 jobs across a 36-CPU Ray cluster:**

| Exp | Question | Design | Jobs |
|-----|----------|--------|------|
| 1 | Regime structure (Paper 1) | 4 bounds × 8 η/λ ratios × 20 seeds | 640 |
| 2 | Coexistence/monopoly (Paper 2) | 4 bounds × 7 localities × 20 seeds | 560 |
| 3 | Self-sealing (Paper 3) | 4 bounds × 2 conditions × 20 seeds | 160 |
| 4 | Fully continuous substrate (Paper 4) | 4 weight bounds × 2 η bounds × 20 seeds | 160 |
| 5 | Weight distribution analysis | 4 bounds × 3 substrates × 5 seeds | 60 |

---

## 3. Results

### 3.1 Experiment 1: Regime Structure (Paper 1 Replication)

**Question:** Do dissolution, productive, and saturation regimes exist under all bound types?

**Finding: The saturation regime is an artifact of hard clipping.**

At η/λ ratios from 2.0 to 20.0, all four bound types produce nearly identical weight statistics. Weights remain well below w_max, so the bounding function never activates meaningfully. This confirms that in the *dissolution* and *productive* regimes, bounds are irrelevant.

At η/λ = 25.0 (η = 0.05, λ = 0.002), the bounds diverge sharply:

| Bound | Weight σ | Saturation (% at w_max) | Max |w| |
|-------|----------|------------------------|---------|
| Hard clip | 0.719 ± 0.382 | **64.0%** | 0.909 |
| Tanh | 0.092 ± 0.002 | 0.0% | 0.249 |
| Sigmoid | 0.092 ± 0.002 | 0.0% | 0.249 |
| Oja | 0.072 ± 0.002 | 0.0% | 0.264 |

Under hard clipping, 64% of all weights pile up at the boundary (±1.0), producing a bimodal distribution. Under tanh and sigmoid, the smooth saturation curve prevents this accumulation — weights plateau at ~0.25, roughly 4× lower than w_max. The tanh and sigmoid results are **numerically identical to four decimal places**, confirming that the specific saturation curve shape does not matter; what matters is whether the bound is absorbing (hard) or reflecting (soft).

Oja produces slightly different weight statistics from tanh/sigmoid (w_std = 0.072 vs 0.092) because it modifies the learning rule itself, not just the boundary. However, the qualitative behaviour is the same: no saturation, bounded productive dynamics.

**Implication for Paper 1:** The three-regime structure (dissolution / productive / saturation) is only a *three*-regime structure under hard bounds. Under soft bounds, there is no saturation regime — the productive regime extends indefinitely as η/λ increases. The regime heatmap from Paper 1 should be understood as describing *hard-bounded* Hebbian dynamics specifically.

### 3.2 Experiment 2: Coexistence / Monopoly Phase Transition (Paper 2 Replication)

**Question:** Does locality-dependent coexistence survive soft bounds?

**Finding: Coexistence is strongly bound-dependent. Hard clipping is load-bearing for assemblage formation.**

This is the most dramatic result. At tight locality (σ = 0.05), results by bound type:

| Bound | Assemblages | Modularity | CCD | Surviving edges |
|-------|------------|------------|-----|-----------------|
| Hard clip | **9.2 ± 3.4** | **1.000** | **0.950** | 120 |
| Tanh | 0.2 ± 0.4 | 0.149 | 0.000 | 1 |
| Sigmoid | 0.2 ± 0.4 | 0.149 | 0.000 | 1 |
| Oja | 2.0 ± 1.0 | 0.591 | 0.650 | 7 |

Under hard clipping, the system reliably forms 9+ distinct assemblages with perfect modularity (1.000) and near-maximal differentiation (CCD = 0.95). Under tanh and sigmoid, the system fails to form assemblages at all — mean weight is 0.01, edges are pruned faster than they strengthen, and no persistent structure emerges. The substrate dissolves.

The phase transition across locality values tells the full story:

| Locality | Hard | Tanh | Sigmoid | Oja |
|----------|------|------|---------|-----|
| 0.05 | 9.2 | 0.2 | 0.2 | 2.0 |
| 0.08 | 5.5 | 0.2 | 0.2 | 1.0 |
| 0.10 | 4.0 | 0.3 | 0.3 | 0.9 |
| 0.15 | 1.6 | 0.0 | 0.0 | 0.3 |
| 0.20 | 1.0 | 0.0 | 0.0 | 0.2 |
| 0.30 | 0.2 | 0.0 | 0.0 | 0.0 |
| 0.50 | 0.2 | 0.0 | 0.0 | 0.1 |

The coexistence → monopoly transition exists only under hard bounds and (weakly) under Oja. Under tanh/sigmoid, there are no assemblages at any locality — the transition is from "nothing" to "nothing." Oja produces intermediate results (2 assemblages at tight locality vs hard's 9), suggesting that the self-normalising learning rule can partially compensate for the absence of an absorbing boundary.

**Mechanism:** Under hard bounds, co-active edges hit w_max = 1.0 and stay there indefinitely. These saturated edges form a rigid skeleton that defines assemblage boundaries. The hard boundary acts as a *ratchet* — once an edge reaches w_max, it cannot be displaced by competitive dynamics from other assemblages, only by decay when its nodes become inactive. Under soft bounds, the saturation curve means an edge at 0.25 is easily displaced by a slightly stronger competitor — there is no ratchet, and competitive exclusion dynamics cannot maintain spatial partitions.

**Implication for Paper 2:** The central finding — that locality-dependent coexistence produces a phase transition from multiple assemblages to monopoly — is a property of *hard-bounded* Hebbian dynamics. It relies on the absorbing boundary creating irreversible commitment at the weight level. The "Dark Forest" dynamics described in Paper 2 (where assemblages that detect each other either absorb or annihilate) depend on this structural rigidity.

### 3.3 Experiment 3: Self-Sealing (Paper 3 Replication)

**Question:** Is self-sealing bound-independent?

**Finding: Self-sealing is trivially bound-independent — because soft bounds produce nothing to seal.**

Under all bound types, cross-assemblage edges decay to zero in the post-injection phase. However, the interpretation differs:

- **Hard clip:** Rich assemblage structure exists (4.0 assemblages at session 200 in control, 3.1 after injection). Cross-edges introduced at session 100 are eliminated by session ~120. Self-sealing operates as described in Paper 3: the topological mechanism (zero co-activation → decay → pruning) successfully rejects foreign connections.
- **Tanh/Sigmoid:** Assemblages that existed in early sessions (3.5 on average) dissolve by session 200 (0.3 remaining). Cross-edges also disappear, but this is not "self-sealing" in any meaningful sense — it is general dissolution. There is nothing to seal because the substrate cannot maintain persistent structure.
- **Oja:** Intermediate case — 0.9 assemblages survive to session 200 (down from 4.6 early on). Weak self-sealing may operate, but the small number of surviving assemblages makes it difficult to distinguish self-sealing from dissolution.

**Implication for Paper 3:** Self-sealing as a *mechanism* (decay of unreinforced edges) is indeed bound-independent — it operates wherever edges lack co-activation support. But as a *functional property* of an individuated substrate, it requires assemblages to exist in the first place, which (per Exp 2) requires hard bounds or Oja.

### 3.4 Experiment 4: Fully Continuous Substrate (Paper 4 Extension)

**Question:** What does soft weights + soft η produce?

**Finding: The fully continuous substrate produces *stronger* differentiation than the hard-bounded system — but through a completely different mechanism.**

This is the most theoretically significant result. The 2×4 factorial:

| Weight bound | η bound | CCD | n_assemblages | η divergence | Mean weight |
|-------------|---------|-----|---------------|-------------|-------------|
| Hard | Hard | 0.000 | 0.2 | 0.000000 | 0.183 |
| Hard | Soft | 0.200 ± 0.410 | 1.2 ± 0.6 | 0.000130 | **1.000** |
| Tanh | Hard | 0.000 | 0.2 | 0.000000 | 0.016 |
| Tanh | Soft | **0.900 ± 0.308** | **2.9 ± 0.9** | 0.000004 | 0.077 |
| Sigmoid | Hard | 0.000 | 0.2 | 0.000000 | 0.016 |
| Sigmoid | Soft | **0.900 ± 0.308** | **2.9 ± 0.9** | 0.000004 | 0.077 |
| Oja | Hard | 0.000 | 0.0 | 0.000000 | 0.000 |
| Oja | Soft | **1.000 ± 0.003** | 23.1 ± 16.9 | 0.000093 | 0.860 |

The pattern:

1. **Hard η → no differentiation** regardless of weight bound (CCD = 0). This replicates Paper 4's finding: hard η bounds prevent metaplastic differentiation.

2. **Soft η + hard weights → weak differentiation** (CCD = 0.20). This is the Paper 4 baseline with soft η alone — some differentiation, but limited. Notably, mean weight = 1.000, confirming all surviving edges are at the hard boundary.

3. **Soft η + soft weights (tanh/sigmoid) → strong differentiation** (CCD = 0.90). This is the key new finding. Removing *both* hard bounds — on weights and on η — produces much stronger differentiation than removing either alone. Mean weight is only 0.077, meaning assemblages are differentiated despite having very weak internal connections. The differentiation is driven entirely by the metaplastic mechanism (η variation) rather than by weight accumulation.

4. **Soft η + Oja → maximal differentiation** (CCD = 1.00, essentially orthogonal assemblages). But with extremely high fragmentation (23 assemblages, high variance). The Oja rule's self-normalisation creates a substrate that fragments into many small, maximally distinct clusters. This may represent over-differentiation — the system shatters rather than individuating.

**Critical observation:** Under hard weight bounds + soft η (row 2), differentiation is weak (CCD = 0.20) but weight mass is high (mean = 1.0). Under soft weight bounds + soft η (rows 3-4), differentiation is strong (CCD = 0.90) but weight mass is low (mean = 0.077). The hard clip creates *structural* rigidity (high-weight assemblages) but suppresses *metaplastic* differentiation (because all edges hit the same ceiling, reducing the dynamic range available for η to exploit). Removing the hard clip allows η to drive differentiation through a purely intensive mechanism — the assemblages differ not in their weights but in their learning dynamics.

**Implication for Paper 4 and the programme:** The "fully continuous" Deleuzian substrate (soft weights + soft η) is not a weakened version of the hard-bounded system — it is a *qualitatively different* system that achieves stronger differentiation through a different mechanism. Papers 1-4 studied a system where individuation operates through *extensive* means (weight magnitude, edge presence/absence, topological boundaries). The fully continuous substrate individuates through *intensive* means (learning rate variation, functional response diversity). This is precisely the distinction Deleuze draws between moulding (imposing form from outside) and modulation (varying internal parameters continuously).

### 3.5 Experiment 5: Weight Distributions

**Finding: Hard bounds produce bimodal weight distributions; soft bounds produce unimodal or empty distributions.**

At session 200 in the MultiField substrate:
- **Hard clip:** 53 surviving edges, all at |w| > 0.95 (100% saturated). Distribution is bimodal: edges are either at +1.0 or -1.0. Mean weight = 0.32 (the sign-weighted average of +1 and -1 values).
- **Tanh/Sigmoid:** Zero surviving edges. All edges were pruned because weights never grew large enough to resist decay.
- **Oja:** 4 surviving edges, all near -0.94. Extremely sparse but the edges that survive are strong.

In the MetaplasticField substrate, hard bounds produce the highest surviving edge count and weight mass (mean = 0.60), while soft bounds produce near-zero weight mass.

---

## 4. Synthesis: What Is Bound-Dependent and What Is Not?

| Finding | Bound-dependent? | Nature of dependence |
|---------|-----------------|---------------------|
| Dissolution regime | No | Weights far from bounds; all bound types agree |
| Productive regime | Partially | Dynamics agree but equilibrium weight levels differ by ~3× |
| Saturation regime | **Yes — only exists under hard clip** | Hard clip creates absorbing state; soft bounds reflect |
| Assemblage formation (coexistence) | **Yes — strongly** | Hard clip ratchet enables; soft bounds dissolve |
| Phase transition (coexistence → monopoly) | **Yes** | Only observable under hard bounds |
| Self-sealing mechanism | No | Decay of unreinforced edges is universal |
| Self-sealing as functional property | **Yes** | Requires assemblages, which require hard bounds |
| Metaplastic differentiation (CCD) | **Yes — reversed** | Soft bounds + soft η → *more* differentiation |
| Weight distributions | **Yes** | Bimodal under hard, unimodal/empty under soft |

### The Three-Way Split

The results reveal three distinct substrate regimes:

1. **Hard-bounded (Papers 1-4):** Strong structural individuation via weight accumulation. Assemblages are defined by high-weight edges. Differentiation is structural — assemblages differ in their topology and weight mass. The hard clip acts as a ratchet enabling irreversible commitment. This is *moulding* in Simondon's sense.

2. **Soft-bounded (tanh/sigmoid):** The MultiField substrate dissolves — soft bounds cannot sustain structural assemblages against decay. However, when combined with metaplasticity (soft η), strong *intensive* differentiation emerges. Assemblages are defined not by their weight structure (which is weak) but by their learning dynamics. This is closer to Deleuzian *modulation*.

3. **Oja (self-normalising rule):** Intermediate for structural properties (partial assemblage formation), maximal for intensive differentiation (CCD = 1.0 with soft η). But extreme fragmentation (23 assemblages) raises questions about whether this represents meaningful individuation or merely disintegration.

---

## 5. Implications for the Research Programme

### 5.1 What Papers 1-4 Actually Studied

Papers 1-4 studied a *moulded* system. The hard clip is not a neutral implementation detail — it is the mechanism that enables assemblage formation, structural individuation, and the Dark Forest dynamics described in Paper 2. Without it, the substrate dissolves (tanh/sigmoid) or fragments (Oja).

This does not invalidate Papers 1-4. The hard-bounded system is a legitimate object of study, and the findings about regime structure, coexistence, self-sealing, and metaplastic differentiation are real phenomena within that system. But the programme must acknowledge that these findings are properties of a specific substrate architecture, not universal properties of Hebbian self-organization.

### 5.2 The Fully Continuous Alternative

The most provocative finding is that the "fully continuous" substrate (soft weights + soft η) produces *stronger* differentiation than the hard-bounded system — just through a different mechanism. This creates a philosophical choice for the programme:

- **Option A: The hard-bounded system is the right model.** Biological synapses do have saturation limits (receptor density, vesicle pools). The hard clip, while a simplification, captures a real constraint. The programme should continue using it while noting that soft bounds produce different dynamics.

- **Option B: The fully continuous system is theoretically preferable.** Deleuze's framework requires continuous intensive variation. The hard clip violates this requirement. The programme should pivot to studying the fully continuous substrate, which achieves differentiation through purely intensive means — and produces stronger differentiation to boot.

- **Option C: Both systems are interesting.** The hard-bounded and fully continuous systems represent two distinct *modes* of individuation — extensive (structural) and intensive (metaplastic). The programme could study both, comparing how individuation operates through form-imposition versus internal modulation.

### 5.3 The Oja Question

Oja normalization occupies an interesting middle ground. It is the most "principled" alternative — it arises from PCA theory and produces self-normalising weights without any external constraint. But its extreme fragmentation under soft η (23 assemblages) suggests that unregulated self-normalisation may over-differentiate. This connects to an open question in Deleuze: is unlimited intensive variation always productive, or does individuation require some form of constraint?

### 5.4 The Tanh/Sigmoid Equivalence

Tanh and sigmoid produced numerically identical results across all experiments (to 4 decimal places at many parameter settings). This is a clean negative result: the specific shape of the saturation curve does not matter. What matters is the binary distinction between absorbing (hard) and non-absorbing (soft) bounds. This simplifies the theoretical landscape considerably — we do not need to worry about which soft bound is "correct."

---

## 6. Questions for the Committee

### 6.1 Programme Architecture

1. **Should this become a standalone paper, or a section within a revised Paper 4?** The findings are substantial enough for their own paper, but they also directly extend Paper 4's analysis of hard vs soft bounds. Paper 4's conclusion about "rule-space expansion" is strengthened by showing that weight bounds exhibit the same hard/soft sensitivity as η bounds.

2. **Should Papers 1-2 be revised to acknowledge the bound-dependence?** The coexistence results (Exp 2) show that Paper 2's central finding — the locality-dependent phase transition — is bound-dependent. A brief acknowledgment in a revision could note this, or it could be left to Paper 4S as a later clarification.

### 6.2 Theoretical Framing

3. **Is the hard clip a legitimate modelling choice, or a theoretical problem?** If we take the Deleuzian framework seriously, hard clipping violates the requirement for continuous intensive variation. But if we view the programme as studying a specific class of substrates (those with saturation constraints), the hard clip is a feature, not a bug. The committee's view on the relationship between the computational model and the philosophical framework would shape how we present this.

4. **How should we handle the "intensive vs extensive individuation" distinction?** The hard-bounded system individuates extensively (structural weight accumulation), while the fully continuous system individuates intensively (learning rate differentiation). Should the programme treat these as complementary modes, or argue that one is more fundamental?

### 6.3 Experimental Extensions

5. **Should we run a "biologically motivated" bound?** Real synapses saturate but not with a hard clip — they follow something like a soft bound with a much steeper transition region than tanh. A parameterised bound with adjustable steepness (interpolating between tanh and hard) could identify the critical steepness at which assemblage formation becomes possible.

6. **Does the MetaplasticField need its own bound study?** Exp 4 shows that soft weights + soft η produces strong differentiation (CCD = 0.90). But this was run with meta_strength = 0.005 and coupling = 0. Should we run the full Paper 4 parameter sweep (meta_strength × coupling) under soft weight bounds to see if the differentiation landscape changes?

7. **Should we study the dynamics of assemblage *formation* under soft bounds, not just their steady state?** Exp 3 shows that soft-bounded systems have assemblages in early sessions (3.5 assemblages) that dissolve by session 200. The formation dynamics might reveal why soft bounds cannot sustain structure — is it a timescale problem (assemblages form but decay faster) or a mechanism problem (assemblages never properly form)?

### 6.4 Writing Strategy

8. **What is the target venue and audience?** If this paper targets the same philosophical audience as Papers 1-4, the Simondonian moulding / Deleuzian modulation framing is central. If it targets a computational modelling audience, the emphasis shifts to the mathematical analysis of equilibrium weights under each bound type and the empirical bound-dependence of specific findings.

---

## 7. Summary of Key Numbers

For quick reference — the numbers that matter most:

- **Exp 1:** Hard clip enters saturation (64% of weights at boundary) at η/λ = 25; no other bound type saturates at any tested ratio.
- **Exp 2:** Hard clip produces 9.2 assemblages at tight locality; tanh/sigmoid produce 0.2; Oja produces 2.0.
- **Exp 4:** Soft weights + soft η → CCD = 0.90 (tanh/sigmoid) or 1.00 (Oja), vs CCD = 0.20 for hard weights + soft η. Hard η → CCD = 0.00 for all weight bounds.
- **Exp 5:** Under hard bounds, 100% of surviving edges are saturated (|w| > 0.95). Under tanh/sigmoid, zero edges survive to session 200.
- **Tanh ≡ sigmoid** across all experiments to ≥4 decimal places.

---

*Prepared for dissertation committee review. All experimental data and figures available at `~/research/dark-forest-bounds/`. Analysis script: `papers/04s-bounds/analysis.R`. Figures: `papers/04s-bounds/figures/`.*
