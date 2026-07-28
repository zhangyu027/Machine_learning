"""Model-card writer for local MLOps governance demonstration."""

from __future__ import annotations

from pathlib import Path
import json
from typing import Any, Dict


def write_model_card(metrics: Dict[str, Any], path: str | Path = "outputs/model_card.json") -> None:
    card = {
        "model_name": "healthcare_multimodal_readmission_risk_demo",
        "intended_use": "Portfolio demonstration for healthcare multimodal data engineering and ML platform design.",
        "not_for_clinical_use": True,
        "limitations": [
            "Synthetic data only",
            "Not for clinical use",
            "Requires external validation before production use",
        ],
        "metrics": metrics,
        "governance": {
            "pii": "hashed identifiers in production pattern; synthetic IDs in demo data",
            "monitoring": "CloudWatch/SageMaker Model Monitor recommended for production",
            "auditability": "feature, model, and model-card artifacts are written during pipeline execution",
        },
    }
    path = Path(path)
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(card, indent=2))
