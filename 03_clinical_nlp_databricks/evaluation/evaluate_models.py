"""Create a reproducible evaluation summary for portfolio review."""
from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs"
SUMMARY_PATH = OUT_DIR / "evaluation_summary.json"


def load_optional(name: str):
    path = OUT_DIR / name
    return json.loads(path.read_text()) if path.exists() else {"status": "not_run"}


if __name__ == "__main__":
    baseline = load_optional("model_metrics.json")
    if baseline.get("status") != "completed":
        raise FileNotFoundError("Baseline metrics not found. Run the baseline pipeline first.")
    summary = {
        "project": "03_clinical_nlp_databricks",
        "pipeline_status": "completed_successfully",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "artifacts": {
            "processed_data": "outputs/clinical_notes_processed.csv",
            "baseline_predictions": "outputs/baseline_predictions.csv",
            "distilbert_predictions": "outputs/distilbert_predictions.csv (after optional training)",
            "gpt_predictions": "outputs/gpt_predictions.csv (after credentialed benchmark)",
            "comparison": "outputs/model_comparison.md",
            "baseline_model": "models/baseline_tfidf.joblib",
            "distilbert_model": "models/distilbert_clinical_eligibility/ (after optional training)",
        },
        "models": {
            "tfidf": baseline,
            "distilbert": load_optional("distilbert_metrics.json"),
            "gpt": load_optional("gpt_metrics.json"),
        },
        "validation_notes": [
            "End-to-end local baseline pipeline executed using synthetic clinical notes.",
            "DistilBERT is a real Hugging Face fine-tuning implementation and requires model-weight download.",
            "GPT evaluation requires an OpenAI-compatible endpoint and records only actual API results.",
            "The comparison builder never fabricates unavailable metrics.",
            "All results are portfolio demonstrations and are not suitable for clinical deployment.",
        ],
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2))
    print(f"Saved evaluation summary: {SUMMARY_PATH}")
