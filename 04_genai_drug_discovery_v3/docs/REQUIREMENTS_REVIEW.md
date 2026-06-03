# Requirements Review

## Uploaded V2.1 requirement baseline

The uploaded requirement file contains a lightweight deployment stack:

- pandas
- numpy
- scikit-learn
- streamlit
- pytest
- optional/commented rdkit-pypi

This is appropriate for Streamlit Cloud-style deployment because it avoids heavy scientific libraries that can fail to install in constrained environments.

## V3 requirement strategy

V3 uses a two-level strategy:

1. `requirements.txt` keeps the app deployable and testable.
2. `requirements-v3-full.txt` adds the full scientific and enterprise stack.

## Core default requirements

- pandas, numpy, scikit-learn: tables, features, and RAG fallback similarity
- streamlit: scientist-facing UI
- pytest: validation
- requests: optional public API calls
- fastapi, uvicorn, pydantic: enterprise service layer
- joblib: future model serialization
- plotly: dashboard-ready visualization

## Optional full stack

- rdkit-pypi: production chemistry descriptors and molecular graphs
- torch, torch-geometric: graph neural networks
- shap: explainability
- mlflow: experiment tracking and model registry readiness
- biopython: PubMed/Entrez integration path
- sentence-transformers, faiss-cpu: semantic RAG retrieval

## Design principle

The project should never fail only because an optional scientific dependency is unavailable. Default code paths use deterministic fallbacks; full-science paths can be enabled when the environment supports them.
