from pathlib import Path
import json
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


FEATURE_COLS = [
    "total_services_lag1",
    "total_services_rolling3",
    "avg_risk_score_lag1",
    "avg_risk_score_rolling3",
    "avg_social_need_lag1",
    "avg_social_need_rolling3",
    "total_prior_utilization_lag1",
    "total_prior_utilization_rolling3",
    "record_count",
]


def train_forecasting_model(
    feature_path="data/feature_store/monthly_program_features.parquet",
    model_path="outputs/models/demand_forecast_model.joblib",
    metrics_path="outputs/tables/forecast_model_metrics.json",
    predictions_path="outputs/tables/forecast_predictions.csv",
):
    df = pd.read_parquet(feature_path)

    X = df[FEATURE_COLS]
    y = df["target_next_month_demand"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=250,
        random_state=42,
        min_samples_leaf=2,
    )
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    metrics = {
        "mae": float(mean_absolute_error(y_test, pred)),
        "rmse": float(mean_squared_error(y_test, pred) ** 0.5),
        "r2": float(r2_score(y_test, pred)),
        "n_test": int(len(y_test)),
        "model_type": "RandomForestRegressor",
    }

    model_path = Path(model_path)
    metrics_path = Path(metrics_path)
    predictions_path = Path(predictions_path)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    pred_df = X_test.copy()
    pred_df["actual_demand"] = y_test.values
    pred_df["predicted_demand"] = pred
    pred_df.to_csv(predictions_path, index=False)

    return metrics


if __name__ == "__main__":
    print(train_forecasting_model())
