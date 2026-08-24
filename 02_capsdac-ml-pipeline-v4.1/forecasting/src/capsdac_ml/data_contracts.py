from __future__ import annotations

import re
from typing import Any

import pandas as pd

REQUIRED_COLUMNS = [
    "SnapshotMonth",
    "VendorNumber",
    "LEAName",
    "PreschoolCDSCode",
    "SiteName",
    "County",
    "EnrollmentCount",
    "FundingType",
    "DataSource",
]

KEY_COLUMNS = ["SnapshotMonth", "PreschoolCDSCode"]
MONTH_PATTERN = re.compile(r"^\d{4}-\d{2}$")


def build_validation_report(df: pd.DataFrame) -> dict[str, Any]:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    duplicate_count = int(df.duplicated(KEY_COLUMNS).sum()) if not missing else 0
    negative_count = int((df["EnrollmentCount"] < 0).sum()) if "EnrollmentCount" in df.columns else 0
    bad_month_count = 0
    if "SnapshotMonth" in df.columns:
        bad_month_count = int((~df["SnapshotMonth"].astype(str).str.match(MONTH_PATTERN)).sum())

    return {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "required_columns": REQUIRED_COLUMNS,
        "missing_required_columns": missing,
        "duplicate_grain_count": duplicate_count,
        "negative_enrollment_count": negative_count,
        "bad_month_format_count": bad_month_count,
        "snapshot_month_min": None if "SnapshotMonth" not in df.columns or df.empty else str(df["SnapshotMonth"].min()),
        "snapshot_month_max": None if "SnapshotMonth" not in df.columns or df.empty else str(df["SnapshotMonth"].max()),
        "month_count": 0 if "SnapshotMonth" not in df.columns else int(df["SnapshotMonth"].nunique()),
        "site_count": 0 if "PreschoolCDSCode" not in df.columns else int(df["PreschoolCDSCode"].nunique()),
        "vendor_count": 0 if "VendorNumber" not in df.columns else int(df["VendorNumber"].nunique()),
    }


def validate_enrollment_snapshot(df: pd.DataFrame) -> dict[str, Any]:
    report = build_validation_report(df)
    if report["missing_required_columns"]:
        raise ValueError(f"Missing required columns: {report['missing_required_columns']}")
    if df.empty:
        raise ValueError("Enrollment snapshot is empty")
    if report["negative_enrollment_count"] > 0:
        raise ValueError("EnrollmentCount must be non-negative")
    if report["duplicate_grain_count"] > 0:
        raise ValueError(f"Duplicate records found at grain {KEY_COLUMNS}")
    if report["bad_month_format_count"] > 0:
        raise ValueError("SnapshotMonth must use YYYY-MM format")
    if report["month_count"] < 12:
        raise ValueError(f"V4 expects at least 12 distinct months; found {report['month_count']}")

    pd.to_datetime(df["SnapshotMonth"] + "-01", errors="raise")
    return report
