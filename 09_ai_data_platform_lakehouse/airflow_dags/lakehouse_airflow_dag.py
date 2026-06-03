"""
Airflow-style DAG skeleton for the AI Lakehouse pipeline.

This file is intentionally lightweight so the package runs locally without Airflow.
In production, these tasks would become Airflow PythonOperator tasks.
"""

from datetime import datetime

DAG_ID = "ai_data_platform_lakehouse_pipeline"
SCHEDULE = "@daily"
START_DATE = datetime(2026, 1, 1)

TASKS = [
    "generate_or_ingest_raw_events",
    "bronze_ingest",
    "silver_clean",
    "gold_certified_tables",
    "data_quality_checks",
    "feature_store_build",
    "train_mlflow_forecast_model",
    "publish_dashboard_outputs",
]


def describe_dag():
    return {
        "dag_id": DAG_ID,
        "schedule": SCHEDULE,
        "start_date": str(START_DATE),
        "tasks": TASKS,
    }


if __name__ == "__main__":
    print(describe_dag())
