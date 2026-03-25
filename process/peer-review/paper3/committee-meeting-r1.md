# Dissertation Committee Meeting — Paper 3 R1 Revision Strategy

**Date:** March 15, 2026
**Re:** Revision strategy for Paper 3 after Minor Revision decision from *Artificial Life*

**Committee:**
- Dr. Elena Vasquez (Chair) — Complex Systems, Santa Fe Institute
- Dr. James Okafor — Computational Neuroscience, UCL
- Dr. Marie-Claire Dupont — Philosophy of Technology, European Graduate School

---

## Agreed Action Plan

### Priority 1 — Required Revisions (Week 1)

1. **Edge injection re-run** (Days 1-2). Three initialization levels: pruning threshold (10⁻⁴), median within-assemblage weight, mean within-assemblage weight. Cross with existing α strengths and injection rates. Report persistence duration, steady-state count, and whether anti-Hebbian fires during transient. ~1,440 simulations, ~3h on cluster.

2. **Temporal variation results section** (Days 2-3). Write up existing 1,094 simulations as dedicated results section with one figure (cross-assemblage edges across switching periods). Resolves simulation count discrepancy simultaneously. Check transient self-sealing rate across switching periods.

3. **Analytic supplement on expected edge survival** (Days 3-4, Okafor drafts). Derive expected reinforcement for cross-assemblage edges under Gaussian encounter locality. Show survival time as function of initial weight, co-activation probability, and decay rate.

4. **Trilemma language** (Day 4). Soften to "structural incompatibility." State conditions precisely, demonstrate empirical joint impossibility, conjecture structural with analytic support.

5. **Crystalline individuation precision** (Day 4). Two-sentence fix: crystal as product characterization (identical structure, exhausted potential), not process analogy (transduction/propagation).

6. **Bare vs. complex repetition** (Day 5). One paragraph in Discussion. Bare = Papers 1-3. Complex = what the substrate cannot achieve.

### Priority 2 — Recommended Additions (Week 2)

7. **Decay rate sensitivity** — three λ values (0.001, 0.005, 0.01)
8. **Transient analysis** — sessions 1-20, max cross-edge count, Clopper-Pearson CI
9. **Assemblage detection threshold sensitivity** — 50th/90th percentile
10. **DeLanda cascades** — two sentences on truncated symmetry-breaking
11. **Transindividuation** — one paragraph on failure of transindividual relation
12. **Dark precursor correction** — one sentence (event, not mechanism)

### Priority 3 — Explicitly NOT Doing

- BCM implementation (scope out as future work in Discussion)
- Homeostatic scaling implementation (scope out)
- STDP implementation (scope out)
- Connell IDH integration
- Expanded Oja/Foldiak background

### Key Disagreements Resolved

- **Trilemma**: Okafor wanted formalization, Dupont wanted softening. **Resolved:** Soften language but include analytic support.
- **Philosophy scope**: Okafor worried about philosophical apparatus overwhelming empirical result. **Resolved:** Include required additions only + brief DeLanda/transindividuation. Don't expand Connell.
- **Edge injection risk**: If non-zero initialization shows persistent cross-edges + no differentiation, this actually *strengthens* the paper (Okafor's point: functional isolation even with maintained topology).

### Timeline

| Day | Task |
|-----|------|
| 1-2 | Edge injection re-run (computation) |
| 2-3 | Temporal variation writeup |
| 3-4 | Analytic supplement (Okafor) |
| 4 | Trilemma language + crystalline fix |
| 5 | Bare/complex repetition paragraph; Okafor reviews computation |
| 6 | Decay sensitivity + transient analysis |
| 7 | DeLanda, transindividuation, detection threshold |
| 8 | Dupont reviews philosophical sections |
| 9-10 | Vasquez reviews full revision |
| 11-13 | Final edits + response letter |
| 14 | Submit |

### Paper 4 Implications

The self-sealing result provides precise design requirements for the next substrate. Paper 4 should introduce a substrate designed from philosophical requirements for differenciation — not "try BCM" but heterogeneous plasticity rules, intensive gradients, maintained cross-assemblage connectivity by design. Separate planning meeting after revision submission.
