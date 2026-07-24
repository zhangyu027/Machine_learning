"""Deterministic ADMET prediction service for enterprise demo workflows."""

from __future__ import annotations
import math
from dataclasses import dataclass, asdict


@dataclass
class ADMETPrediction:
    smiles: str
    oral_absorption_probability: float
    bbb_penetration_probability: float
    cyp_inhibition_risk: float
    clearance_risk: float
    solubility_score: float
    toxicity_risk: float
    drug_likeness_score: float
    development_recommendation: str

    def to_dict(self) -> dict:
        return asdict(self)


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _clip(x: float) -> float:
    return float(max(0.0, min(1.0, x)))


class ADMETPredictionService:
    def _proxy_descriptors(self, smiles: str) -> dict:
        s = smiles or ""
        atoms = sum(1 for ch in s if ch.isalpha() and ch.isupper())
        hetero = sum(1 for ch in s if ch in "NOSPFClBrI")
        rings = sum(1 for ch in s if ch.isdigit())
        branches = s.count("(")
        polarity = hetero / max(atoms, 1)
        complexity = len(s) / 50.0 + rings * 0.08 + branches * 0.05
        return {"atoms": atoms, "hetero": hetero, "rings": rings, "branches": branches, "polarity": polarity, "complexity": complexity}

    def predict(self, smiles: str) -> ADMETPrediction:
        d = self._proxy_descriptors(smiles)
        oral_abs = _clip(_sigmoid(1.6 - 1.4*d["polarity"] - 0.6*d["complexity"]))
        bbb = _clip(_sigmoid(0.8 - 2.5*d["polarity"] + 0.4*d["rings"]))
        cyp = _clip(_sigmoid(-1.2 + 0.7*d["rings"] + 0.5*d["complexity"]))
        clearance = _clip(_sigmoid(-0.8 + 0.5*d["polarity"] + 0.4*d["complexity"]))
        sol = _clip(_sigmoid(1.1 + 1.5*d["polarity"] - 0.8*d["complexity"]))
        tox = _clip(_sigmoid(-1.5 + 0.8*d["complexity"] + 0.4*d["rings"]))
        drug_like = _clip(0.35*oral_abs + 0.25*sol + 0.2*(1-tox) + 0.2*(1-cyp))
        rec = "advance" if drug_like >= 0.70 and tox < 0.35 else ("review" if drug_like >= 0.50 and tox < 0.55 else "deprioritize")
        return ADMETPrediction(smiles, oral_abs, bbb, cyp, clearance, sol, tox, drug_like, rec)
