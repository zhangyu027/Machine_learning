"""Deterministic clinical entity extraction for synthetic/demo notes.

The extractor is intentionally dependency-light and auditable. It recognizes ages,
conditions, medications, laboratory measurements, hospitalizations, and negation.
A production deployment can replace or augment it with scispaCy/MedCAT/ClinicalBERT NER.
"""
from __future__ import annotations

import re
from typing import Optional
from pydantic import BaseModel, Field


class LabResult(BaseModel):
    name: str
    value: float
    unit: Optional[str] = None


class ClinicalEntities(BaseModel):
    age: Optional[int] = None
    conditions: list[str] = Field(default_factory=list)
    medications: list[str] = Field(default_factory=list)
    labs: list[LabResult] = Field(default_factory=list)
    recent_hospitalization: Optional[bool] = None
    negated_conditions: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    evidence: dict[str, list[str]] = Field(default_factory=dict)


DEFAULT_CONDITIONS = [
    "diabetes", "heart failure", "asthma", "hypertension", "kidney disease",
    "chronic kidney disease", "copd", "cancer", "lung cancer", "pneumonia"
]
DEFAULT_MEDICATIONS = [
    "metformin", "insulin", "beta blocker", "steroid", "ace inhibitor",
    "diuretic", "warfarin", "aspirin"
]
LAB_PATTERN = re.compile(
    r"\b(?P<name>hba1c|a1c|creatinine|egfr|hemoglobin|platelets?|alt|ast)\s*"
    r"(?:is|=|:)?\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>%|mg/dl|g/dl|ml/min(?:/1\.73m2)?|u/l|k/ul)?\b",
    re.IGNORECASE,
)
AGE_PATTERNS = [
    re.compile(r"\bpatient\s+age\s+(\d{1,3})\b", re.I),
    re.compile(r"\bage\s*[:=]?\s*(\d{1,3})\b", re.I),
    re.compile(r"\b(\d{1,3})[- ]year[- ]old\b", re.I),
]


class ClinicalEntityExtractor:
    def __init__(self, conditions: list[str] | None = None, medications: list[str] | None = None):
        self.conditions = sorted(conditions or DEFAULT_CONDITIONS, key=len, reverse=True)
        self.medications = sorted(medications or DEFAULT_MEDICATIONS, key=len, reverse=True)

    @staticmethod
    def _is_negated(text: str, start: int) -> bool:
        window = text[max(0, start - 45):start].lower()
        return bool(re.search(r"\b(no|denies|without|negative for|no history of)\b[^.;,]{0,35}$", window))

    def extract(self, note_text: str) -> ClinicalEntities:
        text = " ".join(note_text.split())
        lower = text.lower()
        evidence: dict[str, list[str]] = {}

        age = None
        for pattern in AGE_PATTERNS:
            match = pattern.search(text)
            if match:
                candidate = int(match.group(1))
                if 0 < candidate < 121:
                    age = candidate
                    evidence.setdefault("age", []).append(match.group(0))
                    break

        conditions: list[str] = []
        negated: list[str] = []
        for term in self.conditions:
            for match in re.finditer(rf"\b{re.escape(term)}\b", lower):
                target = negated if self._is_negated(lower, match.start()) else conditions
                if term not in target:
                    target.append(term)
                    evidence.setdefault("negated_conditions" if target is negated else "conditions", []).append(
                        text[max(0, match.start()-30):min(len(text), match.end()+30)]
                    )

        medications: list[str] = []
        for term in self.medications:
            match = re.search(rf"\b{re.escape(term)}\b", lower)
            if match and not self._is_negated(lower, match.start()):
                medications.append(term)
                evidence.setdefault("medications", []).append(
                    text[max(0, match.start()-25):min(len(text), match.end()+25)]
                )

        labs = []
        for match in LAB_PATTERN.finditer(text):
            name = match.group("name").lower()
            if name == "a1c":
                name = "hba1c"
            labs.append({"name": name, "value": float(match.group("value")), "unit": match.group("unit")})
            evidence.setdefault("labs", []).append(match.group(0))

        recent_hospitalization: Optional[bool] = None
        hosp_match = re.search(r"\b(recent hospitalization|hospitalized within|recently hospitalized)\b", lower)
        no_hosp = re.search(r"\b(no|without|denies)\s+(?:a\s+)?recent hospitalization\b", lower)
        if no_hosp:
            recent_hospitalization = False
            evidence.setdefault("recent_hospitalization", []).append(no_hosp.group(0))
        elif hosp_match:
            recent_hospitalization = True
            evidence.setdefault("recent_hospitalization", []).append(hosp_match.group(0))

        missing = []
        if age is None:
            missing.append("age")
        if not conditions:
            missing.append("diagnosis/condition")
        if "missing lab" in lower or "laboratory values are missing" in lower or "missing laboratory" in lower:
            missing.append("required laboratory values")

        return ClinicalEntities(
            age=age,
            conditions=conditions,
            medications=medications,
            labs=labs,
            recent_hospitalization=recent_hospitalization,
            negated_conditions=negated,
            missing_information=missing,
            evidence=evidence,
        )
