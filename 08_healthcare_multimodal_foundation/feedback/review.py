"""Human-in-the-loop clinician review and auditable feedback records."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal


ReviewDecision = Literal["accept", "reject", "override"]
VALID_REVIEW_DECISIONS: frozenset[str] = frozenset(
    {"accept", "reject", "override"}
)


@dataclass(frozen=True, slots=True)
class ClinicianReview:
    """A clinician's review of a previously generated prediction."""

    prediction_id: str
    clinician_id: str
    decision: ReviewDecision
    corrected_label: str | None = None
    comment: str = ""


class FeedbackRepository:
    """Append clinician review records to a local JSON Lines file."""

    def __init__(
        self,
        path: str | Path = "outputs/clinician_feedback.jsonl",
    ) -> None:
        self.path = Path(path)

    def record(self, review: ClinicianReview) -> dict[str, Any]:
        """Validate and persist one clinician review record.

        FastAPI validates normal API requests before this method is called.
        This defensive check also protects direct internal callers.
        """
        if review.decision not in VALID_REVIEW_DECISIONS:
            raise ValueError(
                "Invalid decision. Expected one of: accept, reject, override."
            )

        if not review.prediction_id.strip():
            raise ValueError("prediction_id must not be empty")

        if not review.clinician_id.strip():
            raise ValueError("clinician_id must not be empty")

        row: dict[str, Any] = {
            **asdict(review),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file_handle:
            file_handle.write(json.dumps(row, ensure_ascii=False) + "\n")

        return row
