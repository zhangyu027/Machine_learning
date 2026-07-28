"""Dependency-light vector index with a FAISS-compatible conceptual interface."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class SearchResult:
    document_id: str
    score: float
    text: str
    metadata: dict

class InMemoryVectorStore:
    def __init__(self):
        self._ids: list[str] = []
        self._vectors: list[np.ndarray] = []
        self._texts: list[str] = []
        self._metadata: list[dict] = []

    def add(self, document_id: str, vector, text: str, metadata: dict | None = None):
        vector = np.asarray(vector, dtype=float)
        vector = vector / max(np.linalg.norm(vector), 1e-12)
        self._ids.append(document_id); self._vectors.append(vector)
        self._texts.append(text); self._metadata.append(metadata or {})

    def search(self, query_vector, top_k: int = 5, metadata_filter: dict | None = None) -> list[SearchResult]:
        if not self._vectors: return []
        q = np.asarray(query_vector, dtype=float); q = q / max(np.linalg.norm(q), 1e-12)
        scores = np.asarray(self._vectors) @ q
        candidates = []
        for i, score in enumerate(scores):
            if metadata_filter and any(self._metadata[i].get(k) != v for k, v in metadata_filter.items()):
                continue
            candidates.append(SearchResult(self._ids[i], float(score), self._texts[i], self._metadata[i]))
        return sorted(candidates, key=lambda r: r.score, reverse=True)[:top_k]
