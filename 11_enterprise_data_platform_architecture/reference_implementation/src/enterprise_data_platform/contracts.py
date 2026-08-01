"""Data-contract loading and validation."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    """Raised when a contract is malformed or data violates the contract."""


@dataclass(frozen=True)
class FieldSpec:
    name: str
    type: str
    required: bool = False
    allowed_values: tuple[Any, ...] = ()


@dataclass(frozen=True)
class DataContract:
    dataset: str
    version: str
    grain: tuple[str, ...]
    fields: tuple[FieldSpec, ...]
    freshness_hours: int

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DataContract":
        required = {"dataset", "version", "grain", "fields", "freshness_hours"}
        missing = required - payload.keys()
        if missing:
            raise ContractError(f"Missing contract keys: {sorted(missing)}")
        fields = tuple(
            FieldSpec(
                name=item["name"],
                type=item["type"],
                required=bool(item.get("required", False)),
                allowed_values=tuple(item.get("allowed_values", [])),
            )
            for item in payload["fields"]
        )
        return cls(
            dataset=str(payload["dataset"]),
            version=str(payload["version"]),
            grain=tuple(payload["grain"]),
            fields=fields,
            freshness_hours=int(payload["freshness_hours"]),
        )

    @classmethod
    def load(cls, path: str | Path) -> "DataContract":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def _matches_type(value: Any, expected: str) -> bool:
    if value is None:
        return True
    mapping = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
    }
    if expected not in mapping:
        raise ContractError(f"Unsupported field type: {expected}")
    return isinstance(value, mapping[expected]) and not (
        expected in {"integer", "number"} and isinstance(value, bool)
    )


def validate_record(record: dict[str, Any], contract: DataContract) -> list[str]:
    errors: list[str] = []
    for field in contract.fields:
        value = record.get(field.name)
        if field.required and (value is None or value == ""):
            errors.append(f"{field.name}: required value missing")
            continue
        if not _matches_type(value, field.type):
            errors.append(f"{field.name}: expected {field.type}")
        if value is not None and field.allowed_values and value not in field.allowed_values:
            errors.append(f"{field.name}: value not in allowed set")
    return errors
