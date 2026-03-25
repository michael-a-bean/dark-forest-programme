# Paper 5 Proposal: Topology Dependence of Self-Organised Differentiation

## Working Title

"Does the Dark Forest Have Roads? How Network Topology Governs Individuation, Coexistence, and Differentiation in Hebbian Substrates"

---

## Motivation

All experiments in the Dark Forest programme (Papers 1-4S) use regular 2D lattices with Euclidean locality. This is the programme's most significant limitation, identified by both the academic audit and the mock defence (Beer: "Write that topology paper next"). Three specific concerns:

1. The **coexistence-monopoly transition** is governed by encounter locality on a lattice. On scale-free graphs, high-degree hubs may connect everything, collapsing the locality parameter's meaning.

2. The **local homeostatic mechanism** regulates toward spatial neighbours' mean activity. On non-lattice topologies, "local" is defined by graph distance, not Euclidean distance. The mechanism's behaviour may change qualitatively.

3. The **pruning confound** removes weak edges regardless of topology. But soft-bounded equilibrium weights may differ on graphs with heterogeneous degree distributions, shifting the critical threshold.

## Research Questions

1. Does the coexistence-monopoly phase transition exist on non-lattice topologies?
2. Does self-sealing (operational closure) depend on lattice regularity?
3. Does local homeostatic metaplasticity produce functional differentiation on non-lattice graphs?
4. Is the pruning confound topology-dependent? Does the critical threshold (1e-6 to 1e-5) shift?
5. Is the hard clip still qualitatively irreducible on non-lattice topologies?

## Experimental Design

### Topologies to test

| Topology | Generator | Key property | Prediction |
|---|---|---|---|
| **2D lattice** (baseline) | Grid(n) | Regular, Euclidean | Known — Papers 1-4S |
| **Random geometric** | RGG(n, r) | Spatial but irregular | Similar to lattice with noise |
| **Small-world** | Watts-Strogatz(n, k, p) | Clustering + shortcuts | Shortcuts may break locality barrier |
| **Scale-free** | Barabási-Albert(n, m) | Hubs, power-law degree | Hubs may enforce monopoly |
| **Erdős-Rényi** | ER(n, p) | No spatial structure | Locality parameter meaningless |

### Experiments

**Exp 1: Coexistence sweep** — For each topology, sweep the locality parameter (or its topological analog: neighbourhood radius for RGG, rewiring probability for WS, preferential attachment degree for BA). Map the coexistence-monopoly transition. n=20 seeds × 5 topologies × 7 parameter values = 700 jobs.

**Exp 2: Self-sealing** — Replicate Paper 3's cross-assemblage edge injection on each topology. Does self-sealing occur? Is the timeline (14 sessions on lattice) topology-dependent? 5 topologies × 20 seeds = 100 jobs.

**Exp 3: Metaplastic differentiation** — Replicate Paper 4's local homeostatic mechanism on each topology. Measure response rank, eta divergence, critical period. 5 topologies × 4 conditions × 20 seeds = 400 jobs.

**Exp 4: Pruning confound** — Replicate Paper 4S's factorial (pruning on/off × bound type) on each topology. Is the disordinal interaction topology-dependent? 5 topologies × 3 bounds × 2 prune × 20 seeds = 600 jobs.

**Exp 5: Steepness sweep** — Replicate the non-monotonic steepness result on each topology. Does the dead zone (k=2-50) persist? 5 topologies × 7 k values × 20 seeds = 700 jobs.

**Total: ~2,500 jobs.** Feasible on the existing 68-CPU cluster in ~2-3 days.

### Implementation

The MultiField substrate needs one modification: replace the 2D grid position-based encounter mechanism with a graph-distance-based mechanism. Encounters are sampled from neighbours within graph distance r (instead of Euclidean distance σ). The `_local_encounter_pair()` method becomes topology-aware.

For the local homeostatic target, "spatial neighbours" becomes "graph neighbours within radius r" — a natural generalisation.

### Metrics

Same as Papers 4-4S: response rank (SVD, participation ratio), eta divergence (F-ratio), assemblage count, CCD (with spatial-null qualification), modularity.

## Predictions

| Finding | Lattice | RGG | Small-world | Scale-free | ER |
|---|---|---|---|---|---|
| Coexistence | Sharp transition | Similar | Shifted (shortcuts) | Monopoly dominant | No coexistence |
| Self-sealing | 14 sessions | Similar | Faster (shortcuts) | Very fast (hubs) | Instantaneous |
| Metaplastic diff. | Rank 5.6 | Similar | Reduced? | Low (hubs suppress) | Zero |
| Pruning confound | Disordinal | Similar | Disordinal | Unknown | Unknown |
| Hard clip irreducibility | Non-monotonic | Similar | Unknown | Unknown | Unknown |

The strongest prediction: **scale-free topology will suppress coexistence and differentiation** because hub nodes connect assemblages that would otherwise be isolated, enforcing the monopoly dynamic. This would confirm that the Dark Forest metaphor (isolation enables coexistence) is topology-dependent.

The most interesting prediction: **small-world topology may show a novel transition** where a few long-range shortcuts are constructive (enabling inter-assemblage communication after the critical period) but too many are destructive (enforcing monopoly before consolidation).

## Philosophical Framing

The topology question maps onto Simondon's concept of the **associated milieu**: the environment that co-individuates with the entity. On a lattice, the milieu is spatially local. On a scale-free graph, the milieu includes distant hub connections. The question becomes: what topological structure of the milieu permits transduction without homogenisation?

DeLanda's assemblage theory predicts that relations of exteriority (portable identity) should be more achievable on topologies where assemblages have more distinct connectivity profiles. Scale-free graphs, paradoxically, may produce stronger individuation (each node's neighbourhood is unique) but weaker coexistence (hubs enforce coupling).

## Target Venue

*Artificial Life* — consistent with the programme.

## Timeline

| Week | Activity |
|---|---|
| 1-2 | Implement topology-aware substrate, validate on lattice baseline |
| 3-4 | Run Exps 1-5 on cluster (~2,500 jobs) |
| 5-6 | Analysis and figures |
| 7-8 | Draft paper |
| 9-10 | Committee review, revision, submit |

## Relation to Dissertation

This paper directly addresses the lattice-specificity limitation identified in the defence. If results confirm topology-dependence, it strengthens the programme by showing which findings are universal (pruning confound?) and which are lattice-specific (coexistence transition?). If results show topology-independence, it dramatically strengthens the programme's generalisability.

Either outcome is publishable.
