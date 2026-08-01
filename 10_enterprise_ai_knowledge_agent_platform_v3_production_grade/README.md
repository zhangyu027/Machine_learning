# Enterprise AI Knowledge Agent Platform

> **Important:** Synthetic portfolio reference implementation only. Retrieved documents are untrusted evidence. This system is not approved for production enterprise decisions without organization-specific security, privacy, legal, and model-risk validation.

A production-oriented RAG and agent platform demonstrating deterministic fallback embeddings, versioned indexes, safe SQL templates, prompt-injection defenses, typed FastAPI contracts, evaluation metrics, observability, Docker, Kubernetes, and CI/CD.

## Implemented

- Named installable package under `src/enterprise_ai_agent`
- Stable SHA-256 fallback embeddings
- Versioned candidate-to-active index promotion
- Document, image-note, and SQL routing
- Read-only allowlisted SQL templates
- Grounding-risk heuristic (not claimed as hallucination detection)
- Prompt-injection screening for retrieved content
- Recall@K, MRR, citation precision, and route accuracy
- `/health`, `/ready`, `/metrics/`, and `/v1/query`
- Docker, Kubernetes, and GitHub Actions scaffolding

## Quick start

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-api.txt -r requirements-dev.txt -e .
python -m scripts.initialize_demo
python -m scripts.build_index
EAK_API_KEY=test-secret uvicorn enterprise_ai_agent.api.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Validation

```bash
pytest -q
ruff check .
python -m compileall src scripts tests
```

## Remaining limitations

The answer generator is evidence-summary based unless a separately governed LLM integration is added. Prompt-injection screening and grounding-risk checks are rule-based safeguards, not proofs of safety or factuality. SQLite, local files, and the fallback vector index are local demonstrations rather than enterprise-scale services.
