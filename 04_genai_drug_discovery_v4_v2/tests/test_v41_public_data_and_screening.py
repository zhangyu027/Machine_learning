from pharma_genai.connectors.public_data import PublicDataConnector
from pharma_genai.services.candidate_screening import CandidateScreeningPipeline


def test_pubchem_aspirin_has_smiles():
    rec = PublicDataConnector().pubchem_lookup("aspirin")
    assert rec is not None
    assert rec.compound_id == "2244"
    assert rec.smiles == "CC(=O)OC1=CC=CC=C1C(=O)O"


def test_cross_source_lookup():
    records = PublicDataConnector().lookup_all_sources("aspirin")
    assert len(records) >= 3
    assert all(r.smiles for r in records)


def test_candidate_screening_pipeline_runs():
    result = CandidateScreeningPipeline().screen_by_name("aspirin")
    assert result["smiles_validation"]["is_valid"]
    assert result["admet_prediction"]["development_recommendation"] in {"advance", "review", "deprioritize"}
    assert result["reliability"]["reliability_label"] in {"high", "medium", "low"}
