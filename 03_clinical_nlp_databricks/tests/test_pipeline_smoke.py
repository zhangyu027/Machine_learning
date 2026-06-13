from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_pipeline_runs_end_to_end():
    subprocess.run([sys.executable, str(ROOT / "scripts" / "run_pipeline.py")], check=True)
    assert (ROOT / "outputs" / "clinical_notes_processed.csv").exists()
    assert (ROOT / "outputs" / "model_metrics.json").exists()
    assert (ROOT / "outputs" / "evaluation_summary.json").exists()
    assert (ROOT / "models" / "baseline_tfidf.joblib").exists()
