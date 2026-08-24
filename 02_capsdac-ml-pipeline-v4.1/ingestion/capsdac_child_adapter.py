from __future__ import annotations

from pathlib import Path
import zipfile

import numpy as np
import pandas as pd

# Deliberately excludes names, addresses, DOB, local child IDs, and all other child PII.
ALLOWED_CHILD_COLUMNS = [
    "ReportMonth",
    "VendorNumber",
    "LEAID",
    "LEAName",
    "CountyName",
    "PreschoolID",
    "PreschoolName",
    "PreschoolCDSCode",
    "ChildUniqueID",
    "EnrollmentType",
    "FamilyMonthlyIncome",
    "FamilySize",
    "IEPStatus",
    "IsDualLanguageLearnerYN",
    "EligibilityStatusShort",
]


def _read_child_file(path: Path) -> pd.DataFrame:
    """Read the CAPSDAC child extract from CSV or ZIP.

    The source export may contain non-UTF8 bytes, so latin-1 is used as a lossless
    byte-to-character fallback. Only a small approved column allow-list is read.
    """
    path = Path(path)
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as zf:
            members = [n for n in zf.namelist() if n.lower().endswith(".csv") and not n.startswith("__MACOSX/")]
            if len(members) != 1:
                raise ValueError(f"Expected exactly one CSV in {path.name}; found {len(members)}")
            with zf.open(members[0]) as fh:
                return pd.read_csv(fh, usecols=ALLOWED_CHILD_COLUMNS, encoding="latin1", low_memory=False)
    return pd.read_csv(path, usecols=ALLOWED_CHILD_COLUMNS, encoding="latin1", low_memory=False)


def aggregate_child_to_site_month(path: str | Path) -> pd.DataFrame:
    """Convert child-level CAPSDAC rows to privacy-safer site-month features.

    The returned frame contains no child names, addresses, dates of birth, or
    child-level identifiers. ChildUniqueID is used only transiently to de-duplicate
    a child within a site/month and is then discarded.
    """
    raw = _read_child_file(Path(path))
    raw["MonthDate"] = pd.to_datetime(raw["ReportMonth"], format="%b-%Y", errors="coerce")
    if raw["MonthDate"].isna().any():
        raise ValueError("Some ReportMonth values could not be parsed with format Mon-YYYY")

    # De-duplicate repeated child rows at the modeling grain before aggregation.
    raw = raw.drop_duplicates(["MonthDate", "PreschoolCDSCode", "ChildUniqueID"], keep="last")

    raw["IsFT"] = raw["EnrollmentType"].astype(str).str.upper().eq("FT").astype(float)
    raw["HasIEP"] = raw["IEPStatus"].astype(str).str.upper().eq("YES").astype(float)
    raw["IsDLL"] = raw["IsDualLanguageLearnerYN"].astype(str).str.upper().eq("Y").astype(float)
    raw["IsHomelessEligibility"] = raw["EligibilityStatusShort"].astype(str).str.contains("Homeless", case=False, na=False).astype(float)
    raw["FamilyMonthlyIncome"] = pd.to_numeric(raw["FamilyMonthlyIncome"], errors="coerce")
    raw["FamilySize"] = pd.to_numeric(raw["FamilySize"], errors="coerce")

    grouped = raw.groupby(["MonthDate", "PreschoolCDSCode"], as_index=False, dropna=False).agg(
        VendorNumber=("VendorNumber", "first"),
        LEAID=("LEAID", "first"),
        LEAName=("LEAName", "first"),
        County=("CountyName", "first"),
        PreschoolID=("PreschoolID", "first"),
        SiteName=("PreschoolName", "first"),
        EnrollmentCount=("ChildUniqueID", "nunique"),
        FTShare=("IsFT", "mean"),
        IEPShare=("HasIEP", "mean"),
        DLLShare=("IsDLL", "mean"),
        HomelessEligibilityShare=("IsHomelessEligibility", "mean"),
        MedianFamilyMonthlyIncome=("FamilyMonthlyIncome", "median"),
        MeanFamilySize=("FamilySize", "mean"),
    )

    # Agency-level context is derived from the same month and is known at forecast time.
    agency = grouped.groupby(["MonthDate", "VendorNumber"], as_index=False).agg(
        AgencyEnrollment=("EnrollmentCount", "sum"),
        AgencyActiveSites=("PreschoolCDSCode", "nunique"),
    )
    grouped = grouped.merge(agency, on=["MonthDate", "VendorNumber"], how="left")
    grouped["SnapshotMonth"] = grouped["MonthDate"].dt.strftime("%Y-%m")
    grouped["FundingType"] = "CSPP"
    grouped["DataSource"] = "CAPSDAC child extract aggregated to site-month"

    return grouped[
        [
            "SnapshotMonth", "MonthDate", "VendorNumber", "LEAID", "LEAName", "County",
            "PreschoolID", "PreschoolCDSCode", "SiteName", "EnrollmentCount", "FTShare",
            "IEPShare", "DLLShare", "HomelessEligibilityShare", "MedianFamilyMonthlyIncome",
            "MeanFamilySize", "AgencyEnrollment", "AgencyActiveSites", "FundingType", "DataSource",
        ]
    ].sort_values(["MonthDate", "PreschoolCDSCode"]).reset_index(drop=True)


def write_site_month_aggregate(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    out = aggregate_child_to_site_month(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)
    return out
