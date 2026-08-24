import pandas as pd
import pytest

from src.capsdac_ml.data_contracts import validate_enrollment_snapshot


def make_valid_12_month_frame():
    months = pd.date_range("2025-07-01", periods=12, freq="MS")
    return pd.DataFrame({
        "SnapshotMonth": [m.strftime("%Y-%m") for m in months],
        "VendorNumber": [123] * 12,
        "LEAName": ["Vendor"] * 12,
        "PreschoolCDSCode": ["001"] * 12,
        "SiteName": ["Site"] * 12,
        "County": ["California"] * 12,
        "EnrollmentCount": [10] * 12,
        "FundingType": ["CSPP"] * 12,
        "DataSource": ["sample"] * 12,
    })


def test_validate_enrollment_snapshot_passes():
    report = validate_enrollment_snapshot(make_valid_12_month_frame())
    assert report["month_count"] == 12


def test_validate_enrollment_snapshot_rejects_short_history():
    df = make_valid_12_month_frame().iloc[:11].copy()
    with pytest.raises(ValueError, match="at least 12"):
        validate_enrollment_snapshot(df)
