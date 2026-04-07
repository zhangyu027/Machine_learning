from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class GraphCache:
    embeddings: np.ndarray
    probabilities: np.ndarray
    rel_paths: list[str]

class SimpleKNNGraphRefiner:
    def __init__(self, k: int = 5, alpha: float = 0.7):
        self.k = k
        self.alpha = alpha
        self.cache: Optional[GraphCache] = None

    def fit(self, embeddings: np.ndarray, probabilities: np.ndarray, rel_paths: list[str]):
        self.cache = GraphCache(
            embeddings=np.asarray(embeddings, dtype=np.float32),
            probabilities=np.asarray(probabilities, dtype=np.float32),
            rel_paths=list(rel_paths),
        )

    def refine(self, query_embedding: np.ndarray, base_probability: np.ndarray) -> Dict[str, np.ndarray]:
        if self.cache is None or len(self.cache.embeddings) == 0:
            return {
                "final_probability": base_probability,
                "neighbor_probability": base_probability,
                "indices": np.array([], dtype=np.int64),
            }

        sims = cosine_similarity(query_embedding.reshape(1, -1), self.cache.embeddings).flatten()
        top_idx = np.argsort(sims)[::-1][: self.k]
        neighbor_prob = self.cache.probabilities[top_idx].mean(axis=0)
        final_prob = self.alpha * base_probability + (1.0 - self.alpha) * neighbor_prob
        return {
            "final_probability": final_prob,
            "neighbor_probability": neighbor_prob,
            "indices": top_idx,
        }
