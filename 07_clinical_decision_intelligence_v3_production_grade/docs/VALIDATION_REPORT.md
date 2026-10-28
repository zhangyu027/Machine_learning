# Validation Report

## Validation environment

- Package build environment: Linux container
- Python: 3.13
- Test framework: pytest
- Data: synthetic patient encounters supplied with the source package

## Evidence collected

- Python compilation: passed for `src/` and `scripts/`
- Test suite: **12 passed in 1.13 seconds**
- Full training pipeline: passed
- Production evaluation script: passed
- Readmission ROC AUC: **0.7434**
- Readmission average precision: **0.5619**
- Propensity-score matched ATT: **-0.1092** across **18,572** matched pairs
- Typed API tests cover health, readiness, authentication, prediction, FHIR output, feedback, and OpenAPI response schemas

## External gates not executed in this environment

- Docker image build and smoke test
- Docker Compose multi-service validation
- Kubernetes client-side or cluster validation
- GitHub Actions execution

These gates must pass in the target environment before merge.

## Merge gate

Merge only when:

1. All tests pass in a clean Python 3.11 environment.
2. GitHub Actions quality and container jobs pass.
3. Docker health, readiness, prediction, FHIR, feedback, and metrics checks pass.
4. Kubernetes manifests validate.
5. No secrets, generated reports, processed data, caches, or unintended model artifacts are tracked.
6. OpenAPI and documentation match observed API behavior.

## Supplemental local Docker and MLflow validation — 2026-10-28

The earlier results above are retained as a **separate package-validation run**. The following observations were reported from a subsequent macOS Python 3.11 / Docker Compose local test; they do not supersede the earlier metrics.

- FastAPI health, readiness and version endpoints responded; authenticated prediction, FHIR-style prediction and clinician feedback requests returned HTTP 200 using synthetic test data.
- Prometheus reported its API scrape target UP (1/1). Grafana login UI loaded; Grafana datasource/dashboard query validation remains outstanding.
- MLflow experiment `clinical-decision-intelligence-v3` successfully logged a model and registered `readmission-risk-xgboost` **version 1**.
- Successful MLflow run: `1164e2fd7bf94475b4b8791c4f3562c3` (`defiant-cat-899`).
- Latest **ROC-AUC 0.7432348468848465**; **average precision 0.5620893332451523**.
- Earlier MLflow runs failed before model registration due to cross-environment artifact URI configuration and a client/server mismatch (Mac 3.16.1 vs Docker 2.22.0). Artifact serving was configured, a fresh experiment created, and the client pinned to 2.22.0.
- Remaining warning: logged model has no signature or input example.

These observations partially address the original “Docker smoke test not executed” gap but **do not demonstrate** a clean CI run, Kubernetes validation, prospective/clinical validation, production-grade security, or full monitoring dashboard operation. Keep the merge gates above in force.
