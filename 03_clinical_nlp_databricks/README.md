# Clinical NLP + Databricks

A portfolio-ready project for clinical trial optimization using NLP on healthcare text.

## What this project demonstrates
- Spark / Databricks preprocessing for large-scale clinical text
- Baseline NLP model with TF-IDF + Logistic Regression
- Transformer-based classification with DistilBERT
- Evaluation workflows and confusion matrix analysis
- Lightweight FastAPI inference service
- Interview-ready system design story

## Use case
This project frames a realistic healthcare workflow:
- classify trial notes or patient summaries into `eligible`, `not_eligible`, or `needs_review`
- support clinical trial diagnostic optimization and coordinator triage

## Project structure
```text
03_clinical_nlp_databricks/
├── databricks_pipeline/
├── nlp_models/
├── evaluation/
├── notebooks/
├── api/
├── docs/
└── README.md
```

## Quick start

### 1. Create a GitHub-safe synthetic dataset
```bash
python notebooks/demo_dataset_builder.py
```

### 2. Run Spark preprocessing
```bash
python databricks_pipeline/spark_preprocess.py
```

### 3. Train baseline model
```bash
python nlp_models/train_baseline_tfidf.py
```

### 4. Evaluate baseline
```bash
python evaluation/evaluate_models.py
```

### 5. Train transformer model
```bash
python nlp_models/train_bert_classifier.py
```

### 6. Start inference API
```bash
uvicorn api.app:app --reload
```

## Databricks job
A sample Databricks job JSON is included in `databricks_pipeline/databricks_job_config.json`.

## Architecture
Raw notes -> Spark preprocessing -> baseline / transformer model -> evaluation -> API inference

## Interview angle
This project is strong for ML engineer / health AI interviews because it shows:
- classical NLP and modern transformer trade-offs
- Spark + Databricks workflow design
- production-oriented inference thinking
- healthcare problem framing
