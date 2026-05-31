"""Rule-based ADMET and toxicity models for portfolio demonstration.

This module combines RDKit descriptors with transparent medicinal chemistry rules.
It is not a substitute for validated commercial ADMET models; it is a portfolio-ready
framework that can be retrained with assay labels from ChEMBL/Tox21/TDC/ADMETlab.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List
from .featurization import MolecularFeatures, featurize_smiles

def _clip(x, lo=0.0, hi=1.0): return max(lo, min(hi, x))
def _sigmoid(x):
    import math
    return 1/(1+math.exp(-x))

def _risk_label(score: float) -> str:
    if score < 0.33: return "low"
    if score < 0.66: return "medium"
    return "high"

@dataclass
class ADMETPrediction:
    smiles: str
    valid: bool
    logp: float
    tpsa: float
    mol_wt: float
    qed: float
    lipinski_violations: int
    drug_likeness_score: float
    oral_absorption_probability: float
    solubility_risk: float
    bbb_penetration_probability: float
    cyp_inhibition_risk: float
    herg_toxicity_risk: float
    hepatotoxicity_risk: float
    ames_mutagenicity_risk: float
    overall_toxicity_risk: float
    development_priority: str
    notes: List[str]

    def to_dict(self) -> Dict[str, object]: return asdict(self)

def lipinski_violations(f: MolecularFeatures) -> int:
    return int(f.mol_wt > 500) + int(f.logp > 5) + int(f.hbd > 5) + int(f.hba > 10)

def predict_admet_from_features(f: MolecularFeatures) -> ADMETPrediction:
    if not f.valid:
        return ADMETPrediction(f.smiles, False, f.logp, f.tpsa, f.mol_wt, f.qed, 99, 0, 0, 1, 0, 1, 1, 1, 1, 1, "invalid", [f.error or "Invalid SMILES"])
    violations=lipinski_violations(f)
    notes=[]
    if violations: notes.append(f"Lipinski violations: {violations}")
    if f.tpsa > 140: notes.append("High TPSA may reduce permeability")
    if f.logp > 5: notes.append("High lipophilicity may increase toxicity/poor solubility")
    if f.mol_wt > 500: notes.append("High molecular weight may reduce oral drug-likeness")
    if f.qed >= .65: notes.append("Favorable QED-like profile")
    drug_like = _clip(0.42*f.qed + 0.18*(1-violations/4) + 0.16*_clip(1-abs(f.logp-2.5)/5) + 0.14*_clip(1-f.tpsa/180) + 0.10*_clip(1-f.rotatable_bonds/12))
    oral_abs = _clip(_sigmoid(2.2 - 0.016*f.tpsa - 0.003*max(f.mol_wt-350,0) - .45*violations + .18*f.logp))
    sol_risk = _clip(_sigmoid(-2.0 + .42*f.logp + .004*max(f.mol_wt-300,0) - .015*f.tpsa + .12*f.aromatic_rings))
    bbb = _clip(_sigmoid(1.4 + .46*f.logp - .035*f.tpsa - .005*max(f.mol_wt-300,0) - .35*f.hbd))
    cyp = _clip(_sigmoid(-2.1 + .52*f.logp + .18*f.aromatic_rings + .08*f.halogen_count + .002*f.mol_wt))
    herg = _clip(_sigmoid(-3.0 + .55*f.logp + .25*f.aromatic_rings + .005*f.mol_wt + .12*f.formal_charge))
    hepato = _clip(_sigmoid(-2.4 + .45*f.logp + .12*f.halogen_count + .18*f.aromatic_rings + .003*max(f.mol_wt-250,0)))
    # crude structural-alert proxy when no SMARTS model available
    ames = _clip(_sigmoid(-2.5 + .22*f.hetero_atom_count + .35*f.aromatic_rings + .18*f.halogen_count))
    tox = _clip(.35*herg + .30*hepato + .20*ames + .15*cyp)
    priority = "advance" if drug_like >= .62 and tox < .45 and oral_abs > .55 else ("review" if drug_like >= .42 and tox < .70 else "deprioritize")
    return ADMETPrediction(f.smiles, True, f.logp, f.tpsa, f.mol_wt, f.qed, violations, round(drug_like,3), round(oral_abs,3), round(sol_risk,3), round(bbb,3), round(cyp,3), round(herg,3), round(hepato,3), round(ames,3), round(tox,3), priority, notes)

def predict_admet(smiles: str) -> ADMETPrediction:
    return predict_admet_from_features(featurize_smiles(smiles))
