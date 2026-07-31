"""Automated metrics for multimodal retrieval and grounded generation."""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any


def recall_at_k(retrieved: Sequence[str], relevant: set[str], k: int) -> float:
    """Return the fraction of relevant documents retrieved in the first *k* results.

    This is true Recall@K. The prior implementation returned a binary success
    indicator, which is more accurately called Hit Rate@K.
    """
    if not relevant or k <= 0:
        return 0.0
    retrieved_at_k = set(retrieved[:k])
    return len(retrieved_at_k & relevant) / len(relevant)


def hit_rate_at_k(retrieved: Sequence[str], relevant: set[str], k: int) -> float:
    """Return 1.0 when any relevant document appears in the first *k* results."""
    if not relevant or k <= 0:
        return 0.0
    return float(bool(set(retrieved[:k]) & relevant))


def reciprocal_rank(retrieved: Sequence[str], relevant: set[str]) -> float:
    """Return the reciprocal rank of the first relevant result."""
    for index, document_id in enumerate(retrieved, start=1):
        if document_id in relevant:
            return 1.0 / index
    return 0.0


def citation_precision(citations: Sequence[str], supporting: set[str]) -> float:
    """Return the share of citations that are supported by the reference set."""
    if not citations:
        return 0.0
    return sum(citation in supporting for citation in citations) / len(citations)


def groundedness(answer_claims: Sequence[str], supported_claims: set[str]) -> float:
    """Return the share of answer claims present in the supported-claims set."""
    if not answer_claims:
        return 0.0
    return sum(claim in supported_claims for claim in answer_claims) / len(answer_claims)


def _required_list(case: Mapping[str, Any], key: str) -> list[str]:
    value = case.get(key)
    if value is None:
        raise ValueError(f"Evaluation case is missing required field: {key}")
    if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
        raise TypeError(f"Evaluation field '{key}' must be a sequence of strings")
    result = list(value)
    if not all(isinstance(item, str) for item in result):
        raise TypeError(f"Evaluation field '{key}' must contain only strings")
    return result


def evaluate_cases(cases: Sequence[Mapping[str, Any]], k: int = 5) -> dict[str, float]:
    """Aggregate retrieval and grounding metrics across evaluation cases."""
    if k <= 0:
        raise ValueError("k must be greater than zero")
    if not cases:
        return {}

    rows: list[dict[str, float]] = []
    for case in cases:
        retrieved = _required_list(case, "retrieved")
        relevant = set(_required_list(case, "relevant"))
        citations = _required_list(case, "citations")
        answer_claims = _required_list(case, "answer_claims")
        supported_claims = set(_required_list(case, "supported_claims"))

        rows.append(
            {
                f"recall_at_{k}": recall_at_k(retrieved, relevant, k),
                f"hit_rate_at_{k}": hit_rate_at_k(retrieved, relevant, k),
                "mrr": reciprocal_rank(retrieved, relevant),
                "citation_precision": citation_precision(citations, relevant),
                "groundedness": groundedness(answer_claims, supported_claims),
            }
        )

    return {
        metric: sum(row[metric] for row in rows) / len(rows)
        for metric in rows[0]
    }
