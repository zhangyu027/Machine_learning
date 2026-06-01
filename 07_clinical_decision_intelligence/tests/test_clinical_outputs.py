import pandas as pd

def test_risk_scores_exist():
    df=pd.read_csv('reports/model_outputs/patient_risk_effect_recommendations.csv')
    assert 'predicted_readmission_risk' in df.columns
