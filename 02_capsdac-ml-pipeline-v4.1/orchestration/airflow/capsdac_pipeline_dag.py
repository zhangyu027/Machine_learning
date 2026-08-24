from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="capsdac_enrollment_forecast",
    start_date=datetime(2026, 1, 1),
    schedule="@monthly",
    catchup=False,
    tags=["capsdac", "forecast", "education-data"],
) as dag:
    validate = BashOperator(task_id="validate_raw_snapshot", bash_command="python scripts/run_capsdac_pipeline.py")
    visualize = BashOperator(task_id="generate_visualization_report", bash_command="python scripts/generate_visualization_report.py")
    validate >> visualize
