# CAPSDAC Level 3 Architecture

```text
Monthly snapshot arrives
        ↓
Data contract validation
        ↓
Feature store build
        ↓
3-month-ahead target creation
        ↓
Expanding-window model comparison
        ↓
Local MLflow-style experiment tracking
        ↓
Champion/challenger registry decision
        ↓
Forecast publication
        ↓
Drift monitoring + retraining decision
        ↓
FastAPI + Streamlit dashboard
```

## Production mapping

| Demo component | Production equivalent |
|---|---|
| CSV sample data | Data Lake / BigQuery / Snowflake tables |
| Local feature file | Feature store or governed curated table |
| Local run artifacts | MLflow Tracking or Vertex AI Experiments |
| Local model registry | MLflow Registry or Vertex AI Model Registry |
| Manual make command | Airflow, Cloud Composer, GitHub Actions, or Cloud Build |
| Streamlit dashboard | Internal monitoring dashboard or BI reporting |
| FastAPI local app | Containerized service on Cloud Run, GKE, or App Service |
```
