from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from config import cfg

def load_metadata_table(csv_path: Path | None = None) -> pd.DataFrame:
    csv_path = csv_path or cfg.metadata_csv
    if not csv_path.exists():
        return pd.DataFrame(columns=["rel_path", *cfg.metadata_features, "label"])
    df = pd.read_csv(csv_path)
    expected = {"rel_path", *cfg.metadata_features}
    missing = expected.difference(df.columns)
    if missing:
        raise ValueError(f"Missing metadata columns: {sorted(missing)}")
    return df

def build_metadata_lookup(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    lookup: Dict[str, Dict[str, float]] = {}
    for _, row in df.iterrows():
        lookup[str(row["rel_path"])] = {feat: float(row[feat]) for feat in cfg.metadata_features}
    return lookup

def fit_or_transform_scaler(
    rows: Iterable[Dict[str, float]],
    scaler: StandardScaler | None = None
) -> Tuple[np.ndarray, StandardScaler]:
    array = np.array([[row.get(feat, 0.0) for feat in cfg.metadata_features] for row in rows], dtype=np.float32)
    if scaler is None:
        scaler = StandardScaler()
        array = scaler.fit_transform(array)
    else:
        array = scaler.transform(array)
    return array.astype(np.float32), scaler

def metadata_dict_to_vector(metadata: Dict[str, float]) -> np.ndarray:
    return np.array([float(metadata.get(feat, 0.0)) for feat in cfg.metadata_features], dtype=np.float32)
