"""
MLflow-ready training script.

This runs the same model and logs metrics/artifacts if MLflow is available.
"""

import mlflow
from ml.train_forecast_model import train_forecasting_model


def main():
    with mlflow.start_run(run_name="lakehouse_demand_forecast"):
        metrics = train_forecasting_model()
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                mlflow.log_metric(key, value)
        mlflow.log_artifact("outputs/tables/forecast_predictions.csv")
        mlflow.log_artifact("outputs/tables/forecast_model_metrics.json")
        print(metrics)


if __name__ == "__main__":
    main()
