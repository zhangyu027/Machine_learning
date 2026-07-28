"""Human-in-the-loop clinician review and auditable feedback records."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path

@dataclass
class ClinicianReview:
    prediction_id: str; clinician_id: str; decision: str; corrected_label: str | None = None; comment: str = ""

class FeedbackRepository:
    def __init__(self, path: str = "outputs/clinician_feedback.jsonl"): self.path = Path(path)
    def record(self, review: ClinicianReview) -> dict:
        if review.decision not in {"accept", "reject", "override"}: raise ValueError("Invalid decision")
        row = {**asdict(review), "timestamp": datetime.now(timezone.utc).isoformat()}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f: f.write(json.dumps(row) + "\n")
        return row
