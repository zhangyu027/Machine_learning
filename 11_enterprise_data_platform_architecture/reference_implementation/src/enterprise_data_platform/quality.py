"""Reusable quality-rule engine with severity-aware failure behavior."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable


class DataQualityError(RuntimeError):
    """Raised when one or more critical quality checks fail."""


@dataclass(frozen=True)
class QualityResult:
    rule: str
    severity: str
    passed: bool
    failed_records: int
    message: str


Rule = Callable[[list[dict[str, Any]]], QualityResult]


def required_fields_rule(fields: list[str], severity: str = "critical") -> Rule:
    def evaluate(rows: list[dict[str, Any]]) -> QualityResult:
        failed = sum(any(row.get(field) in (None, "") for field in fields) for row in rows)
        return QualityResult(
            rule=f"required_fields:{','.join(fields)}",
            severity=severity,
            passed=failed == 0,
            failed_records=failed,
            message="Required-field validation",
        )
    return evaluate


def unique_grain_rule(fields: list[str], severity: str = "critical") -> Rule:
    def evaluate(rows: list[dict[str, Any]]) -> QualityResult:
        keys = [tuple(row.get(field) for field in fields) for row in rows]
        failed = len(keys) - len(set(keys))
        return QualityResult(
            rule=f"unique_grain:{','.join(fields)}",
            severity=severity,
            passed=failed == 0,
            failed_records=failed,
            message="Business-grain uniqueness validation",
        )
    return evaluate


def allowed_values_rule(field: str, allowed: set[Any], severity: str = "high") -> Rule:
    def evaluate(rows: list[dict[str, Any]]) -> QualityResult:
        failed = sum(row.get(field) not in allowed for row in rows)
        return QualityResult(
            rule=f"allowed_values:{field}",
            severity=severity,
            passed=failed == 0,
            failed_records=failed,
            message="Approved-code validation",
        )
    return evaluate


def run_quality_checks(rows: list[dict[str, Any]], rules: list[Rule]) -> list[dict[str, Any]]:
    results = [rule(rows) for rule in rules]
    critical = [result for result in results if result.severity == "critical" and not result.passed]
    if critical:
        names = ", ".join(result.rule for result in critical)
        raise DataQualityError(f"Critical quality checks failed: {names}")
    return [asdict(result) for result in results]
