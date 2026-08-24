import pandas as pd
from src.capsdac_ml.feature_engineering import FEATURES, TARGET_COL, build_monthly_features


def test_build_monthly_features_supports_12_month_history():
    months = pd.date_range("2025-07-01", periods=12, freq="MS")
    df = pd.DataFrame({
        "SnapshotMonth": [m.strftime("%Y-%m") for m in months],
        "MonthDate": months,
        "VendorNumber": [6111] * 12,
        "LEAID": ["D14"] * 12,
        "LEAName": ["Example LEA"] * 12,
        "County": ["Example"] * 12,
        "PreschoolID": [1] * 12,
        "PreschoolCDSCode": ["SITE001"] * 12,
        "SiteName": ["Example Site"] * 12,
        "EnrollmentCount": list(range(50, 62)),
        "FTShare": [0.4] * 12,
        "IEPShare": [0.1] * 12,
        "DLLShare": [0.5] * 12,
        "HomelessEligibilityShare": [0.02] * 12,
        "MedianFamilyMonthlyIncome": [3000] * 12,
        "MeanFamilySize": [3.5] * 12,
        "AgencyEnrollment": list(range(500, 512)),
        "AgencyActiveSites": [10] * 12,
        "FundingType": ["CSPP"] * 12,
        "DataSource": ["test"] * 12,
    })
    out = build_monthly_features(df)
    assert all(c in out.columns for c in FEATURES)
    assert TARGET_COL in out.columns
    assert out["MonthDate"].nunique() == 8  # Oct through May for lag-3 + H1 target
    assert out["TargetMonth"].iloc[-1] == "2026-06"
