import pytest

from src.healthcare_mm.evaluation.multimodal_eval import (
    citation_precision,
    evaluate_cases,
    groundedness,
    hit_rate_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k_uses_fraction_of_all_relevant_documents() -> None:
    assert recall_at_k(["a", "x", "b"], {"a", "b", "c"}, 2) == pytest.approx(1 / 3)
    assert recall_at_k(["a", "x", "b"], {"a", "b", "c"}, 3) == pytest.approx(2 / 3)


def test_hit_rate_at_k_remains_available_as_binary_metric() -> None:
    assert hit_rate_at_k(["x", "a"], {"a", "b"}, 1) == 0.0
    assert hit_rate_at_k(["x", "a"], {"a", "b"}, 2) == 1.0


def test_retrieval_edge_cases() -> None:
    assert recall_at_k([], {"a"}, 5) == 0.0
    assert recall_at_k(["a"], set(), 5) == 0.0
    assert recall_at_k(["a"], {"a"}, 0) == 0.0
    assert reciprocal_rank(["x", "a"], {"a"}) == 0.5
    assert reciprocal_rank([], {"a"}) == 0.0


def test_grounding_metrics() -> None:
    assert citation_precision(["a", "x"], {"a", "b"}) == 0.5
    assert citation_precision([], {"a"}) == 0.0
    assert groundedness(["c1", "c2"], {"c1"}) == 0.5
    assert groundedness([], {"c1"}) == 0.0


def test_evaluate_cases_aggregates_metrics() -> None:
    cases = [
        {
            "retrieved": ["a", "x"],
            "relevant": ["a", "b"],
            "citations": ["a"],
            "answer_claims": ["c1", "c2"],
            "supported_claims": ["c1"],
        },
        {
            "retrieved": ["z", "b"],
            "relevant": ["b"],
            "citations": ["z"],
            "answer_claims": ["c3"],
            "supported_claims": ["c3"],
        },
    ]
    result = evaluate_cases(cases, k=2)
    assert result["recall_at_2"] == pytest.approx(0.75)
    assert result["hit_rate_at_2"] == 1.0
    assert result["mrr"] == pytest.approx(0.75)
    assert result["citation_precision"] == pytest.approx(0.5)
    assert result["groundedness"] == pytest.approx(0.75)


def test_evaluate_cases_validates_inputs() -> None:
    with pytest.raises(ValueError, match="k must be greater than zero"):
        evaluate_cases([], k=0)
    with pytest.raises(ValueError, match="missing required field"):
        evaluate_cases([{}])
