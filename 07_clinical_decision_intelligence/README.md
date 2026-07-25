# Clinical Decision Intelligence V3 — Production Healthcare ML

A production-oriented healthcare decision-support portfolio project combining readmission-risk prediction, causal treatment-effect estimation, explainability, model governance, API serving, monitoring, and simulated clinical integration.

> **Safety boundary:** This is an educational portfolio system, not a medical device and not intended for diagnosis or treatment decisions without clinician review and formal validation.

## Architecture

```text
FHIR/EHR simulation or feature store
              ↓
        FastAPI service
              ↓
 XGBoost risk model + causal models
              ↓
 Calibration + fairness + SHAP
              ↓
 Clinician review and feedback log
              ↓
 Prometheus/Grafana + drift monitoring
              ↓
 MLflow experiments and model registry
```

## V3 production additions

- MLflow experiment tracking and registered-model scaffold
- Authenticated FastAPI prediction and FHIR-style endpoints
- Docker, Docker Compose, Kubernetes Deployment, Service, and HPA
- Prometheus metrics and starter Grafana dashboard
- Local feature-store abstraction designed for migration to Feast
- Fairness evaluation by sex and insurance group
- Calibration curve data and Brier score
- FHIR R4 `RiskAssessment` simulation
- Clinician accept/reject feedback loop
- GitHub Actions testing, evaluation, and Docker build
- Drift utility using Population Stability Index

## Existing analytical foundation

- XGBoost 30-day readmission model
- SHAP explainability
- Propensity score matching
- Doubly robust treatment-effect estimation
- Causal-forest-style T-learner
- Patient-level risk and treatment-benefit recommendations

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PWD
export CDI_API_KEY=demo-secret
uvicorn src.api.app:app --reload
```

Test:

```bash
curl -X POST http://localhost:8000/v1/predict   -H 'Content-Type: application/json'   -H 'X-API-Key: demo-secret'   -d '{"patient_id":"P-100","age":72,"sex":"F","insurance":"Medicare","hospital_id":"H1","comorbidity_index":4,"prior_admissions_12m":2,"severity_score":7.5,"care_management_program":1,"length_of_stay":5}'
```

## Production evaluation

```bash
python scripts/evaluate_production_readiness.py
python scripts/train_with_mlflow.py
```

## Full stack

```bash
cp .env.example .env
# edit .env before use
docker compose up --build
```

Services: API `:8000`, MLflow `:5000`, Prometheus `:9090`, Grafana `:3000`.

## Interview narrative

“I built a clinical decision-intelligence platform that predicts 30-day readmission risk and estimates heterogeneous benefit from a care-management intervention. I extended the analytical pipeline into a production architecture with MLflow model governance, authenticated FastAPI serving, fairness and calibration evaluation, a FHIR-style integration layer, clinician feedback capture, Prometheus/Grafana monitoring, Docker/Kubernetes deployment, and automated CI. I treated the recommendation as decision support rather than autonomous medicine, preserving clinician review and auditability.”

## Tradeoffs to discuss

- Prediction performance versus calibration and subgroup reliability
- Real-time feature freshness versus operational complexity
- Local feature-store demo versus managed Feast infrastructure
- FHIR simulation versus certified EHR integration
- Risk score usefulness versus alert fatigue
- Model automation versus mandatory clinician oversight

## Repository map

- `src/api/` serving, schemas, authentication, rate limiting
- `src/evaluation/` calibration and fairness
- `src/features/` feature-store abstraction
- `src/integrations/` FHIR simulation and clinician feedback
- `src/monitoring/` Prometheus metrics and drift
- `scripts/` training and production evaluation
- `monitoring/`, `k8s/`, `.github/workflows/` operations scaffolding
