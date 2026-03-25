# Artificial Life — Editorial Decision

**Manuscript:** "Dark Forest in Silica: Emergent Structure in Goalless Hebbian Networks"
**Authors:** Michael Bean and Gen (Independent Researchers)
**Submission type:** Article
**Date:** March 13, 2026

---

## Decision: MAJOR REVISION

Dear Michael Bean and Gen,

Thank you for submitting your manuscript to *Artificial Life*. Your paper has been reviewed by three experts with complementary expertise: computational artificial life (Reviewer 1), continental philosophy and computational modeling (Reviewer 2), and multi-agent systems and game theory (Reviewer 3). All three reviewers found the research question genuinely interesting and several results noteworthy, but each identified substantial issues that must be addressed before the paper can be considered for publication.

I concur with the reviewers' unanimous recommendation of **Major Revision**. Below I summarize the key issues that must be addressed in your revision, organized by priority.

---

## Critical Issues (must be resolved)

### 1. Figure/Text Discrepancy in Substrate Experiment

All three reviewers flagged that the substrate-timeline.png and substrate-spatial-heatmap.png figures appear to show a **saturated regime** (693 active edges, weights at 1.0, 120-node single community, near-uniform activation 0.93–1.0) rather than the selective individuation described in the text (3 surviving edges, 3-node assemblage, dark background with bright band at 0.1–0.2). This discrepancy is the single most serious issue. Either the figures are from a different parameter setting than described, or the text overstates the results. Please resolve this completely before resubmission.

### 2. Single Random Seed / No Statistical Analysis

All reviewers noted that the primary experiments use a single random seed (seed 42) with no replication. Key statistics (9% connection persistence, weight std of 0.0055, drift baseline of 0.05) are presented as system properties rather than as single-realization observations. **Required:** Replicate the baseline experiment across at minimum 10 seeds. Report means and confidence intervals for all quantitative claims. The parameter regime boundaries (Tables 1 and 5) should also be verified across seeds.

### 3. Inadequate Engagement with Prior Literature

Reviewers 1 and 3 independently identified substantial gaps in the literature review:

- **Hebbian self-organization:** Kohonen SOMs, competitive learning (Rumelhart & Zipser 1985), Linsker (1988), Hebbian assembly formation (Palm et al. 2014), synaptic consolidation (Zenke & Gerstner 2017)
- **Edge-of-chaos / criticality:** Kauffman (1993), Langton (1990), Bertschinger & Natschläger (2004) — the "narrow productive regime" finding maps directly to this literature
- **Digital ecosystem competition:** Ray/Tierra (1991), Ofria & Wilke/Avida (2004), Fontana & Buss/AlChemy (1994) — the competitive exclusion result must be contextualized against these established systems
- **Evolutionary dynamics and Hebbian learning:** Watson & Szathmáry (2016)

Without this positioning, it is impossible to assess what is genuinely novel versus rediscovery.

---

## Major Issues (must be substantially addressed)

### 4. Competition Experiment Design

Reviewer 3 raised critical concerns about the Phase 1 competition experiment:
- The softmax temperature T=5.0 produces near-uniform allocation, making the "cooperation persists despite competition" finding potentially trivial
- Both networks receive identical structured input — given the passive mirror finding, synchronization is a foregone conclusion, not a dynamical outcome
- **Required:** Conduct a systematic temperature sweep. Test with different structured inputs to each network. Only then can the cooperation result be meaningfully interpreted.

### 5. Philosophical Claims Overreach Evidence

Reviewer 2 provided a detailed critique:
- The three-regime BwO mapping conflates standard bifurcation behavior with qualitatively distinct Deleuzian concepts (the "cancerous" BwO involves metastasis/reproduction, not mere saturation)
- The claim to have "computationally demonstrated" Simondon's individuation is substantially overreaching — the substrate experiment shows symmetry-breaking under gradient with positive feedback, not transduction in the Simondonian sense
- Desiring-production is invoked in the introduction but never operationalized
- **Required:** Either develop the philosophical mappings with more rigor (showing structural rather than superficial correspondence) or explicitly frame them as heuristic/interpretive rather than formal demonstrations.

### 6. The "Goalless" Framing Is Overstated

Reviewers 1 and 2 both noted that the system's designed input channels, spatial gradients, and activity-dependent encounters constitute strong inductive biases. The paper should distinguish between "no loss function" (accurate) and "no goal" (overstated). Reviewer 2 suggests engaging with Deleuze's concept of the *diagram* or *abstract machine* to address this tension philosophically.

### 7. PCA Variance Discrepancy

Reviewer 1 noted that the text claims "approximately 30% of variance" for the first two PCA components, but the generated figure shows PC1: 4%, PC2: 4% (8% total). This must be corrected. At 8% variance explained, the trajectory figure's interpretive value is limited.

---

## Minor Issues

### From Reviewer 1:
1. Orphan drift figure (generated but not referenced in some versions)
2. Dark Forest framing is premature given results — consider reframing title
3. Sparse parameter sweep (Table 1: only 4 entries)
4. Incomplete Bhalla et al. (2018) reference; uncited references (Meulemans 2022, Parisi 2013, DeLanda 2006/2016)
5. Inconsistent vector notation (bold vs. non-bold)
6. Multi-field substrate experiment needs accompanying figures

### From Reviewer 2:
7. Engage Simondon secondary literature (Combes 2013, Barthélémy 2015)
8. Bénard convection analogy undercuts Simondon claim — Prigogine already explains this
9. Palpation methodology is standard perturbation analysis renamed — moderate novelty claim
10. BFF reference is unpublished — reduce argumentative weight or find published version
11. "Dark Forest result" label for competitive exclusion is misleading

### From Reviewer 3:
12. Discuss what prevents full synchronization in coupled networks (similarity 0.66, not 1.0)
13. Two separate Discussion sections — consolidate structure
14. Report computational cost and test whether competitive exclusion timescale is an artifact of run length
15. Add Hardin (1960), Nowak (2006) to bibliography

---

## Questions for Authors (from reviewers, aggregated)

1. What happens with non-linguistic structured input (sinusoidal, Markov chains)? Can you separate "Hebbian structure formation" from "character co-occurrence memorization"?
2. What if coupled networks receive *different* structured inputs?
3. How sensitive is the substrate individuation to random seed? Does it always select 3 nodes at position 0.1–0.2?
4. Can you articulate a prediction the Deleuzian framework generates that dynamical systems theory alone would not?
5. Does the passive mirror result undermine the entire research program rather than redirect it?
6. Have you tested for multiple attractors (Hopfield capacity of ~9–10)?
7. Would anti-Hebbian/inhibitory dynamics change the regime structure?

---

## Strengths Noted by Reviewers

Despite the issues above, all reviewers recognized genuine merit:

- The ablation study is methodologically rigorous and produces a clean, important negative result
- The thermodynamic vs. strategic competition distinction is a valuable conceptual contribution
- The three-regime universality, while needing better literature contextualization, is well-documented
- The writing is unusually clear and engaging for a technical paper
- The authors' willingness to report deflating results (passive mirror, cooperation over competition) is scientifically commendable
- The research program is well-structured (Phase 1 → Phase 2 progression)

---

## Path Forward

A successful revision should:

1. **Resolve the substrate figure discrepancy** — this is blocking
2. **Replicate with multiple seeds** and report statistics
3. **Add a Related Work section** engaging with the literature identified above
4. **Conduct a competition temperature sweep** and test with asymmetric inputs
5. **Temper philosophical claims** to match evidence strength
6. **Fix the PCA variance discrepancy**
7. **Add multi-field substrate figures**
8. Consider whether the Dark Forest title serves or hinders the paper

We look forward to receiving your revised manuscript.

Sincerely,
*Associate Editor, Artificial Life*

---

## Individual Reviews

Full reviews from all three reviewers are attached below.

---

# Reviewer 1 (Computational ALife)

**Recommendation: Major Revision**

[See full review in reviewer-1.md]

---

# Reviewer 2 (Philosophy / Deleuze)

**Recommendation: Major Revision**

[See full review in reviewer-2.md]

---

# Reviewer 3 (Multi-Agent Systems / Game Theory)

**Recommendation: Major Revision**

[See full review in reviewer-3.md]
