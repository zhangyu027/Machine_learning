"""Uncertainty and reliability utilities for V3.

V3 combines three concepts commonly expected in pharmaceutical modeling:
1. Applicability domain: are descriptors inside the training-like region?
2. Decision-boundary uncertainty: is the prediction close to the decision threshold?
3. Proxy ensemble disagreement: do different model views disagree?
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import math
import numpy as np


@dataclass
class ReliabilityResult:
    confidence_score: float
    uncertainty_score: float
    reliability_label: str
    domain_applicability: float
    ensemble_disagreement: float
    explanation: List[str]


def sigmoid(x: float) -> float:
    return float(1.0 / (1.0 + math.exp(-x)))


def descriptor_domain_score(desc: Dict[str, float]) -> float:
    ranges = {
        "mw": (150, 650),
        "logp": (-1.0, 6.0),
        "tpsa": (20, 160),
        "hbd": (0, 6),
        "hba": (0, 12),
        "rotatable_bonds": (0, 12),
    }
    scores = []
    for key, (lo, hi) in ranges.items():
        val = float(desc.get(key, 0.0))
        if lo <= val <= hi:
            scores.append(1.0)
        else:
            center = (lo + hi) / 2.0
            width = (hi - lo) / 2.0
            scores.append(float(np.exp(-abs(val - center) / max(width, 1.0))))
    return float(np.clip(np.mean(scores), 0.0, 1.0))


def proxy_ensemble_predictions(desc: Dict[str, float]) -> Dict[str, List[float]]:
    mw = desc.get("mw", 0.0)
    logp = desc.get("logp", 0.0)
    tpsa = desc.get("tpsa", 0.0)
    hbd = desc.get("hbd", 0.0)
    hba = desc.get("hba", 0.0)
    qed = desc.get("qed_like", 0.5)
    absorption_views = [
        sigmoid(2.2 - 0.012 * max(0, tpsa - 80) - 0.22 * max(0, hbd - 3) + 0.7 * qed),
        sigmoid(1.7 - 0.008 * max(0, mw - 450) - 0.2 * max(0, hba - 8) + 0.3 * logp),
        sigmoid(2.0 - 0.16 * abs(logp - 2.5) - 0.006 * max(0, tpsa - 100)),
    ]
    tox_views = [
        sigmoid(-2.0 + 0.35 * max(0, logp - 4) + 0.003 * max(0, mw - 500)),
        sigmoid(-2.4 + 0.018 * max(0, tpsa - 140) + 0.2 * max(0, hba - 10)),
        sigmoid(-1.8 + 0.5 * max(0, 0.35 - qed)),
    ]
    return {"oral_absorption": absorption_views, "toxicity": tox_views}


def conformal_interval(point: float, uncertainty: float, alpha: float = 0.1) -> Dict[str, float]:
    """A lightweight conformal-style interval for bounded probabilities."""
    margin = float(np.clip(1.64 * uncertainty * (1.0 - alpha), 0.03, 0.45))
    return {"lower": float(np.clip(point - margin, 0.0, 1.0)), "upper": float(np.clip(point + margin, 0.0, 1.0)), "alpha": alpha}


def reliability_from_predictions(desc: Dict[str, float], predictions: Dict[str, float]) -> ReliabilityResult:
    ensembles = proxy_ensemble_predictions(desc)
    disagreement = float(np.mean([np.std(vals) for vals in ensembles.values()]))
    domain = descriptor_domain_score(desc)
    boundary_uncertainty = float(np.mean([1.0 - abs(float(v) - 0.5) * 2.0 for v in predictions.values() if 0 <= float(v) <= 1]))
    uncertainty = float(np.clip(0.45 * (1.0 - domain) + 0.35 * disagreement + 0.20 * boundary_uncertainty, 0.0, 1.0))
    confidence = float(np.clip(1.0 - uncertainty, 0.0, 1.0))
    label = "high" if confidence >= 0.78 else "medium" if confidence >= 0.55 else "low"
    explanation = []
    if domain < 0.75:
        explanation.append("Descriptor values are partially outside the model applicability domain.")
    if disagreement > 0.18:
        explanation.append("Proxy ensemble views disagree; experimental validation should be prioritized.")
    if boundary_uncertainty > 0.55:
        explanation.append("Prediction sits near a decision boundary.")
    explanation.append(f"Reliability combines domain coverage={domain:.3f}, ensemble disagreement={disagreement:.3f}, and boundary uncertainty={boundary_uncertainty:.3f}.")
    return ReliabilityResult(round(confidence, 3), round(uncertainty, 3), label, round(domain, 3), round(disagreement, 3), explanation)
