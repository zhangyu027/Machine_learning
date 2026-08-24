"""Forecast monitoring utilities for CAPSDAC.

Tracks distribution shift and simple forecast-output guardrails. This is a
starter suitable for Cloud Scheduler + Cloud Run Job, Composer, or Vertex AI
Model Monitoring integration.
"""
from __future__ import annotations

from pathlib import Path
import json
import pandas as pd


def compare_forecast_totals(previous: pd.DataFrame, current: pd.DataFrame) -> dict:
    prev_total = float(previous["PredictedEnrollment"].sum())
    cur_total = float(current["PredictedEnrollment"].sum())
    pct_change = (cur_total - prev_total) / max(prev_total, 1.0)
    return {
        "previous_total": prev_total,
        "current_total": cur_total,
        "pct_change": pct_change,
        "alert": abs(pct_change) > 0.15,
    }


def monitor_outputs(output_dir: str = "outputs/forecasts") -> dict:
    out = Path(output_dir)
    statewide = out / "statewide_forecast.csv"
    vendor = out / "vendor_forecast.csv"
    result = {"statewide_exists": statewide.exists(), "vendor_exists": vendor.exists()}
    if vendor.exists():
        df = pd.read_csv(vendor)
        result.update({
            "vendor_rows": int(len(df)),
            "min_prediction": float(df["PredictedEnrollment"].min()),
            "max_prediction": float(df["PredictedEnrollment"].max()),
            "negative_prediction_alert": bool((df["PredictedEnrollment"] < 0).any()),
        })
    return result


if __name__ == "__main__":
    metrics = monitor_outputs()
    Path("outputs/metrics").mkdir(parents=True, exist_ok=True)
    Path("outputs/metrics/monitoring_summary.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))
