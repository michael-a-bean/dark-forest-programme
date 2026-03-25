# Artificial Life — Editorial Decision

**Manuscript:** "Coexistence Without Differentiation: The Self-Sealing Dynamics of Hebbian Individuation"
**Authors:** Michael Bean
**Submission type:** Article
**Date:** March 15, 2026

---

## Decision: MINOR REVISION

Dear Michael Bean,

Thank you for submitting your manuscript to *Artificial Life*. Your paper has been reviewed by three experts: computational artificial life (Reviewer 1), theoretical neuroscience and synaptic plasticity (Reviewer 2), and philosophy of technology and process philosophy (Reviewer 3). This is the third paper in a series previously published in this journal, and the reviewers were familiar with the prior work.

The reviewers unanimously found the central result — that Hebbian substrates produce "self-sealing" individuation, eliminating cross-assemblage edges within 20 sessions across 2,414 simulations — to be genuine, well-evidenced, and a meaningful contribution to the field. The self-sealing concept, the coexistence-interaction trilemma, and the three-paper arc were all identified as strengths. However, two reviewers (R1, R2) raised concerns about the edge injection experiment design, and all three identified areas where the paper's claims outrun its evidence or where important connections are undertheorized.

I concur with the majority recommendation of **Minor Revision**, though I note that Reviewer 2's recommendation of Major Revision is driven primarily by the edge injection design issue (M2), which is addressable without extensive new computation.

---

## Required Revisions

### 1. Edge Injection Initialization (R1-M2, R2-M2 — Critical)

Both Reviewers 1 and 2 identified that injected cross-assemblage edges are initialized at weight 0, which is below the pruning threshold. This means injected edges are immediately pruned rather than being "actively eliminated by Hebbian dynamics." The self-sealing claim requires distinguishing between these two scenarios. **Please either:** (a) re-run the injection experiment with edges initialized at a non-zero weight (e.g., the median within-assemblage weight) and report the results, **or** (b) provide a clear argument for why zero-initialization is the appropriate test and acknowledge the limitation.

### 2. Temporal Variation Results (R1-M1)

The abstract and introduction claim that temporal environmental variation was tested, but no dedicated results are presented. Either report the temporal variation results with at least one figure, or remove the claim from the abstract and introduction.

### 3. Simulation Count Discrepancy (R1-m2)

The stated total of 2,414 simulations does not match the two described experiments (840 + 480 = 1,320). Clarify the provenance of the additional simulations or correct the count.

### 4. Trilemma Formalization (R1-M3, R3-M2)

Both Reviewers 1 and 3 noted that the "trilemma" is presented discursively rather than formally demonstrated. Either sharpen the logical structure (state the three conditions precisely and demonstrate their joint incompatibility) or soften the language to "structural tension" rather than "trilemma."

### 5. Crystalline Individuation Precision (R3-M1)

Reviewer 3 correctly notes that Simondon's crystal individuates at its boundary through propagation, whereas your assemblages nucleate independently. Clarify which aspect of crystalline individuation you are claiming and acknowledge the limits of the analogy.

### 6. Deleuze on Repetition (R3-M3)

Reviewer 3 identifies a missed connection to Deleuze's distinction between bare and complex repetition (*Difference and Repetition*, Chapter 1) that would strengthen the philosophical argument. Please engage with this distinction and locate the self-sealing phenomenon within Deleuze's theory of repetition.

---

## Recommended Revisions (not required but encouraged)

- Decay rate sensitivity analysis (R2-M3): Varying λ would strengthen the "structural" claim
- Transient differentiation analysis during sessions 1-20 (R1-m5, R2-Q)
- DeLanda's symmetry-breaking cascades as an alternative framing (R3-m1)
- Simondon's transindividuation as the concept for what fails (R3-m2)
- Formal statistical bound on cross-edge counts: report maximum, not just mean (R1-m3)
- Oja convergence caveat for nonlinear recurrent dynamics (R2-m2)

---

## Summary

This paper characterizes a genuine structural limitation of Hebbian substrates and introduces the "self-sealing" concept, which names a phenomenon not previously articulated in the literature. The three-paper arc provides a compelling narrative about the boundary of correlation-based learning. The required revisions are tractable and would strengthen the paper without changing its core message. I look forward to receiving the revised manuscript.

Sincerely,
*Editor, Artificial Life*
