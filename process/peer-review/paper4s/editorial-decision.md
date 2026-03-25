# Artificial Life — Editorial Decision

**Manuscript:** "Pruning as Confound: How Maintenance Processes Obscure Functional Diversity in Self-Organising Networks"
**Authors:** Michael Bean
**Submission type:** Article
**Date:** March 24, 2026

---

## Decision: MAJOR REVISION

Dear Michael Bean,

Thank you for submitting your manuscript to *Artificial Life*. Your paper has been reviewed by three experts: computational artificial life and self-organization (Reviewer 1), theoretical neuroscience and synaptic plasticity (Reviewer 2), and philosophy of technology and process philosophy (Reviewer 3). This is a companion paper to the Dark Forest series previously published in this journal, and the reviewers were familiar with the prior work.

All three reviewers found the central contribution — the identification of a disordinal interaction between pruning threshold and weight bounding strategy — to be genuine, well-evidenced, and methodologically important for the field. Reviewer 3 described the philosophical self-criticism as "genuine, not performative" and the empirical design as "remarkably thorough." Reviewer 1 called the transparency about limitations of prior work "commendable."

However, two reviewers (R1, R2) recommend Major Revision, primarily on grounds of insufficient validation of the replacement metric (response rank) and concerns about the edge-cap mechanism that substitutes for pruning. Reviewer 3 recommends Accept with minor revisions but raises substantive philosophical concerns about the deployment of Simondonian concepts.

I concur with the majority recommendation of **Major Revision**. The pruning confound is a real and important finding, but the paper must demonstrate that its proposed remedies (edge cap, response rank) do not introduce new confounds, and that the philosophical framing is internally consistent.

---

## Required Revisions

### 1. Edge Cap Sensitivity Analysis (R2-M1 — Critical)

Reviewer 2 correctly identifies that the rank-based edge cap at 20,000 is itself a form of preferential weak-edge removal. If soft-bounded networks generate more low-weight edges, the cap activates more aggressively for exactly those conditions, potentially reintroducing the confound. **Please run a sweep over cap values (e.g., 10k, 20k, 50k, unlimited) with the 2×4 factorial design and report whether the disordinal interaction is cap-dependent.** This is essential for the paper's central claim.

### 2. Response Rank Validation (R1-M3, R2-M3 — Critical)

Both R1 and R2 note that the SVD rank threshold (1% of largest singular value) is a free parameter whose choice determines the paper's central metric. **Please provide:** (a) full singular value spectra for representative seeds in each regime, (b) a sensitivity analysis over threshold choices (0.1%, 1%, 5%, 10%), and (c) the participation ratio as a threshold-free alternative (R2's suggestion). The distinction between rank 1.2 and 4.7 must be shown to be robust to reasonable threshold variation.

### 3. Eta ANOVA Power and Selection (R2-M2)

The eta ANOVA with 6/50 qualifying seeds is a concern shared by both empirical reviewers. **Please address:** (a) what the 44 excluded seeds produce (failure mode analysis), (b) whether the selection criterion (≥2 assemblages) inflates the effect size, and (c) whether a non-parametric alternative or a model that incorporates the zero-assemblage seeds would change the conclusion. The d=5.62 needs explicit justification or recalculation.

### 4. CCD Null Model Specification (R1-M2)

The CCD invalidation is stated but not fully specified. **Please provide** the null model construction procedure (how weight values are permuted, what spatial structure is preserved, what assemblage detection is used on permuted weights) in sufficient detail for replication.

### 5. Generality Across Network Scales (R1-M1)

The factorial is conducted on a single 20×20 grid. While this matches the prior papers, the claim that pruning is a confound "for the field" requires evidence beyond one topology. **Please provide** at least one additional grid size (e.g., 30×30 or 10×10) showing the interaction persists.

### 6. Simondonian Terminology (R3-M1, M2, M3)

Reviewer 3 identifies a genuine inconsistency: the hard clip is described as both "mould" (Discussion) and "structural germ" (supplement framing). These are distinct Simondonian concepts. **Please resolve this equivocation** by either (a) showing evidence of spatial/temporal propagation (which would justify "germ"), or (b) adopting "limit condition" as the more accurate term (R3's suggestion). Additionally, clarify whether the three-regime taxonomy represents three instances of the same transductive process or three genuinely different operations.

---

## Recommended Revisions (not required but encouraged)

### 7. Pruning Literature Context (R2-Q6)

Reviewer 2 notes that the computational neuroscience literature treats pruning as constructive (improving generalization). A paragraph situating your confound finding within this broader perspective would strengthen the Discussion.

### 8. Fine-Grained Threshold Sweep (R1-M4, R2-M7)

Both R1 and R2 request finer resolution around the 1e-6 to 1e-5 critical region and around the k=1.5 steepness transition. Dedicated figures for these transitions would strengthen the quantitative claims.

### 9. Steepness Mechanism (R1-m1, R2-M7)

The non-monotonic steepness result is one of the paper's most interesting findings but is underexplored. A mechanistic explanation of why intermediate steepness produces monopoly (beyond the current paragraph) would add substantial value.

### 10. Abstract Accessibility (R1-m4)

The abstract packs too many numerical results. Consider restructuring to lead with the qualitative finding (pruning reverses the bound-type ranking) and defer specific numbers to the Results.

---

## Summary of Reviewer Recommendations

| Reviewer | Expertise | Recommendation | Primary Concern |
|---|---|---|---|
| R1 | Computational ALife | Major Revision | Generality, CCD null specification, response rank validation |
| R2 | Theoretical Neuroscience | Major Revision | Edge cap confound, eta ANOVA power, SVD threshold sensitivity |
| R3 | Philosophy of Technology | Accept (minor) | Simondonian terminology consistency |

The empirical core of this paper is strong and the confound identification is a genuine service to the field. The revisions requested are primarily about hardening the evidence for the replacement metrics and mechanisms, not about the central finding itself. I look forward to seeing the revised manuscript.

Sincerely,
*Editor, Artificial Life*

---

*Full reviews from all three reviewers are attached below.*

- Reviewer 1: [See R1 review]
- Reviewer 2: [See R2 review]
- Reviewer 3: [See R3 review]
