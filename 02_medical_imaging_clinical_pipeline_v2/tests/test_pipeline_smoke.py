from pathlib import Path
import subprocess
import sys


def test_pipeline_smoke():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run([sys.executable, "scripts/run_pipeline.py"], cwd=root, capture_output=True, text=True, check=True)
    assert "completed successfully" in result.stdout
    assert (root / "outputs" / "tables" / "gold_patient_imaging_features.csv").exists()
    assert (root / "evaluation" / "evaluation_summary.json").exists()
