"""SMILES validation utilities with optional RDKit support."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SmilesValidationResult:
    smiles: str
    is_valid: bool
    canonical_smiles: str
    method: str
    message: str


def validate_smiles(smiles: str) -> SmilesValidationResult:
    raw = (smiles or "").strip()
    if not raw:
        return SmilesValidationResult(raw, False, "", "fallback", "Empty SMILES")
    try:
        from rdkit import Chem  # type: ignore
        mol = Chem.MolFromSmiles(raw)
        if mol is None:
            return SmilesValidationResult(raw, False, "", "rdkit", "RDKit could not parse SMILES")
        return SmilesValidationResult(raw, True, Chem.MolToSmiles(mol, canonical=True), "rdkit", "Valid SMILES")
    except Exception:
        allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789[]=#()@+-\\/.")
        plausible = len(raw) >= 2 and all(ch in allowed for ch in raw)
        return SmilesValidationResult(
            raw, plausible, raw, "fallback",
            "Plausible SMILES syntax" if plausible else "Invalid characters in SMILES"
        )
