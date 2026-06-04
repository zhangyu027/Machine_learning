from pathlib import Path
import json

def write_model_card(metrics, path="outputs/model_card.json"):
    card = {
        "model_name": "healthcare_multimodal_readmission_risk_demo",
        "intended_use": "Portfolio demonstration for healthcare multimodal data engineering and ML platform design.",
        "limitations": ["Synthetic data only", "Not for clinical use", "Requires external validation before production use"],
        "metrics": metrics,
        "governance": {"pii": "hashed identifiers", "monitoring": "CloudWatch/SageMaker Model Monitor recommended"}
    }
    Path(path).parent.mkdir(exist_ok=True)
    Path(path).write_text(json.dumps(card, indent=2))
