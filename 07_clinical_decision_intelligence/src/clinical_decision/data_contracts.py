from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import pandas as pd

@dataclass(frozen=True)
class ClinicalContract:
    required_columns: Sequence[str] = (
        "patient_id", "age", "sex", "comorbidity_score", "baseline_risk_score",
        "treatment", "readmission_30d", "length_of_stay", "site_id"
    )

    def validate(self, df: pd.DataFrame) -> None:
        missing = [c for c in self.required_columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        if df.patient_id.duplicated().any():
            raise ValueError("patient_id must be unique")
        if not set(df.treatment.dropna().unique()).issubset({0, 1}):
            raise ValueError("treatment must be binary 0/1")
