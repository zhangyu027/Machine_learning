from pathlib import Path

from clinical_decision_intelligence.ml.predictor import ReadmissionPredictor


def test_model_generates_bounded_risk_score() -> None:
    model_path = Path("models/xgboost_readmission_model.joblib")
    predictor = ReadmissionPredictor(model_path)
    risk = predictor.predict(
        [
            {
                "age": 72,
                "sex": "F",
                "insurance": "Medicare",
                "hospital_id": "H1",
                "comorbidity_index": 4,
                "prior_admissions_12m": 2,
                "severity_score": 7.5,
                "care_management_program": 1,
                "length_of_stay": 5,
            }
        ]
    )[0]
    assert 0.0 <= risk <= 1.0
