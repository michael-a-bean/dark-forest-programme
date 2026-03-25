# Dark Forest Programme: Literature Connections Report

**Prepared by Ava Sterling | 2026-03-25**

---

## 1. Network Science: Coexistence-Monopoly as a Percolation Phase Transition

**What was known.** The coexistence-to-monopoly transition governed by encounter locality maps directly onto percolation theory. Li et al. (2021) provide a comprehensive review showing that clustered networks have larger percolation thresholds because clustering reinforces the core at the expense of global connections (DOI: 10.1016/j.physrep.2020.12.003). In ecological network models, the competitive exclusion principle (Gause's law) predicts that species sharing a limiting resource cannot coexist indefinitely — the stronger competitor monopolizes. Hardin explicitly drew the parallel between ecological competitive exclusion and economic monopoly. Johnson & Bronstein (2019) showed that spatial heterogeneity and mutualistic interactions can prevent exclusion, creating coexistence regimes with sharp transition boundaries (DOI: 10.1002/ecy.2708).

**What you add.** The Dark Forest programme demonstrates that encounter locality — effectively a spatial interaction radius — governs a sharp phase transition between assemblage coexistence and monopoly on a 2D lattice. This is a concrete computational realization of competitive exclusion operating through Hebbian dynamics rather than resource competition. The "Dark Forest" metaphor itself captures something the ecological literature has theorized but rarely demonstrated in neural substrates: that spatial isolation is the mechanism preserving coexistence, and that increasing interaction range triggers monopoly through a percolation-like threshold.

**What was missed.** The programme should explicitly cite neuropercolation theory (Kozma & Puljic, Scholarpedia), which extends percolation phase transitions to neural populations on lattices — precisely the substrate architecture used here. The community detection literature on modularity optimization (Newman, 2006) would formalize why self-sealing produces high-modularity structures. Additionally, the 2025 paper on network structure influencing self-organized criticality in neural networks with dynamical synapses (Frontiers in Systems Neuroscience, 2025) directly examines how lattice vs. small-world vs. scale-free topologies affect critical dynamics — relevant to predicting how Dark Forest results would change on different substrates.

---

## 2. Reservoir Computing: Assemblages as a Physical Reservoir

**What was known.** Echo state networks require the "separation property" — distinct inputs must produce distinct internal states — and the "echo state property" — initial conditions must wash out (Jaeger, 2001). Recent work shows that multi-layered reservoirs diversify temporal representations, with entropy of recurrent unit activations measuring representational richness (Gallicchio & Micheli, 2017). The ESN-GA-SRG framework (2023) explicitly optimizes the separation ratio as a topology-selection criterion (DOI: 10.1016/j.eswa.2023.120440).

**What you add.** The response rank metric (5.6 independent functional dimensions) is essentially measuring the separation property of a self-organized reservoir. The assemblages function as a spatially partitioned reservoir where each partition develops distinct dynamics through metaplastic differentiation. This is a reservoir that builds itself through Hebbian self-organization rather than random initialization — a significant conceptual advance. The perturbation-response matrix protocol is a novel method for quantifying reservoir quality.

**What was missed.** The liquid state machine framework (Maass et al., 2002) is perhaps even more relevant than ESNs because LSMs explicitly use spatial structure and local connectivity — matching the Dark Forest substrate architecture. The "edge of chaos" literature in reservoir computing (Bertschinger & Natschlager, 2004) would contextualize whether the coexistence regime corresponds to optimal reservoir computation. The programme should test whether assemblage outputs can actually be read out linearly to solve benchmark tasks — this would validate the reservoir interpretation quantitatively.

---

## 3. Graph Neural Networks: Weight Dynamics as Learned Message Passing

**What was known.** Message-passing neural networks (MPNNs) aggregate information from local neighborhoods, with graph attention networks (GATs) learning weighted aggregation. Recent work on RANGE (Nature Communications, 2026) shows that attention-based aggregation with positional encodings reduces oversquashing (DOI: 10.1038/s41467-026-69715-3). Spatio-temporal GNNs (STGCN, MTGNN) combine spatial graph convolution with temporal dynamics.

**What you add.** The Hebbian weight dynamics on the spatial graph implement a form of unsupervised, self-organizing message passing where edge weights are learned through local correlation rather than backpropagation. The locality parameter functions as an attention radius. Self-sealing is analogous to the oversmoothing problem in deep GNNs — but here it is a feature (producing distinct communities) rather than a bug.

**What was missed.** The connection to graph rewiring methods is unexplored. Recent work on dynamic graph construction (adaptive adjacency matrices in MTGNN) parallels how Hebbian dynamics effectively rewire the substrate. The programme could frame self-sealing as a natural solution to the oversquashing problem — assemblages prevent information from diffusing across the entire graph.

---

## 4. Synaptic Pruning: The Confound as a Novel Contribution

**What was known.** Chechik et al. (1998) showed that under metabolic energy constraints, memory performance is maximized by overgrowth followed by "minimal-value" pruning — removing the weakest synapses first. Navlakha et al. (2015) demonstrated that decreasing-rate pruning produces efficient, robust distributed networks. Concurrence of form and function in developing networks (Navlakha et al., 2018; DOI: 10.1038/s41467-018-04537-6) showed that pruning improves network efficiency. A 2025 paper frames synaptic pruning as a biological inspiration for deep learning regularization (arXiv: 2508.09330).

**What you add.** The pruning confound — that weight threshold pruning (1e-4) interacts disordinally with weight bounding strategy and destroys functional diversity by eliminating weak exploratory connections — is a genuinely novel finding. The existing literature uniformly treats pruning as beneficial (improving efficiency, regularization, robustness). The Dark Forest result shows that pruning can be catastrophic for functional diversity because it removes the low-weight exploratory connections that enable metaplastic differentiation. This effect amplifying with scale is particularly important.

**What was missed.** The programme should engage with the lottery ticket hypothesis (Frankle & Carlin, 2019), which argues that sparse subnetworks within dense networks can match full-network performance. The Dark Forest finding is essentially a counter-example: the "losing tickets" (weak connections) are functionally necessary for differentiation. The connection to the "silent synapse" literature in neuroscience (Bhatt et al., 2009) — where apparently inactive synapses serve developmental functions — would strengthen the biological interpretation.

---

## 5. Bond Percolation: Pruning Threshold as Critical Transition

**What was known.** Removing edges below a weight threshold is formally equivalent to bond percolation. A December 2025 paper (arXiv: 2512.13853) explicitly connects dropout/dropconnect in neural networks to percolation theory, characterizing the relationship between network topology and connectivity under random edge removal. Network robustness research shows that bond percolation thresholds predict the critical point at which network structure undergoes catastrophic change.

**What you add.** The 1e-4 pruning threshold likely corresponds to a bond percolation critical point on the 2D lattice substrate. Below this threshold, weak inter-assemblage connections are removed, fragmenting the network into isolated modules. The disordinal interaction with weight bounding suggests that the percolation threshold itself depends on the weight distribution, which hard clipping vs. soft saturation shapes differently.

**What was missed.** The programme should compute the actual percolation threshold for its substrate and compare with the pruning threshold. Weighted percolation theory (Barrat et al., 2004) provides the formal framework. The connection to "explosive percolation" (Achlioptas et al., 2009) — where competitive edge addition produces discontinuous transitions — may explain the sharpness of the diversity collapse.

---

## 6. Statistical Mechanics: Phase Transitions and Hopfield Connections

**What was known.** Classical Hopfield networks exhibit phase transitions between retrieval and non-retrieval states governed by temperature and memory load. Modern Hopfield networks (Ramsauer et al., 2020) achieve exponential memory capacity through stronger nonlinearities. Phase diagrams show coexistence regions where multiple retrieval states are simultaneously stable. A 2023 study examines storage and learning phase transitions in random-features Hopfield models (arXiv: 2303.16880).

**What you add.** The three regimes (Topological, Structural, Metaplastic) map onto distinct phases in a statistical mechanical sense. The hard clip creates an absorbing boundary that is qualitatively distinct from smooth saturation — this parallels first-order vs. continuous phase transitions. The non-monotonic steepness curve suggests a re-entrant phase boundary.

**What was missed.** The Boltzmann machine literature on learning with bounded weights (Ackley et al., 1985) directly addresses weight saturation effects. The spin glass literature (Mezard et al., 1987) provides formal tools for analyzing the metastable states that assemblages represent. The programme should compute entropy and specific heat analogs to determine whether regime transitions are first-order or continuous.

---

## 7. Topology Dependence: Lattice Specificity and Generalization

**What was known.** Hebbian learning can transform regular lattices into small-world networks through synchronization-based rewiring. Orlandi et al. (2022, eLife; DOI: 10.7554/eLife.74921) showed that in vitro neuronal assemblies self-organize into complex network topologies. The 2025 Frontiers paper demonstrates that network structure (random, small-world, modular, scale-free) directly influences whether neural avalanches follow power-law distributions.

**What you add.** The programme uses a regular 2D lattice, and the coexistence-monopoly transition is likely lattice-specific. On small-world networks, the additional long-range connections would shift the percolation threshold, potentially eliminating the coexistence regime entirely. On scale-free networks, hub nodes might resist self-sealing.

**What was missed.** This is the largest gap. The programme should systematically test Watts-Strogatz (small-world), Barabasi-Albert (scale-free), and Erdos-Renyi (random) substrates. The prediction is clear: increasing small-world rewiring probability should smoothly destroy coexistence, producing a testable connection to the network science literature.

---

## 8. Self-Organized Criticality: Is Coexistence Critical?

**What was known.** Neural systems at criticality exhibit power-law avalanche size distributions with exponent approximately -3/2 (Beggs & Plenz, 2003). Dynamical synapses can drive networks toward criticality (Levina et al., 2007; DOI: 10.1038/nphys758). The 2015 finding that SOC in cortical assemblies occurs in concurrent scale-free and small-world networks (DOI: 10.1371/journal.pone.0129372) is directly relevant.

**What you add.** The coexistence regime may sit near a critical point between the ordered (monopoly) and disordered (no assemblages) phases. The metaplastic mechanism with local homeostasis could function as a self-tuning mechanism driving the system toward criticality.

**What was missed.** The programme has not measured avalanche size distributions, inter-event interval distributions, or branching ratios — the standard signatures of criticality. Computing these for the coexistence regime would either confirm or rule out the SOC interpretation. If assemblage sizes follow a power law, it would connect the Dark Forest dynamics to a deep body of criticality literature.

---

## Summary of Priorities

The three most impactful missed connections, ranked by potential contribution to the programme:

1. **Topology dependence** (Section 7) — testing on non-lattice substrates would massively expand the generality claims and connect to the broadest literature.
2. **Reservoir computing validation** (Section 2) — demonstrating that assemblages can solve benchmark tasks via linear readout would open an entirely new application domain.
3. **Criticality measurements** (Section 8) — computing avalanche statistics would either connect the programme to SOC or definitively distinguish it, either of which is publishable.

Sources:
- [Percolation on complex networks (Li et al., 2021)](https://arxiv.org/abs/2101.11761)
- [Coexistence and competitive exclusion in mutualism (Johnson & Bronstein, 2019)](https://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecy.2708)
- [Self-organization of in vitro neuronal assemblies (Orlandi et al., 2022)](https://elifesciences.org/articles/74921)
- [Concurrence of form and function in developing networks (Navlakha et al., 2018)](https://www.nature.com/articles/s41467-018-04537-6)
- [Dropout as percolation (2025)](https://arxiv.org/abs/2512.13853)
- [Storage and learning phase transitions in Hopfield models (2023)](https://arxiv.org/abs/2303.16880)
- [Dynamical synapses causing SOC (Levina et al., 2007)](https://www.nature.com/articles/nphys758)
- [Network structure influences SOC (2025)](https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2025.1590743/full)
- [Extending GNN range with global encodings (2026)](https://www.nature.com/articles/s41467-026-69715-3)
- [Synaptic pruning as biological inspiration for DL regularization (2025)](https://arxiv.org/html/2508.09330v1)
- [Homeostatic synaptic plasticity as metaplasticity (2019)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6361678/)
- [SOC in cortical assemblies (2015)](https://pubmed.ncbi.nlm.nih.gov/26030608/)
- [Neural assemblies via generative modeling (2023)](https://elifesciences.org/articles/83139)
- [Emergence of spontaneous assembly activity (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6161857/)
- [Neuropercolation (Kozma & Puljic)](http://www.scholarpedia.org/article/Neuropercolation)
