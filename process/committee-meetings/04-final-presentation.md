# Dark Forest Programme — Committee Presentation

## Status: All Experimental Work Complete, All Papers Revised

**Date:** 2026-03-24
**Presenter:** Michael Bean
**Committee:** Vasquez (Chair), Okafor, Dupont

---

## I. Paper 4S: Ready for Submission

### Title
"Pruning as Confound: How Maintenance Processes Obscure Functional Diversity in Self-Organising Networks"

### Manuscript status
- Full Quarto draft: 345 lines, renders clean
- 9 publication figures (PDF + PNG, 300 DPI)
- All statistics verified against raw parquet data (Remy audit)
- Proofreading complete — all issues resolved

### Evidence base
- 28 experiments, ~12,000 simulation jobs, ~2.5M observations
- Key results verified: F factorial (n=30), pruning sweep (n=20), eta ANOVA (n=50), deconfounded probes (n=30), no-pruning replications (n=20)

### Key figures in paper

| Fig | Content | Key number |
|---|---|---|
| 1 | Steepness non-monotonicity | k=1→6.0 asm, hard→4.9, k=2-50→monopoly |
| 2 | Disordinal interaction | Hard 3.9→5.6, tanh 0.2→7.0 |
| 3 | Response rank ± pruning | Rank 1.2→4.7 without pruning |
| 4 | Deconfounded probes | Uniform rank 3.1-3.3, Gaussian 2.0 |
| 5 | Eta F-ratio | F=4.91, p=0.000018, d=5.62 |

### Target venue options
1. *Artificial Life* — consistent with Papers 1-3 venue
2. *Neural Computation* — methodological contribution angle
3. *PLOS Computational Biology* — broader reach, open access

### Remaining tasks before submission
- Final prose polish pass (1-2 days)
- Select venue, format to journal requirements
- Write cover letter

---

## II. Papers 1-4: Revision Status

### Papers 1-3: Minimal changes applied

| Paper | Venue | Status | Changes |
|---|---|---|---|
| 1: Emergent Structure | Published (revised) | Footnote added | Pruning note on monopoly claim |
| 2: Coexistence | Published (revised) | Footnote added | Pruning sensitivity note in Methods |
| 3: Self-Sealing | Published (revised) | Footnote added | Pruning + CCD note in Methods |

**Question for committee:** Papers 1-3 are published. Should the footnotes be:
- (a) Incorporated into revised editions (if journal permits corrigendum/update)
- (b) Left as-is in published versions, with Paper 4S serving as the correction record
- (c) Added to the dissertation versions only

### Paper 4: Substantial revision applied

| Change | Detail |
|---|---|
| Abstract rewritten | Leads with response rank 4.7, revised central claim |
| Metrics reordered | Response rank first, CCD last with caveat |
| 8 figure captions updated | CCD → "geometric separation" throughout |
| Exp 17np results absorbed | No-pruning rank 4.7 integrated into Results |
| Conclusion restructured | Leads with functional evidence |
| Pruning methodological note | Full paragraph in Methods |
| CCD validity caveat | Prominent note after metrics definition |

**Key claim change:** "Local homeostasis enables differentiation" → "Local homeostasis stabilises and amplifies differentiation that Hebbian dynamics produce on spatially structured substrates"

**Question for committee:** Paper 4 title still says "Enables." Should we:
- (a) Change title to "Local Homeostasis Stabilises Differentiation in Hebbian Substrates"
- (b) Keep title, acknowledge in abstract that the claim is refined by Paper 4S
- (c) Keep title as-is (it's technically accurate — homeostasis does enable, even if it's not the sole enabler)

---

## III. Programme Status and Next Steps

### Completed deliverables
- All 5 paper drafts revised
- Paper 4S complete draft
- Dissertation frame (236 lines)
- Programme audit report
- 9 publication figures
- Statistical report (eta ANOVA)
- Quarto book project configured (_quarto.yml)
- All proofreading issues resolved

### Committee's 12-week timeline (from 2026-03-24)

| Weeks | Target | Status |
|---|---|---|
| 1-4 | Paper 4 revision + Paper 4S draft | **DONE** (ahead of schedule) |
| 2-6 | Paper 4S submission-ready | **DRAFT COMPLETE** — needs final polish + venue selection |
| 5-8 | Papers 1-3 footnotes | **DONE** |
| 5-10 | Dissertation frame | **DRAFT COMPLETE** |
| 10-12 | Committee review + final revisions | Not yet started |

### Proposed next steps

**Immediate (weeks 1-2):**
1. Submit Paper 4S to target venue
2. Submit revised Paper 4 (if resubmission needed)

**Short-term (weeks 3-6):**
3. Complete dissertation book rendering (Quarto book project)
4. Write response letters for any Paper 1-3 corrigenda
5. Begin defence preparation

**Medium-term (weeks 7-10):**
6. Address reviewer feedback on 4S/4
7. Polish dissertation frame into full introduction/conclusion
8. Assemble complete dissertation document

**Question for committee:**
- Is the programme complete enough for defence scheduling?
- Should Paper 4S submission wait for Paper 4 revision to be accepted, or go in parallel?
- Any additional experiments or analyses needed?

---

## IV. The Elevator Pitch (Dupont, R3 meeting)

> "Self-organising networks on spatially structured substrates spontaneously produce functionally diverse assemblages through Hebbian reinforcement alone, but standard network maintenance — weight pruning — systematically destroys this diversity by selectively removing the weak exploratory connections that distinguish one assemblage from another. Metaplasticity stabilises and amplifies this diversity. The result is a minimal model of how individuation emerges from homogeneous substrates: not through any single mechanism, but through the interaction of spatial structure, reinforcement dynamics, and adaptive learning rules, provided the maintenance regime doesn't destroy the evidence."

---

*All data, code, figures, and analysis scripts are available across the four repositories. Programme audit: `papers/04s-bounds/programme-audit.md`.*
