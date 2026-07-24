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

## Entity extraction and trial matching extension

```text
Clinical note
   ↓
Entity extractor
(age, diagnosis, medication, labs, hospitalization, negation)
   ↓
Structured patient profile
   ↓
Criterion engine
   ├── inclusion criteria
   └── exclusion criteria
   ↓
Matched / failed / unknown evidence
   ↓
Eligible / not eligible / needs review
   ↓
Human trial coordinator
```

The criterion engine keeps every decision traceable. Missing mandatory evidence is not silently treated as a pass; it routes the case to human review.
