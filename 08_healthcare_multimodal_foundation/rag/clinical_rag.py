"""Clinical RAG orchestration with evidence-first fallback behavior."""
from __future__ import annotations
from dataclasses import dataclass
from retrieval.vector_store import InMemoryVectorStore

@dataclass
class ClinicalRAGResponse:
    answer: str
    citations: list[str]
    confidence: float
    requires_clinician_review: bool

class ClinicalRAG:
    def __init__(self, store: InMemoryVectorStore, min_score: float = 0.25):
        self.store = store; self.min_score = min_score

    def answer(self, question: str, query_vector, patient_summary: str = "") -> ClinicalRAGResponse:
        hits = self.store.search(query_vector, top_k=3)
        supported = [h for h in hits if h.score >= self.min_score]
        if not supported:
            return ClinicalRAGResponse(
                answer="Insufficient retrieved evidence. Escalate to clinician review.",
                citations=[], confidence=0.0, requires_clinician_review=True)
        evidence = " ".join(h.text for h in supported)
        answer = f"Evidence-grounded summary for '{question}': {evidence}"
        confidence = sum(h.score for h in supported) / len(supported)
        return ClinicalRAGResponse(answer, [h.document_id for h in supported], confidence, confidence < 0.55)
