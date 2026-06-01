from pharma_genai.pipeline import analyze_smiles, analyze_many

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
