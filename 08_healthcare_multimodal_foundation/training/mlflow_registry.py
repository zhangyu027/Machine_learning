"""MLflow logging with a JSON fallback for offline portfolio execution."""
from __future__ import annotations
import json
from pathlib import Path

def log_and_register(metrics: dict, params: dict, model_path: str, model_name: str = "healthcare-multimodal-foundation") -> dict:
    try:
        import mlflow
        with mlflow.start_run() as run:
            mlflow.log_params(params); mlflow.log_metrics(metrics); mlflow.log_artifact(model_path)
            result = {"backend": "mlflow", "run_id": run.info.run_id, "model_name": model_name}
    except ImportError:
        result = {"backend": "json-fallback", "model_name": model_name, "metrics": metrics, "params": params, "model_path": model_path}
        out = Path("outputs/model_registry_record.json"); out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(result, indent=2))
    return result
