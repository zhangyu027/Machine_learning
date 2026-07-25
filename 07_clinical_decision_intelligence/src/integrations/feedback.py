from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import json

class ClinicianFeedbackStore:
    def __init__(self, path: Path):
        self.path=path; self.path.parent.mkdir(parents=True, exist_ok=True)
    def append(self, feedback: dict) -> dict:
        record={**feedback,"recorded_at":datetime.now(timezone.utc).isoformat()}
        with self.path.open('a') as f: f.write(json.dumps(record)+"\n")
        return record
