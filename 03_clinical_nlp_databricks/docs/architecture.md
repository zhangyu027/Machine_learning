# Clinical NLP Databricks Lakehouse Architecture

This project demonstrates a Databricks-style healthcare NLP data engineering workflow.

```text
Synthetic clinical notes
        ↓
Bronze/raw dataset
        ↓
Silver preprocessing and text standardization
        ↓
Gold/NLP feature table
        ↓
Baseline model training and evaluation
        ↓
API inference and governance artifacts
```

## Data Engineering Focus

- Reproducible local pipeline
- Spark-compatible preprocessing
- Synthetic healthcare text data
- Evaluation summary for auditability
- Lightweight API endpoint for model serving demonstration
