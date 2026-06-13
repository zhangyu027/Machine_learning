"""Create a reproducible evaluation summary for portfolio review."""
from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs"
METRICS_PATH = OUT_DIR / "model_metrics.json"
SUMMARY_PATH = OUT_DIR / "evaluation_summary.json"

if __name__ == "__main__":
    if not METRICS_PATH.exists():
        raise FileNotFoundError("Metrics not found. Run: python nlp_models/train_baseline_tfidf.py")
    metrics = json.loads(METRICS_PATH.read_text())
    summary = {
        "project": "03_clinical_nlp_databricks",
        "pipeline_status": "completed_successfully",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "artifacts": {
            "processed_data": "outputs/clinical_notes_processed.csv",
            "predictions": "outputs/baseline_predictions.csv",
            "metrics": "outputs/model_metrics.json",
            "model": "models/baseline_tfidf.joblib",
        },
        "metrics": metrics,
        "validation_notes": [
            "End-to-end local pipeline executed using synthetic clinical notes.",
            "Databricks-style preprocessing generated a Silver clinical NLP table.",
            "Baseline TF-IDF model trained for pipeline validation.",
            "Metrics are for portfolio demonstration and not clinical deployment.",
        ],
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2))
    print(f"Saved evaluation summary: {SUMMARY_PATH}")
