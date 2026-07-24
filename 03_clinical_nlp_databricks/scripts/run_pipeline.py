"""Run the lightweight local pipeline and build the honest model comparison.

Transformer and GPT benchmarks are explicit opt-in steps because they require downloaded
weights or external credentials. Their absent metrics remain marked as Not run.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
steps = [
    "notebooks/demo_dataset_builder.py",
    "databricks_pipeline/spark_preprocess.py",
    "nlp_models/train_baseline_tfidf.py",
    "evaluation/build_model_comparison.py",
    "evaluation/evaluate_models.py",
]
for step in steps:
    print(f"\n=== Running {step} ===")
    subprocess.run([sys.executable, str(ROOT / step)], check=True)
print("\nClinical NLP Databricks baseline pipeline completed successfully.")
print("Optional: train DistilBERT and run the GPT benchmark, then rebuild the comparison table.")
