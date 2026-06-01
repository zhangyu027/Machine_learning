from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import pandas as pd

@dataclass(frozen=True)
class ExperimentContract:
    required_columns: Sequence[str] = (
        "user_id", "variant", "pre_period_metric", "post_period_metric", "converted", "segment"
    )
    allowed_variants: Sequence[str] = ("control", "treatment")

    def validate(self, df: pd.DataFrame) -> None:
        missing = [c for c in self.required_columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        invalid = set(df["variant"].dropna().unique()) - set(self.allowed_variants)
        if invalid:
            raise ValueError(f"Invalid variants: {invalid}")
        if df.empty:
            raise ValueError("Experiment data is empty")
