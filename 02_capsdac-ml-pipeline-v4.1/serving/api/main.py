from __future__ import annotations

from fastapi import FastAPI
from pathlib import Path
from typing import Any
import json
import pandas as pd

app = FastAPI(title="CAPSDAC V4 12-Month Forecast Serving API", version="4.0")
ROOT = Path(__file__).resolve().parents[2]


def read_json_or_status(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text())
    return {"status": "not_generated", "hint": "Run `make run` first."}


def read_csv_or_empty(path: Path) -> list[dict[str, Any]]:
    if path.exists():
        return pd.read_csv(path).to_dict(orient="records")
    return []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "capsdac-v4-forecast-api", "version": "4.0"}


@app.get("/forecasts/statewide")
def statewide_forecast() -> list[dict[str, Any]]:
    return read_csv_or_empty(ROOT / "outputs" / "forecasts" / "statewide_forecast.csv")


@app.get("/forecasts/sites")
def site_forecasts(limit: int = 25) -> list[dict[str, Any]]:
    rows = read_csv_or_empty(ROOT / "outputs" / "forecasts" / "site_forecast.csv")
    return rows[:limit]


@app.get("/forecasts/vendors/top")
def top_vendor_forecast(limit: int = 10) -> list[dict[str, Any]]:
    path = ROOT / "outputs" / "forecasts" / "vendor_forecast.csv"
    if path.exists():
        df = pd.read_csv(path)
        return df.sort_values("PredictedEnrollment", ascending=False).head(limit).to_dict(orient="records")
    return []


@app.get("/metrics/model")
def model_metrics() -> dict[str, Any]:
    return read_json_or_status(ROOT / "outputs" / "metrics" / "model_metrics.json")


@app.get("/metrics/leaderboard")
def model_leaderboard(limit: int = 10) -> list[dict[str, Any]]:
    path = ROOT / "outputs" / "metrics" / "model_leaderboard.csv"
    if path.exists():
        return pd.read_csv(path).head(limit).to_dict(orient="records")
    return []


@app.get("/monitoring/drift")
def monitoring_drift() -> dict[str, Any]:
    return read_json_or_status(ROOT / "outputs" / "reports" / "drift_report.json")


@app.get("/monitoring/retraining")
def monitoring_retraining() -> dict[str, Any]:
    return read_json_or_status(ROOT / "outputs" / "retraining" / "retraining_decision.json")


@app.get("/registry/champion")
def champion_registry() -> dict[str, Any]:
    return read_json_or_status(ROOT / "models" / "registry" / "model_registry.json")
