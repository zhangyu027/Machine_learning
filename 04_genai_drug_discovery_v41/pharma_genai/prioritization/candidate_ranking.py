"""Transparent multi-objective candidate prioritization."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping
import numpy as np

@dataclass(frozen=True)
class PriorityWeights:
    utility: float = 1.0
    uncertainty: float = 0.35
    ood_risk: float = 0.30
    toxicity: float = 0.50


def candidate_priority_score(
    predictions: Mapping[str, float],
    uncertainty: float,
    nearest_similarity: float,
    weights: PriorityWeights = PriorityWeights(),
) -> float:
    absorption = float(predictions.get("oral_absorption_probability", 0.0))
    solubility = float(predictions.get("solubility_score", 0.0))
    likeness = float(predictions.get("drug_likeness_score", 0.0))
    toxicity = float(predictions.get("overall_toxicity_risk", 1.0))
    utility = np.mean([absorption, solubility, likeness])
    ood_risk = 1.0 - float(np.clip(nearest_similarity, 0.0, 1.0))
    score = weights.utility * utility - weights.uncertainty * uncertainty - weights.ood_risk * ood_risk - weights.toxicity * toxicity
    return round(float(score), 4)


def recommendation(score: float, applicability_label: str, toxicity: float) -> str:
    if toxicity >= 0.60:
        return "DEPRIORITIZE"
    if applicability_label == "out_of_domain":
        return "REVIEW"
    if score >= 0.35 and applicability_label == "in_domain":
        return "ADVANCE"
    return "REVIEW"
