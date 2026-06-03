from pharma_genai.pipeline_v3 import analyze_smiles_v3, analyze_many_v3, dataframe_from_results
from pharma_genai.gnn.molecular_gnn import GraphEmbeddingService
from pharma_genai.rag.pubmed_rag import PubMedRAG
from pharma_genai.integrations.public_sources import PublicDataConnector


def test_v3_pipeline_single():
    result = analyze_smiles_v3("CC(=O)Oc1ccccc1C(=O)O", include_literature=True)
    assert result["valid_smiles"] is True
    assert 0 <= result["overall_toxicity_risk"] <= 1
    assert result["reliability_label"] in {"high", "medium", "low"}
    assert "feature_attributions" in result
    assert "literature_context" in result


def test_v3_many_and_dataframe():
    rows = analyze_many_v3(["CCO", "Cn1cnc2c1c(=O)n(C)c(=O)n2C"])
    df = dataframe_from_results(rows)
    assert len(rows) == 2
    assert "development_priority" in df.columns


def test_graph_embedding_fallback_or_rdkit():
    emb = GraphEmbeddingService().embed("CCO")
    assert emb.n_nodes > 0
    assert len(emb.embedding) == 8


def test_rag_and_demo_lookup():
    answer = PubMedRAG().answer("uncertainty ADMET")
    assert answer["evidence"]
    rec = PublicDataConnector().pubchem_lookup("aspirin")
    assert rec is not None
    assert rec.smiles
