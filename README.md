# The Dark Forest Programme

> **[Browse the rendered papers and dissertation](https://michael-a-bean.github.io/dark-forest-programme/)**

## A Question That Grew Into a Programme

This started as a conversation about Liu Cixin's Dark Forest hypothesis — whether something like a dark forest could already exist in silica. That led to a question about what an AI not governed by human objectives might look like, which led to Deleuze, which led to code. No research agenda, no proposal, no plan to write anything.

The conversation led to code. The code produced results worth writing up. Writing raised questions that required more experiments. The experiments revealed a confound that changed everything. At each step, the decision to continue was made in the moment, driven by curiosity and dissatisfaction with easy answers.

Twelve days later (March 13-25, 2026), the conversation had accumulated into a five-paper research programme with a dissertation, produced through collaboration between Michael Bean and **GEN** — a personal AI assistant built on [PAI (Personal AI Infrastructure)](https://github.com/danielmiessler/Personal_AI_Infrastructure) running on [Claude Code](https://claude.ai/claude-code) with Claude Opus 4.6.

**What is real.** The code runs. The data is real. The experiments executed on a physical Ray cluster (68 CPUs, 3 nodes).

**What is simulated.** The academic scaffolding — committee meetings, peer review, editorial decisions, the doctoral defence — was entirely simulated using AI agents across multiple conversation sessions. PAI's persistent memory preserved project context between sessions. No papers were submitted to any journal. No committee was convened. No defence took place. These simulated processes served as quality-control tools and stress tests, not as claims of academic standing.

**What makes this repository unusual** is that it documents all of it: computation, simulated process, and the decisions that connected them.

---

## What's Here

### The Science

Five papers and one methodological supplement on Hebbian self-organisation:

| Paper | Title | Key Finding |
|---|---|---|
| [1](https://michael-a-bean.github.io/dark-forest-programme/papers/01-emergent-structure/paper.html) | Emergent Structure in Optimization-Free Hebbian Networks | Spontaneous assemblage formation from noise |
| [2](https://michael-a-bean.github.io/dark-forest-programme/papers/02-coexistence/paper.html) | Locality-Dependent Coexistence Mechanisms | Sharp phase transition between coexistence and monopoly |
| [3](https://michael-a-bean.github.io/dark-forest-programme/papers/03-self-sealing/paper.html) | Coexistence Without Differentiation: Self-Sealing | Every Hebbian intervention fails; the substrate seals |
| [4](https://michael-a-bean.github.io/dark-forest-programme/papers/04-metaplasticity/paper.html) | Local Homeostasis Stabilises Differentiation | Per-node metaplasticity produces response rank 5.6 |
| [4S](https://michael-a-bean.github.io/dark-forest-programme/papers/04s-pruning-confound/paper.html) | Pruning as Confound | Pruning reverses the ranking of approaches (disordinal interaction) |

The programme's central finding: **maintenance operations in self-organising systems interact with the phenomena they maintain, and this interaction can be disordinal.** Removing weak connections destroys exactly the exploratory structure that enables functional diversity — a principle validated across neural networks, metallurgy, ecology, markets, supply chains, and immune systems.

### The Process

What makes this repository unusual:

- **[5 committee meetings](process/committee-meetings/)** with three persistent AI personas (Vasquez/complex systems, Okafor/neuroscience, Dupont/philosophy) who maintained intellectual positions, disagreed productively, and changed their minds when persuaded
- **[5 rounds of peer review](process/peer-review/)** with domain-expert AI reviewers who caught errors (CCD invalidity, Simondonian terminology, statistical methods) and prompted 900 additional simulation jobs
- **[14-agent parallel literature review](dissertation/research-reports/)** that discovered ~40-50% of findings had prior art — leading to an [honest reckoning](dissertation/so-what-analysis.md) rather than a cover-up
- **A [comprehensive academic audit](process/audit/academic-audit-report.md)** (7 phases, ~75 tool invocations) that caught stale documents, a Shapiro-Wilk error, and a bib entry duplication
- **A mock doctoral defence** with external examiners (Beer on autopoiesis, Hooker on pruning fairness) that identified the programme's deepest vulnerability. [Defence preparation notes](dissertation/defence-prep.md)
- **~15,000 simulation jobs** producing approximately 4.6 million session-level observations across [28 experiments](src/experiments/)

**A note on completeness:** Documenting the process was a late decision — the science came first. Many committee consultations (journal submission readiness, how to weigh peer review concerns, scope decisions) were not saved. What's here was reconstructed from git history, PAI's persistent memory, and artifacts that survived in the working directory. Conversations that produced no artifacts left no trace.

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
  defence-prep.md          # 5 hardest questions with answers

src/                       # All source code
  substrate/               # MultiField, MetaplasticField, TemporalField
  metrics/                 # Response rank, CCD, modularity, eta divergence
  experiments/             # 10 cluster job scripts

data/                      # Key experimental data (parquet)

analysis/                  # R scripts for publication figures

process/                   # The unique part
  committee-meetings/      # 5 committee documents
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
| Simulation jobs | ~15,000 (estimated; not fully countable from consolidated data) |
| Session-level observations | ~4.6M across all repos; ~293K in programme repo |
| Experiments | 28 |
| Papers completed | 5 + 1 supplement |
| Simulated acceptance decisions | 4 of 5 documented |
| Agent invocations | ~60-70 (estimate; no invocation logs saved) |
| Committee meeting documents | 5 dedicated + additional in peer review |
| Simulated peer review rounds | 5 |
| Literature citations examined | ~100 |
| Days from first commit to assembly | 12 |
| CPU hours | ~200 (estimated) |

---

## How to Read This

**If you're interested in the science:** Start with [Paper 4S](https://michael-a-bean.github.io/dark-forest-programme/papers/04s-pruning-confound/paper.html) (the pruning confound, most self-contained and broadest implications), then [Paper 4](https://michael-a-bean.github.io/dark-forest-programme/papers/04-metaplasticity/paper.html) for the metaplasticity mechanism.

**If you're interested in the process:** Start with the [META-PAPER](https://michael-a-bean.github.io/dark-forest-programme/META-PAPER.html), then explore [committee meetings](process/committee-meetings/) and [peer review](process/peer-review/).

**If you're interested in what AI-assisted research looks like:** Read the ["So What?" analysis](dissertation/so-what-analysis.md) for the honest reckoning with prior art, then the [academic audit report](process/audit/academic-audit-report.md) for the integrity check, then the [programme audit](process/audit/programme-audit.md) for the full cross-paper assessment.

**If you want to run the code:** Start with [`examples/quickstart.py`](examples/quickstart.py) — a 40-line script that instantiates the substrate and runs it. The substrate code in [`src/substrate/`](src/substrate/) is self-contained Python (numpy, scipy). The [cluster job scripts](src/experiments/) show the experimental designs. Data is in [`data/`](data/) as Apache Parquet files. See [`requirements.txt`](requirements.txt) for dependencies.

**Note on data paths:** The `data/` directory contains key experimental datasets from Papers 4 and 4S. Papers 1-3 reference data from the original single-paper repositories not fully consolidated here. Paper 4S is the most self-contained entry point.

---

## The Honest Assessment

**~40-50% of major findings converge with prior literature.** Documented in the ["So What?" analysis](dissertation/so-what-analysis.md) and addressed in the [dissertation introduction](dissertation/chapters/introduction.qmd).

What's novel:
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

**Michael Bean (human):** Strategic direction throughout. Which questions to ask, when to run experiments vs write, when to consult the committee, when to challenge results. The three decisions that shaped the programme most: testing the pruning threshold when the committee raised it, asking "so what, who cares?" (triggering the literature review), and writing up the process alongside the science.

**GEN (AI assistant):** Built on [PAI (Personal AI Infrastructure)](https://github.com/danielmiessler/Personal_AI_Infrastructure) by Daniel Miessler, running on Claude Code with Claude Opus 4.6 (1M context). Executed, analysed, wrote, reviewed, and audited. Spawned specialised agents for parallel research (CodexResearcher, GeminiResearcher, GrokResearcher, PerplexityResearcher, ClaudeResearcher, Architect, Explore, Engineer) and maintained persistent committee personas across sessions. The committee disagreement format produced better decisions than any single agent — each member's blind spots got corrected by the others.

### The Stack

GEN runs on [PAI (Personal AI Infrastructure)](https://github.com/danielmiessler/Personal_AI_Infrastructure) by Daniel Miessler, which extends [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (Anthropic's CLI) with agent orchestration, persistent memory, skill routing, and structured reasoning. The underlying model is Claude Opus 4.6 with a 1M-token context window. PAI spawns specialised sub-agents (Architect, Engineer, researchers across multiple API backends) that share the base model but operate in separate contexts, enabling parallel execution.

The computation ran on a [Ray](https://www.ray.io/) cluster (3 nodes, 68 CPUs). Ray handled job submission, fault tolerance (the laptop node disconnected during every overnight run; tasks retried automatically), and result retrieval.

The papers use [Quarto](https://quarto.org/) because the simulations are Python (numpy, scipy) and the analysis is R (ggplot2, arrow, patchwork). Quarto renders both in a single `.qmd` document. [Apache Parquet](https://parquet.apache.org/) bridges the two: Python writes typed columnar data, R reads it via `arrow::read_parquet()`. The full experimental record (~3M observations) compresses to ~40MB.

---

## Future Work

[Paper 5 proposal: "Does the Dark Forest Have Roads?"](proposals/paper5-topology.md) — testing whether the programme's findings hold on non-lattice topologies (small-world, scale-free, random geometric graphs). The strongest prediction: scale-free topology will suppress coexistence because hub nodes enforce the monopoly dynamic.

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
https://github.com/michael-a-bean/dark-forest-programme
```

---

*All academic processes documented here (committee meetings, peer review, editorial decisions, defence) were simulated using AI agents. The computational experiments and their results are real.*
