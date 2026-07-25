from rag.ollama_client import build_prompt
from security.rate_limit import InMemoryRateLimiter
from evaluation.evaluate_rag import reciprocal_rank, citation_rate


def test_prompt_contains_grounding_instruction():
    prompt = build_prompt("What is this?", [{
        "filename": "doc.txt", "chunk_index": 1, "score": 0.9, "text": "A grounded fact"
    }])
    assert "Do not invent facts" in prompt
    assert "doc.txt" in prompt


def test_reciprocal_rank():
    results = [{"filename": "wrong.txt", "rank": 1}, {"filename": "expected_doc.txt", "rank": 2}]
    assert reciprocal_rank(results, "expected") == 0.5


def test_citation_rate():
    assert citation_rate("Supported by file.txt, chunk 2") == 1.0
    assert citation_rate("No citation") == 0.0


def test_rate_limiter():
    limiter = InMemoryRateLimiter(1)
    assert limiter.allow("client") is True
    assert limiter.allow("client") is False
