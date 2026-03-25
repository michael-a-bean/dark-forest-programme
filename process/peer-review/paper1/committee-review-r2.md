# Committee Review of Revised Draft — Round 2

**Date:** March 13, 2026
**Re:** "Emergent Structure in Optimization-Free Hebbian Networks" (revised)

---

## Overall Verdict: 85% Ready — 4 Required Fixes, 5 Recommended

All three committee members agree the revision is substantially improved. The critical issues from R1 are resolved. The paper is stronger without Dark Forest framing. The philosophical calibration is well-executed.

---

## Required Before Resubmission

### 1. Reframe Competition Temperature Sweep Honestly (Okafor — CRITICAL)

**Problem:** The temperature sweep (T=0.5 to T=50.0) produces **identical results at every temperature** — resource share = 0.500, similarity = 1.000 by session 23. Temperature has no measurable effect. Presenting six indistinguishable conditions as a sweep is misleading.

**Fix:** Reframe as a strong confirmation of passive mirror dominance: "The softmax temperature had no measurable effect on convergence dynamics. At all temperatures tested, shared input drove complete synchronization, confirming that the passive mirror property dominates competitive pressure."

### 2. Add Watson & Szathmáry (2016) (Vasquez + Okafor)

Essential citation missing. "How Can Evolution Learn?" connects Hebbian learning to evolutionary memory — directly relevant to passive mirror and competitive exclusion findings. Add to Related Work.

### 3. Add Markov Chain Description to Methods (Vasquez)

The Markov input experiment reports results but never describes the chain's order, state space, or transition probabilities. A reviewer will ask "what Markov chain?" Add a brief paragraph in Methods.

### 4. Report Multi-field Monopoly Session Statistics (Vasquez)

"7 of 10 collapse to monopoly" — but at what session? Report mean and range. Are the 3 non-monopoly seeds trending toward monopoly or stable? This was specifically requested by R3.

---

## Strongly Recommended

### 5. Develop Diagram Concept in Discussion (Dupont)

The diagram/abstract machine concept is introduced in Background and confirmed in Substrate results but underplayed in Discussion. Add a dedicated paragraph: η/λ is not merely a parameter — it is a diagram whose universality across architectures constitutes evidence for DeLanda's thesis.

### 6. Complete Tracing → Mapping Arc (Dupont)

Passive mirror = Deleuzian "tracing" is introduced but the substrate section doesn't close the arc by noting it approaches "mapping" (producing structure not present in input). One paragraph in Discussion.

### 7. Explicit Philosophy Defense (Dupont)

Add 2-3 sentences in Discussion listing the framework's concrete contributions: (1) rejected normalization schemes with hidden objectives, (2) predicted three-regime structure, (3) provided diagram concept for universality.

### 8. Acknowledge Markov Activation Density Confound (Okafor)

Text vs. Markov differs in activation density (multi-dimensional vs. one-hot-ish), not just correlational structure. Acknowledge this or add a character-shuffled text control.

### 9. Report Computational Cost (Okafor)

One sentence: "Each 20-session baseline run completes in approximately X seconds on [hardware]."

---

## What's Well Done

- **Replication:** 30 seeds baseline, 10 everywhere else, mean ± SD throughout
- **Literature:** Related Work section is substantive, covers all essential citations except Watson & Szathmáry
- **Philosophy calibration:** "can be read as," "resonates with," "structurally analogous" — all correctly tempered
- **Simondon passage:** "the single best philosophical revision in the paper" (Dupont)
- **"Optimization-free" framing:** thorough, honest, self-aware
- **Desiring-production:** cleanly removed with no gaps
- **Paper is stronger without Dark Forest:** unanimous committee agreement

---

## How Reviewers Will Likely Respond

| Reviewer | Prediction |
|----------|-----------|
| R1 (Computational ALife) | Likely satisfied. Literature gap addressed. May ask about Watson & Szathmáry and computational cost. |
| R2 (Philosophy) | Should be satisfied. All overclaiming addressed. May push on tracing/mapping development. |
| R3 (Multi-agent / Game Theory) | Most likely to push back. Will note competition sweep is null. May ask for asymmetric input. Multi-field monopoly session stats will be requested if not reported. |

---

## Bottom Line (Vasquez)

"The revision is substantial, responsive, and honest. Fix the four required items — especially the competition reframing — and this is ready to resubmit. The paper that comes out is significantly better than what went in. The Dark Forest removal was the right call."
