"""Offline/online feature store abstraction; replace backend with Feast in production."""
from __future__ import annotations
from datetime import datetime, timezone

class FeatureStore:
    def __init__(self): self._online: dict[str, dict] = {}
    def write(self, entity_id: str, features: dict, event_time: str | None = None):
        self._online[entity_id] = {"features": features, "event_time": event_time or datetime.now(timezone.utc).isoformat()}
    def get_online_features(self, entity_id: str, names: list[str] | None = None) -> dict:
        row = self._online.get(entity_id, {"features": {}})["features"]
        return row if names is None else {name: row.get(name) for name in names}
