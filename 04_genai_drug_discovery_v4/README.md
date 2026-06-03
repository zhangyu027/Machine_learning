# Pharmaceutical GenAI Drug Discovery V4 Enterprise Platform

This dedicated V3 project evolves the V2.1 pharmaceutical ML demo into an enterprise-style drug discovery AI platform. It keeps the Streamlit portfolio app deployable, while adding production-ready architectural seams for graph neural networks, public chemistry data integration, multi-task ADMET prediction, uncertainty estimation, explainability, RAG, FastAPI, Docker, MLflow-style tracking, and CI/CD.

## What changed from V2.1

V2.1 validated the core local workflow: SMILES input, molecular property prediction, ADMET/toxicity scoring, reliability labels, uncertainty explanations, and Streamlit output.

V3 adds:

- Graph Neural Network readiness via PyTorch Geometric-compatible interfaces
- ChEMBL, PubChem, DrugBank, and BindingDB integration layer
- Multi-task ADMET prediction across absorption, BBB, CYP, clearance, solubility, toxicity, and drug-likeness tasks
- Conformal-style uncertainty intervals and ensemble-disagreement reliability scoring
- SHAP-ready explainability with deterministic fallback feature attribution
- PubMed-style RAG literature evidence retrieval
- FastAPI service layer for enterprise deployment
- Docker and docker-compose deployment files
- MLflow-ready experiment tracking with JSON fallback
- GitHub Actions CI/CD pipeline

## Quick start

```bash
cd 04_genai_drug_discovery_v3_enterprise
conda create -n pharma_v3 python=3.11 -y
conda activate pharma_v3
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pytest
```

## Launch Streamlit

```bash
streamlit run app/streamlit_app.py
```

Example SMILES:

```text
CCO
CC(=O)Oc1ccccc1C(=O)O
Cn1cnc2c1c(=O)n(C)c(=O)n2C
```

## Run CLI

```bash
python -m pharma_genai.cli_v3 --smiles "CCO" "CC(=O)Oc1ccccc1C(=O)O" --literature
```

## Run FastAPI

```bash
uvicorn pharma_genai.api.service:app --reload --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/docs
```

Analyze molecules:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"smiles":["CCO","CC(=O)Oc1ccccc1C(=O)O"],"include_literature":true}'
```

## Docker

```bash
cd 04_genai_drug_discovery_v3_enterprise
Docker build -f deployment/Dockerfile -t pharma-genai-v3 .
docker run -p 8501:8501 pharma-genai-v3
```

Or:

```bash
cd deployment
docker compose up --build
```

## Optional full scientific stack

The default requirements are intentionally deployable. For a workstation or cloud instance with scientific dependencies, install:

```bash
python -m pip install -r requirements-v3-full.txt
```

This enables RDKit, PyTorch Geometric, SHAP, MLflow, BioPython, sentence transformers, and FAISS.

## Scientific disclaimer

This is a portfolio and decision-support prototype. It is not a validated clinical, regulatory, or production medicinal chemistry system. Predictions are demonstration outputs unless trained and validated on appropriate proprietary or public experimental datasets.


## V3.1 Enterprise Upgrade

This package includes a V3.1 reliability and connector upgrade for the pharmaceutical GenAI drug discovery platform.

### What changed

- Fixed the PubChem aspirin fallback record so `PublicDataConnector().pubchem_lookup("aspirin")` returns a non-empty SMILES string.
- Added deterministic offline PubChem, ChEMBL, and DrugBank-style connector records.
- Added SMILES validation with optional RDKit support and a lightweight fallback validator.
- Added an ADMET prediction service interface that can later be replaced by trained XGBoost, PyTorch, or GNN models.
- Added uncertainty and reliability scoring for portfolio decision support.
- Added an integrated candidate screening pipeline.
- Added V3.1 integration tests covering public-data lookup, cross-source lookup, and end-to-end candidate screening.

### Validation

Run:

```bash
pytest -q
```

The original failing test should now pass because aspirin resolves to:

```text
CC(=O)OC1=CC=CC=C1C(=O)O
```

### Interview positioning

This upgrade moves the project from a demo molecule-generation system toward an enterprise-style pharmaceutical decision platform: public chemistry data integration, valid molecular representation, ADMET prediction, reliability scoring, and testable service interfaces.
