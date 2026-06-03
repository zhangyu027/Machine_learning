"""V3 enterprise orchestration pipeline."""
from __future__ import annotations
from typing import Dict, List, Sequence
import pandas as pd

from .multitask_admet import MultiTaskADMETPredictor
from .gnn.molecular_gnn import GraphEmbeddingService
from .explainability.shap_explainer import fallback_feature_importance, shap_ready_notice
from .rag.pubmed_rag import PubMedRAG
from .integrations.public_sources import PublicDataConnector


def analyze_smiles_v3(smiles: str, include_literature: bool = True) -> Dict[str, object]:
    predictor = MultiTaskADMETPredictor()
    row = predictor.predict_one(smiles)
    graph = GraphEmbeddingService().embed(smiles)
    explanation = fallback_feature_importance(row)
    result = {
        **row,
        "graph_backend": graph.backend,
        "graph_embedding": graph.embedding,
        "graph_n_nodes": graph.n_nodes,
        "graph_n_edges": graph.n_edges,
        "explainability_backend": shap_ready_notice(),
        "feature_attributions": explanation,
    }
    if include_literature:
        rag = PubMedRAG()
        result["literature_context"] = rag.answer("ADMET toxicity uncertainty explainability graph neural networks")
    return result


def analyze_many_v3(smiles_list: Sequence[str], include_literature: bool = False) -> List[Dict[str, object]]:
    rows = [analyze_smiles_v3(s, include_literature=include_literature) for s in smiles_list if str(s).strip()]
    return sorted(rows, key=lambda r: (r["development_priority"] != "advance", -float(r["drug_likeness_score"]), float(r["overall_toxicity_risk"])))


def dataframe_from_results(rows: List[Dict[str, object]]) -> pd.DataFrame:
    flat = []
    for r in rows:
        flat.append({k: v for k, v in r.items() if not isinstance(v, (list, dict))})
    return pd.DataFrame(flat)


def lookup_and_analyze(compound_name: str) -> Dict[str, object]:
    connector = PublicDataConnector()
    rec = connector.pubchem_lookup(compound_name)
    if rec is None:
        raise ValueError(f"Compound not found in online/demo sources: {compound_name}")
    result = analyze_smiles_v3(rec.smiles)
    result["source_record"] = {"source": rec.source, "compound_id": rec.compound_id, "name": rec.name, "target": rec.target, "activity": rec.activity}
    return result
