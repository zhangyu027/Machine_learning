"""Transformer training placeholder for Databricks/SageMaker extension.

This portfolio package keeps the local demo lightweight. In production, this step can
be replaced by a Databricks or SageMaker training job using a clinical transformer.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "bert_training_plan.json"
OUT.parent.mkdir(parents=True, exist_ok=True)
plan = {
    "status": "placeholder_created",
    "reason": "Local portfolio demo avoids downloading large transformer weights.",
    "production_extension": [
        "Use Hugging Face clinical transformer or domain-adapted BERT model.",
        "Register trained model in MLflow Model Registry.",
        "Deploy batch or real-time inference through Databricks Jobs or model serving.",
    ],
}
OUT.write_text(json.dumps(plan, indent=2))
print(f"Saved transformer training plan: {OUT}")
