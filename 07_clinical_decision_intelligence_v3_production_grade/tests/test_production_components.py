import numpy as np, pandas as pd
from clinical_decision_intelligence.evaluation.calibration import calibration_report
from clinical_decision_intelligence.evaluation.fairness import subgroup_fairness_report
from clinical_decision_intelligence.integrations.fhir import patient_features_to_fhir_risk_assessment
from clinical_decision_intelligence.monitoring.drift import population_stability_index

def test_calibration_report():
    r=calibration_report([0,0,1,1],[.1,.2,.8,.9],bins=2); assert r['brier_score'] < .1

def test_fairness_report():
    df=pd.DataFrame({'y':[0,1,0,1],'p':[.1,.9,.3,.8],'g':['A','A','B','B']})
    r=subgroup_fairness_report(df,'y','p','g'); assert len(r['subgroups'])==2

def test_fhir_resource():
    r=patient_features_to_fhir_risk_assessment('123',.72); assert r['resourceType']=='RiskAssessment'

def test_psi_identical_is_near_zero():
    x=np.arange(1,101); assert population_stability_index(x,x) < 1e-9
