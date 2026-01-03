import numpy as np
from typing import List

def compute_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:

    a = np.array(vec_a)
    b = np.array(vec_b)

    dot_product = np.dot(a, b)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))