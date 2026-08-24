from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path


class ClinicianFeedbackStore:
    """Append-only local demo store; replace with a transactional store in production."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def append(self, feedback: dict) -> dict:
        record = {
            **feedback,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
        with self._lock, self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record) + "\n")
        return record
