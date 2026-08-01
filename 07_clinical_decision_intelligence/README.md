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

Services: API `8000`, MLflow `5000`, Prometheus `9090`, Grafana `3000`.

## Interview positioning

> I designed a clinical decision-intelligence platform that combines predictive risk modeling with treatment-effect estimation. I focused on the data and ML platform around the models: reproducible packaging, governed API contracts, FHIR-style interoperability, clinician feedback, fairness and calibration evaluation, model monitoring, MLflow tracking, container deployment, Kubernetes security controls, and CI quality gates. I explicitly positioned the output as clinician-reviewed decision support rather than autonomous medicine.

## Principal-level design tradeoffs

- Predictive discrimination versus calibration and subgroup reliability
- Real-time features versus operational and governance complexity
- Model reproducibility versus artifact size and distribution strategy
- Local JSONL feedback versus transactional, auditable clinical systems
- FHIR simulation versus certified EHR integration
- Automated recommendations versus mandatory clinician oversight
