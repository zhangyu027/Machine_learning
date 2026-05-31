from pharma_genai.featurization import is_valid_smiles_proxy
from pharma_genai.admet_reliability import ADMETReliabilityEnsemble

def test_validity_proxy():
    assert is_valid_smiles_proxy("CCO")
    assert not is_valid_smiles_proxy("CCO)")

def test_admet_model_predicts():
    smiles = ["CCO", "CCN", "c1ccccc1", "CC(=O)O", "CCOC(=O)N", "CN1CCCC1", "CCN(CC)CC", "O=C(O)c1ccccc1"]
    model = ADMETReliabilityEnsemble().fit(smiles)
    out = model.predict(["CCO", "CCN"])
    assert {"smiles", "admet_score", "uncertainty", "reliability"}.issubset(out.columns)
    assert len(out) == 2
