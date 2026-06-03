"""Uncertainty and reliability scoring for ADMET portfolio decisions."""

from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass
class ReliabilityAssessment:
    confidence_score: float
    uncertainty_score: float
    reliability_label: str
    applicability_domain: str
    explanation: str

    def to_dict(self) -> dict:
        return asdict(self)


class UncertaintyService:
    def assess(self, prediction: dict) -> ReliabilityAssessment:
        probs = [
            prediction.get("oral_absorption_probability", 0.5),
            prediction.get("solubility_score", 0.5),
            1 - prediction.get("toxicity_risk", 0.5),
            1 - prediction.get("cyp_inhibition_risk", 0.5),
        ]
        boundary_uncertainty = 1 - min(abs(p - 0.5) for p in probs) * 2
        disagreement = max(probs) - min(probs)
        uncertainty = max(0.0, min(1.0, 0.6*boundary_uncertainty + 0.4*disagreement))
        confidence = 1 - uncertainty
        label = "high" if confidence >= 0.75 else ("medium" if confidence >= 0.55 else "low")
        domain = "inside_demo_domain" if prediction.get("drug_likeness_score", 0) >= 0.35 else "edge_of_demo_domain"
        explanation = f"Reliability is {label}; confidence={confidence:.2f}, uncertainty={uncertainty:.2f}, domain={domain}."
        return ReliabilityAssessment(confidence, uncertainty, label, domain, explanation)
