"""Wenkel Liang-style reliability scoring and uncertainty estimation.

The design mirrors the professional idea in Wenkel Liang's background: ensemble
prediction reliability analysis for pharmaceutical ML. Here we estimate uncertainty
from descriptor-domain coverage, rule conflicts, and ensemble proxy disagreement.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List
from .featurization import MolecularFeatures
from .admet import ADMETPrediction

@dataclass
class ReliabilityScore:
    confidence_score: float
    uncertainty_score: float
    reliability_label: str
    domain_applicability: str
    ensemble_disagreement: float
    explanation: List[str]
    beta_binomial_alpha: float
    beta_binomial_beta: float

    def to_dict(self) -> Dict[str, object]: return asdict(self)

def estimate_reliability(f: MolecularFeatures, p: ADMETPrediction) -> ReliabilityScore:
    if not f.valid:
        return ReliabilityScore(0,1,"invalid","out_of_domain",1,["Invalid molecular representation"],1,10)
    penalties=[]
    domain=1.0
    checks=[(80 <= f.mol_wt <= 650, "MW outside typical small-molecule range"),
            (-2 <= f.logp <= 6, "LogP outside model comfort range"),
            (0 <= f.tpsa <= 180, "TPSA outside model comfort range"),
            (f.rotatable_bonds <= 15, "High rotatable bond count"),
            (f.heavy_atoms <= 70, "Large heavy-atom count")]
    for ok,msg in checks:
        if not ok:
            domain -= .14; penalties.append(msg)
    # uncertainty highest near decision boundaries and when toxicity/drug-likeness conflict
    boundary = min(abs(p.drug_likeness_score-.62), abs(p.overall_toxicity_risk-.45), abs(p.oral_absorption_probability-.55))
    boundary_uncertainty=max(0, .25-boundary)*1.4
    conflict=abs(p.drug_likeness_score - (1-p.overall_toxicity_risk))
    ensemble_disagreement=round(max(0,min(1, boundary_uncertainty + .20*conflict + (1-domain)*.45)),3)
    confidence=round(max(0,min(1, .52*domain + .28*(1-ensemble_disagreement) + .20*f.qed)),3)
    uncertainty=round(1-confidence,3)
    if confidence >= .75: label="high"
    elif confidence >= .50: label="moderate"
    else: label="low"
    applicability="in_domain" if domain>=.78 else ("borderline" if domain>=.55 else "out_of_domain")
    explanation=[]
    if penalties: explanation.extend(penalties)
    explanation.append(f"Reliability combines descriptor-domain coverage, decision-boundary uncertainty, and proxy ensemble disagreement={ensemble_disagreement}.")
    # Beta-binomial style pseudo-counts for uncertainty communication
    strength=20*confidence + 2
    alpha=round(1 + strength*max(.01, confidence),2)
    beta=round(1 + strength*max(.01, 1-confidence),2)
    return ReliabilityScore(confidence, uncertainty, label, applicability, ensemble_disagreement, explanation, alpha, beta)
