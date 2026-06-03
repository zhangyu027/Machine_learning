"""Molecular feature engineering for V2/V3.

The module uses RDKit when available and deterministic proxy descriptors when RDKit
is not installed. This design keeps the portfolio project deployable on Streamlit
Cloud while supporting real cheminformatics environments.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
import re
from typing import Dict, List, Sequence

import numpy as np

try:  # pragma: no cover - depends on optional runtime
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors, QED, AllChem
    RDKIT_AVAILABLE = True
except Exception:  # pragma: no cover
    Chem = None
    Descriptors = Crippen = rdMolDescriptors = QED = AllChem = None
    RDKIT_AVAILABLE = False

ATOM_PATTERN = re.compile(r"Cl|Br|[BCNOFPSI]|[cnosp]|\[[^\]]+\]")


def is_valid_smiles_proxy(smiles: str) -> bool:
    """Lightweight SMILES validity check used when RDKit is absent."""
    if not isinstance(smiles, str) or not smiles.strip():
        return False
    if smiles.count("(") != smiles.count(")"):
        return False
    if any(ch in smiles for ch in [" ", "\t", "\n"]):
        return False
    return bool(ATOM_PATTERN.search(smiles))


def is_valid_smiles(smiles: str) -> bool:
    if RDKIT_AVAILABLE:
        return Chem.MolFromSmiles(smiles) is not None
    return is_valid_smiles_proxy(smiles)


def _stable_float(seed: str, low: float, high: float) -> float:
    value = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12], 16)
    return low + (value / float(16**12 - 1)) * (high - low)


def proxy_descriptors(smiles: str) -> Dict[str, float]:
    """Deterministic chemistry-inspired descriptors for demo/fallback mode."""
    atoms = ATOM_PATTERN.findall(smiles or "")
    heavy_atoms = max(len(atoms), 1)
    hetero = sum(1 for atom in atoms if any(x in atom for x in ["N", "O", "S", "P", "n", "o", "s"]))
    carbons = sum(1 for atom in atoms if atom in ["C", "c"])
    rings = sum(ch.isdigit() for ch in smiles) / 2.0
    branches = smiles.count("(")
    aromatic = sum(1 for atom in atoms if atom in ["c", "n", "o", "s"])
    mw = 12.01 * carbons + 14.01 * sum("N" in a or a == "n" for a in atoms) + 16.0 * sum("O" in a or a == "o" for a in atoms) + 35.45 * sum("Cl" in a for a in atoms) + 79.9 * sum("Br" in a for a in atoms)
    if mw <= 0:
        mw = 18.0 * heavy_atoms
    logp = 0.54 * carbons - 0.8 * hetero + 0.25 * aromatic + _stable_float(smiles + "logp", -0.35, 0.35)
    tpsa = 12.0 * hetero + 5.0 * branches + _stable_float(smiles + "tpsa", 0, 10)
    hbd = max(0, smiles.count("N") + smiles.count("O") - smiles.count("=O") - smiles.count("n"))
    hba = max(0, smiles.count("N") + smiles.count("O") + smiles.count("n") + smiles.count("o"))
    rot = max(0, heavy_atoms - rings * 2 - branches - 4)
    qed_like = _qed_like(mw, logp, hbd, hba, tpsa, rot)
    return {
        "valid_smiles": float(is_valid_smiles_proxy(smiles)),
        "mw": round(mw, 3),
        "logp": round(logp, 3),
        "hbd": float(hbd),
        "hba": float(hba),
        "tpsa": round(tpsa, 3),
        "rotatable_bonds": float(rot),
        "heavy_atoms": float(heavy_atoms),
        "ring_count": float(rings),
        "aromatic_atoms": float(aromatic),
        "qed_like": round(qed_like, 3),
    }


def _qed_like(mw: float, logp: float, hbd: float, hba: float, tpsa: float, rot: float) -> float:
    components = [
        math.exp(-((mw - 350) / 260) ** 2),
        math.exp(-((logp - 2.4) / 2.2) ** 2),
        1.0 / (1.0 + max(0.0, hbd - 3.0)),
        1.0 / (1.0 + max(0.0, hba - 7.0) / 2.0),
        math.exp(-((tpsa - 70) / 90) ** 2),
        1.0 / (1.0 + max(0.0, rot - 8.0) / 3.0),
    ]
    return float(np.clip(np.mean(components), 0.0, 1.0))


def rdkit_descriptors(smiles: str) -> Dict[str, float]:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        d = proxy_descriptors(smiles)
        d["valid_smiles"] = 0.0
        return d
    return {
        "valid_smiles": 1.0,
        "mw": float(Descriptors.MolWt(mol)),
        "logp": float(Crippen.MolLogP(mol)),
        "hbd": float(rdMolDescriptors.CalcNumHBD(mol)),
        "hba": float(rdMolDescriptors.CalcNumHBA(mol)),
        "tpsa": float(rdMolDescriptors.CalcTPSA(mol)),
        "rotatable_bonds": float(rdMolDescriptors.CalcNumRotatableBonds(mol)),
        "heavy_atoms": float(mol.GetNumHeavyAtoms()),
        "ring_count": float(rdMolDescriptors.CalcNumRings(mol)),
        "aromatic_atoms": float(sum(1 for a in mol.GetAtoms() if a.GetIsAromatic())),
        "qed_like": float(QED.qed(mol)),
    }


def calculate_descriptors(smiles: str) -> Dict[str, float]:
    return rdkit_descriptors(smiles) if RDKIT_AVAILABLE else proxy_descriptors(smiles)


def morgan_fingerprint(smiles: str, n_bits: int = 256) -> np.ndarray:
    """Return RDKit Morgan fingerprint or deterministic hashed fallback."""
    if RDKIT_AVAILABLE:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            arr = np.zeros((n_bits,), dtype=np.float32)
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=n_bits)
            # Avoid importing DataStructs unless RDKit is available
            from rdkit import DataStructs
            DataStructs.ConvertToNumpyArray(fp, arr)
            return arr
    bits = np.zeros(n_bits, dtype=np.float32)
    grams = [smiles[i:i+3] for i in range(max(1, len(smiles)-2))]
    for gram in grams:
        bits[int(hashlib.md5(gram.encode()).hexdigest(), 16) % n_bits] = 1.0
    return bits


def graph_features(smiles: str) -> Dict[str, object]:
    """Create a graph-ready molecular representation.

    Uses RDKit atom/bond topology when available. Otherwise, returns a simple
    sequential proxy graph so downstream GNN demos can still execute.
    """
    if RDKIT_AVAILABLE:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            node_features = []
            edge_index = []
            for atom in mol.GetAtoms():
                node_features.append([
                    atom.GetAtomicNum(),
                    atom.GetDegree(),
                    float(atom.GetIsAromatic()),
                    atom.GetFormalCharge(),
                ])
            for bond in mol.GetBonds():
                i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
                edge_index.extend([[i, j], [j, i]])
            return {"node_features": node_features, "edge_index": edge_index, "backend": "rdkit"}
    n = int(calculate_descriptors(smiles)["heavy_atoms"])
    node_features = [[6, 2, 0.0, 0] for _ in range(n)]
    edge_index = [[i, i+1] for i in range(max(0, n-1))] + [[i+1, i] for i in range(max(0, n-1))]
    return {"node_features": node_features, "edge_index": edge_index, "backend": "proxy"}


def featurize_many(smiles_list: Sequence[str]) -> List[Dict[str, float]]:
    return [calculate_descriptors(s) for s in smiles_list]

# ---------------------------------------------------------------------------
# Backward-compatible V2 data structure
# ---------------------------------------------------------------------------
@dataclass
class MolecularFeatures:
    smiles: str
    valid: bool
    mol_wt: float
    logp: float
    hbd: float
    hba: float
    tpsa: float
    rotatable_bonds: float
    heavy_atoms: float
    aromatic_rings: float
    hetero_atom_count: float
    halogen_count: float
    formal_charge: float
    qed: float
    error: str = ""

    def to_dict(self) -> Dict[str, object]:
        return self.__dict__.copy()


def featurize_smiles(smiles: str) -> MolecularFeatures:
    """V2-compatible feature object backed by the V3 descriptor engine."""
    valid = is_valid_smiles(smiles)
    d = calculate_descriptors(smiles)
    atoms = ATOM_PATTERN.findall(smiles or "")
    halogens = sum(1 for atom in atoms if atom in {"Cl", "Br", "F", "I"})
    hetero = sum(1 for atom in atoms if any(x in atom for x in ["N", "O", "S", "P", "n", "o", "s"]))
    # Proxy aromatic ring count: aromatic atoms / 6 unless RDKit exact rings are present
    aromatic_rings = float(d.get("ring_count", 0.0)) if d.get("aromatic_atoms", 0.0) else 0.0
    return MolecularFeatures(
        smiles=smiles,
        valid=bool(valid),
        mol_wt=round(float(d.get("mw", 0.0)), 3),
        logp=round(float(d.get("logp", 0.0)), 3),
        hbd=float(d.get("hbd", 0.0)),
        hba=float(d.get("hba", 0.0)),
        tpsa=round(float(d.get("tpsa", 0.0)), 3),
        rotatable_bonds=float(d.get("rotatable_bonds", 0.0)),
        heavy_atoms=float(d.get("heavy_atoms", 0.0)),
        aromatic_rings=aromatic_rings,
        hetero_atom_count=float(hetero),
        halogen_count=float(halogens),
        formal_charge=0.0,
        qed=round(float(d.get("qed_like", 0.0)), 3),
        error="" if valid else "Invalid SMILES",
    )
