"""Weight modularity metric.

Measures how much of the total weight mass is within assemblages
vs between them. 1.0 = perfectly modular, 0.5 = random.
"""

import numpy as np


def weight_modularity(weights, assemblages):
    """Compute within-assemblage weight mass / total weight mass.

    Parameters
    ----------
    weights : dict of (i, j) -> float
        Sparse weight dictionary.
    assemblages : list of sets
        Each set contains node indices for one assemblage.

    Returns
    -------
    float
        Modularity score in [0, 1]. Returns 0.0 if no weights.
    """
    if not weights or not assemblages:
        return 0.0

    node_to_asm = {}
    for asm_idx, nodes in enumerate(assemblages):
        for node in nodes:
            node_to_asm[node] = asm_idx

    within_mass = 0.0
    total_mass = 0.0

    for (i, j), w in weights.items():
        mass = abs(w)
        total_mass += mass
        asm_i = node_to_asm.get(i, -1)
        asm_j = node_to_asm.get(j, -1)
        if asm_i >= 0 and asm_i == asm_j:
            within_mass += mass

    if total_mass < 1e-12:
        return 0.0

    return within_mass / total_mass
