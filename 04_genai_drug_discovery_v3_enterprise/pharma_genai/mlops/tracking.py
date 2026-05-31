"""MLflow-ready tracking utilities with graceful fallback."""
from __future__ import annotations
from typing import Dict, Any
import json
import os
from datetime import datetime

try:  # pragma: no cover
    import mlflow
    MLFLOW_AVAILABLE = True
except Exception:  # pragma: no cover
    mlflow = None
    MLFLOW_AVAILABLE = False


def log_run(params: Dict[str, Any], metrics: Dict[str, float], artifact_dir: str = "outputs/mlruns_fallback") -> Dict[str, Any]:
    if MLFLOW_AVAILABLE:  # pragma: no cover
        with mlflow.start_run():
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            return {"backend": "mlflow", "run_id": mlflow.active_run().info.run_id}
    os.makedirs(artifact_dir, exist_ok=True)
    path = os.path.join(artifact_dir, f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
    payload = {"backend": "json_fallback", "params": params, "metrics": metrics, "created_utc": datetime.utcnow().isoformat()}
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    payload["path"] = path
    return payload
