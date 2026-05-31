# Pharmaceutical GenAI Drug Discovery V3 Enterprise Platform

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
curl http://localhost:8000/health
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
