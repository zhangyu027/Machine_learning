# 08 Healthcare Multimodal Foundation Model System

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
app/                    Streamlit entry point placeholder
data/sample/            Synthetic local demo data
docs/                   Executive and architecture documentation
notebooks/              Demonstration notebook
scripts/                Local runnable pipeline
src/healthcare_mm/      Ingestion, lakehouse, features, models, MLOps, security
tests/                  Pytest validation
aws/                    Glue/SageMaker/Step Functions/Terraform skeletons
executive_materials/    Executive report and deck
.github/workflows/      CI workflow
```

## Local Demo

From the project root:

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
pytest -q
```

The pipeline writes demo artifacts to:

```text
outputs/gold_patient_encounter.csv
outputs/model_features.csv
outputs/model_metrics.json
outputs/model_card.json
models/readmission_gbm.joblib
```

You can also run:

```bash
python -m scripts.run_pipeline
```

## Principal Data Engineer Interview Narrative

“I designed the enterprise data foundation for regulated healthcare multimodal AI. The platform integrates FHIR-style patient and encounter data, labs, vitals, notes, and imaging metadata into a lakehouse architecture. It includes Glue-based ETL patterns, a gold patient-encounter table, feature engineering for multimodal modeling, SageMaker training orchestration, PII controls, model-card governance, and CI/CD readiness.”

## Production Positioning

This is a portfolio-grade reference implementation using synthetic data. The production architecture would move raw and curated data to S3, run ETL through Glue or EMR, orchestrate workflows through Step Functions or Airflow, train/register models through SageMaker, and enforce access controls, monitoring, lineage, and auditability.

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

Keep large data and models in S3, Git LFS, or release artifacts instead.
