import numpy as np

def normalize_scores(scores) -> np.ndarray:
    """A normalizer made for the doc_scores (array)"""
    scores = np.array(scores, dtype=float)
    max_v = scores.max()
    min_v = scores.min()
    if max_v == min_v:
        # this is to avoid 0 division, return an array of same dimension of 1s
        return np.ones_like(scores)
    range_v = max_v - min_v

    return (scores - min_v) / range_v