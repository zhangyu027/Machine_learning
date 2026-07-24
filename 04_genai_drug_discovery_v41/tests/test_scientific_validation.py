import numpy as np
from pharma_genai.data.scaffold_split import scaffold_split_indices, assert_no_scaffold_overlap
from pharma_genai.evaluation.calibration import brier_score, expected_calibration_error
from pharma_genai.evaluation.applicability_domain import ApplicabilityDomain, tanimoto_similarity
from pharma_genai.prioritization.candidate_ranking import candidate_priority_score, recommendation


def test_scaffold_split_has_no_overlap():
    smiles = ["CCO", "CCN", "CCC", "c1ccccc1", "c1ccncc1", "CC(=O)O", "CCCl", "CCBr", "COC", "CNC"]
    tr, va, te = scaffold_split_indices(smiles, 0.6, 0.2)
    assert sorted(tr + va + te) == list(range(len(smiles)))
    assert_no_scaffold_overlap(smiles, [tr, va, te])


def test_calibration_metrics_ranges():
    y = np.array([0, 0, 1, 1])
    p = np.array([0.1, 0.2, 0.8, 0.9])
    assert 0 <= brier_score(y, p) <= 1
    assert 0 <= expected_calibration_error(y, p, n_bins=4) <= 1


def test_applicability_domain_and_ranking():
    ad = ApplicabilityDomain(["CCO", "c1ccccc1", "CC(=O)O"])
    result = ad.assess("CCO")
    assert result.label == "in_domain"
    assert tanimoto_similarity([1,0,1], [1,0,1]) == 1.0
    preds = {"oral_absorption_probability": .8, "solubility_score": .7, "drug_likeness_score": .75, "overall_toxicity_risk": .1}
    score = candidate_priority_score(preds, uncertainty=.1, nearest_similarity=.9)
    assert recommendation(score, "in_domain", .1) in {"ADVANCE", "REVIEW"}
