"""Chemical applicability-domain analysis using nearest-neighbor Tanimoto similarity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import numpy as np
from ..featurization import morgan_fingerprint


def tanimoto_similarity(a, b) -> float:
    aa = np.asarray(a, dtype=bool); bb = np.asarray(b, dtype=bool)
    union = np.logical_or(aa, bb).sum()
    return float(np.logical_and(aa, bb).sum() / union) if union else 1.0


@dataclass(frozen=True)
class ApplicabilityResult:
    nearest_similarity: float
    label: str
    nearest_training_smiles: str


class ApplicabilityDomain:
    def __init__(self, training_smiles: Sequence[str], n_bits: int = 256, in_domain: float = 0.55, borderline: float = 0.35):
        if not training_smiles:
            raise ValueError("training_smiles cannot be empty")
        self.training_smiles = list(training_smiles)
        self.n_bits = n_bits
        self.in_domain = in_domain
        self.borderline = borderline
        self._fps = [morgan_fingerprint(s, n_bits=n_bits) for s in self.training_smiles]

    def assess(self, smiles: str) -> ApplicabilityResult:
        fp = morgan_fingerprint(smiles, n_bits=self.n_bits)
        sims = [tanimoto_similarity(fp, train_fp) for train_fp in self._fps]
        best = int(np.argmax(sims)); score = float(sims[best])
        label = "in_domain" if score >= self.in_domain else "borderline" if score >= self.borderline else "out_of_domain"
        return ApplicabilityResult(round(score, 4), label, self.training_smiles[best])
