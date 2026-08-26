from pharma_genai.featurization import is_valid_smiles_proxy
from pharma_genai.admet_reliability import ADMETReliabilityEnsemble
from pharma_genai.pipeline_v3 import analyze_smiles_v3, analyze_many_v3, dataframe_from_results
from pharma_genai.gnn.molecular_gnn import GraphEmbeddingService
from pharma_genai.rag.pubmed_rag import PubMedRAG
from pharma_genai.integrations.public_sources import PublicDataConnector
from pharma_genai.pipeline import analyze_smiles, analyze_many

def test_validity_proxy():
    assert is_valid_smiles_proxy("CCO")
    assert not is_valid_smiles_proxy("CCO)")

def test_admet_model_predicts():
    smiles = ["CCO", "CCN", "c1ccccc1", "CC(=O)O", "CCOC(=O)N", "CN1CCCC1", "CCN(CC)CC", "O=C(O)c1ccccc1"]
    model = ADMETReliabilityEnsemble().fit(smiles)
    out = model.predict(["CCO", "CCN"])
    assert {"smiles", "admet_score", "uncertainty", "reliability"}.issubset(out.columns)
    assert len(out) == 2

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


def test_single_smiles_has_admet_and_reliability():
    r=analyze_smiles("CC(=O)Oc1ccccc1C(=O)O")
    assert r["valid"] is True
    assert "overall_toxicity_risk" in r
    assert "confidence_score" in r
    assert r["development_priority"] in {"advance","review","deprioritize","invalid"}

def test_batch_returns_rows():
    df=analyze_many(["CCO", "not a smiles"])
    assert len(df)==2
    assert "reliability_label" in df.columns
