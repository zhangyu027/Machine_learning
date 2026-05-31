"""RDKit-first molecular feature engineering with a safe pure-Python fallback.

The fallback is intentionally simple so the project demo runs on machines where RDKit
is not installed. For real pharmaceutical use, install RDKit and retrain/calibrate on
validated ADMET datasets.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import math
import re
from typing import Dict, List, Optional

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors, QED
    from rdkit.Chem import AllChem, DataStructs
    RDKIT_AVAILABLE = True
except Exception:  # pragma: no cover
    Chem = None
    RDKIT_AVAILABLE = False

@dataclass
class MolecularFeatures:
    smiles: str
    valid: bool
    mol_wt: float
    logp: float
    tpsa: float
    hbd: int
    hba: int
    rotatable_bonds: int
    aromatic_rings: int
    heavy_atoms: int
    qed: float
    formal_charge: int
    halogen_count: int
    hetero_atom_count: int
    ring_count: int
    fraction_csp3: float
    source: str
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)

_ATOMIC_WEIGHTS = {"C":12.01,"N":14.01,"O":16.00,"S":32.06,"P":30.97,"F":19.00,"Cl":35.45,"Br":79.90,"I":126.90,"H":1.008}

def _fallback_features(smiles: str, error: Optional[str] = None) -> MolecularFeatures:
    tokens = re.findall(r"Cl|Br|[CNOSPFIcnosp]", smiles or "")
    if not smiles or not tokens or any(ch in smiles for ch in [' ', '\\']):
        return MolecularFeatures(smiles, False, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,"fallback", error or "Invalid or unsupported SMILES")
    heavy_atoms=len(tokens)
    hetero=sum(1 for t in tokens if t.upper() not in {"C","H"})
    halogen=sum(1 for t in tokens if t in {"F","Cl","Br","I"})
    arom=sum(1 for t in tokens if t.islower())//6
    ring_count=len(set(re.findall(r"[1-9]", smiles)))
    mol_wt=sum(_ATOMIC_WEIGHTS.get(t.capitalize(), 12.0) for t in tokens)
    hba=sum(1 for t in tokens if t.upper() in {"N","O","S"})
    hbd=max(0, min(hba, smiles.count('N')+smiles.count('O')))
    # crude empirical fallback; use only for demos when RDKit unavailable
    logp=0.54*sum(1 for t in tokens if t.upper()=="C") + 0.25*halogen - 1.1*hetero
    tpsa=20.2*hba + 12.0*hbd
    rot=max(0, smiles.count('-') + smiles.count('CC') - ring_count)
    qed=max(0.05, min(0.95, 1 - (abs(mol_wt-350)/600 + max(logp-5,0)/5 + max(tpsa-140,0)/160)/3))
    csp3=max(0.0, min(1.0, smiles.count('C')/max(1,sum(1 for t in tokens if t.upper()=="C"))))
    return MolecularFeatures(smiles, True, round(mol_wt,3), round(logp,3), round(tpsa,3), hbd,hba,rot,arom,heavy_atoms,round(qed,3),0,halogen,hetero,ring_count,round(csp3,3),"fallback", error)

def featurize_smiles(smiles: str) -> MolecularFeatures:
    smiles = (smiles or "").strip()
    if not RDKIT_AVAILABLE:
        return _fallback_features(smiles)
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return _fallback_features(smiles, "RDKit could not parse SMILES")
        heavy = mol.GetNumHeavyAtoms()
        hetero = sum(1 for a in mol.GetAtoms() if a.GetAtomicNum() not in (1,6))
        halogen = sum(1 for a in mol.GetAtoms() if a.GetSymbol() in {"F","Cl","Br","I"})
        return MolecularFeatures(
            smiles=smiles, valid=True,
            mol_wt=round(float(Descriptors.MolWt(mol)),3),
            logp=round(float(Crippen.MolLogP(mol)),3),
            tpsa=round(float(rdMolDescriptors.CalcTPSA(mol)),3),
            hbd=int(Lipinski.NumHDonors(mol)), hba=int(Lipinski.NumHAcceptors(mol)),
            rotatable_bonds=int(Lipinski.NumRotatableBonds(mol)),
            aromatic_rings=int(Lipinski.NumAromaticRings(mol)), heavy_atoms=int(heavy),
            qed=round(float(QED.qed(mol)),3), formal_charge=int(sum(a.GetFormalCharge() for a in mol.GetAtoms())),
            halogen_count=int(halogen), hetero_atom_count=int(hetero), ring_count=int(Lipinski.RingCount(mol)),
            fraction_csp3=round(float(rdMolDescriptors.CalcFractionCSP3(mol)),3), source="rdkit"
        )
    except Exception as exc:
        return _fallback_features(smiles, str(exc))

def morgan_fingerprint(smiles: str, radius: int = 2, n_bits: int = 2048) -> List[int]:
    """Return Morgan fingerprint bits. Falls back to hashed character n-grams."""
    smiles=(smiles or '').strip()
    if RDKIT_AVAILABLE:
        mol=Chem.MolFromSmiles(smiles)
        if mol is not None:
            fp=AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
            arr=[0]*n_bits
            DataStructs.ConvertToNumpyArray(fp, arr)
            return [int(x) for x in arr]
    bits=[0]*n_bits
    for n in (1,2,3):
        for i in range(max(0,len(smiles)-n+1)):
            bits[hash(smiles[i:i+n]) % n_bits]=1
    return bits

def is_valid_smiles_proxy(smiles: str) -> bool:
    """Backward-compatible validity helper retained for older tests."""
    return bool(featurize_smiles(smiles).valid)
