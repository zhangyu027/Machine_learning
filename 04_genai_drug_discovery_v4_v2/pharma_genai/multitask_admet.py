"""Multi-task ADMET and toxicity prediction layer.

This module is intentionally deployable without proprietary training data. It uses
transparent calibrated proxy functions for demonstration and can be swapped with
real scikit-learn, PyTorch, or GNN models in production.
"""
from __future__ import annotations
from dataclasses import asdict
from typing import Dict, List, Sequence
import numpy as np

from .featurization import calculate_descriptors, morgan_fingerprint, is_valid_smiles
from .uncertainty import sigmoid, reliability_from_predictions, conformal_interval


TASKS = [
    "oral_absorption_probability",
    "bbb_penetration_probability",
    "cyp_inhibition_risk",
    "clearance_risk",
    "solubility_score",
    "overall_toxicity_risk",
    "drug_likeness_score",
]


class MultiTaskADMETPredictor:
    """V3 multi-task ADMET predictor with uncertainty-aware outputs."""
    def __init__(self, model_name: str = "v4_principal_multitask_admet") -> None:
        self.model_name = model_name

    def predict_one(self, smiles: str) -> Dict[str, object]:
        desc = calculate_descriptors(smiles)
        valid = is_valid_smiles(smiles)
        mw = desc.get("mw", 0.0)
        logp = desc.get("logp", 0.0)
        tpsa = desc.get("tpsa", 0.0)
        hbd = desc.get("hbd", 0.0)
        hba = desc.get("hba", 0.0)
        rot = desc.get("rotatable_bonds", 0.0)
        qed = desc.get("qed_like", 0.5)
        fp_density = float(np.mean(morgan_fingerprint(smiles, 128)))
        preds = {
            "oral_absorption_probability": sigmoid(2.4 + 1.2*qed - 0.010*max(0, tpsa-85) - 0.18*max(0, hbd-3) - 0.004*max(0, mw-500)),
            "bbb_penetration_probability": sigmoid(1.4 + 0.25*logp - 0.018*tpsa - 0.20*hbd - 0.002*max(0, mw-400)),
            "cyp_inhibition_risk": sigmoid(-2.2 + 0.45*max(0, logp-3.2) + 0.002*max(0, mw-380) + 1.6*fp_density),
            "clearance_risk": sigmoid(-1.4 + 0.006*max(0, mw-450) + 0.10*max(0, rot-6) + 0.05*max(0, hba-8)),
            "solubility_score": sigmoid(1.9 - 0.45*max(0, logp-2.5) - 0.004*max(0, mw-350) + 0.007*min(tpsa, 120)),
            "overall_toxicity_risk": sigmoid(-2.4 + 0.5*max(0, logp-4.0) + 0.003*max(0, mw-500) + 0.55*max(0, 0.55-qed)),
            "drug_likeness_score": float(np.clip(qed, 0.0, 1.0)),
        }
        reliability = reliability_from_predictions(desc, {
            "oral_absorption": preds["oral_absorption_probability"],
            "toxicity": preds["overall_toxicity_risk"],
            "drug_likeness": preds["drug_likeness_score"],
        })
        intervals = {k + "_interval": conformal_interval(float(v), reliability.uncertainty_score) for k, v in preds.items()}
        priority = self._priority(preds, reliability.confidence_score, valid)
        notes = self._notes(desc, preds, valid)
        out = {"smiles": smiles, **desc, "valid_smiles": bool(valid), **{k: round(float(v), 3) for k, v in preds.items()}, **intervals}
        out.update({
            "development_priority": priority,
            "confidence_score": reliability.confidence_score,
            "uncertainty_score": reliability.uncertainty_score,
            "reliability_label": reliability.reliability_label,
            "domain_applicability": reliability.domain_applicability,
            "ensemble_disagreement": reliability.ensemble_disagreement,
            "reliability_explanation": reliability.explanation,
            "notes": notes,
            "model_name": self.model_name,
        })
        return out

    def predict_many(self, smiles_list: Sequence[str]) -> List[Dict[str, object]]:
        rows = [self.predict_one(s) for s in smiles_list]
        return sorted(rows, key=lambda r: (r["development_priority"] != "advance", -float(r["drug_likeness_score"]), float(r["overall_toxicity_risk"])))

    @staticmethod
    def _priority(preds: Dict[str, float], confidence: float, valid: bool) -> str:
        if not valid:
            return "reject"
        if preds["overall_toxicity_risk"] > 0.55 or preds["drug_likeness_score"] < 0.35:
            return "deprioritize"
        if confidence < 0.55:
            return "review"
        if preds["oral_absorption_probability"] > 0.55 and preds["drug_likeness_score"] > 0.55 and preds["overall_toxicity_risk"] < 0.35:
            return "advance"
        return "review"

    @staticmethod
    def _notes(desc: Dict[str, float], preds: Dict[str, float], valid: bool) -> List[str]:
        notes: List[str] = []
        if not valid:
            notes.append("Invalid or unsupported SMILES; do not use for scientific decision making.")
        if desc.get("mw", 0) > 500:
            notes.append("High molecular weight may reduce oral developability.")
        if desc.get("tpsa", 0) > 120:
            notes.append("High TPSA may reduce membrane permeability.")
        if desc.get("logp", 0) > 5:
            notes.append("High LogP may increase lipophilicity-driven toxicity risk.")
        if preds["cyp_inhibition_risk"] > 0.5:
            notes.append("CYP inhibition risk should be experimentally assessed.")
        if preds["drug_likeness_score"] >= 0.7:
            notes.append("Favorable QED-like profile.")
        return notes or ["No major heuristic alerts detected."]
