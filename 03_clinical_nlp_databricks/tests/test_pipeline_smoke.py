from pathlib import Path
import json
import subprocess
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_runs_end_to_end():
    subprocess.run([sys.executable, str(ROOT / "scripts" / "run_pipeline.py")], check=True)
    assert (ROOT / "outputs" / "clinical_notes_processed.csv").exists()
    assert (ROOT / "outputs" / "model_metrics.json").exists()
    assert (ROOT / "outputs" / "evaluation_summary.json").exists()
    assert (ROOT / "outputs" / "model_comparison.csv").exists()
    assert (ROOT / "models" / "baseline_tfidf.joblib").exists()
    metrics = json.loads((ROOT / "outputs" / "model_metrics.json").read_text())
    assert "eligible_recall" in metrics
    assert "latency_ms_per_note" in metrics
    comparison = pd.read_csv(ROOT / "outputs" / "model_comparison.csv")
    assert comparison["Model"].tolist() == ["TF-IDF", "DistilBERT", "GPT"]
    assert comparison.loc[comparison.Model == "DistilBERT", "Status"].iloc[0] in {"not_run", "completed"}
