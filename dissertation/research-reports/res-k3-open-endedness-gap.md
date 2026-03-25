SUMMARY: Comprehensive literature research on why Hebbian substrates plateau at parametric differentiation and cannot achieve open-ended evolution or qualitative novelty, mapped against the Dark Forest programme's "productive fracture."

ANALYSIS:

## 1. MODES Framework -- Measuring Open-Ended Evolution

The MODES (Measurements of Open-Ended Dynamics in Evolving Systems) toolbox, published by Dolson et al. (2019) in *Artificial Life* 25(1):50, provides the consensus measurement framework for open-ended evolution. It operationalises four hallmarks:

- **Change potential**: the system continues to produce new states over time (non-stasis).
- **Novelty potential**: new states are genuinely novel, not recombinations of existing types.
- **Complexity potential**: the complexity of entities increases over time.
- **Ecological potential**: entities interact in ways that create new niches, which in turn drive further novelty.

**Direct relevance to the Dark Forest programme**: Your metaplastic substrate demonstrably achieves *change potential* (assemblages emerge, consolidate, differentiate their eta values) and limited *ecological potential* (critical period dynamics show that coupling after consolidation navigates rather than homogenises). But the programme's own finding -- that response rank tops out at 5.6 and all assemblages operate within the same Hebbian vocabulary -- maps precisely onto the MODES distinction between novelty-within-a-model (variation) and novelty-that-changes-the-model (innovation). Your substrate generates variation but not innovation in the MODES sense. The assemblages differ in parameter values but not in the class of operations they perform.

## 2. Architectural Features That Enable Qualitative Novelty

### Lenia (Chan, 2019)

Standard Lenia discovers 400+ species across 18 families, but with a critical constraint: each species exists only in a world governed by specific fixed update rule parameters. Creatures found in only a small subspace of parameter space, and different species cannot coexist in the same simulation because they require different global rules. This is the same structural problem your Dark Forest substrate faces -- the rule is uniform, so all assemblages are structural clones.

### Flow-Lenia (Plantec et al., 2023 -- ALIFE Best Paper)

Flow-Lenia makes two changes that directly address the productive fracture:

1. **Mass conservation**: prevents the "runaway reinforcement" problem (analogous to your self-sealing). Matter cannot be created or destroyed, so one assemblage cannot monopolise the substrate.
2. **Parameter localisation**: the update rule parameters are embedded *within* the CA dynamics themselves, becoming dynamic and spatially localised. Different cells carry different rules, which can mix at boundaries.

This is the architectural move your programme identifies as missing. Flow-Lenia's parameter localisation is structurally analogous to making the Hebbian learning rule itself a local, evolvable variable -- which is exactly what your metaplastic field attempts. The critical difference: in Flow-Lenia, the *kind* of rule can change (different kernel shapes, different growth functions), not just the *rate* parameter. Your metaplastic field localises eta (a scalar rate parameter) but the Hebbian update equation remains fixed. This is the precise gap between parametric and qualitative differenciation.

Recent work (2025, *Artificial Life* 31(2):228) confirms Flow-Lenia produces emergent evolutionary dynamics resembling allopatric speciation -- different localised rules diverge from a common ancestor, producing genuine qualitative novelty.

### Neural Cellular Automata (Mordvintsev et al., 2020)

Growing NCA replaces fixed CA rules with trainable neural networks, enabling morphogenesis and regeneration. But the training is external (backpropagation through time), not intrinsic. The NCA does not evolve new rules autonomously -- it learns them from an external objective. Recent limitations (2024-2025): strictly local information propagation, anisotropy problems, scalability issues, deterministic nature. NCA achieves self-organisation but not open-ended evolution because the rule space is explored by gradient descent toward a fixed target, not by intrinsic dynamics.

## 3. The Gap Between Self-Organisation and Evolution

This is the most theoretically rich question, and multiple lines converge on the same answer.

### Pattee & Sayama (2019): "Evolved Open-Endedness, Not Open-Ended Evolution"

The key distinction: open-endedness is not a property of the evolutionary mechanism itself but a *consequence* of evolved organisms creating new mechanisms. Self-organisation in a fixed-rule system reaches an attractor and stays there -- it produces structure but not innovation. Evolution creates organisms that *change the rules* by constructing new mechanisms (symbolic languages, genetic regulatory networks, immune systems). Open-endedness is evolved, not given.

This maps directly onto the Dark Forest finding: your Hebbian substrate self-organises into assemblages (individuation), but the assemblages cannot construct new mechanisms because the update rule is fixed. The metaplastic extension adds a second layer (eta variation) but the Hebbian equation itself is invariant. Pattee and Sayama's framework predicts exactly this plateau.

### Adams, Zenil, Davies & Walker (2017): Formal Proof That State-Dependent Rules Are Necessary

This is the closest thing to a formal proof in the literature. Published in *Scientific Reports* 7:997, Adams et al. provide:

- **Formal definitions**: Unbounded evolution = trajectories non-repeating within the expected Poincare recurrence time. Innovation = trajectories not reproducible by an isolated (fixed-rule) system.
- **Experimental test**: Three variants of CA with time-varying rules: (a) random rule changes, (b) periodic rule changes, (c) state-dependent rule changes.
- **Result**: Only state-dependent dynamics produces open-ended evolution in a scalable manner. Fixed rules and externally-driven rule changes (random, periodic) produce bounded dynamics.

The implication for Hebbian substrates is direct: a system where the update rule is fixed (even if parameters vary) will eventually exhaust its state space and plateau. The system's trajectory will repeat within the Poincare recurrence time because the rule constrains the accessible state space to a finite basin. State-dependent rules -- where the current state of the system modifies the rule governing the next state -- are necessary for unbounded novelty.

### Adams, Berner, Davies & Walker (2017): Physical Universality

The companion paper in *Entropy* 19(9):461 strengthens this: physical universality (the ability to reach any state from any other state) and open-ended dynamics both require state-dependent laws. A fixed-rule system, no matter how complex, has a fixed transition graph -- it can reach only those states accessible from its initial condition under that rule. State-dependent rules make the transition graph itself dynamic, opening paths that did not previously exist.

## 4. Theoretical Work on Necessary Conditions

### Banzhaf et al. (2016): Three-Level Taxonomy of Novelty

Published in *Theory in Biosciences* 135:131-161. The taxonomy is:

1. **Variation**: novelty within the current model (different parameter values, different spatial configurations). Your substrate produces this.
2. **Innovation**: novelty that changes the model (new types of interactions, new state variables). Your metaplastic extension partially approaches this by adding eta as a new state variable, but the Hebbian equation remains fixed.
3. **Emergence**: novelty that changes the meta-model (new levels of organisation, new kinds of entities). This is what your programme identifies as absent.

The paper argues that a sufficiently large search space is necessary but not sufficient. What matters is the *structure* of the space -- whether it admits transitions between qualitatively different regions.

### Soros & Stanley (2014, 2017): Four Necessary Conditions

Tested in the artificial world Chromaria:

1. Entities must interact with their environment (not just each other).
2. A minimal criterion must be met before reproduction (non-trivial selection).
3. The environment must support multiple ecological niches.
4. Entities must have the capacity to modify their environment (niche construction).

Your substrate satisfies (1) partially and (3) partially, but (2) and (4) are absent. There is no reproduction and no niche construction -- assemblages do not modify the rule space or create new niches for other assemblages.

### Taylor et al. (2019): Three Kinds of Open-Endedness

"Evolutionary Innovations and Where to Find Them" (*Artificial Life* 25(2):207-224) identifies:

1. **Exploratory**: variation within existing types. Your substrate achieves this.
2. **Expansive**: new types created through novel combinations of existing building blocks. Requires "transdomain bridges" -- mechanisms that connect different domains of behavior.
3. **Transformational**: new types that redefine the space of possibilities. Requires "non-additive compositional systems" where combining elements produces qualitatively new properties.

The critical insight: the factors enabling expansive and transformational open-endedness "relate not to the generic evolutionary properties of individuals and populations, but rather to the nature of the building blocks out of which individual organisms are constructed, and the laws and properties of the environment in which they exist." Your Hebbian building blocks (weights, activations, learning rates) are all continuous scalars updated by a fixed equation. There is no compositional structure that could produce qualitatively new operations from combinations of existing ones.

## 5. Is There a Formal Proof That Fixed-Rule Systems Cannot Produce Qualitative Novelty?

Not a single clean theorem, but a convergent argument from multiple directions:

**Adams et al. (2017)** provide the strongest formal result: in their CA experiments, only state-dependent rules produce unbounded evolution as formally defined (non-repeating trajectories beyond Poincare recurrence time). Fixed rules produce bounded dynamics by construction -- the transition function is a fixed map on a finite state space, so the trajectory must eventually repeat.

**The Poincare recurrence argument**: Any deterministic system with a fixed rule on a bounded state space has a finite number of states. By the pigeonhole principle, it must revisit a state, and from that point the trajectory repeats. A Hebbian substrate with hard weight bounds, bounded activations, and bounded eta operates on a bounded (though high-dimensional) state space with a fixed update rule. It will therefore plateau. The question is only whether the transient before recurrence is long enough to be observationally interesting -- which your programme shows it is (1000+ sessions of stable differentiation is a very long transient in a 400-node system).

**The key escape hatch**: State-dependent rules break the Poincare argument because the transition function itself changes. The state space is no longer fixed; new dimensions open as the rules change. This is why Flow-Lenia's parameter localisation matters -- it makes the rule a function of the state, not a fixed external constraint.

**What your programme demonstrates**: The metaplastic field localises a *parameter* (eta) but not the *form* of the rule (Hebbian correlation). This produces parametric differentiation (different values of eta across assemblages, F=4.9) but not qualitative differenciation (different kinds of learning rules). The "productive fracture" is precisely located at this boundary: the transition from variation to innovation in Banzhaf's taxonomy, from exploratory to expansive open-endedness in Taylor's framework, from bounded to unbounded dynamics in Adams et al.'s formalism.

ACTIONS:
- Read the full Dark Forest Paper 4 manuscript and response letter
- Read the metaplastic field implementation and metrics code
- Conducted 12 parallel web searches across the four research questions
- Cross-referenced findings against the programme's experimental results

RESULTS:

The literature converges on a single structural diagnosis: Hebbian substrates with fixed update rules cannot achieve qualitative novelty because the rule constrains the system to a bounded transition graph. The programme's metaplastic extension localises a parameter but not the rule form, producing parametric differentiation (variation in Banzhaf's terms) but not qualitative differenciation (innovation/emergence). Five independent theoretical frameworks (MODES, Banzhaf taxonomy, Adams et al. formalism, Soros-Stanley conditions, Taylor's three kinds) all locate the barrier at the same point: the transition from parameter variation to rule-form change.

STATUS: Research complete. All four questions addressed with primary literature from 2016-2025.

CAPTURE:
- Adams et al. 2017 (*Scientific Reports* 7:997): Only state-dependent rules produce OEE. The strongest formal argument against fixed-rule systems.
- Adams et al. 2017 (*Entropy* 19:461): Physical universality requires state-dependent laws.
- Banzhaf et al. 2016 (*Theory in Biosciences* 135:131): Three-level novelty taxonomy (variation/innovation/emergence). Paper 4 achieves variation only.
- Dolson et al. 2019 (*Artificial Life* 25(1):50): MODES metrics -- change, novelty, complexity, ecological potential.
- Plantec et al. 2023 (ALIFE Best Paper): Flow-Lenia parameter localisation is the architectural move that crosses from parametric to qualitative novelty in CA systems.
- Taylor et al. 2019 (*Artificial Life* 25(2):207): Exploratory/expansive/transformational OEE. Expansive requires "transdomain bridges."
- Pattee & Sayama 2019 (*Artificial Life* 25(1):4): Open-endedness is evolved, not given. Self-organisation plateaus because it cannot construct new mechanisms.
- Soros & Stanley 2014: Four necessary conditions for OEE including niche construction and minimal reproduction criterion.
- Lyle et al. 2024 (*Nature*): Loss of plasticity in deep networks -- Hebbian-like learning loses capacity to form new representations over time.
- Chan 2019 (*Complex Systems* 28(3)): Standard Lenia -- 400+ species but each requires specific global rules, preventing coexistence.

NEXT:
1. The programme could test whether making the *form* of the learning rule state-dependent (not just eta, but the update equation itself varying per assemblage) crosses the productive fracture.
2. Flow-Lenia's architecture provides a direct template: embed rule parameters as dynamic fields that evolve through the substrate's own dynamics, not just scalar rates but kernel shapes or nonlinearity types.
3. Adams et al.'s formal framework could be applied directly to the substrate: measure whether trajectories repeat within estimated Poincare recurrence time under current vs. state-dependent rules.
4. The Banzhaf taxonomy could structure Paper 5: explicitly map which level of novelty each experimental condition achieves.

STORY EXPLANATION:
1. The Dark Forest programme found Hebbian substrates produce individuation but not qualitative differenciation -- the "productive fracture."
2. MODES metrics (Dolson 2019) measure four hallmarks of open-ended evolution; the substrate achieves change potential but not novelty or complexity potential.
3. Banzhaf's taxonomy (2016) distinguishes variation, innovation, and emergence -- the substrate produces variation within a fixed model only.
4. Adams et al. (2017) formally demonstrated that only state-dependent rules produce unbounded evolution; fixed rules produce bounded dynamics by Poincare recurrence.
5. Flow-Lenia (Plantec 2023) shows the architectural solution: localise not just parameters but the rule form itself, making different cells carry different update equations.
6. Standard Lenia and Neural CA both plateau because their rules are globally fixed -- different spatial positions cannot develop qualitatively different dynamics.
7. Pattee and Sayama (2019) explain the mechanism: open-endedness must be evolved through organisms constructing new mechanisms, which fixed-rule substrates cannot do.
8. The productive fracture sits precisely at the boundary between parameter variation and rule-form change -- crossing it requires making the Hebbian equation itself a state-dependent variable.

COMPLETED: Fixed-rule Hebbian systems plateau because only state-dependent rules produce qualitative novelty.

Sources:
- [MODES Toolbox (Dolson et al. 2019)](https://direct.mit.edu/artl/article/25/1/50/2915/The-MODES-Toolbox-Measurements-of-Open-Ended)
- [Formal Definitions of Unbounded Evolution (Adams et al. 2017)](https://www.nature.com/articles/s41598-017-00810-8)
- [Physical Universality and State-Dependent Laws (Adams et al. 2017)](https://www.mdpi.com/1099-4300/19/9/461)
- [Defining Open-Ended Novelty (Banzhaf et al. 2016)](https://link.springer.com/article/10.1007/s12064-016-0229-7)
- [Flow-Lenia (Plantec et al. 2023)](https://arxiv.org/abs/2212.07906)
- [Flow-Lenia Emergent Evolutionary Dynamics (2025)](https://direct.mit.edu/artl/article/31/2/228/130572/Flow-Lenia-Emergent-Evolutionary-Dynamics-in-Mass)
- [Evolved Open-Endedness (Pattee & Sayama 2019)](https://direct.mit.edu/artl/article-abstract/25/1/4/2911/Evolved-Open-Endedness-Not-Open-Ended-Evolution)
- [Evolutionary Innovations (Taylor et al. 2019)](https://direct.mit.edu/artl/article/25/2/207/2924/Evolutionary-Innovations-and-Where-to-Find-Them)
- [Necessary Conditions for OEE (Soros & Stanley 2014)](https://www.semanticscholar.org/paper/Identifying-Necessary-Conditions-for-Open-Ended-the-Soros-Stanley/4671423a1b65f3e35dce603f8746e72ae31193dc)
- [Lenia (Chan 2019)](https://arxiv.org/abs/1812.05433)
- [Growing Neural Cellular Automata (Mordvintsev et al. 2020)](https://distill.pub/2020/growing-ca/)
- [Loss of Plasticity in Deep Networks (Lyle et al. 2024)](https://www.nature.com/articles/s41586-024-07711-7)
- [Open-Ended Evolution Encyclopedia](https://alife.org/encyclopedia/introduction/open-ended-evolution/)
