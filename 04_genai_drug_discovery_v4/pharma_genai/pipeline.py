"""End-to-end pharmaceutical ML pipeline."""
from __future__ import annotations
from pathlib import Path
from typing import Iterable, List, Dict
import csv
import pandas as pd
from .featurization import featurize_smiles
from .admet import predict_admet_from_features
from .reliability import estimate_reliability

def analyze_smiles(smiles: str) -> Dict[str, object]:
    f=featurize_smiles(smiles)
    p=predict_admet_from_features(f)
    r=estimate_reliability(f,p)
    out={**f.to_dict(), **p.to_dict(), **r.to_dict()}
    out["smiles"]=smiles
    return out

def analyze_many(smiles_list: Iterable[str]) -> pd.DataFrame:
    rows=[analyze_smiles(s) for s in smiles_list if str(s).strip()]
    df=pd.DataFrame(rows)
    if not df.empty and "development_priority" in df:
        order={"advance":0,"review":1,"deprioritize":2,"invalid":3}
        df["priority_rank"]=df["development_priority"].map(order).fillna(9)
        df=df.sort_values(["priority_rank","confidence_score","drug_likeness_score"], ascending=[True,False,False]).drop(columns=["priority_rank"])
    return df

def read_smiles_file(path: str, column: str = "smiles") -> List[str]:
    p=Path(path)
    if p.suffix.lower() in {".csv", ".tsv"}:
        sep='\t' if p.suffix.lower()=='.tsv' else ','
        df=pd.read_csv(p, sep=sep)
        col=column if column in df.columns else df.columns[0]
        return [str(x) for x in df[col].dropna().tolist()]
    return [line.strip() for line in p.read_text().splitlines() if line.strip() and not line.startswith('#')]

def analyze_file(input_path: str, output_path: str = "outputs/admet_v2_predictions.csv", column: str = "smiles") -> str:
    smiles=read_smiles_file(input_path, column)
    df=analyze_many(smiles)
    out=Path(output_path); out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return str(out)
