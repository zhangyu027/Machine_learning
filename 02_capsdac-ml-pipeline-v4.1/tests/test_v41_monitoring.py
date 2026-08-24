import pandas as pd
from forecasting.src.capsdac_ml.monitoring import drift_report
from forecasting.src.capsdac_ml.feature_engineering import FEATURES


def test_temporal_features_excluded_from_operational_drift():
    months = pd.date_range('2025-01-01', periods=7, freq='MS')
    rows=[]
    for i,m in enumerate(months):
        row={"MonthDate":m,"EnrollmentCount":10.0}
        for f in FEATURES: row[f]=10.0
        row['month_sin']=float(i*100); row['month_cos']=float(i*100); row['trend_index']=float(i)
        rows.append(row)
    report=drift_report(pd.DataFrame(rows))
    temporal=[r for r in report['features'] if r['feature']=='trend_index'][0]
    assert temporal['included_in_operational_status'] is False
