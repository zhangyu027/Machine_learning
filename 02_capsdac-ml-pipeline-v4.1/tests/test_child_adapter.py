from pathlib import Path
import pandas as pd

from ingestion.capsdac_child_adapter import aggregate_child_to_site_month


def test_adapter_removes_child_identifiers(tmp_path: Path):
    p = tmp_path / "child.csv"
    pd.DataFrame({
        "ReportMonth": ["Jul-2025", "Jul-2025"],
        "VendorNumber": [1, 1],
        "LEAID": ["A", "A"],
        "LEAName": ["LEA", "LEA"],
        "CountyName": ["County", "County"],
        "PreschoolID": [10, 10],
        "PreschoolName": ["Site", "Site"],
        "PreschoolCDSCode": ["001", "001"],
        "ChildUniqueID": ["c1", "c2"],
        "EnrollmentType": ["FT", "PT"],
        "FamilyMonthlyIncome": [2000, 3000],
        "FamilySize": [3, 4],
        "IEPStatus": ["YES", "NO"],
        "IsDualLanguageLearnerYN": ["Y", "N"],
        "EligibilityStatusShort": ["Income Eligible", "Homeless (Experiencing Homelessness)"],
    }).to_csv(p, index=False)
    out = aggregate_child_to_site_month(p)
    assert out.loc[0, "EnrollmentCount"] == 2
    assert "ChildUniqueID" not in out.columns
    assert out.loc[0, "FTShare"] == 0.5
