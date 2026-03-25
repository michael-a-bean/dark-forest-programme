# AI as Research Infrastructure: A Case Study in Dissertation-Scale Computational Science

## How GEN/PAI/Claude Code Conducted, Validated, and Defended a Five-Paper Doctoral Programme

---

## Abstract

We document the research process behind a doctoral dissertation comprising five papers and one methodological supplement in computational artificial life, produced over 12 days (March 13-25, 2026) using **GEN** — a personal AI assistant built on [PAI (Personal AI Infrastructure)](https://github.com/danielmiessler/Personal_AI_Infrastructure) by Daniel Miessler, running on [Claude Code](https://claude.ai/claude-code) with Claude Opus 4.6 (1M context). The process involved autonomous experiment design and cluster execution (~15,000 simulation jobs, ~3M observations), simulated dissertation committee meetings with persistent AI personas, AI-conducted peer review at a simulated journal, comprehensive literature search using 14 parallel research agents across 5 API backends, a full academic integrity audit, and a mock doctoral defence with external examiners. We describe the architecture, the specific roles played by AI agents at each stage, the failure modes encountered, and the surprising discoveries that emerged from the process — including several findings that were independently validated against prior literature the system had not been designed to search. The case raises questions about the nature of academic discovery when the researcher, the committee, the reviewers, and the auditors are all AI systems operating under the direction of a single human principal.

---

## 1. Origin: From Conversation to Computation

### 1.1 The Seed (March 13, 2026)

The programme began as a conversation about Deleuze's concept of differenciation and whether purely goalless dynamics could produce qualitatively different kinds from identical starting conditions. The initial git commit at `dark-forest-silica` (2026-03-13 00:17:53) was titled "Initial commit — Dark Forest in Silica project." Within 30 minutes, the repository contained a Deleuzian philosophical framework (609 lines of research on Difference and Repetition) and the first Hebbian network experiments.

The velocity was striking: by 16:43 the same day, the multi-field substrate (the foundation for all five papers) was implemented and producing results. By 23:08, the full reproducible pipeline (Python → Parquet → R → Quarto) was operational. Paper 1 went through committee review and acceptance within 24 hours of the first commit.

### 1.2 Philosophical Research as Computational Scaffold

Before any code was written, PAI conducted deep philosophical research that shaped the entire programme. Two research documents survive in the silica repository's memory:

- **"Capacities, Intent, and Affordances"** — a synthesis of Gibson's affordance theory and DeLanda's capacity concept, establishing the relational ontology that would later become the response rank metric's theoretical grounding.
- **"Qualitative Differentiation from Homogeneous Substrates"** — a careful reading of Deleuze's distinction between differentiation (virtual determination) and differenciation (actualisation into distinct kinds), which generated the specific prediction that the Hebbian substrate would achieve the former but not the latter.

This prediction — the "productive fracture" — proved correct across all subsequent experiments and became the programme's central philosophical result. The philosophical framework was not applied post-hoc; it generated testable predictions that were subsequently confirmed or falsified.

### 1.3 The Acceleration

| Date | Milestone |
|---|---|
| Mar 13 | Paper 1: substrate, experiments, pipeline, paper draft, committee review, acceptance |
| Mar 14 | Paper 2: coexistence, coupling analysis, acceptance |
| Mar 15 | Paper 3: self-sealing, 1400 simulations, committee meeting, editorial decision |
| Mar 16-17 | Cluster setup, Paper 4 repo scaffolded, experiments 1-3 launched |
| Mar 17-20 | Papers 4 experiments 1-19 on Ray cluster (6,070 jobs) |
| Mar 20 | Paper 4S repo scaffolded, initial bounds experiments |
| Mar 22 | Committee-requested experiments (Okafor concerns) |
| Mar 23 | Pruning confound discovered, Phases 1-3 experiments |
| Mar 24 | Paper 4S peer review, Paper 4 revision, functional validation, academic audit |
| Mar 25 | Dissertation assembly, 14-researcher literature review, mock defence, corrections |

---

## 2. The PAI Architecture

### 2.1 System Overview

**GEN** is the human principal's personal AI assistant, built on [PAI (Personal AI Infrastructure)](https://github.com/danielmiessler/Personal_AI_Infrastructure) by Daniel Miessler. PAI is a Claude Code-based system that extends Anthropic's CLI with:

- **Agent spawning**: the ability to launch specialised sub-agents (Explore, Architect, Engineer, CodexResearcher, GeminiResearcher, GrokResearcher, PerplexityResearcher, ClaudeResearcher) for parallel task execution
- **Persistent memory**: a file-based memory system at `~/.claude/MEMORY/` with work items, learning signals, and relationship context
- **Work tracking**: PRD-based task management with ISC (Ideal State Criteria) for each work item
- **Algorithm mode**: a structured reasoning protocol for complex tasks
- **Skills**: modular capabilities (Research, Thinking, etc.) invoked by slash commands
- **Voice notifications**: an HTTP-based notification system for status updates

### 2.2 The Agent Taxonomy

Throughout the programme, different agent types served different roles:

| Agent Type | Role in Programme | Instances |
|---|---|---|
| **Architect** | Committee members (Vasquez, Okafor, Dupont), system design | ~15 |
| **CodexResearcher (Remy)** | Technical feasibility, code review, programme audit, proofreading | ~8 |
| **Explore** | Codebase analysis, file search, data verification | ~10 |
| **ClaudeResearcher** | Academic literature search | ~5 |
| **GeminiResearcher** | Multi-perspective literature search | ~5 |
| **GrokResearcher** | Contrarian analysis, cross-domain connections | ~5 |
| **PerplexityResearcher** | Philosophy literature, source verification | ~3 |
| **General-purpose** | Statistical reproduction, Paper 4 structural analysis | ~5 |

Total agent invocations across the programme: approximately 60-70.

---

## 3. The Simulated Committee

### 3.1 Persistent Personas

Three AI committee members maintained consistent intellectual positions throughout:

**Dr. Elena Vasquez (Chair, Complex Systems, Santa Fe Institute)**: Pragmatic, scope-focused, protective of timeline. Consistently pushed for "minimum viable experiments" and warned against scope creep. Made the decisive calls on submission timing and paper structure.

**Dr. James Okafor (Computational Neuroscience, UCL)**: Statistically rigorous, methodologically demanding. Raised the two concerns (pruning confound, CCD invalidity) that reshaped the entire programme. His insistence on nested ANOVA, Wilcoxon robustness checks, and deconfounded probes substantially improved the statistical grounding.

**Dr. Marie-Claire Dupont (Philosophy of Technology, EGS)**: Philosophically precise, resistant to superficial deployment of Deleuze/Simondon. Her correction of "structural germ" to "limit condition" was validated by the external examiner (Beer) in the mock defence. Her framing of the "productive fracture" became the programme's central philosophical contribution.

### 3.2 How the Committee Was Used

The committee met (was invoked) at six key decision points:

1. **R1 review of initial findings** — assessed the five original experiments
2. **Debate on next steps** — disagreed productively on scope (Vasquez: 2 experiments, Okafor: 3, Dupont: 1)
3. **R2 review after committee experiments** — all concerns confirmed
4. **R3 review with full results** — revised narrative, new title
5. **Final pre-submission review** — approved with two minor edits
6. **Response to peer review** — triaged reviewer concerns, planned revision

The committee's most significant contribution was the **debate format**: when members disagreed (which happened regularly), the disagreement produced better decisions than any individual member would have reached. Vasquez's pragmatism moderated Okafor's experimental ambition; Dupont's philosophical precision corrected Vasquez's tendency to dismiss philosophical contributions as "too cute."

### 3.3 Emergent Committee Dynamics

An unexpected finding: the committee developed what appeared to be genuine intellectual relationships. Okafor's partial concession to Dupont on "phantom individuation" (accepting a threshold-based compromise) was not scripted — it emerged from the dialogue format. Vasquez's shift from "lead with confound" to "lead with steepness" came after being persuaded by both Okafor and Dupont in the same meeting. These shifts were persistent across sessions because the committee members' positions were regenerated from the accumulated context of prior meetings.

---

## 4. The Simulated Peer Review

### 4.1 Architecture

Each paper submission involved:
1. Three AI reviewers with distinct expertise profiles (matching Artificial Life's typical reviewer pool)
2. Reviewers given the full paper text and asked for structured reviews (summary, recommendation, major/minor concerns, strengths, questions)
3. An editorial decision synthesising the reviews
4. Response letter addressing each concern
5. Revision and resubmission

### 4.2 Quality of AI Peer Review

The AI reviewers identified genuine issues:

- **R1 (ALife, Paper 4S)**: Flagged that CCD invalidation was "underdeveloped" and response rank "not validated" — both legitimate concerns addressed by new experiments
- **R2 (Neuroscience, Paper 4S)**: Identified the edge cap as a potential confound — "the most dangerous item on the list" — which was definitively resolved by the cap sensitivity sweep
- **R3 (Philosophy, Paper 4S)**: Corrected "structural germ" to "limit condition" — a genuine Simondonian error that an informed reviewer would catch

The AI reviewers also made mistakes:
- Remy's first proofread incorrectly flagged data as wrong (the data was correct; Remy had a loading error)
- R1 for Paper 4 read both Paper 4 and Paper 4S, creating confusion about which paper contained which numbers
- Some reviewer questions were answerable from the paper itself, suggesting incomplete reading

### 4.3 The Review Loop as Quality Improvement

Papers improved measurably through the review process. Paper 4S gained:
- Edge cap sensitivity analysis (Rev1: 360 jobs)
- Grid size generality (Rev2: 240 jobs)
- Full SVD threshold sweep with participation ratio (Rev3: 180 jobs)
- 7 new literature citations
- Corrected Simondonian terminology

Total: 900 additional simulation jobs and 3 new figures generated specifically to address reviewer concerns. This mirrors the real peer review process where revision experiments often exceed the original submission.

---

## 5. The Technical Research Assistant (Remy)

### 5.1 Role

The CodexResearcher agent "Remy" served as the programme's technical conscience — a persistent technical advisor who:

- Assessed experimental feasibility and compute time before each cluster submission
- Conducted the comprehensive programme audit (76 tool uses, 114K tokens, 12 minutes)
- Proofread every paper revision, catching numerical inconsistencies
- Generated all 9 publication figures via the R analysis script
- Wrote the 450-line Methods chapter for the dissertation

### 5.2 Remy's Contribution to the Pruning Discovery

When the committee requested experiments to test the pruning confound, Remy's feasibility assessment identified a critical risk: "Pruning=0 memory explosion. With prune_threshold=0 on a 20×20 grid, encounter_rate=20 creates 20 new edges/step × 300 steps/session = 6000 edges/session." This led to the max_edges cap design, which later became the subject of a reviewer concern (R2's critical concern about the cap reintroducing the confound) and a definitive resolution (the cap never activates because edges self-stabilise at ~1,350).

### 5.3 Remy's Errors

Remy was not infallible. In the final proofread before Paper 4S resubmission, Remy incorrectly flagged the response rank data as wrong ("hard noprune rank@1% = 4.3, not 5.6"). Direct verification against the parquet data confirmed the paper's numbers were correct. This false alarm delayed submission by approximately 20 minutes but reinforced the importance of verifying auditor claims against primary data.

---

## 6. The Literature Review: 14 Agents in Parallel

### 6.1 Architecture

The "So What?" analysis deployed 14 research agents simultaneously across 5 API backends:

- 3 Claude agents (academic literature search)
- 3 Gemini agents (multi-perspective analysis)
- 3 Grok agents (contrarian analysis, cross-domain connections)
- 5 domain-specific contextualizers (network science, ALife, philosophy, applications, neuroscience)

### 6.2 The Uncomfortable Discovery

The literature review found that approximately 40-50% of the programme's major findings had substantial prior art:
- Pruning destroys diversity → Hooker et al. 2019, Tran et al. 2022
- Critical periods emerge → Achille et al. 2019, Kleinman et al. 2024
- Response rank as metric → Stringer et al. 2019 (standard tool)
- Self-sealing = autopoiesis → Maturana & Varela 1980
- Fixed rules can't produce novelty → Adams et al. 2017

This discovery could have been devastating. Instead, the committee reframed it: "Convergent discovery from independent starting points is evidence that the underlying phenomenon is real, not an artifact of one methodology."

### 6.3 The Cross-Domain Principle

The Grok agent's cross-domain analysis identified what may be the programme's most generalisable finding: weak-element pruning destroying functional diversity is a universal principle across self-organising systems. The agent verified this across metallurgy (grain boundaries), ecology (mass extinction), markets (killer acquisitions), supply chains (redundancy removal), and immune systems (thymic selection), each with primary literature citations.

---

## 7. The Academic Audit

### 7.1 The Coordinator Pattern

The academic audit used a novel architecture: a single coordinating agent that spawned specialised sub-agents for each verification phase. The coordinator:

1. Read the relevant files
2. Designed a specific verification task
3. Spawned a sub-agent with precise instructions
4. Reviewed the sub-agent's findings
5. Recorded PASS/FAIL for each check
6. Produced the final report

### 7.2 What the Audit Found

Seven phases, all passed with specific corrections:
- **Citation verification**: PASS (1 bib author duplication)
- **Code-data consistency**: PASS (all numbers exact)
- **Statistical methods**: PASS (Shapiro-Wilk p-value was wrong: 0.40 should be 0.99)
- **Internal consistency**: FAIL → PASS (dissertation-frame.qmd had stale "structural germ" and "4.7")
- **Philosophical terms**: PASS (Adams et al. "proved" → "demonstrated")
- **Reproducibility**: PASS (3/3 chains verified)
- **Prose quality**: PASS

The audit caught errors that multiple rounds of proofreading had missed: the dissertation-frame.qmd was an earlier document that hadn't been updated when Papers 4/4S were revised. This is a realistic failure mode — maintaining consistency across a multi-document programme is exactly where automated auditing adds value.

---

## 8. The Mock Defence

### 8.1 External Examiners

The mock defence introduced two new AI personas not previously involved in the programme:

- **Prof. Randall Beer** (Indiana University) — chosen for expertise in computational autopoiesis, directly relevant to the self-sealing/operational closure claims
- **Prof. Sara Hooker** (Cohere) — chosen as the author whose prior work (Hooker et al. 2019) most directly preceded the pruning confound finding

### 8.2 The Hardest Moment

Beer's question — "perhaps there's no individual there to transplant — just a spatial pattern in a continuous field" — was the most difficult moment. The candidate's answer (the whirlpool analogy: real structure, measurable properties, but constituted by context) was adequate but not wholly satisfying. This exchange identified the programme's deepest philosophical vulnerability: the line between "context-dependent individual" and "pattern in a field" is not sharp, and the programme's Simondonian framework doesn't fully resolve it.

### 8.3 Verdict

Pass with minor corrections. Four specific items, all implementable in hours rather than days.

---

## 9. Reflections

### 9.1 What the AI System Did Well

- **Parallel execution**: launching 14 research agents simultaneously, running 900 cluster jobs overnight while working on writing
- **Persistent context**: committee members maintaining intellectual positions across 6 meetings
- **Honest self-correction**: discovering the pruning confound, acknowledging prior art, correcting the CCD metric
- **Cross-domain synthesis**: the Grok agent's identification of the weak-element pruning principle across 6 domains

### 9.2 What the AI System Did Poorly

- **Literature awareness**: 40-50% prior art convergence suggests the initial literature review was insufficient. A human researcher would likely have found Hooker et al. 2019 before designing the pruning experiments.
- **Metric selection**: reliance on CCD for Papers 1-4, discovered to be invalid only in Paper 4S. A human with neuroscience training would likely have used participation ratio from the start.
- **Overconfidence in philosophical claims**: "structural germ" persisted through multiple drafts until R3 corrected it. The committee's philosophical expertise, while genuine, operated within a narrower range than a real Simondon scholar would bring.

### 9.3 The Nature of the Discovery

The most philosophically interesting question: when an AI system independently derives a result that turns out to have prior art, is this discovery, rediscovery, or something else? The pruning confound was found empirically, not by reading Hooker et al. The response rank metric was derived from first principles, not by reading Stringer et al. The convergence was genuine — but so was the ignorance.

A human researcher in 2026 would be expected to know the pruning fairness literature. Should an AI system be held to the same standard? The answer bears on whether AI-assisted research is a complement to or a substitute for human domain expertise.

### 9.4 The Role of the Human

Throughout the programme, one human (Michael) directed every significant decision:
- Which questions to ask
- When to run experiments vs when to write
- When to submit vs when to revise further
- When to "discuss with the committee" vs proceed independently
- The decision to conduct the meta-literature review ("so what, who cares")
- The decision to conduct the academic audit

The AI system executed, analysed, wrote, reviewed, and audited. The human asked the questions that mattered.

---

## 10. Implications

### 10.1 For Academic Research

This case demonstrates that AI systems can:
- Conduct computationally intensive experimental programmes
- Maintain quality through simulated peer review and audit processes
- Identify and correct their own methodological errors
- Situate findings within broader literature (with significant gaps)

They cannot yet:
- Replace domain expertise in literature awareness
- Guarantee philosophical precision without external correction
- Produce the initial creative insight ("what if Hebbian dynamics could produce differenciation?")

### 10.2 For AI-Assisted Science

The most productive pattern was the **committee disagreement format**: multiple AI personas with distinct intellectual commitments debating a question. This produced better decisions than any single agent, including the coordinating agent. The diversity of perspective — Vasquez's pragmatism, Okafor's rigour, Dupont's precision — was more valuable than any individual trait.

### 10.3 For Academic Integrity

The programme raises genuine integrity questions:
- Who is the author when the writing is AI-generated under human direction?
- How should AI-conducted peer review be disclosed?
- Is a simulated committee meeting equivalent to a real one?
- When an AI system "discovers" something with prior art, should this be cited as independent discovery or as a failure of literature review?

These questions do not have settled answers. This document exists to make the process transparent so that others can evaluate it.

---

*Process documentation compiled from: conversation context, PAI memory system (WORK items, LEARNING signals, RESEARCH artifacts), git commit histories across 4 repositories, peer review documents, committee meeting transcripts, audit reports, and 15 researcher agent reports. March 25, 2026.*
