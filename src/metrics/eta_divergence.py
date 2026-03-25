"""Eta divergence — learning rate divergence across assemblages.

Measures the variance of mean learning rate across assemblages.
0 = all assemblages have the same mean eta (homogeneous rules).
> 0 = assemblages have differentiated their learning dynamics.
"""

import numpy as np


def eta_divergence(node_eta, assemblages):
    """Variance of per-assemblage mean eta.

    Parameters
    ----------
    node_eta : np.ndarray
        Per-node learning rate array.
    assemblages : list of sets
        Each set contains node indices for one assemblage.

    Returns
    -------
    float
        Variance of assemblage-level mean etas. 0.0 if < 2 assemblages.
    """
    if len(assemblages) < 2:
        return 0.0

    asm_means = []
    for nodes in assemblages:
        node_list = sorted(nodes)
        if node_list:
            asm_means.append(np.mean(node_eta[node_list]))

    if len(asm_means) < 2:
        return 0.0

    return float(np.var(asm_means))
