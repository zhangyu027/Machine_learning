# Requirements Review: V4.1 Dependency Strategy

## Design principle

The project should never fail only because an optional scientific dependency is unavailable. Default paths should support demo, tests, Streamlit, and API smoke checks. Full scientific environments can enable RDKit, GNN, SHAP, RAG embeddings, and MLflow.

## Recommended files

| File | Purpose |
|---|---|
| `requirements.txt` | Core deployable stack: pandas, numpy, scikit-learn, requests, pydantic, FastAPI, Streamlit, pytest, plotly |
| `requirements-dev.txt` | Developer tools: pytest-cov, ruff, mypy, notebook tooling |
| `requirements-ml.txt` | ML stack: torch, transformers, sentence-transformers, SHAP, MLflow, Biopython, FAISS |
| `requirements-v4-optional.txt` | Full optional scientific/enterprise stack |

## RDKit recommendation

Prefer Conda for RDKit:

```bash
conda install -c conda-forge rdkit -y
```

## DeepChem note

DeepChem may print warnings about optional TensorFlow, JAX, DGL, Lightning, ChemBERTa, or transformer components. These warnings do not block basic MoleculeNet dataset downloads using `featurizer="Raw"`.

## Validation commands

```bash
python -m pip install -e .
pytest
python -c "from pharma_genai.data.scaffold_split import scaffold_split_indices; print('scaffold split OK')"
python -c "from pharma_genai.models.classical_baselines import build_baselines; print('baselines OK')"
```
