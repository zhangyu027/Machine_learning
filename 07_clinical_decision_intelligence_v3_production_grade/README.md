# 07 Clinical Decision Intelligence — Production Reference Platform

> **Important:** This repository uses synthetic data and is intended for educational and portfolio demonstration only. It is not a medical device and must not be used for diagnosis, treatment, triage, or other clinical decision-making.

This project demonstrates how a Principal Data Engineer or ML Platform Engineer can turn clinical prediction and causal-inference workflows into a governed, observable, deployable decision-support platform.

## What the platform demonstrates

- 30-day readmission-risk modeling
- Propensity-score and doubly robust treatment-effect estimation
- Causal-forest-style heterogeneous treatment-effect modeling
- SHAP explainability, calibration, fairness, and drift utilities
- Authenticated FastAPI serving with typed OpenAPI contracts
- FHIR R4-style `RiskAssessment` output
- Clinician feedback capture
- Prometheus/Grafana observability
- MLflow experiment tracking
- Docker, Kubernetes, and GitHub Actions deployment scaffolding

## Safety and implementation boundaries

The included models and data are demonstration artifacts. The repository has not undergone clinical validation, regulatory review, hospital security review, prospective evaluation, or human-factors testing. The local feedback store is JSONL-based and the FHIR adapter is a simulation rather than a certified EHR integration.

## Repository structure

```text
src/clinical_decision_intelligence/
  api/            FastAPI service and schemas
  causal/         Treatment-effect methods
  core/           Central configuration
  evaluation/     Calibration and fairness
  features/       Feature-store abstraction
  integrations/   FHIR and clinician feedback
  ml/             Training, prediction, explainability
  monitoring/     Metrics and drift
scripts/          Pipeline, evaluation, and MLflow entry points
tests/            Unit and API integration tests
k8s/              Kubernetes Deployment, Service, and HPA
monitoring/       Prometheus and Grafana assets
docs/             Architecture, deployment, validation, and review documents
```

## Local installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-all.txt
```

## Run tests and pipeline

```bash
CDI_API_KEY=test-secret pytest -q
python -m scripts.run_full_pipeline
python -m scripts.evaluate_production_readiness
```

## Run the API

```bash
export CDI_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
uvicorn clinical_decision_intelligence.api.app:app --reload
```

### API endpoints

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| GET | `/health` | Process health and version | No |
| GET | `/ready` | Model readiness | No |
| GET | `/version` | Service version | No |
| GET | `/metrics` | Prometheus metrics | No |
| POST | `/v1/predict` | Readmission-risk estimate | API key |
| POST | `/v1/predict/fhir` | FHIR-style RiskAssessment | API key |
| POST | `/v1/feedback` | Clinician feedback | API key |

Swagger UI: `http://127.0.0.1:8000/docs`

## Docker Compose

```bash
cp .env.example .env
# Replace the API key in .env before starting.
docker compose up --build -d
docker compose ps
curl --fail http://127.0.0.1:8000/health
```

Services (host ports): API `8000`, MLflow `5001` (container port `5000`), Prometheus `9090`, Grafana `3000`.

## Interview positioning

> I designed a clinical decision-intelligence platform that combines predictive risk modeling with treatment-effect estimation. I focused on the data and ML platform around the models: reproducible packaging, governed API contracts, FHIR-style interoperability, clinician feedback, fairness and calibration evaluation, model monitoring, MLflow tracking, container deployment, Kubernetes security controls, and CI quality gates. I explicitly positioned the output as clinician-reviewed decision support rather than autonomous medicine.

## Principal-level design tradeoffs

- Predictive discrimination versus calibration and subgroup reliability
- Real-time features versus operational and governance complexity
- Model reproducibility versus artifact size and distribution strategy
- Local JSONL feedback versus transactional, auditable clinical systems
- FHIR simulation versus certified EHR integration
- Automated recommendations versus mandatory clinician oversight

## Verified local integration and model results (2026-10-28)

The following observations were reported from a local macOS/Python 3.11 and Docker Compose test. They are **development smoke tests, not clinical validation or production deployment evidence**.

| Component | Observed result |
|---|---|
| API `GET /health`, `/ready`, `/version` | Successful; model loaded, service version 3.1.0 |
| Authenticated `POST /v1/predict` | HTTP 200 for a synthetic encounter; risk 0.4024517536, category `moderate`, clinician review required |
| Authenticated `POST /v1/predict/fhir` | HTTP 200; FHIR-style `RiskAssessment` with probability 0.402452 |
| Authenticated `POST /v1/feedback` | HTTP 200; synthetic feedback acknowledged (durable persistence not independently verified) |
| Prometheus | `http://api:8000/metrics` target UP (1/1) |
| MLflow | Experiment creation, metric/artifact logging, model registration succeeded |
| Grafana | Login UI reachable; datasource and dashboard queries not yet verified |
| Kubernetes, CI, production security | Not established by these local checks |

**Latest MLflow training run:** `clinical-decision-intelligence-v3`, run `1164e2fd7bf94475b4b8791c4f3562c3` (`defiant-cat-899`), registered model `readmission-risk-xgboost` version **1**.

| Metric | Latest local MLflow run | Earlier package validation (see `docs/VALIDATION_REPORT.md`) |
|---|---:|---:|
| ROC-AUC | **0.7432348469** | 0.7434 |
| Average precision | **0.5620893332** | 0.5619 |

These are **different runs**; no claim is made about statistical significance, real-world generalization, calibration, clinical utility, or performance on actual patient data. A model-signature/input-example warning remains a documentation/deployment improvement opportunity.

### Reproduce the MLflow run locally

The MLflow server is pinned to `ghcr.io/mlflow/mlflow:v2.22.0`. **Pin the Mac client to `mlflow==2.22.0` too** (see `requirements.txt`) to avoid newer-client `/api/2.0/mlflow/logged-models` 404 errors.

```bash
python -m pip install -r requirements.txt
export CDI_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
docker compose config --quiet
docker compose up -d --build
curl --fail http://127.0.0.1:5001/health
export MLFLOW_TRACKING_URI=http://127.0.0.1:5001
python scripts/train_with_mlflow.py
```

For Mac-hosted training use `http://127.0.0.1:5001`; from containers use `http://mlflow:5000`. The MLflow server must serve artifacts via `--serve-artifacts --artifacts-destination /mlflow-data/artifacts` and retain its `mlflow-data` volume. Existing experiments with old local artifact URIs may need a fresh experiment rather than simply re-running. Never use `docker compose down -v` when preserving MLflow experiments.

See [interview notes](docs/INTERVIEW_NOTES.md) for a concise explanation of design decisions, debugging, results, and limitations.
