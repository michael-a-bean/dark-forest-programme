---

## Dark Forest Programme: Broader Literature Connections

### 1. Morphogenesis and Turing Patterns

**What was known.** Muolo et al. (2024, *Proc. R. Soc. A*) consolidated a decade of work showing that Turing patterns on discrete topologies behave qualitatively differently from continuum reaction-diffusion: the Laplacian eigenspectrum of sparse graphs supports only low-mode instabilities, typically producing single-differentiated-node solutions (Wolfrum 2012) rather than distributed periodic patterns. Krause et al. (2024, *Bull. Math. Biol.*) proved that satisfying linear Turing instability conditions is *insufficient* for sustained nonlinear pattern formation -- transient patterns can collapse even when the instability criterion is met.

**What the programme adds.** The Dark Forest results provide a concrete empirical case confirming both theoretical predictions simultaneously: sparse, dynamically rewiring topology (point 1 of the Discussion) defeats distributed Turing patterns, and even where instability conditions are met (soft eta bounds, Exp 11), the resulting patterns are weak and dominated by a simpler local-homeostatic mechanism. The programme also extends the hard/soft bound distinction from synaptic weights (van Rossum et al. 2000) to the metaplastic level, showing that absorbing boundary states at the learning-rate level kill reaction-diffusion dynamics just as they do at the synaptic level.

**What was missed.** The programme did not engage with non-Turing morphogenetic mechanisms that could operate on the same substrate. Mechanochemical models where spatial deformation couples to chemical dynamics (Turing patterns on growing domains, Crampin et al. 1999; recent work by Krause et al. 2023 on growing-domain instabilities) bypass the fixed-topology problem entirely. If the grid itself could grow or deform in response to assemblage activity, Turing-like instabilities might succeed where static-grid Turing fails. Neural cellular automata (Mordvintsev et al. 2020, *Distill*) demonstrate that differentiable morphogenesis on grids can achieve regenerative target patterns via gradient descent -- a mechanism the programme never tested because the substrate is unsupervised. The programme also did not consider higher-order Turing patterns on simplicial complexes (Muolo et al. 2024), where hypergraph structure enables instabilities impossible on pairwise graphs.

### 2. Open-Ended Evolution and the Productive Fracture

**What was known.** The open-ended evolution (OEE) community distinguishes parametric variation within a fixed genotype-phenotype map from genuine novelty that expands the map itself (Banzhaf et al. 2016; Aguilar et al. 2014). The MODES toolbox (Dolson et al. 2019, *Artif. Life*) provides quantitative metrics: change potential, novelty potential, complexity potential, and ecological potential. Flow-Lenia (Plantec et al. 2023; 2025 *Artif. Life*) achieves a key architectural step toward OEE by localizing CA update-rule parameters within the creatures themselves, enabling portable individuality and inter-creature interaction under shared dynamics.

**What the programme adds.** The "productive fracture" is a precise characterization of where the substrate sits on the OEE spectrum: it achieves change potential (assemblages diverge) and ecological potential (coexistence), but zero novelty potential and zero complexity potential. All variation is parametric -- different values of eta and gain, never new update rules. The transplant result (Exp 19) sharpens this: even the parametric variation is context-dependent, not portable. This directly maps onto the OEE distinction between variation-within-map and map-expansion.

**What was missed.** The programme does not apply MODES metrics quantitatively. Running the MODES toolbox on assemblage time-series would yield a formal classification (bounded, class II, class III, etc.) that would make the "productive fracture" claim empirically grounded rather than qualitative. The programme also does not engage with Quality-Diversity algorithms (Mouret & Clune 2015; Leniabreeder, 2024) that use MAP-Elites to discover diverse Lenia creatures -- a methodology that could be applied to the Dark Forest substrate to search for conditions enabling novelty potential. The connection to neural cellular automata (Growing NCA, Mordvintsev et al. 2020) is also absent: NCAs achieve morphogenetic self-repair through gradient-based rule optimization, demonstrating that rule-space exploration *is* computationally achievable in grid substrates when you add a training signal.

### 3. Autopoiesis and Operational Closure

**What was known.** Maturana and Varela (1972/1980) defined autopoiesis as a system that continuously produces the components constituting it, creating an operationally closed boundary. Beer (2020, *Adapt. Behav.*) revisited autopoiesis in the Game of Life ("Bittorio"), showing that even minimal CA structures can exhibit structural coupling with their environment. The enactivist tradition (Thompson 2007; Barandiaran 2017, *Topoi*) extends operational closure to define minimal cognition as sense-making by autonomous agents.

**What the programme adds.** Self-sealing assemblages *are* operationally closed systems in precisely the autopoietic sense: they continuously regenerate their own boundary (Hebbian reinforcement of internal edges, pruning of external ones), and perturbation experiments (Exp 9) confirm they resist disruption up to 50% scramble. The programme provides a quantitative demonstration of autopoietic closure emerging spontaneously from Hebbian dynamics without being designed in -- something the theoretical autopoiesis literature discusses but rarely demonstrates computationally outside of toy models.

**What was missed.** The programme never uses the word "autopoiesis" or makes this connection explicit. More critically, it does not ask whether assemblages exhibit *cognition* in the enactivist minimal sense -- adaptive modulation of coupling with the environment based on significance for self-maintenance. The perturbation-response experiments (Exp 9, 12, 17) test resilience but not adaptive response -- does a perturbed assemblage *change its behavior* in functionally relevant ways, or merely return to its prior attractor? The distinction between attractor stability and adaptive sense-making is precisely what the enactivist literature cares about, and the programme has the data to test it.

### 4. Developmental Biology: Critical Periods and Canalization

**What was known.** Waddington's epigenetic landscape (1957) formalized canalization: developmental trajectories become increasingly constrained, funneling into stable cell fates. Recent computational work reconstructs these landscapes quantitatively (Rand et al. 2021, *Cell Syst.*; Evoscape, PNAS 2025). In neuroscience, critical periods are windows where experience shapes circuit structure, after which plasticity declines and existing structure becomes resistant to change (Hensch 2005). The BCM theory (Bienenstock et al. 1982) provides a Hebbian account of critical period dynamics through sliding thresholds.

**What the programme adds.** The critical period finding (Exp 8) -- coupling before consolidation destroys diversity, coupling after preserves it -- is a computational demonstration of canalization in a non-biological substrate. The three regimes (topological, structural, metaplastic individuation) map onto Waddington's progressive valley-deepening: early plasticity allows multiple outcomes, late intervention cannot reshape carved basins. The metaplastic mechanism is essentially a BCM-like sliding threshold operating at the assemblage level rather than the single-neuron level.

**What was missed.** The programme does not connect to the substantial literature on *de-differentiation* and *reprogramming*. Biological systems can reset critical periods (Bhatt & bhalla cortical experiments; Yamanaka factors in cell biology). Can the substrate's canalization be reversed? The perturbation experiments test resilience, not reversibility of differentiation. A "reprogramming" experiment -- resetting all eta values to baseline after differentiation and testing whether the same or different assemblage patterns re-emerge -- would directly test whether canalization in this substrate is reversible or permanent, connecting to the Waddington landscape literature on the depth and shape of attractor basins.

### 5. Collective Intelligence and Swarm Systems

**What was known.** Swarm intelligence research (Bonabeau et al. 1999; recent review by Tan & Zheng 2023, *Nat. Sci. Rev.*) demonstrates that collective behavior emerges from local interactions through stigmergy -- indirect communication via environmental modification. Key features include decentralized control, positive feedback loops, and threshold-based recruitment.

**What the programme adds.** Assemblages exhibit collective behavior through pure Hebbian reinforcement -- a form of weight-mediated stigmergy where each node's activity modifies connection strengths that then influence neighboring nodes. The locality parameter controlling coexistence vs. monopoly (Papers 1-2) directly parallels the interaction radius in swarm models: local interactions enable diverse collectives, global interactions produce consensus (monopoly).

**What was missed.** The programme does not test whether assemblages can perform collective computation -- decision-making, signal processing, or information integration that goes beyond individual node dynamics. Swarm intelligence research asks what collectives *can do* that individuals cannot. The functional probe (Exp 12) measures signal amplification, but not whether assemblages can solve problems, classify inputs, or coordinate responses in ways that exploit their collective structure. Testing assemblage-level computation (e.g., can different assemblages learn different input-output mappings?) would bridge to the collective intelligence literature.

### 6. Artificial Chemistry and Organization Theory

**What was known.** Chemical Organization Theory (Dittrich & Fenizio 2007) defines organizations as *closed and self-maintaining* sets of molecular species -- where closure means all products of reactions among set members are themselves members, and self-maintenance means all members can be produced from existing members. Mathis et al. (2024, *Chaos*) revisited AlChemy (Fontana & Buss 1994), finding that complex stable organizations emerge more frequently than expected but *cannot be easily combined into higher-order entities*.

**What the programme adds.** Assemblages satisfy the COT definition of organization: they are closed (self-sealing eliminates external connections) and self-maintaining (Hebbian reinforcement regenerates internal structure). The finding that assemblages cannot differentiate -- producing structural clones -- precisely parallels the AlChemy 2024 result that organizations "cannot be easily combined into higher-order entities." Both systems achieve organizational closure but fail to compose into hierarchically novel structures. The metaplastic mechanism that breaks this barrier (local homeostasis) could be understood in COT terms as introducing a *catalytic environment* that differentially modulates reaction rates (learning rates) based on organizational context.

**What was missed.** The programme does not formalize weight dynamics as a reaction network or apply COT analysis tools. Mapping the Hebbian update rule, pruning, and edge creation as "reactions" in a formal artificial chemistry would enable rigorous comparison with AlChemy and identification of precisely which organizational properties (closure types, self-maintenance modes) assemblages possess. The COT framework could also formalize the self-sealing barrier: assemblages achieve *reflexive closure* (all products remain internal) but not *generative closure* (ability to produce new reaction types).

### 7. Information Theory of Emergence

**What was known.** Hoel (2025, *Causal Emergence 2.0*) introduced a framework for quantifying emergent complexity across scales, measuring how widely distributed a system's causal workings are across macro and micro levels. IIT 4.0 (Tononi et al. 2023) formalized integrated information (phi) as a measure of irreducible cause-effect power. Rosas et al. (2024) developed partial information decomposition approaches to quantify synergistic and redundant information in complex systems.

**What the programme adds.** The response rank metric (SVD of perturbation-response matrix) is already an information-theoretic measure of functional dimensionality -- how many independent modes of response the system supports. Rank = 1 means purely redundant information across assemblages; rank > 1 means synergistic information that cannot be reduced to any single assemblage's response.

**What was missed.** The programme does not compute phi, effective information, or causal emergence measures. These would answer whether assemblages are "emergent" by formal criteria -- does the assemblage level have higher effective information than the node level? Does coarse-graining nodes into assemblages increase causal determinism? The Causal Emergence 2.0 framework could classify the substrate as causally "top-heavy" (assemblage level more causally informative) or "bottom-heavy" (node level sufficient). Given that the transplant result shows assemblage identity is spatially determined, one might predict the system is bottom-heavy: the node-level spatial context is causally primary, and assemblage-level descriptions are redundant summaries. Testing this would be a striking result either way.

### 8. Digital Organisms: Avida and Tierra

**What was known.** Avida (Ofria & Wilke 2004) and Tierra (Ray 1992) are the canonical digital evolution platforms. Avida gives each organism a private memory space and virtual CPU, enabling evolution of novel computational strategies (logic operations) through mutation. Despite this, even Avida eventually reaches evolutionary plateaus where novelty ceases (Channon 2019). The key architectural features enabling *partial* open-endedness are: (a) a Turing-complete instruction set allowing unbounded behavioral complexity, (b) resource-mediated environmental feedback creating ecological niches, (c) mutation operators that can produce qualitatively new instruction sequences, and (d) competitive exclusion driving arms races.

**What the programme adds.** The Dark Forest substrate lacks all four features. (a) The Hebbian update rule is parametrically variable but not Turing-complete -- there is no instruction set to mutate. (b) Energy sources create spatial structure but not functional niches. (c) There are no mutation operators; variation arises only through the interaction of deterministic dynamics with initial noise. (d) Assemblages compete for space but not for functionally differentiated resources. The "productive fracture" diagnosis is confirmed by comparison: Avida achieves OEE (temporarily) because organisms carry their own instructions; assemblages cannot carry anything.

**What was missed.** The comparison is stated in the paper's conclusion (connecting to Plantec 2023 on Flow-Lenia parameter localization) but not developed with respect to Avida/Tierra specifically. The programme does not ask: what minimal modification to the substrate would enable instruction-carrying? If each assemblage could modify not just its eta values but its *update rule* -- e.g., locally switching between Hebbian and anti-Hebbian learning, or developing inhibitory connections with distinct dynamics -- this would be the substrate equivalent of Avida's instruction-set mutations. The programme identifies "rule-space expansion" as the next frontier but does not prototype it. Even a proof-of-concept where assemblages can toggle between two pre-defined update rules based on local conditions would test whether rule-carrying enables genuine differenciation.

---

### Summary of Missed Connections

The most significant gaps, ranked by potential impact on the programme's theoretical contribution:

1. **Autopoiesis/operational closure** -- the self-sealing property IS autopoietic closure, and naming it so connects the programme to a 50-year theoretical tradition. This is essentially free.
2. **MODES metrics** -- running formal OEE measures on the substrate would convert the qualitative "productive fracture" into a quantitative classification. Moderate implementation effort, high theoretical payoff.
3. **Causal emergence** -- applying Hoel's CE 2.0 to test whether assemblage-level descriptions are causally emergent would directly address whether these are "real" macro-entities or mere summaries.
4. **COT formalization** -- mapping weight dynamics as reactions in an artificial chemistry framework would connect to the AlChemy 2024 revival and provide rigorous organizational analysis.
5. **Non-Turing morphogenesis** -- growing-domain instabilities and higher-order (simplicial) Turing patterns are architecturally compatible with the substrate but untested.

Sources:
- [Turing patterns on discrete topologies (Muolo et al. 2024)](https://royalsocietypublishing.org/doi/10.1098/rspa.2024.0235)
- [Flow-Lenia: Emergent Evolutionary Dynamics (2025)](https://direct.mit.edu/artl/article/31/2/228/130572/Flow-Lenia-Emergent-Evolutionary-Dynamics-in-Mass)
- [Toward Artificial Open-Ended Evolution within Lenia (2024)](https://arxiv.org/html/2406.04235v1)
- [Self-Organization in Computation & Chemistry: Return to AlChemy (2024)](https://arxiv.org/abs/2408.12137)
- [Causal Emergence 2.0: Quantifying Emergent Complexity (2025)](https://arxiv.org/abs/2503.13395)
- [Growing Neural Cellular Automata (Mordvintsev et al. 2020)](https://distill.pub/2020/growing-ca/)
- [Bittorio Revisited: Structural Coupling in Game of Life (Beer 2020)](https://journals.sagepub.com/doi/abs/10.1177/1059712319859907)
- [Chemical Organization Theory as General Framework (2024)](https://www.mdpi.com/2079-8954/12/4/111)
- [MODES Toolbox (Dolson et al. 2019)](https://direct.mit.edu/artl/article/25/1/50/2915/The-MODES-Toolbox-Measurements-of-Open-Ended)
- [IIT 4.0 (Tononi et al. 2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10581496/)
- [Emergence and Causality Survey (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10887681/)
- [Turing Instabilities Are Not Enough (Krause et al. 2024)](https://link.springer.com/article/10.1007/s11538-024-01386-z)
- [Beyond Metaphor: Quantitative Waddington Landscapes (2025)](https://academic.oup.com/bib/article/26/6/bbaf661/8376798)
- [From Animal Collective Behaviors to Swarm Robotics (2023)](https://academic.oup.com/nsr/article/10/5/nwad040/7043485)
- [Optimal Network Sizes for Turing Patterns (2025)](https://www.nature.com/articles/s41598-025-86854-7)
