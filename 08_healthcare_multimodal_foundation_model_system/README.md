# 08 Healthcare Multimodal Foundation Model System

**Merged Principal Data Engineer Edition**

This package merges the original #08 folder structure:

```text
app/
data/
docs/
notebooks/
scripts/
src/
tests/
```

with the Principal Data Engineer upgrade layer:

```text
aws/
  glue_jobs/
  sagemaker/
  step_functions/
  terraform/
executive_materials/
.github/workflows/
```

## Purpose

This project is designed for **Principal Data Engineer / AWS Senior Data Engineer / Healthcare AI Platform** interviews.

It demonstrates how to build the enterprise data foundation for multimodal healthcare AI:

- FHIR-style patient and encounter data
- Labs, vitals, clinical notes, and imaging metadata
- S3 lakehouse architecture
- Glue ETL to gold patient-encounter tables
- Multimodal feature engineering
- SageMaker training and model registry design
- PII controls and healthcare governance
- CI/CD and infrastructure-as-code skeleton

## Why Merge Instead of Keeping V1/V2 Separately

The Principal DE package is not a separate product. It is an architectural upgrade to the same healthcare multimodal AI system.

Keeping one folder is clearer for recruiters:

```text
08_healthcare_multimodal_foundation_model_system
```

rather than:

```text
08_healthcare_multimodal_foundation_model_system
08_healthcare_multimodal_foundation_model_system_v2
```

## Local Demo

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
pytest -q
```

## Principal Data Engineer Interview Narrative

“I designed the enterprise data foundation for regulated healthcare multimodal AI. The platform integrates FHIR-style patient and encounter data, labs, vitals, notes, and imaging metadata into a lakehouse architecture. It includes Glue-based ETL patterns, a gold patient-encounter table, feature engineering for multimodal modeling, SageMaker training orchestration, PII controls, model-card governance, and CI/CD readiness.”

## Recommended GitHub Cleanup

Do not commit:

```text
.venv/
__pycache__/
.pytest_cache/
large raw images
trained checkpoints
outputs/
*.zip
```

Keep large data and models in S3, Git LFS, or release artifacts instead.
