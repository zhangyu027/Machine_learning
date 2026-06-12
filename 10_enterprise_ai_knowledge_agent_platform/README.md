# 10 Enterprise AI Knowledge Agent Platform

**Principal Data Engineer / Enterprise AI Platform Edition**

This project upgrades a local RAG chatbot into an enterprise-style AI knowledge agent platform. It demonstrates document retrieval, SQL analytics, image-note retrieval, routing, confidence scoring, hallucination-risk checks, evaluation artifacts, and local/private deployment patterns.

## What This Project Includes

- Agent orchestration and routing
- Document RAG over local files
- SQL analytics over local CSV/SQLite data
- Image-note retrieval
- FAISS vector search when available
- Deterministic local fallback vector search when FAISS or sentence-transformers are unavailable
- Optional Ollama local LLM integration
- Citation confidence scoring
- Hallucination risk checks
- Benchmark evaluation workflow
- Streamlit app
- Jupyter notebook

## Folder Structure

```text
agents/                 Agent router and orchestrator
app/                    Streamlit app
build_index.py          Builds vector store and SQLite database
data/                   Documents, image notes, and SQL sample data
docs/                   Architecture and project documentation
evaluation/             Evaluation questions and benchmark script
notebooks/              Demo notebook
outputs/                Generated evaluation outputs
rag/                    Document loader, vector store, Ollama client
tests/                  Pytest smoke tests
tools/                  SQL, image, confidence, hallucination tools
vector_store/           Local vector index and metadata
```

## Local Demo

From the project root:

```bash
pip install -r requirements.txt
python build_index.py
python run_agent.py
pytest -q
```

Run benchmark evaluation:

```bash
python evaluation/evaluate_agent.py
```

Outputs:

```text
vector_store/index.faiss              # when FAISS is installed
vector_store/index_fallback.npz       # deterministic fallback vector index
vector_store/metadata.json
data/sql/enterprise_agent.db
outputs/tables/agent_evaluation_results.csv
outputs/tables/agent_evaluation_summary.csv
evaluation/evaluation_summary.json
```

## Optional Ollama Setup

Install Ollama and pull a local model:

```bash
ollama pull llama3.2
```

The platform can run without Ollama by using retrieved evidence summaries. This keeps the demo runnable in environments without a local LLM.

## Example Questions

```text
What should healthcare AI governance include?
Why is de-identification important for public-sector analytics?
Which portfolio projects have the highest priority and why?
What does the platform architecture diagram show?
```

## Why This Is More Than a Chatbot

A chatbot usually produces a direct answer. This platform demonstrates enterprise AI system design:

1. route the question,
2. select tools,
3. retrieve evidence,
4. query structured data,
5. cite sources,
6. score confidence,
7. check hallucination risk,
8. persist evaluation outputs.

## Principal Data Engineer Interview Narrative

“I designed a private enterprise AI knowledge agent platform with document RAG, SQL analytics, image-note retrieval, orchestration, confidence scoring, hallucination risk checks, and evaluation artifacts. The system supports local/private deployment and demonstrates how enterprise AI platforms can be governed, evaluated, and integrated with structured and unstructured data sources.”

## Production Positioning

This is a portfolio-grade reference implementation using local synthetic/sample data. A production version would use governed document stores, enterprise identity and access controls, managed vector infrastructure, observability, audit logs, model governance, CI/CD, and human review workflows.

## Recommended GitHub Cleanup

Do not commit:

```text
.venv/
__pycache__/
.pytest_cache/
.DS_Store
large raw documents
private documents
*.zip
```

Keep only synthetic/sample data and safe portfolio artifacts in GitHub.
