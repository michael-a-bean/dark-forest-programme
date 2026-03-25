# Paper 2 — R1 Peer Review Summary

**Manuscript:** "Conditions for Stable Coexistence in Optimization-Free Hebbian Substrates"
**Journal:** Artificial Life (MIT Press)
**Date:** March 14, 2026

## Decisions
- **Reviewer 1** (Computational ALife): Minor Revision
- **Reviewer 2** (Ecology/Coexistence Theory): Major Revision
- **Reviewer 3** (Philosophy + Computation): Minor Revision

## Critical Issues (all reviewers)

### 1. Ecological framing is misleading (R2, strongest)
What we call "coexistence" is spatial subdivision of identical competitors — allopatry, not niche-mediated coexistence. Chesson's mechanisms are cited but not applied. Tilman, Hubbell, Durrett & Levin are in the bibliography but never discussed.

### 2. "Differential coupling" at broad locality is unsubstantiated (R1, R3)
We claim assemblages at broad locality "couple to different combinations of hotspot energy" but present no evidence. Need: weight vector similarity between coexisting assemblages as a function of locality.

### 3. Differenciation (with a c) is the missing diagnostic concept (R3)
The planning document has the right analysis — "individuation without differenciation" — but it's not in the paper. Without it, the reader doesn't understand WHY assemblages are identical.

### 4. Hotspot placement confound (R1)
For n>4 hotspots, positions use a single random seed. The migrating ridge could be geometry-dependent. Need robustness check.

### 5. Migrating ridge may not be novel (R2)
The ridge is a predictable consequence of patch-size vs. dispersal-range geometry (Tilman 1994, Hanski 1998). Need comparison to existing spatial competition predictions.

### 6. Statistical gaps (R1, R2)
- No formal test of phase transition sharpness (sigmoidal fit)
- No confidence intervals on heatmap cells
- No logistic regression with interaction term
- Stability check only at one locality

### 7. Designed vs emergent milieus (R3)
Tight-locality milieus are designed by the experiment, not emergent. The associated milieu concept is only genuinely earned in the broad-locality regime.

### 8. DeLandian vs Deleuzian diagram (R3)
Our usage is DeLandian (topological invariant). Should note this is not the full Deleuzian diagram (generative machine producing novelty from chaos).

## Minor Issues (consolidated)
- Show threshold sensitivity figure, not just assert it
- Grid size result needs a figure
- Show weight distribution bimodality histogram
- Spatial visualization of coexistence vs monopoly
- Clarify hotspot placement algorithm
- Extend stability check to transition regime (ℓ=0.10-0.12)
- Report effect sizes, not just p-values
- Discuss Tilman, Hubbell, Durrett & Levin substantively
- Dark precursor reference in conclusion is imprecise
