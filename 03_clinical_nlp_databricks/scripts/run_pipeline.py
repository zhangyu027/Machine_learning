"""Run the local end-to-end Clinical NLP Databricks demo pipeline."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
steps = [
    "notebooks/demo_dataset_builder.py",
    "databricks_pipeline/spark_preprocess.py",
    "nlp_models/train_baseline_tfidf.py",
    "evaluation/evaluate_models.py",
]
for step in steps:
    print(f"\n=== Running {step} ===")
    subprocess.run([sys.executable, str(ROOT / step)], check=True)
print("\nClinical NLP Databricks pipeline completed successfully.")
