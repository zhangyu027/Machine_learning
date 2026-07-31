# 08 Healthcare Multimodal Foundation Model System
> **Important:** This repository uses synthetic data and is intended for
> educational and portfolio demonstration only. It is not a medical device
> and must not be used for diagnosis, treatment, triage, or other clinical
> decision-making.

# Healthcare Multimodal Foundation Model System

> **Important:** This repository uses synthetic data and is intended for
> educational and portfolio demonstration only. It is not a medical device
> and must not be used for diagnosis, treatment, triage, or other clinical
> decision-making.

**Merged Principal Data Engineer Edition**

This package merges the original #08 folder structure with a Principal Data Engineer upgrade layer for healthcare AI platform interviews.

## What This Demonstrates

This project shows how a Principal Data Engineer can design the enterprise data foundation for regulated healthcare multimodal AI:

- FHIR-style patient and encounter data
- Labs, vitals, clinical notes, and imaging metadata
- Local synthetic data validation pipeline
- Gold patient-encounter table construction
- Multimodal feature engineering
- Baseline readmission model for pipeline validation
- Model-card and governance artifacts
- AWS Glue, SageMaker, Step Functions, Terraform, and CI/CD skeletons
- PII controls and healthcare governance patterns

## Folder Structure

```text
app/                    Streamlit user interface entry point
data/sample/            Synthetic local demo data
docs/                   Executive and architecture documentation
notebooks/              Demonstration notebook
scripts/                Local runnable pipeline
src/healthcare_mm/      Ingestion, lakehouse, features, models, MLOps, security
tests/                  Pytest validation
aws/                    Glue/SageMaker/Step Functions/Terraform skeletons
executive_materials/    Executive report and deck
.github/workflows/      CI workflow
outputs/                Generated evaluation artifacts
models/                 Trained demonstration models
```

## Local Demo

From the project root:

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
pytest -q
```

You can also run:

```bash
python -m scripts.run_pipeline
```

The pipeline writes demo artifacts to:

```text
outputs/gold_patient_encounter.csv
outputs/model_features.csv
outputs/model_metrics.json
outputs/model_card.json
models/readmission_gbm.joblib
```

## Validation and Evaluation Artifacts

After successfully running the pipeline:

```bash
python -m scripts.run_pipeline
```

Create and maintain:

```text
outputs/evaluation_summary.json
```

Example metrics from a successful run:

```json
{
  "project": "08_healthcare_multimodal_foundation_model_system",
  "pipeline_status": "completed_successfully",
  "gold_table": "outputs/gold_patient_encounter.csv",
  "feature_table": "outputs/model_features.csv",
  "metrics": {
    "roc_auc": 0.42966751918158574,
    "average_precision": 0.16451864892744827,
    "test_rows": 125,
    "feature_count": 26
  }
}
```

Validation checklist:

```bash
python -m scripts.run_pipeline
pytest -q
```

Expected result:

```text
Healthcare multimodal pipeline completed successfully.
22 passed
```

This confirms that the synthetic-data pipeline executes from ingestion through evaluation artifact generation. It does not establish clinical validity or useful predictive performance.

## Principal Data Engineer Interview Narrative

“I designed the enterprise data foundation for regulated healthcare multimodal AI. The platform integrates FHIR-style patient and encounter data, labs, vitals, notes, and imaging metadata into a lakehouse architecture. It includes Glue-based ETL patterns, a gold patient-encounter table, feature engineering for multimodal modeling, SageMaker training orchestration, PII controls, model-card governance, and CI/CD readiness.”

## Production Positioning

This is a portfolio-grade reference implementation using synthetic data. The production architecture would move raw and curated data to S3, run ETL through Glue or EMR, orchestrate workflows through Step Functions or Airflow, train/register models through SageMaker, and enforce access controls, monitoring, lineage, and auditability.

Evaluation summaries, model cards, and validation artifacts are persisted to support reproducibility, auditability, and governance review.

## Recommended GitHub Cleanup

Do not commit:

```text
.venv/
__pycache__/
.pytest_cache/
large raw images
trained checkpoints
outputs/
models/*.joblib
*.zip
```

Keep large data and models in S3, Git LFS, or release artifacts.

# V2 Production Multimodal Foundation Upgrade

This edition adds an executable and production-oriented AI layer on top of the existing healthcare lakehouse:

- **Multimodal transformer:** vision, clinical-text, and structured-EHR projection and fusion, with an optional PyTorch transformer implementation.
- **Vector retrieval:** normalized similarity search with metadata filtering and a migration path to FAISS/Milvus.
- **Clinical RAG:** evidence-first retrieval, citations, confidence thresholds, and clinician-review fallback.
- **GPU optimization:** container/Kubernetes GPU resource scaffold; production path supports mixed precision, batching, and compiled inference.
- **MLflow:** experiment logging and model-registry integration with an offline JSON fallback.
- **Kubernetes:** replicated deployment, readiness probe, service, autoscaling, and GPU limits.
- **Observability:** Prometheus request/latency metrics and optional OpenTelemetry dependencies.
- **Distributed training:** torchrun environment helpers and documented DeepSpeed/Ray extension path.
- **Feature store:** online feature retrieval interface designed for later Feast replacement.
- **FHIR integration:** Bundle ingestion and FHIR R4-style RiskAssessment output.
- **Clinician review:** append-only accept/reject/override feedback for audit and retraining.
- **Automated evaluation:** Recall@K, MRR, citation precision, and groundedness.

## Production API

```bash
pip install -r requirements.txt -r requirements-production.txt
export PYTHONPATH=.
API_KEY=test-secret python -m pytest -q
uvicorn api.main:app --reload
```
The generated API key is stored only in the current terminal session. Use the
same value in the `X-API-Key` request header when calling protected endpoints.

Endpoints:

```text
### API endpoints

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| GET | `/health` | Service health and version | No |
| GET | `/metrics/` | app.mount("/metrics", make_asgi_app()) | No |
| POST | `/v1/predict` | Demonstration multimodal prediction | API key |
| POST | `/v1/reviews` | Clinician-review feedback | API key |
```

## V2 Architecture

```text
FHIR/EHR + Clinical Notes + Imaging
              ↓
      Lakehouse / Feature Store
              ↓
Vision Encoder + Text Encoder + Structured Encoder
              ↓
       Transformer Fusion Layer
              ↓
Risk Head + Multimodal Embedding Index
              ↓
 Clinical RAG + Evidence Validation
              ↓
FHIR RiskAssessment + Clinician Review
              ↓
MLflow Registry + Prometheus/OpenTelemetry
              ↓
Docker / Kubernetes / GPU Serving
```

## Responsible interview positioning

This is a synthetic-data, portfolio-grade reference implementation. The local NumPy fusion encoder, in-memory vector store, FHIR simulator, and JSON registry fallback are executable demonstrations. PyTorch distributed training, Feast, external FHIR servers, production vector databases, GPU serving, and hospital deployment are integration paths and scaffolds—not claims of live clinical deployment.


## Model-performance interpretation

The included baseline model is a pipeline-validation artifact trained on synthetic data. Reported metrics validate code execution and artifact generation only. They must not be interpreted as evidence of clinical usefulness. A production evaluation would require patient-level leakage controls, prevalence reporting, calibration analysis, fairness analysis, external validation, and clinical review.

## Safety disclaimer

This repository uses synthetic data and is intended for educational and portfolio demonstration purposes only. It is not a medical device and must not be used for diagnosis, treatment, triage, or clinical decision-making.

## Modeling limitation

The production API currently uses a deterministic completeness-based
demonstration heuristic. It does not load the pipeline's trained
`readmission_gbm.joblib` artifact.

The trained baseline model and the API-serving heuristic are separate
portfolio demonstrations. Neither has been clinically validated, and neither
should be used for diagnosis, treatment, triage, or patient-level decisions.

## Implementation status

| Capability | Status |
|---|---|
| Synthetic multimodal ingestion and gold-table pipeline | Executable locally |
| Baseline model and governance artifacts | Executable locally |
| In-memory retrieval and evaluation utilities | Executable demonstration |
| FastAPI health, prediction, and review endpoints | Executable demonstration |
| Prometheus `/metrics` endpoint | Requires API integration described in `API_PATCH_GUIDE.md` |
| External FHIR servers, production vector databases, Feast, distributed training, GPU serving, and hospital deployment | Integration paths/scaffolds |
