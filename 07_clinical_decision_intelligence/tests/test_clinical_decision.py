import pandas as pd
from clinical_decision.data_contracts import ClinicalContract
from clinical_decision.features import build_features
from clinical_decision.propensity import estimate_propensity_scores


def sample_df():
    return pd.DataFrame({
        "patient_id": [1,2,3,4,5,6],
        "age": [60,70,55,65,50,72],
        "sex": ["Female","Male","Female","Male","Female","Male"],
        "comorbidity_score": [1,3,2,4,1,5],
        "baseline_risk_score": [.2,.5,.3,.6,.1,.7],
        "prior_visits": [0,2,1,3,0,4],
        "lab_abnormality_score": [0.1,0.3,-0.2,1.0,0.2,.8],
        "site_id": ["S1","S1","S2","S2","S3","S3"],
        "treatment": [0,1,0,1,0,1],
        "readmission_30d": [0,1,0,1,0,1],
        "length_of_stay": [2,5,3,6,2,7],
    })


def test_contract():
    ClinicalContract().validate(sample_df())


def test_feature_engineering():
    out = build_features(sample_df())
    assert "is_female" in out.columns


def test_propensity_scores_range():
    out = estimate_propensity_scores(build_features(sample_df()))
    assert out.propensity_score.between(0,1).all()
