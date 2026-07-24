"""Transparent patient-to-trial criteria matching.

Criteria are evaluated independently and returned as matched, failed, or unknown.
Unknown mandatory criteria trigger human review rather than being treated as passed.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal, Optional
from pydantic import BaseModel, Field
from clinical_entities.extractor import ClinicalEntities, ClinicalEntityExtractor


class Criterion(BaseModel):
    id: str
    description: str
    field: Literal["age", "condition", "medication", "lab", "recent_hospitalization"]
    operator: Literal["gte", "lte", "between", "contains", "not_contains", "eq"]
    value: object
    required: bool = True


class TrialDefinition(BaseModel):
    trial_id: str
    title: str
    inclusion_criteria: list[Criterion] = Field(default_factory=list)
    exclusion_criteria: list[Criterion] = Field(default_factory=list)


class CriterionOutcome(BaseModel):
    criterion_id: str
    description: str
    category: Literal["inclusion", "exclusion"]
    status: Literal["matched", "failed", "unknown"]
    observed_value: object | None = None
    reason: str


class MatchResult(BaseModel):
    trial_id: str
    title: str
    eligibility: Literal["eligible", "not_eligible", "needs_review"]
    match_score: float = Field(ge=0, le=1)
    matched_criteria: list[CriterionOutcome]
    failed_criteria: list[CriterionOutcome]
    unknown_criteria: list[CriterionOutcome]
    requires_human_review: bool
    extracted_entities: ClinicalEntities


class TrialMatcher:
    def __init__(self, extractor: ClinicalEntityExtractor | None = None):
        self.extractor = extractor or ClinicalEntityExtractor()

    @staticmethod
    def load_trials(path: str | Path) -> list[TrialDefinition]:
        return [TrialDefinition.model_validate(item) for item in json.loads(Path(path).read_text())]

    @staticmethod
    def _observed(entities: ClinicalEntities, criterion: Criterion):
        if criterion.field == "age": return entities.age
        if criterion.field == "condition": return entities.conditions
        if criterion.field == "medication": return entities.medications
        if criterion.field == "recent_hospitalization": return entities.recent_hospitalization
        if criterion.field == "lab":
            lab_name = str(criterion.value.get("name", "")).lower() if isinstance(criterion.value, dict) else ""
            return next((lab.value for lab in entities.labs if lab.name == lab_name), None)
        return None

    @staticmethod
    def _compare(observed, criterion: Criterion) -> Optional[bool]:
        if observed is None or observed == []:
            return None
        value = criterion.value
        if criterion.field == "lab" and isinstance(value, dict):
            target = value.get("value")
        else:
            target = value
        op = criterion.operator
        if op == "gte": return float(observed) >= float(target)
        if op == "lte": return float(observed) <= float(target)
        if op == "between": return float(value[0]) <= float(observed) <= float(value[1])
        if op == "contains": return str(target).lower() in {str(x).lower() for x in observed}
        if op == "not_contains": return str(target).lower() not in {str(x).lower() for x in observed}
        if op == "eq": return observed == target
        return None

    def _outcome(self, entities: ClinicalEntities, criterion: Criterion, category: str) -> CriterionOutcome:
        observed = self._observed(entities, criterion)
        result = self._compare(observed, criterion)
        # Inclusion is matched when true; exclusion is matched when exclusion condition is absent/false.
        passed = result if category == "inclusion" else (not result if result is not None else None)
        if passed is None:
            status, reason = "unknown", "Required patient information was not found."
        elif passed:
            status, reason = "matched", "Patient evidence satisfies this criterion."
        else:
            status, reason = "failed", "Patient evidence does not satisfy this criterion."
        return CriterionOutcome(
            criterion_id=criterion.id, description=criterion.description, category=category,
            status=status, observed_value=observed, reason=reason,
        )

    def match(self, note_text: str, trial: TrialDefinition) -> MatchResult:
        entities = self.extractor.extract(note_text)
        outcomes = [self._outcome(entities, c, "inclusion") for c in trial.inclusion_criteria]
        outcomes += [self._outcome(entities, c, "exclusion") for c in trial.exclusion_criteria]
        matched = [o for o in outcomes if o.status == "matched"]
        failed = [o for o in outcomes if o.status == "failed"]
        unknown = [o for o in outcomes if o.status == "unknown"]
        required_total = len(outcomes)
        score = len(matched) / required_total if required_total else 0.0
        if failed:
            eligibility = "not_eligible"
        elif unknown:
            eligibility = "needs_review"
        else:
            eligibility = "eligible"
        return MatchResult(
            trial_id=trial.trial_id, title=trial.title, eligibility=eligibility,
            match_score=round(score, 4), matched_criteria=matched, failed_criteria=failed,
            unknown_criteria=unknown, requires_human_review=bool(unknown), extracted_entities=entities,
        )

    def rank(self, note_text: str, trials: list[TrialDefinition]) -> list[MatchResult]:
        rank_order = {"eligible": 2, "needs_review": 1, "not_eligible": 0}
        results = [self.match(note_text, trial) for trial in trials]
        return sorted(results, key=lambda r: (rank_order[r.eligibility], r.match_score), reverse=True)
