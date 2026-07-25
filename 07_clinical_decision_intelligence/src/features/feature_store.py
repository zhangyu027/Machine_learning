from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import pandas as pd

@dataclass
class LocalFeatureStore:
    """Small offline feature-store interface; swap with Feast in production."""
    path: Path
    key: str = "patient_id"

    def materialize(self, frame: pd.DataFrame) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_parquet(self.path, index=False)
        (self.path.with_suffix('.metadata.json')).write_text(json.dumps({
            "key": self.key, "columns": list(frame.columns), "rows": len(frame)
        }, indent=2))

    def get_online_features(self, entity_id: str) -> dict:
        frame = pd.read_parquet(self.path)
        row = frame.loc[frame[self.key].astype(str) == str(entity_id)]
        if row.empty:
            raise KeyError(f"Unknown {self.key}: {entity_id}")
        return row.iloc[-1].to_dict()
