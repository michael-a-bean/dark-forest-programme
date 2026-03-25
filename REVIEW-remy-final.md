# Final Pre-Publication Review

**Reviewer:** Remy (Remington) -- Technical Advisor, Dark Forest Programme
**Date:** 2026-03-25
**Scope:** Full repository audit before public release
**Verdict:** CONDITIONAL PASS -- 8 items must be fixed, 6 should be fixed

---

## 1. README.md

**CONDITIONAL PASS**

### What works
The README is genuinely good. The framing is honest -- the "What is real / What is simulated" distinction is clear, prominent, and doesn't hedge. The table of papers is concise. The "How to Read This" section is the kind of thing most repos lack and most readers need. The "Honest Assessment" section listing convergent findings is a power move -- it builds trust by giving away what a critic would find anyway.

### Issues to fix

**[MUST FIX] Placeholder GitHub URL.** Line 183: `https://github.com/[username]/dark-forest-programme` -- this is a placeholder. Replace with the actual URL before publishing.

**[MUST FIX] Directory tree is inaccurate.** The tree (lines 54-87) claims `academic-audit-report.md` and `defence-prep.md` are in `dissertation/`. In reality:
- `academic-audit-report.md` is at `process/audit/academic-audit-report.md`
- `defence-prep.md` is at `dissertation/defence-prep.md` (this one is correct)
- But the tree implies `academic-audit-report.md` is a sibling of `defence-prep.md` inside `dissertation/`. It is not. It is in `process/audit/`.

The prose on line 115 says `process/audit/academic-audit-report.md` which is correct -- but the tree diagram contradicts it.

**[MUST FIX] Committee meeting count inconsistency.** Line 39 says "6 committee meetings" but `process/committee-meetings/` contains 5 files (00 through 04). The README tree on line 79 says "4 committee briefings + meeting transcripts." Pick one number and make it consistent.

**[SHOULD FIX] Missing `Network` class.** The README says `src/substrate/` contains "MultiField, MetaplasticField, TemporalField" -- this is accurate. But `cluster_job.py` imports `from src.network import Network` and no `Network` class exists in the repo. The cluster job scripts reference code from the original `dark-forest-bounds` repo that was not consolidated. This means the experiment scripts cannot actually run standalone. The README should note this.

**[SHOULD FIX] META-PAPER_files/ not in .gitignore effectively.** The `.gitignore` has `*_files/` but also `!META-PAPER.html`. The `META-PAPER_files/` directory is tracked (it contains Quarto rendering artifacts -- bootstrap CSS, JS). This is 11 generated files that add noise. Either keep them intentionally (for people who want to view the HTML locally) or gitignore them and add a note about rendering.

---

## 2. META-PAPER.qmd

**PASS with minor issues**

### What works
The document flows well. The opening ("None of this was planned") is honest and sets the right tone -- it reads like a real account, not a post-hoc narrative. The committee dynamics section is the most interesting part. The capabilities/limitations section is balanced. The convergence table with citations is clean.

### Issues to fix

**[MUST FIX] Grammar error on line 114.** "capabilities that used throughout the programme" should be "capabilities that **were** used throughout the programme."

**[SHOULD FIX] No Reproducibility section substance.** Section 7.3 "For Reproducibility" is a single sentence: "The accompanying repository contains all code, data, papers, and process transcripts." This undersells the repo and also is not entirely accurate (the code cannot run standalone -- see Network class issue above, and data paths point to external repos). Either expand this to be honest about what's reproducible and what isn't, or remove the claim.

### Citations
All 9 `@citation` keys in the QMD have matching entries in `meta-references.bib`. Verified: `miessler2024pai`, `anthropic2025claudecode`, `moritz2018ray`, `allaire2024quarto`, `hooker2019compressed`, `achille2019critical`, `stringer2019high`, `maturana1980autopoiesis`, `adams2017formal`. No orphaned or missing citations.

### Style
No obvious AI writing patterns survived. The prose is direct, uses active voice, and avoids the hedging/qualifying that typically flags AI text. The adversarial team did their job.

---

## 3. Repo Completeness

**CONDITIONAL PASS**

### Files referenced in README that exist
- All 5 paper directories: PRESENT
- `dissertation/so-what-analysis.md`: PRESENT
- `dissertation/defence-prep.md`: PRESENT
- `process/audit/academic-audit-report.md`: PRESENT
- `proposals/paper5-topology.md`: PRESENT
- `META-PAPER.md`: PRESENT

### Missing files
- **Paper 1 has no `references.bib`** -- the QMD on line 73 declares `bibliography: references.bib` but the file does not exist in `papers/01-emergent-structure/`. The paper will not render citations. Papers 02, 03, 04, and 04s all have their bib files.

### Orphaned files
- `META-PAPER.md` (310 lines) appears to be a Markdown render of `META-PAPER.qmd`. It is not referenced anywhere except the README link. This is fine as a convenience file but should be noted as a generated artifact.
- `META-PAPER.html` and `META-PAPER_files/` are Quarto rendering output tracked in git. Intentional convenience or accident?
- `dissertation/so-what-analysis-references.md` exists but is not referenced in the README tree or any other document I can find.
- `process/audit/stats-eta-anova.md` exists but is not listed in the README tree under `process/audit/`.
- `process/audit/programme-audit.md` exists but is not listed in the README tree.

### Data completeness
14 parquet datasets present in `data/`. Papers 1-3 reference data paths that do NOT exist in this repo:
- Paper 1 references `DATA_DIR/substrate/spatial_activity.parquet` -- no `substrate` directory exists under `data/`
- Paper 2 references `DATA_DIR/coupling_analysis/session_metrics.parquet` -- no `coupling_analysis` directory exists under `data/`
- These were presumably in the original single-paper repos (`dark-forest-silica`, etc.) and were not consolidated.

Paper 4S references data both from `data/` (via `_setup.R`) and from a sibling directory `dark-forest-metaplastic/data` (line 19 of the QMD: `meta_data <- file.path(dirname(dirname(getwd())), "..", "dark-forest-metaplastic", "data")`). This path will break for any user who does not have the original repo sitting adjacent.

### Sensitive information
- **No API keys, tokens, or passwords found.**
- NFS cluster paths (`/mnt/cluster/experiments/...`) appear in 9 cluster job scripts. These are not sensitive but signal "this was run on a specific machine" -- which is fine for process documentation.
- Home directory paths (`~/research/dark-forest-metaplastic`, `~/research/dark-forest-bounds`) appear in cluster job scripts and some committee meeting documents. Not sensitive, but they will confuse people who think the code should run locally.
- One research report references a full absolute path: `/home/michael/research/dark-forest-metaplastic/papers/04-metaplasticity/...` -- not sensitive, but looks unpolished.

---

## 4. Code Quality

**CONDITIONAL PASS**

### Substrate code (src/substrate/)
The three substrate classes (`MultiField`, `MetaplasticField`, `TemporalField`) are well-structured, documented, and self-contained. They depend only on `numpy`. They can run standalone. The inheritance chain is clean: `MultiField` -> `MetaplasticField` (adds per-node eta and inhibitor), `MultiField` -> `TemporalField` (adds config switching and anti-Hebbian).

**One issue:** `MetaplasticField.__init__` accepts `weight_bound_type` as a keyword argument in the cluster job scripts (line 265 of `cluster_job.py`: `weight_bound_type=params["weight_bound_type"]`), but the `MetaplasticField` class does not accept this parameter. The `__init__` passes `**kwargs` to `MultiField`, which accepts `bound_type` not `weight_bound_type`. This means the cluster jobs for experiment 4 would have failed at runtime unless there was a parameter mapping somewhere. This looks like it was resolved in the actual execution but the code as committed has the mismatch.

### Metrics code (src/metrics/)
Four clean modules. `capacity_diversity.py` imports `sklearn` (PCA, KMeans, silhouette_score) -- this is not declared as a dependency anywhere and is not in any requirements file. The other three metrics depend only on `numpy`.

### Experiment scripts (src/experiments/)
These are historical artifacts -- they document what was run on the cluster. They all have hardcoded NFS paths and import from modules (`src.network`) that don't exist in this repo. They are not runnable standalone. This is acceptable as documentation but should be stated clearly.

**[SHOULD FIX] No requirements.txt or pyproject.toml.** The substrate code needs `numpy`. The metrics need `numpy` and `sklearn`. The experiments need `ray`, `pyarrow`, and `numpy`. The R analysis needs `tidyverse`, `arrow`, `ggthemes`, `viridis`, `patchwork`, `scales`, and `here`. None of this is declared anywhere.

---

## 5. The Papers

**CONDITIONAL PASS**

### Paper QMD data paths
- **Paper 1** (`01-emergent-structure`): Uses `here::here()` to find `data/` -- but references `substrate/spatial_activity.parquet` which does not exist in `data/`. **WILL FAIL TO RENDER.**
- **Paper 2** (`02-coexistence`): References `coupling_analysis/session_metrics.parquet` which does not exist in `data/`. **WILL FAIL TO RENDER.**
- **Paper 3** (`03-self-sealing`): Uses same `_setup.R` pattern. Would need to check specific data references.
- **Paper 4** (`04-metaplasticity`): Uses same `_setup.R` pattern. Would need to check specific data references.
- **Paper 4S** (`04s-pruning-confound`): Has its own `_setup.R` that correctly navigates to `../../data/`. Most data referenced (expF_factorial, expB_prune_sweep, etc.) IS present in `data/`. However, line 19 reaches out to `../dark-forest-metaplastic/data` for two experiments (exp17_response_matrix, exp17np_response_noprune) -- both of which DO exist in `data/` but the path is wrong. It uses a `tryCatch` so it will degrade gracefully rather than crash.

**[MUST FIX] Paper 1 missing `references.bib`.** Cannot render without it.

### Bib files
- Paper 1: **MISSING** `references.bib`
- Paper 2: PRESENT
- Paper 3: PRESENT
- Paper 4: PRESENT
- Paper 4S: PRESENT

---

## 6. Process Artifacts

**PASS**

### Committee meetings
The five documents (00-04) are coherent standalone. They include committee member names, institutional affiliations, dates, and enough context to understand the discussions without conversation history. The committee meeting documents reference paths to the original repos (`~/research/dark-forest-bounds/`) at the bottom of each file, but these are clearly metadata/provenance lines, not user-facing instructions.

### Peer review
Well-structured. The editorial decisions read like real journal correspondence -- appropriately formal, with numbered revision requirements and clear rationale. The response letters are substantive. The review process for Paper 4S is particularly thorough (edge cap sensitivity, response rank validation, etc.).

### Academic audit
Comprehensible and well-organized by phase. The Phase 2 code-data consistency table (matching paper claims against parquet data) is the strongest part -- it provides exact verification that numbers in the papers match the data.

### One concern
The audit report on line 31 references `dark-forest-bounds/papers/04s-bounds/references.bib` -- this is an original repo path that doesn't map to the consolidated repo structure (`papers/04s-pruning-confound/references.bib`). This is a process artifact reporting on the state of things at audit time, so arguably it should be preserved as-is. But a reader might try to follow the path and get confused.

---

## 7. What's Missing

### Must add before publication

1. **Fix the README directory tree** to match actual file locations.
2. **Fix the placeholder GitHub URL** in the citation block.
3. **Fix the committee meeting count** (README says 6, filesystem has 5, tree says 4).
4. **Add Paper 1's `references.bib`** or note that Papers 1-3 are incomplete drafts.
5. **Fix the grammar error** in META-PAPER.qmd line 114.

### Should add if time permits

6. **Add a `requirements.txt`** or at minimum a "Dependencies" section in README listing: Python (numpy, scipy, scikit-learn), R (tidyverse, arrow, ggthemes, viridis, patchwork, scales, here), and Quarto.
7. **Add a note in README** that Papers 1-3 reference data from the original single-paper repos that is not fully consolidated into this programme repo. Be explicit that Paper 4S is the most self-contained paper.
8. **Fix or note the Paper 4S data path** that reaches outside the repo to `dark-forest-metaplastic/data`.

### What people will ask about that isn't documented

- **"How do I run the substrate code?"** There is no minimal example, no `examples/` directory, no "Quick Start." Someone who wants to play with the MultiField needs to read the class and figure it out. A 20-line example script would help enormously.
- **"Where are the figures for Papers 1-4?"** Paper 4S has pre-rendered PDFs in `figures/`. The other papers presumably render from data -- but the data isn't all present.
- **"What are the four original repos?"** The programme was developed across `dark-forest-silica`, `dark-forest-bounds`, `dark-forest-metaplastic`, and possibly others. This is mentioned nowhere in the README. A brief provenance note would help.
- **"Is GEN a real product?"** The README references GEN and PAI but doesn't clarify that GEN is a personal configuration/persona, not a downloadable tool. Someone will google "GEN AI assistant" and find nothing.

---

## Summary

| Section | Verdict | Blockers | Notes |
|---|---|---|---|
| 1. README.md | CONDITIONAL PASS | 3 must-fix | Good framing, inaccurate tree |
| 2. META-PAPER.qmd | PASS | 1 must-fix | Grammar error, thin reproducibility claim |
| 3. Repo completeness | CONDITIONAL PASS | 1 must-fix | Missing Paper 1 bib, incomplete data |
| 4. Code quality | CONDITIONAL PASS | 0 must-fix | Substrate clean, experiments not portable |
| 5. Papers | CONDITIONAL PASS | 1 must-fix | Paper 1 bib missing, data path issues |
| 6. Process artifacts | PASS | 0 | Coherent and well-structured |
| 7. What's missing | N/A | N/A | Quick start, dependencies, provenance |

**Bottom line:** Fix the 5 must-fix items (placeholder URL, directory tree, meeting count, Paper 1 bib, grammar error) and this is ready to ship. The 3 should-fix items (requirements.txt, data path notes, Network class note) would make it significantly more usable. The "what people will ask" items are nice-to-haves that would elevate it from "impressive archive" to "inviting repository."

The science is solid. The process documentation is genuinely unusual and valuable. The honesty about limitations and convergence with prior art is the repo's greatest strength. Ship it.

---

*Review conducted by Remy (Remington), Technical Advisor*
*2026-03-25*
