# Final Check — 10 Enterprise AI Knowledge Agent Platform

Recommended validation commands:

```bash
pip install -r requirements.txt
python build_index.py
python run_agent.py
python evaluation/evaluate_agent.py
pytest -q
```

Expected outcome:

- Vector store metadata and fallback index are generated.
- SQLite database is generated.
- Agent returns a routed, evidence-based answer.
- Evaluation outputs are generated.
- Tests pass.

Notes:

- FAISS, sentence-transformers, and Ollama are supported but not required for the fallback smoke path.
- The project uses synthetic/sample portfolio data only.
- Do not commit `.venv`, cache folders, private documents, or large files.
