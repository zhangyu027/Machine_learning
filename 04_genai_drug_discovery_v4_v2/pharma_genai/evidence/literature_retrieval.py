"""Evidence-support interface that keeps literature separate from model predictions."""
from __future__ import annotations
from typing import Dict, List, Protocol

class EvidenceRetriever(Protocol):
    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]: ...


def build_evidence_query(compound_name: str = "", target: str = "", liability: str = "") -> str:
    terms = [t.strip() for t in [compound_name, target, liability] if t and t.strip()]
    return " AND ".join(terms) if terms else "drug discovery ADMET evidence"


def evidence_packet(prediction: Dict[str, object], citations: List[Dict[str, str]]) -> Dict[str, object]:
    return {
        "model_prediction": prediction,
        "literature_evidence": citations,
        "separation_notice": "Model outputs are predictions; retrieved publications are supporting evidence and do not validate the prediction.",
    }
