# Defence Preparation — Five Hardest Questions

## Q1: "Hooker et al. showed in 2019 that pruning forgets rare classes. How is your finding different?"

**Answer (30 sec):** Hooker identified the *what* — disproportionate forgetting. Tran identified the *why* — gradient-norm asymmetry. Our contribution is threefold: (1) we show the interaction is *disordinal* — pruning doesn't just hurt some approaches more, it *reverses the ranking* — no prior work shows this; (2) we identify the precise critical threshold (1e-6 to 1e-5); (3) we demonstrate this in a self-organising substrate with no external training signal, where the weak connections ARE the differentiation mechanism, not noise obscuring pre-existing structure.

## Q2: "You use 'autopoiesis' and 'operational closure.' Isn't this just metaphor?"

**Answer (30 sec):** We use these as structural descriptors of measurable properties — self-reinforcing pathway dynamics and resistance to 50% perturbation — not as claims about meeting the full criteria for autopoietic organisation. We cite Beer (2020) explicitly to distinguish computational analogs from the full biological concept. The assemblages are operationally closed but not self-producing. The connection is structural, not metaphorical, and positioning it honestly within the autopoietic hierarchy (Maturana & Varela → Beer → Thompson) shows where the analogy holds and where it breaks down.

## Q3: "Your 'productive fracture' — isn't this just the open-endedness problem that Adams et al. (2017) already formalised?"

**Answer (30 sec):** Adams et al. proved that state-dependent rules are *necessary* for unbounded evolution. Our contribution is the *empirical demonstration* of where a specific substrate hits that boundary, and the *diagnosis* of what's missing. The productive fracture is not a theoretical prediction — it's a measured result (response rank 5.6, eta F=4.9, but no qualitative novelty) that we locate precisely within Adams' framework. We also identify the specific architectural change needed: making the update equation state-dependent, not just the learning rate parameter. This is the bridge from Adams' formalism to concrete substrate design.

## Q4: "Stringer et al. (2019, Nature) already use participation ratio. Tang et al. link dimensionality to memory. What does your eigenspectrum analysis add?"

**Answer (30 sec):** Stringer characterised the *healthy* spectrum in visual cortex. We characterise how *pruning deforms it*. Tang showed dimensionality predicts performance cross-sectionally. We show the *dynamical process* by which consolidation and pruning reduce dimensionality over time. The contribution is not the metric — we acknowledge this is a standard tool — but the result: that a self-organising Hebbian substrate independently arrives at the same dimensionality structure observed in cortex, and that pruning collapses it from 5.6 to 1.0. The convergence between our computational substrate and Stringer's biological measurements is itself evidence that the underlying phenomenon is real.

## Q5: "If 40-50% of your findings have prior art, what is the original contribution of this dissertation?"

**Answer (60 sec):** Three things are genuinely new. First, the *disordinal interaction* — pruning reverses the ranking of approaches. No prior work in any domain shows this. Second, the *hard clip irreducibility* — the non-monotonic steepness result, the critical threshold boundaries, the grid-size scaling law. These are specific quantitative results with no precedent. Third, the *philosophical architecture* — the Simondon-Deleuze-DeLanda diagnostic sequence that generates testable predictions (Turing failure under hard bounds, predicted; self-sealing as bare repetition, confirmed; productive fracture at the rule-space boundary, measured).

The convergent findings are not redundant — they validate the framework. A Hebbian substrate arriving at autopoiesis through Deleuzian diagnostics, at the same critical periods that emerge in deep networks, using the same dimensionality measures that characterise biological cortex — this convergence from an independent starting point is evidence that the philosophical framework identifies real structure, not artifacts of one methodology.

The dissertation is not "we discovered X." It is "we built a minimal substrate, derived predictions from a philosophical framework, tested them, and found that several results converge with established findings across neuroscience, ML, and complex systems — confirming the framework identifies real structure. Within that convergent landscape, we found specific interaction effects and quantitative boundaries that are genuinely new."
