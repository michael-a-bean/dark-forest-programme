# Dissertation Committee Meeting — March 13, 2026

**Re:** Revision strategy for "Dark Forest in Silica" after Major Revision decision from *Artificial Life*

**Committee:**
- Dr. Elena Vasquez (Chair) — Complex Systems, Santa Fe Institute
- Dr. James Okafor — Computational Neuroscience, UCL
- Dr. Marie-Claire Dupont — Philosophy of Technology, European Graduate School

---

## Committee Consensus: The Paper Is Saveable in ~3 Weeks

All three committee members agree the reviews are fair and the paper is publishable with revision. The reviewers are sympathetic — they called the writing clear, the ablation study rigorous, and the negative results commendable. This is a "we want to accept this" set of reviews.

---

## TIER 1: Blocking Issues (Do First)

### 1. Substrate Figure Discrepancy (ALL REVIEWERS)

**The problem:** The substrate-timeline.png and spatial-heatmap.png show a *saturated* regime (693 edges, weights at 1.0, 120-node community, uniform activation 0.93–1.0). The text describes *selective individuation* (3 edges, 3 nodes, bright band at 0.1–0.2 against dark background). These cannot both be true.

**Vasquez:** "This is worse than a formatting error. If any reviewer suspects the text describes results that don't exist, the paper is dead."

**Okafor:** "You almost certainly generated figures at gradient=0.5 or 1.0 instead of 0.3. The git status shows these PNGs were recently modified. Check which run produced them."

**Action:** Trace provenance. Regenerate from gradient=0.3 run. Verify numbers match text. Do this before anything else.

### 2. Multi-Seed Replication (ALL REVIEWERS)

**The problem:** Everything runs on seed 42. Statistics like "9% persistence" and "weight std 0.0055" are single-realization numbers presented as system properties.

**Okafor's prescription:**
- Phase 1 baseline: 30 seeds minimum
- Parameter sweep (Table 1): 10 seeds per setting, expand from 4 to 8 entries
- Substrate gradient sweep: 10 seeds per gradient value, add gradient=0.2 and 0.4
- Multi-field: 10 seeds, report monopoly session (mean + range)
- Use bootstrap CIs, not parametric assumptions
- Total: ~300-400 runs. Computationally cheap — a day of batch compute.

**What to expect:** Phase 1 equilibrium is a strong attractor — variance will be small. Substrate individuation will show variance in node count (2-5) and position. Report the distribution.

### 3. Literature Review (REVIEWERS 1 + 3)

**Essential citations (must add):**
| Reference | Why |
|-----------|-----|
| Langton (1990) "Edge of Chaos" | Your three-regime finding IS this |
| Kauffman (1993) "Origins of Order" | NK landscapes, same critical regime pattern |
| Linsker (1988) | Direct predecessor — Hebbian self-org without supervision |
| Kohonen (1982) / SOMs | Competitive Hebbian learning with spatial organization |
| Ray (1991) / Tierra | Digital ecology, competitive exclusion |
| Ofria & Wilke (2004) / Avida | Must cite if claiming competitive exclusion results |
| Watson & Szathmáry (2016) | Hebbian learning as evolutionary memory |

**Add a Related Work section** (2-3 pages) between Background and Methods. Three subsections: (1) Hebbian self-organization, (2) Edge of chaos / criticality, (3) Digital ecosystems.

**Vasquez:** "Do not treat this as an obligation — treat it as ammunition. Every connection to prior work is evidence that your findings are real."

---

## TIER 2: Major Issues (Must Address)

### 4. Competition Experiment Redesign (REVIEWER 3)

**The confounds:**
- T=5.0 is too soft (near-uniform allocation)
- Identical input guarantees synchronization (passive mirror finding predicts this)

**Okafor's prescription:**
- Temperature sweep: T = {0.5, 1.0, 2.0, 5.0, 10.0, 50.0}, 10 seeds each
- Asymmetric inputs: (a) same text, (b) different texts, (c) English vs. Markov chain
- Predict: critical T below which one network dies → another three-regime result

### 5. Philosophical Claims Calibration (REVIEWER 2)

**Dupont's assessment — where Reviewer 2 is right:**

| Claim | Problem | Fix |
|-------|---------|-----|
| "Cancerous BwO" = saturation | Cancerous BwO involves metastasis/reproduction, not fixation | Rename to "stratified" or "overcoded" BwO |
| "Simondon computationally demonstrated" | Overreach — this is symmetry-breaking, not full transduction | Say "structurally analogous to Simondon's individuation schema" |
| Desiring-production invoked but not operationalized | Appears in intro, vanishes forever | **Remove entirely from this paper** |
| "Maps precisely onto" the three dangers | Claims isomorphism you can't support | Soften to "resonates with" or "is illuminated by" |

**Dupont's assessment — where Reviewer 2 is WRONG:**

- **"Merely decorative" is wrong.** The framework did genuine *design work*: choosing hard clipping over Oja/BCM, predicting three regimes before confirming them, driving the Phase 2 transition from clusters to identical substrate. These are design choices the philosophy generated. Defend this.

- **Reviewer 2 missed the passive mirror as "tracing."** In *A Thousand Plateaus*, Deleuze distinguishes tracing (reproducing existing structure) from mapping (producing new structure). Phase 1 = tracing machine. Phase 2 substrate = begins to approach mapping. This is the paper's strongest philosophical result and the reviewer didn't engage with it.

- **Reviewer 2's demand for predictions DST "alone" can't generate misunderstands the relationship.** Deleuze's ontology IS a philosophy of dynamical systems (via DeLanda). It provides ontological interpretation, not competing mathematical predictions. Say this explicitly.

**Dupont's key recommendation — ADD the concept of the *diagram/abstract machine*:** The parameter ratio η/λ is a Deleuzian diagram — an abstract relation producing the same three-regime pattern across every architecture. This is a strong claim well-supported by evidence and genuinely novel.

### 6. "Goalless" Framing (REVIEWERS 1 + 2)

**Vasquez:** Replace "goalless" with "optimization-free" or "loss-free" throughout. Add one paragraph distinguishing "no loss function" (accurate) from "no designed structure" (not what you have).

### 7. PCA Variance (REVIEWER 1)

**Okafor:** Text says 30%, figure shows 8%. Almost certainly computed on different sessions or different phase subsets. Fix: report actual numbers from the figure. At 8% in 64 dimensions with stochastic input, that's expected — acknowledge limited interpretive value.

---

## TIER 3: Minor Issues (Worth Doing, Not Blocking)

- Consolidate two Discussion sections into one
- Add multi-field substrate figures (data exists)
- Fix bibliography (remove uncited refs, complete Bhalla et al., add Hardin 1960)
- Standardize vector notation
- Report computational cost per run
- Moderate palpation novelty claim ("epistemological reorientation, not methodological innovation")
- Consider: Markov chain input experiment (separates "structure formation" from "character memorization")

---

## What NOT to Do

**Vasquez:** "Do NOT remove the philosophy to appease Reviewer 1. Do NOT change the title prematurely. Do NOT over-respond to 'does the passive mirror undermine the whole program?' — that's a provocation, not a suggestion."

**Dupont:** "Do NOT add desiring-production development — save it for a future paper. Do NOT claim formal isomorphism where you have heuristic correspondence. Do NOT treat the philosophy as separate from the experiments — the point is that it *drove* the experimental design."

---

## Specific Textual Changes (from Dupont)

| Location | Current | Revised |
|----------|---------|---------|
| Abstract | "the network is a Body without Organs whose..." | "We interpret this system through Deleuze and Guattari's Body without Organs, which guided both design and analysis" |
| §2.2 | "A neural network without a loss function *is* a BwO" | "can be *read as* a BwO" |
| §4.1 | "Cancerous BwO" | "Stratified BwO" — cite ATP p.159: "You will be organized, you will be an organism" |
| §4.1 | "This maps precisely onto" | "This pattern resonates with... while also exhibiting what Langton (1990) identified as the 'edge of chaos'" |
| Table 6 | "Simondon computationally demonstrated" | "Structurally analogous to Simondon's individuation schema" |
| Discussion | (add new) | Introduce the *diagram* concept: η/λ as abstract machine producing same pattern across architectures |
| Discussion | (add new) | Passive mirror = Deleuzian "tracing"; substrate individuation = beginning of "mapping" |

---

## Timeline

| Week | Tasks |
|------|-------|
| 1 | Fix substrate figures; fix structural issues (Discussion merge, refs, notation) |
| 2 | Multi-seed replication runs (batch compute); write Related Work section |
| 3 | Competition temperature sweep + asymmetric inputs; Markov chain experiment |
| 4 | Statistical analysis; update all quantitative claims with CIs; PCA fix |
| 5 | Revise philosophical claims (Dupont's changes); write response letter |
| 6 | Buffer, proofread, final figure verification |

---

## Response Letter Strategy (Vasquez)

Open by acknowledging the figure discrepancy directly and explaining what happened. Structure around three themes:

1. **Corrections** — "We apologize for these errors and have corrected them"
2. **Strengthening** — "These suggestions substantially improved the paper"
3. **Calibration** — "We have recalibrated our claims to match the evidence while preserving the interpretive framework that motivated the experimental design"

Point-by-point responses with page/line references for every reviewer comment.

---

## Final Word (Vasquez)

"The reviewers have given you a roadmap to a much stronger paper. The figure discrepancy is your most urgent problem because it is the only issue that could cause a reviewer to question your integrity. Fix that first, verify everything, then work through the rest systematically. The paper that comes out of this revision will be substantially better than what went in. That is what major revisions are for."
