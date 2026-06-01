# Architecture

```text
User question
     ↓
Agent Router
     ↓
Document RAG Agent / SQL Analytics Agent / Image Notes Agent
     ↓
Evidence Aggregator
     ↓
Local LLM Answer Generator with Ollama
     ↓
Citation Confidence Scoring
     ↓
Hallucination Risk Check
     ↓
Final answer + sources + risk report
```

## Why local/private

This project can run without paid APIs. Documents remain local, embeddings are generated locally, and LLM output can be served through Ollama.
