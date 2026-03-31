# AI as Research Infrastructure
Michael Bean
2026-03-25

# How It Started

On March 13, 2026, Michael Bean started a conversation with GEN about
Liu Cixin’s Dark Forest hypothesis and Fermi’s paradox — whether
something like a dark forest could already exist in silica. The
conversation pivoted to what an AI not governed by human objectives
might look like: what dynamics would emerge if you removed optimisation,
fitness functions, and error signals entirely? Michael then brought in
Deleuze and asked how his work might connect, and things went from
there.

There was no research plan. The first git commit (00:17 AM) was titled
“Initial commit — Dark Forest in Silica project.” Within the same
session, GEN produced 609 lines of philosophical research on Deleuze’s
distinction between differentiation and differenciation. From this
emerged a prediction that shaped what followed: a Hebbian substrate
would achieve individuation (the emergence of distinct entities) but not
differenciation (the emergence of qualitatively different kinds).

The git log gives the timeline: multi-field substrate producing
assemblages at 16:43, the full pipeline running by 23:08, the first
paper through simulated committee review before midnight.[1]

# The Five Papers

## Paper 1: Individuation (March 13)

The first paper asked what pure Hebbian dynamics produce. The answer:
spontaneous assemblage formation from noise, governed by three regimes
(dissolution, productive, saturation) depending on the
learning-rate-to-decay ratio. In the multi-field substrate, multiple
assemblages formed transiently but converged to monopoly within 30
sessions.

The paper went through simulated peer review, committee discussion,
revision, and acceptance within a single day. The pace — committee
review, revision, acceptance before sunrise — makes sense only if you
think of it as removing every queue: no waiting for cluster allocation,
for co-authors to respond, for reviewers to find time.

## Paper 2: Coexistence (March 14)

The monopoly result in Paper 1 raised an immediate question: what
conditions permit stable coexistence? Michael’s intuition was that
spatial locality — how far nodes look when forming connections — would
be the controlling variable.

It was. A sharp phase transition at encounter locality ℓ ≈ 0.10–0.15
separated a coexistence regime (six to nine assemblages) from monopoly.
The result came from a 1,120-job parameter sweep on a newly configured
Ray cluster (three physical nodes, 68 CPUs). A coupling analysis
revealed that tight-locality assemblages coexist through niche
partitioning: each occupies a distinct spatial region with minimal
encounter overlap. Broad locality destroys this partition.

The head node ran on a home server, a second node on a workstation, and
the third on a laptop connected over WiFi. The laptop disconnected
repeatedly during overnight runs; Ray retried failed tasks on the
remaining nodes without intervention. This fault tolerance proved
essential for the rest of the programme.

## Paper 3: The Self-Sealing Barrier (March 15–16)

The assemblages from Papers 1 and 2 were structural clones — identical
internal organisation, differing only in where they sat on the grid. The
Deleuzian framework predicted this: without a mechanism to break
symmetry at the level of dynamics (not just position), the substrate
would produce bare repetition, not complex repetition.

Paper 3 tested every intervention available within the Hebbian
framework: temporal environmental variation, anti-Hebbian lateral
inhibition, and cross-assemblage edge injection at controlled weight
levels. Across 1,400 simulations, all failed. The substrate was
*self-sealing*: cross-assemblage edges decayed within 15 sessions
(median), and artificially maintained edges were co-opted into existing
assemblage structure rather than carrying a differentiation signal.

Nothing worked. The substrate was self-sealing, and breaking it would
require something outside the Hebbian framework.

## Paper 4: Metaplasticity (March 17–20)

The metaplastic mechanism in Paper 4 gave each node its own learning
rate, adjusted homeostatically toward the mean activity of neighbouring
nodes. The hypothesis was that this would create a Turing-like
instability at the metaplastic level, breaking the symmetry that
self-sealing preserves.

The Turing mechanism failed. Under hard *η* bounds, inhibitor coupling
was purely destructive. Under soft bounds, coupling was partially
rescued but inferior to a simpler mechanism: the local homeostatic
target itself, without any inter-assemblage communication, produced
stable differentiation.

This paper required the heaviest computation: 19 experiments, 6,070 jobs
over four days. Some were full parameter sweeps (the corrective
mechanism alone took 980 jobs); others were ten-job probes to snapshot a
single eta distribution. The cluster ran overnight; results were waiting
in Parquet files each morning.

Local homeostasis produced assemblages with response rank 5.6 (over five
independent functional dimensions) and eta divergence *F* = 4.9
(*p* \< 0.0001). But a late finding complicated the story: the baseline
(no metaplasticity) also reached rank 5.6 without pruning.
Metaplasticity stabilised and amplified diversity; it did not create it.

## Paper 4S: The Confound (March 20–25)

Paper 4S began as a methodological check. Michael started investigating
whether the choice of weight bounds influenced the results, then pushed
further into weight clipping. It became the programme’s most
consequential paper.

The answer was yes, but not in the way anyone expected. The weight clip
mattered, but the pruning threshold mattered more. Removing the standard
pruning threshold (10<sup>−4</sup>) reversed the ranking of weight
bounding strategies: soft bounds produced more assemblages than hard
bounds, not fewer. The interaction was disordinal — not a quantitative
shift but a qualitative reversal.

This discovery invalidated the primary metric (centroid cosine distance,
indistinguishable from a spatial null) and reframed every cross-bound
comparison in Papers 1–4. It also revealed that functional
differentiation was stronger than previously measured: response rank
increased from 1.0 to 5.6 without pruning.

The pruning confound was discovered empirically, not by reading the
literature. A subsequent literature review found that Hooker et al.
(2019) had established in 2019 that compressed deep networks
disproportionately lose rare-class capacity — a structurally analogous
finding in a different domain. The committee treated this convergence as
corroborating rather than undermining the result.

# The Tools

## GEN and PAI

GEN is the AI assistant that conducted the computational work, writing,
review, and analysis under Michael’s direction. GEN operates on PAI
(Personal AI Infrastructure) (Miessler 2024), a framework by Daniel
Miessler that extends Claude Code (Anthropic 2025) with agent
orchestration, persistent memory, skill routing, and structured
reasoning protocols. Claude Opus 4.6, with its one-million-token context
window, serves as the underlying model.

PAI’s agent system was central to the programme’s methodology. The
framework can spawn specialised sub-agents — Architect for system
design, CodexResearcher for technical work, Explore for codebase
analysis, and multiple researcher types (Claude, Gemini, Grok,
Perplexity) for literature search — each operating with its own context
but inheriting the base model. This enabled parallel committee meetings
(three agents debating simultaneously), parallel literature reviews
(fourteen agents searching five API backends), and the
coordinator-spawns-specialists pattern used in the academic audit.

PAI’s persistent memory preserved project context across conversation
sessions. Two philosophical research documents from the programme’s
first night — a synthesis of Gibson’s affordance theory with DeLanda’s
capacity concept, and a reading of Deleuze on differenciation — survived
in the memory system and informed experimental decisions days later.

## The Polyglot Pipeline

The choice of Quarto (Allaire et al. 2024) as the publishing system
reflected a practical constraint: the simulations are Python (numpy,
scipy, executed on the Ray cluster), while the statistical analysis and
publication figures are R (ggplot2, arrow, patchwork). Quarto renders
both in a single `.qmd` document, with R reading Python-generated
Parquet files directly via the `arrow` package. This avoided forcing
either language ecosystem to do work it does poorly.

Apache Parquet bridged the two. Python cluster jobs wrote typed,
columnar data files; R read them without parsing ambiguity. The full
experimental record (4.6 million observations) compressed to 40
megabytes.

Ray (Moritz et al. 2018) provided distributed computation. A three-node
cluster (68 CPUs: 32 on a workstation, 24 on a second node, 12 on the
head node) executed all simulation jobs. When the laptop node
disconnected — which happened during every overnight run — Ray retried
failed tasks automatically.

# The Simulated Academic Process

## Committee

Three AI personas served as the dissertation committee throughout the
programme. Each was instantiated from a written character description
and the accumulated transcripts of prior meetings. Each meeting was a
fresh agent invocation conditioned on this context, not a persistent
process with continuous memory.

The neuroscience persona did the most damage — its statistical demands
surfaced the pruning confound and killed the CCD metric, both of which
reshaped the programme. The chair kept pulling scope back (“the existing
results are sufficient”), which was annoying and usually right. The
philosopher caught terminology errors, the most consequential being
“structural germ” for what should have been “limit condition” — an error
that survived an embarrassing number of drafts.

The committee met five times across the programme. Its contribution was
structural: when members disagreed, the disagreement produced decisions
that no individual perspective would have reached. Whether the position
shifts across meetings constitute intellectual development or
context-matching is not clear from the transcripts alone.

## Peer Review

Each paper passed through simulated peer review: three AI reviewers with
distinct expertise profiles, an editorial decision, a response letter
with point-by-point replies, and revision. For Papers 4 and 4S, reviewer
concerns prompted additional experiments: 480 functional validation jobs
for Paper 4 (critical period and perturbation resilience measured on
response rank), and 900 revision jobs for Paper 4S (edge cap sensitivity
sweep, grid size generality, SVD threshold validation).

The review process identified errors the writing process had not. A
reviewer corrected the Simondonian terminology. Another identified a
potential confound in the edge cap replacement mechanism, prompting a
five-condition sweep that definitively resolved the concern (the cap
never activates; edges self-stabilise below any tested limit). A third
flagged that the critical period and perturbation resilience results
were measured only on a geometric metric, prompting the functional
validation experiments that produced some of the programme’s strongest
evidence.

The review process also produced errors. A proofreading agent
incorrectly flagged verified data as wrong. A reviewer confused
cross-paper references after reading both Papers 4 and 4S. Some
questions were answerable from the manuscript.

## The Literature Review

On the programme’s final day, Michael asked: “So what? Who cares?”

Fourteen research agents deployed simultaneously across five API
backends (Claude, Gemini, Grok, Perplexity, and domain-specific
contextualizers) produced the programme’s most clarifying finding:
approximately forty to fifty percent of major results had substantial
prior art. The pruning confound paralleled work in ML compression
fairness (Hooker et al. 2019). The response rank metric was standard in
systems neuroscience (Stringer et al. 2019). Emergent critical periods
had been demonstrated in deep networks (Achille, Rovere, and Soatto
2019). Self-sealing resembled autopoietic operational closure (Maturana
and Varela 1980). The impossibility of qualitative novelty under fixed
rules had been formally demonstrated (Adams et al. 2017).

A contrarian agent (Grok) verified the pruning-destroys-diversity
principle across six non-neural domains — metallurgy, ecology, market
economics, supply chain networks, and immune repertoire maintenance —
each with primary literature. A philosophy agent (Perplexity) identified
connections to 4E cognition, biosemiotics, and biological individuality
theory that the programme had not engaged.

The committee reframed the convergence: independent derivation from an
unrelated starting point constitutes evidence that the phenomena are
real. The findings without prior art — the disordinal interaction, the
non-monotonic steepness result, the critical threshold boundaries, the
grid-size scaling law — survived.

## The Audit

A coordinating agent executed a seven-phase academic integrity audit,
spawning sub-agents for citation verification, code-data consistency
checking, statistical method reproduction, internal consistency across
documents, philosophical terminology validation, reproducibility
tracing, and prose review.

The audit caught errors that multiple proofreading passes had missed: a
Shapiro-Wilk p-value reported as 0.40 (correct value: 0.99, from
different input data), a framing document with stale terminology and
outdated numbers, and a duplicated author name in a bibliography entry.
Three complete claim-to-data chains were traced from paper assertions
through R analysis scripts to Parquet data files to Python cluster job
scripts to substrate source code — all verified.

## The Defence

A simulated doctoral defence introduced two external examiner personas
(modelled on published researchers’ expertise profiles, not the actual
individuals). The most difficult exchange concerned whether self-sealing
assemblages constitute individuals or spatial patterns — a question the
Simondonian framework does not fully resolve. The verdict: pass with
four minor corrections (lattice topology limitations, operational
closure terminology clarification, lottery ticket hypothesis citation,
power analysis for the eta ANOVA).

# Capabilities and Limitations

The committee disagreement format was the biggest surprise. Each
member’s blind spots (the chair’s impatience with philosophy, the
neuroscientist’s scope creep, the philosopher’s indifference to
deadlines) got corrected by the others, producing decisions no single
perspective would have reached. Parallelism helped too: fourteen
literature agents running at once, cluster jobs overnight, a full
committee meeting in one invocation. And directed error-checking worked
— every major catch (pruning confound, CCD invalidity, the Shapiro-Wilk
miscalculation) came from Michael requesting a specific investigation
and the system executing it.

The biggest failure was literature awareness. The ML compression
fairness work (Hooker et al. 2019) would have saved weeks — anyone
trained in that area would have found it before designing the pruning
experiments, not after discovering the confound empirically. Same for
neural dimensionality (Stringer et al. 2019): response rank was derived
from scratch when it was already a standard tool. Centroid cosine
distance was the primary differentiation metric for four papers before a
permutation test killed it; participation ratio would have been the
obvious choice for anyone who had read the literature. And “structural
germ” persisted through several drafts — a Simondonian error a
specialist would have caught on day one.

# What the Human Did

Michael directed every strategic decision: which questions to ask, when
to run experiments or write, when to consult the committee, when to
challenge the results, and when to stop. Three decisions shaped the
programme more than any computational result:

1.  Testing the pruning threshold when the committee raised it, rather
    than dismissing it as a housekeeping parameter.
2.  Asking “so what, who cares?” — which triggered the fourteen-agent
    literature review.
3.  Writing up the process, not just the science.

# Integrity

Standard authorship frameworks do not handle this well. By ICMJE or
CRediT standards, the human qualifies as corresponding author —
conceptualisation and oversight. The AI’s contributions (writing,
analysis, review) do not fit any existing category. The simulated peer
review presents a disclosure challenge: editorial decisions, response
letters, and partial review transcripts are included in the repository,
but no consensus exists on how such processes should be reported.

The system had not read those sources — the git log confirms it. Whether
that counts as independent discovery or a literature review failure
depends on how generous you feel about AI systems.

This document was not the programme’s original intent. The science came
first; documenting the process was a late decision. As a result, the
record is incomplete. Many committee consultations — discussions about
journal submission readiness, how to weigh peer review concerns, whether
to extend the programme or stop — were not saved. The process
documentation in this repository was reconstructed from git history,
PAI’s persistent memory files, and the artifacts that happened to
survive in the working directory. Conversations that produced no
artifacts left no trace.

None of this has institutional standing. No journal submissions, no real
committee, no accredited defence. The experiments and data are real. The
academic scaffolding was simulated. The repository contains what
survived.

# References

Achille, Alessandro, Matteo Rovere, and Stefano Soatto. 2019. “Critical
Learning Periods in Deep Networks.” In *International Conference on
Learning Representations*.

Adams, Alyssa, Hector Zenil, Paul C. W. Davies, and Sara Imari Walker.
2017. “Formal Definitions of Unbounded Evolution and Innovation Reveal
Universal Mechanisms for Open-Ended Evolution in Dynamical Systems.”
*Scientific Reports* 7: 997.

Allaire, J. J., Charles Teague, Carlos Scheidegger, Yihui Xie, and
Christophe Dervieux. 2024. “Quarto: An Open-Source Scientific and
Technical Publishing System.” <https://quarto.org>.

Anthropic. 2025. “Claude Code.”
<https://docs.anthropic.com/en/docs/claude-code>.

Hooker, Sara, Aaron Courville, Gregory Clark, Yann Dauphin, and Andrea
Frome. 2019. “What Do Compressed Deep Neural Networks Forget?” *arXiv
Preprint arXiv:1911.05248*.

Maturana, Humberto R., and Francisco J. Varela. 1980. *Autopoiesis and
Cognition: The Realization of the Living*. Dordrecht: D. Reidel.

Miessler, Daniel. 2024. “Personal AI Infrastructure.”
<https://github.com/danielmiessler/Personal_AI_Infrastructure>.

Moritz, Philipp, Robert Nishihara, Stephanie Wang, Alexey Tumanov,
Richard Liaw, Eric Liang, Melih Elibol, et al. 2018. “Ray: A Distributed
Framework for Emerging AI Applications.” *OSDI*.

Stringer, Carsen, Marius Pachitariu, Nicholas Steinmetz, Matteo
Carandini, and Kenneth D. Harris. 2019. “High-Dimensional Geometry of
Population Responses in Visual Cortex.” *Nature* 571: 361–65.

[1] GEN drafted this document from git timestamps and artifacts. The
author’s experience of these sessions is not available to the system
writing this.
