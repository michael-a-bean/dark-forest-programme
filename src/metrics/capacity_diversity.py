"""Capacity diversity — functional profile clustering of assemblages.

Uses PCA on assemblage weight centroids, then k-means clustering with
silhouette scoring to find optimal k. Measures whether assemblages are
genuinely different kinds (k > 1) or just spatial clones (k = 1).
"""

import numpy as np
from .centroid_distance import assemblage_centroid_vectors


def capacity_diversity(weights, assemblages, n_nodes, max_k=None):
    """Optimal cluster count of assemblage functional profiles.

    Parameters
    ----------
    weights : dict of (i, j) -> float
    assemblages : list of sets
    n_nodes : int
    max_k : int, optional
        Maximum k to try. Defaults to len(assemblages).

    Returns
    -------
    int
        Optimal number of distinct functional profiles.
        1 = all assemblages are clones. > 1 = genuine diversity.
        Returns 0 if fewer than 2 assemblages.
    """
    if len(assemblages) < 2:
        return 0

    centroids = assemblage_centroid_vectors(weights, assemblages, n_nodes)
    if len(centroids) < 2:
        return 0

    X = np.array(centroids)

    # PCA to reduce dimensionality (keep 95% variance or min 2 components)
    from sklearn.decomposition import PCA
    n_components = min(X.shape[0], X.shape[1], 10)
    if n_components < 2:
        n_components = 2
    if n_components > X.shape[0]:
        n_components = X.shape[0]

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    # k-means with silhouette scoring
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    if max_k is None:
        max_k = len(assemblages)
    max_k = min(max_k, len(assemblages))

    if max_k < 2:
        return 1

    best_k = 1
    best_score = -1.0

    for k in range(2, max_k + 1):
        if k >= X_pca.shape[0]:
            break
        km = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = km.fit_predict(X_pca)
        # silhouette_score requires at least 2 distinct labels
        if len(set(labels)) < 2:
            continue
        score = silhouette_score(X_pca, labels)
        if score > best_score:
            best_score = score
            best_k = k

    return best_k
