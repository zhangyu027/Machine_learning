"""FHIR R4 client simulation supporting Bundle ingestion and DiagnosticReport output."""
from __future__ import annotations
import uuid

class FHIRClient:
    def __init__(self, base_url: str = "memory://fhir"):
        self.base_url = base_url; self.resources: dict[tuple[str, str], dict] = {}
    def upsert(self, resource: dict) -> dict:
        rtype = resource.get("resourceType"); rid = resource.get("id") or str(uuid.uuid4())
        if not rtype: raise ValueError("FHIR resourceType is required")
        resource = {**resource, "id": rid}; self.resources[(rtype, rid)] = resource; return resource
    def ingest_bundle(self, bundle: dict) -> int:
        if bundle.get("resourceType") != "Bundle": raise ValueError("Expected FHIR Bundle")
        for entry in bundle.get("entry", []): self.upsert(entry["resource"])
        return len(bundle.get("entry", []))
    def create_risk_assessment(self, patient_id: str, probability: float, rationale: str, evidence_ids: list[str]):
        return self.upsert({
            "resourceType": "RiskAssessment", "status": "final",
            "subject": {"reference": f"Patient/{patient_id}"},
            "prediction": [{"probabilityDecimal": round(float(probability), 4), "qualitativeRisk": {"text": "high" if probability >= .7 else "moderate" if probability >= .4 else "low"}}],
            "basis": [{"reference": x} for x in evidence_ids], "note": [{"text": rationale}],
        })
