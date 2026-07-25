"""Backward-compatible V1 wrapper around the V2 pipeline."""
from __future__ import annotations
import pandas as pd
from .pipeline import analyze_many

class ADMETReliabilityEnsemble:
    """Small sklearn-like wrapper retained for the original project tests.

    V2 does not require fitting for the transparent demo scorer, but fit() stores the
    training SMILES count so the API remains compatible.
    """
    def __init__(self):
        self.training_size = 0
    def fit(self, smiles):
        self.training_size = len(list(smiles))
        return self
    def predict(self, smiles):
        df = analyze_many(smiles)
        return pd.DataFrame({
            "smiles": df["smiles"],
            "admet_score": df["drug_likeness_score"],
            "uncertainty": df["uncertainty_score"],
            "reliability": df["reliability_label"],
        })
