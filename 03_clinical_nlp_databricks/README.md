# 03 Clinical NLP Databricks Lakehouse Pipeline

**Principal Data Engineer Edition**

This project demonstrates a Databricks-style clinical NLP lakehouse pipeline for healthcare AI platform interviews. It is designed to be runnable locally with synthetic data while showing production-oriented Data Engineering patterns.

## What This Demonstrates

- Bronze-to-Silver clinical text preprocessing
- Spark-compatible transformation logic with local fallback
- Synthetic clinical trial screening dataset generation
- TF-IDF baseline model for pipeline validation
- Reproducible evaluation artifacts
- Lightweight FastAPI inference service
- Databricks job configuration skeleton
- Healthcare AI governance and interview narrative

## Folder Structure

```text
databricks_pipeline/      Spark-compatible preprocessing and job config
nlp_models/              Baseline TF-IDF and transformer extension placeholder
evaluation/              Evaluation summary generation
notebooks/               Synthetic dataset builder
api/                     FastAPI inference service
docs/                    Architecture and interview narrative
tests/                   Pytest smoke test
scripts/                 End-to-end local pipeline runner
data/sample/             Synthetic demo data generated locally
outputs/                 Generated validation artifacts
models/                  Local model artifact
```

## Quick Start

From the project root:

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
pytest -q
```

Or run each step individually:

```bash
python notebooks/demo_dataset_builder.py
python databricks_pipeline/spark_preprocess.py
# Optional Spark execution: USE_PYSPARK=1 python databricks_pipeline/spark_preprocess.py
python nlp_models/train_baseline_tfidf.py
python evaluation/evaluate_models.py
python nlp_models/train_bert_classifier.py
```

Start the API after training:

```bash
uvicorn api.app:app --reload
```

## Generated Artifacts

```text
outputs/clinical_notes_processed.csv
outputs/baseline_predictions.csv
outputs/model_metrics.json
outputs/evaluation_summary.json
models/baseline_tfidf.joblib
```

## Data Engineer Interview Narrative

“I built a Databricks-style clinical NLP lakehouse pipeline. The system generates synthetic healthcare notes, performs Spark-compatible Silver preprocessing, trains a baseline NLP model, generates evaluation artifacts, and exposes an API for inference. The project emphasizes reusable data pipelines, validation artifacts, model governance, and production-oriented healthcare AI architecture.”

## Production Positioning

In production, the raw notes would be ingested to cloud object storage, curated through Databricks Delta Lake Bronze/Silver/Gold tables, tracked with MLflow, scheduled through Databricks Jobs or Airflow, and deployed through model serving or batch inference. Governance would include PII controls, data lineage, audit logs, model cards, and evaluation summaries.

## GitHub Cleanup

Do not commit:

```text
.venv/
__pycache__/
.pytest_cache/
.DS_Store
large raw data
trained checkpoints
*.zip
```
