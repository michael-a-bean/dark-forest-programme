# The Dark Forest Programme

## A Complete AI-Assisted Research Programme — From Conversation to Defence

This repository contains the **complete artifacts** of a doctoral-scale research programme in computational artificial life, produced over 12 days (March 13-25, 2026) through collaboration between a human researcher and an AI system (Claude, via the PAI personal AI infrastructure).

**This is not a simulated exercise.** The code runs, the data is real, the experiments executed on a physical Ray cluster (68 CPUs across 3 nodes), and the findings are genuine. What makes this repository unique is that it documents not just the science but the **entire research process** — including the AI-simulated committee meetings, peer reviews, literature searches, audits, and mock defence that shaped the work.

---

## What's Here

### The Science

Five papers and one methodological supplement on Hebbian self-organisation:

| Paper | Title | Key Finding |
|---|---|---|
| 1 | Emergent Structure in Optimization-Free Hebbian Networks | Spontaneous assemblage formation from noise |
| 2 | Locality-Dependent Coexistence Mechanisms | Sharp phase transition between coexistence and monopoly |
| 3 | Coexistence Without Differentiation: Self-Sealing | Every Hebbian intervention fails — the substrate seals |
| 4 | Local Homeostasis Stabilises Differentiation | Per-node metaplasticity produces response rank 5.6 |
| 4S | Pruning as Confound | Pruning reverses the ranking of approaches (disordinal interaction) |

The programme's central finding: **maintenance operations in self-organising systems interact with the phenomena they maintain, and this interaction can be disordinal.** Removing weak connections destroys exactly the exploratory structure that enables functional diversity — a principle validated across neural networks, metallurgy, ecology, markets, supply chains, and immune systems.

### The Process

What makes this repository unusual:

- **6 committee meetings** with three persistent AI personas (Vasquez/complex systems, Okafor/neuroscience, Dupont/philosophy) who maintained intellectual positions, disagreed productively, and changed their minds when persuaded
- **5 rounds of peer review** with domain-expert AI reviewers who found genuine errors (CCD invalidity, Simondonian terminology, statistical methods) and prompted 780 additional simulation jobs
- **14-agent parallel literature review** that discovered ~40-50% of findings had prior art — leading to an honest reckoning rather than a cover-up
- **A comprehensive academic audit** (7 phases, ~75 tool invocations) that caught stale documents, a Shapiro-Wilk error, and a bib entry duplication
- **A mock doctoral defence** with external examiners (Beer on autopoiesis, Hooker on pruning fairness) that identified the programme's deepest vulnerability
- **~15,000 simulation jobs** producing ~3 million observations across 28 experiments

### The Meta-Paper

[`META-PAPER.md`](META-PAPER.md) documents the entire process: how the AI system was used, what it did well (parallel execution, self-correction, cross-domain synthesis), what it did poorly (literature awareness, philosophical overconfidence), and the integrity questions this raises.

---

## Repository Structure

```
papers/                    # 5 paper manuscripts (Quarto)
  01-emergent-structure/
  02-coexistence/
  03-self-sealing/
  04-metaplasticity/
  04s-pruning-confound/

dissertation/              # Dissertation frame
  chapters/                # Introduction, methods, synthesis, conclusion
  research-reports/        # 15 literature analysis reports from 14 agents
  so-what-analysis.md      # "Who cares?" — the honest assessment
  academic-audit-report.md # 7-phase integrity audit
  defence-prep.md          # 5 hardest questions with answers

src/                       # All source code
  substrate/               # MultiField, MetaplasticField, TemporalField
  metrics/                 # Response rank, CCD, modularity, eta divergence
  experiments/             # 11 cluster job scripts

data/                      # Key experimental data (parquet)

analysis/                  # R scripts for publication figures

process/                   # The unique part
  committee-meetings/      # 4 committee briefings + meeting transcripts
  peer-review/             # 5 papers × editorial decisions + response letters
  audit/                   # Programme audit + academic audit + statistical report

proposals/                 # Future work
  paper5-topology.md       # "Does the Dark Forest Have Roads?"

META-PAPER.md              # The process documentation
```

---

## The Numbers

| Metric | Value |
|---|---|
| Simulation jobs | ~15,000 |
| Observations | ~3,000,000 |
| Experiments | 28 |
| Papers | 5 + 1 supplement |
| Agent invocations | ~70 |
| Committee meetings | 6 |
| Peer review rounds | 5 |
| Literature citations verified | ~100 |
| Days from first commit to defence | 12 |
| CPU hours | ~200 |

---

## How to Read This

**If you're interested in the science:** Start with `papers/04s-pruning-confound/paper.qmd` — the pruning confound paper is the most self-contained and has the broadest implications.

**If you're interested in the process:** Start with [`META-PAPER.md`](META-PAPER.md), then explore `process/committee-meetings/` and `process/peer-review/`.

**If you're interested in what AI-assisted research looks like:** Read `dissertation/so-what-analysis.md` for the honest reckoning with prior art, then `process/audit/academic-audit-report.md` for the integrity check.

**If you want to run the code:** The substrate code in `src/substrate/` is self-contained Python (numpy, scipy). The cluster job scripts in `src/experiments/` show the experimental designs. Data is in `data/` as Apache Parquet files readable by pandas, R arrow, or any Parquet reader.

---

## The Honest Assessment

The committee's verdict: **~40-50% of major findings converge with prior literature.** This is not hidden — it's documented in `dissertation/so-what-analysis.md` and addressed head-on in the dissertation introduction.

What's genuinely novel:
- The disordinal interaction (pruning reverses approach rankings) — no prior art
- The hard clip irreducibility (non-monotonic steepness) — no prior art
- The critical threshold boundaries and grid-size scaling law — no prior art
- The philosophical architecture (Simondon→Deleuze→DeLanda diagnostic sequence)
- The baseline=metaplasticity parity on response rank (a productive negative result)

What's convergent with prior work:
- Pruning destroys diversity (Hooker et al. 2019, Tran et al. 2022)
- Critical periods emerge (Achille et al. 2019)
- Response rank as metric (Stringer et al. 2019)
- Self-sealing ≈ autopoiesis (Maturana & Varela 1980)
- Fixed rules can't produce novelty (Adams et al. 2017)

The convergence is interpreted as **evidence the underlying phenomena are real**, not as redundancy.

---

## Who Did What

**Michael Bean (human):** Directed every significant decision. Which questions to ask, when to run experiments vs write, when to submit vs revise, the decision to conduct the meta-literature review, the decision to conduct the audit. Asked the questions that mattered.

**PAI / Claude (AI system):** Executed, analysed, wrote, reviewed, and audited. Spawned specialised agents for parallel research. Maintained persistent committee personas. Identified and corrected its own methodological errors.

The most productive pattern was the **committee disagreement format**: multiple AI personas with distinct intellectual commitments debating a question produced better decisions than any single agent.

---

## License

Code: MIT License
Papers and process documents: CC-BY 4.0

---

## Citation

If you use or reference this work:

```
Bean, M. (2026). The Dark Forest Programme: A Complete AI-Assisted Research
Programme in Computational Artificial Life. GitHub repository.
https://github.com/[username]/dark-forest-programme
```

---

*"The human asked the questions that mattered."*
