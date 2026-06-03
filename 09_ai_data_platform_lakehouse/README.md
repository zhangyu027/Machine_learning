# AI Data Platform / Lakehouse Project

## Project Question

**Can a modern healthcare/public-sector lakehouse improve scalable AI analytics and forecasting workflows?**

This package is tailored to Yu Zhang's background in CAPSDAC/public-sector analytics, Spark/Hadoop-style pipelines, forecasting, healthcare/public-sector governance, and data platform engineering.

---

## What This Package Includes

- Synthetic healthcare/public-sector event data
- Bronze / Silver / Gold lakehouse layers
- Local Delta-style parquet tables
- dbt-style SQL transformation models
- Airflow-style orchestration DAG
- Streaming ingestion simulator
- Data quality checks
- Governance documentation
- Feature store table
- MLflow-ready forecasting training
- Streamlit dashboard
- Jupyter notebook
- Step-by-step run guide

---

## Architecture

```text
Raw healthcare/public-sector events
        ↓
Streaming simulator
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Certified Dataset
        ↓
Feature Store
        ↓
Forecasting Model
        ↓
MLflow / Dashboard / Governance Reports
```

---

## Step-by-Step Run Instructions

### Step 1: Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run full lakehouse pipeline

```bash
python scripts/run_pipeline.py
```

This runs:

1. synthetic event generation
2. Bronze ingestion
3. Silver cleaning
4. Gold certified table creation
5. data quality checks
6. feature store creation
7. forecasting model training
8. visualization generation

### Step 4: Open notebook

```bash
jupyter notebook notebooks/AI_Data_Platform_Lakehouse_Demo.ipynb
```

### Step 5: Launch Streamlit dashboard

```bash
streamlit run app/streamlit_app.py
```

If Streamlit has watcher issues:

```bash
streamlit run app/streamlit_app.py --server.fileWatcherType none
```

### Step 6: Optional MLflow training

```bash
python ml/mlflow_train.py
```

---
```
git status
git add .
git commit -m "Add Phase 2 LSTM telemetry predictive timing upgrade"
git push origin main
``
## Outputs

### Data Lakehouse Layers

```text
data/bronze/events_bronze.parquet
data/silver/events_silver.parquet
data/gold/gold_monthly_program_demand.parquet
data/feature_store/monthly_program_features.parquet
```

### Tables

```text
outputs/tables/gold_monthly_program_demand.csv
outputs/tables/monthly_program_features.csv
outputs/tables/data_quality_report.csv
outputs/tables/forecast_model_metrics.json
outputs/tables/forecast_predictions.csv
```

### Figures

```text
outputs/figures/monthly_program_demand_trend.png
outputs/figures/actual_vs_predicted_demand.png
outputs/figures/forecast_model_metrics.png
outputs/figures/data_quality_pass_rate.png
```

### Model

```text
outputs/models/demand_forecast_model.joblib
```

---

## dbt-style Models

```text
dbt_project/models/bronze/bronze_events.sql
dbt_project/models/silver/silver_events.sql
dbt_project/models/gold/gold_monthly_program_demand.sql
```

These are included to demonstrate analytics engineering design even though the local runnable pipeline uses pandas/parquet.

---

## Airflow-style DAG

```text
airflow_dags/lakehouse_airflow_dag.py
```

This shows orchestration design without requiring local Airflow installation.

---

## Streaming Simulator

```bash
python streaming/streaming_ingestion_simulator.py
```

This simulates micro-batch ingestion similar to Kafka/Kinesis landing files.

---

## Why This Is Strong for Career Positioning

This project supports roles such as:

- Data Platform Engineer
- AI Infrastructure Engineer
- Staff Analytics Engineer
- Databricks Architect
- Healthcare AI Data Engineer
- Public-sector data platform lead

---

## Resume Bullet

Built a healthcare/public-sector AI lakehouse platform using Bronze/Silver/Gold architecture, dbt-style transformation models, Airflow-style orchestration, feature-store generation, data quality checks, governance documentation, MLflow-ready forecasting, and Streamlit reporting.
