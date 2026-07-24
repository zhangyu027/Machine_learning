"""Explainability layer with optional SHAP support and deterministic fallback."""
from __future__ import annotations
from typing import Dict, List
import numpy as np

try:  # pragma: no cover
    import shap
    SHAP_AVAILABLE = True
except Exception:  # pragma: no cover
    shap = None
    SHAP_AVAILABLE = False

FEATURES = ["mw", "logp", "hbd", "hba", "tpsa", "rotatable_bonds", "qed_like"]


def fallback_feature_importance(descriptors: Dict[str, float], task: str = "overall_toxicity_risk") -> List[Dict[str, object]]:
    """Human-readable attribution using distance from ideal medicinal chemistry ranges."""
    ideal = {"mw": 350, "logp": 2.5, "hbd": 2, "hba": 5, "tpsa": 75, "rotatable_bonds": 5, "qed_like": 0.8}
    scale = {"mw": 250, "logp": 3, "hbd": 4, "hba": 7, "tpsa": 100, "rotatable_bonds": 8, "qed_like": 0.6}
    rows = []
    for f in FEATURES:
        value = float(descriptors.get(f, 0.0))
        direction = "risk_increase" if f != "qed_like" else "risk_decrease"
        score = abs(value - ideal[f]) / scale[f]
        if f == "qed_like":
            score = max(0.0, ideal[f] - value) / scale[f]
        rows.append({"feature": f, "value": round(value, 3), "attribution": round(float(score), 3), "direction": direction, "task": task})
    return sorted(rows, key=lambda x: x["attribution"], reverse=True)


def shap_ready_notice() -> str:
    if SHAP_AVAILABLE:
        return "SHAP is installed. Replace fallback model functions with trained model objects to compute SHAP values."
    return "SHAP is optional. Current output uses deterministic medicinal-chemistry attribution fallback."
