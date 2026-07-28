"""Automated metrics for multimodal retrieval and grounded generation."""
from __future__ import annotations

def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    return float(bool(set(retrieved[:k]) & relevant)) if relevant else 0.0

def reciprocal_rank(retrieved: list[str], relevant: set[str]) -> float:
    for i, doc in enumerate(retrieved, 1):
        if doc in relevant: return 1.0 / i
    return 0.0

def citation_precision(citations: list[str], supporting: set[str]) -> float:
    return sum(c in supporting for c in citations) / len(citations) if citations else 0.0

def groundedness(answer_claims: list[str], supported_claims: set[str]) -> float:
    return sum(c in supported_claims for c in answer_claims) / len(answer_claims) if answer_claims else 0.0

def evaluate_cases(cases: list[dict]) -> dict:
    rows = []
    for c in cases:
        rows.append({
            "recall_at_5": recall_at_k(c["retrieved"], set(c["relevant"]), 5),
            "mrr": reciprocal_rank(c["retrieved"], set(c["relevant"])),
            "citation_precision": citation_precision(c["citations"], set(c["relevant"])),
            "groundedness": groundedness(c["answer_claims"], set(c["supported_claims"])),
        })
    return {k: sum(r[k] for r in rows)/len(rows) for k in rows[0]} if rows else {}
