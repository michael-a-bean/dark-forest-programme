"""Assemblage centroid cosine distance — robust differentiation metric.

Computes mean pairwise cosine distance between assemblage centroid weight vectors.
0.0 = identical assemblages (clones), 1.0 = orthogonal assemblages (maximally different).
"""

import numpy as np


def assemblage_centroid_vectors(weights, assemblages, n_nodes):
    """Compute centroid outgoing weight vector for each assemblage."""
    centroids = []
    for nodes in assemblages:
        node_list = sorted(nodes)
        if not node_list:
            continue
        vectors = np.zeros((len(node_list), n_nodes))
        for idx, node in enumerate(node_list):
            for j in range(n_nodes):
                if (node, j) in weights:
                    vectors[idx, j] = weights[(node, j)]
        centroids.append(np.mean(vectors, axis=0))
    return centroids


def centroid_cosine_distance(weights, assemblages, n_nodes):
    """Mean pairwise cosine distance between assemblage centroids.

    Parameters
    ----------
    weights : dict of (i, j) -> float
    assemblages : list of sets
    n_nodes : int

    Returns
    -------
    float
        Mean pairwise cosine distance. 0.0 = clones, 1.0 = orthogonal.
        Returns 0.0 if fewer than 2 assemblages.
    """
    if len(assemblages) < 2:
        return 0.0

    centroids = assemblage_centroid_vectors(weights, assemblages, n_nodes)
    if len(centroids) < 2:
        return 0.0

    distances = []
    for i in range(len(centroids)):
        for j in range(i + 1, len(centroids)):
            norm_i = np.linalg.norm(centroids[i])
            norm_j = np.linalg.norm(centroids[j])
            if norm_i < 1e-12 or norm_j < 1e-12:
                distances.append(1.0)
            else:
                cos_sim = np.dot(centroids[i], centroids[j]) / (norm_i * norm_j)
                distances.append(1.0 - cos_sim)

    return float(np.mean(distances))
