# Technical Design Document

## 1. Purpose

The Clinical Decision Intelligence platform is a synthetic-data reference implementation for governed healthcare ML. It combines readmission-risk prediction, treatment-effect estimation, clinical interoperability patterns, clinician feedback, and MLOps controls.

## 2. Scope

The executable scope includes local data processing, training, model loading, authenticated inference, FHIR-style output, JSONL feedback, fairness and calibration evaluation, Prometheus metrics, and MLflow integration. Hospital deployment, certified EHR integration, managed feature stores, and regulatory validation are outside the demonstrated scope.

## 3. Components

- `core`: environment-based settings and paths
- `ml`: training, prediction, and SHAP explainability
- `causal`: propensity matching, doubly robust estimation, and T-learner proxy
- `evaluation`: calibration and subgroup fairness
- `features`: local feature-store abstraction
- `api`: request/response schemas, authentication, rate limiting, and endpoints
- `integrations`: FHIR-style resources and clinician feedback
- `monitoring`: service metrics and population stability index

## 4. API contracts

The API exposes health, readiness, version, metrics, prediction, FHIR prediction, and feedback endpoints. Protected endpoints require an explicitly configured `CDI_API_KEY`. Pydantic models validate ranges and document response schemas.

## 5. Security and privacy

The container runs as a non-root user. Kubernetes drops Linux capabilities, disables service-account token mounting, and loads the API key from a Secret. The repository excludes `.env`, feedback logs, generated reports, processed data, and model artifacts. These controls are portfolio patterns and do not replace HIPAA risk analysis, enterprise IAM, encryption, de-identification, audit controls, or institutional approval.

## 6. Reliability and observability

Health and readiness are separate. Prometheus captures request counts, latency, risk distribution, feedback decisions, and model-loaded state. Docker and Kubernetes probes use the health and readiness endpoints. Production systems should add distributed tracing, structured logs, alert thresholds, SLOs, and model/data lineage.

## 7. Deployment

The project supports local Python execution, Docker Compose, and Kubernetes manifests. MLflow, Prometheus, and Grafana are included as integration services. Images should be pinned by digest and promoted through environments only after CI and security gates pass.

## 8. Data and model governance

Training and evaluation artifacts are reproducible but not intended for source control. Model bundles should be stored in a registry or artifact repository with checksums, signatures, lineage, approval status, and rollback metadata.

## 9. Known limitations

The model is trained on synthetic data; feedback uses JSONL; FHIR is simulated; raw identifiers may be accepted; there is no clinical validation; and Kubernetes, feature-store, and EHR pathways are scaffolding rather than evidence of live deployment.
