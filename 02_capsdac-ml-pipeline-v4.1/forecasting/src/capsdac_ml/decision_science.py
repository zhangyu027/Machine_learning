from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def _first_existing(df: pd.DataFrame, names: list[str]):
    for n in names:
        if n in df.columns:
            return n
    return None


def build_reconciliation_review(certified_path: Path | None, child_counts_path: Path | None) -> pd.DataFrame:
    """Create an explainable agency review queue when optional reconciliation files are supplied.

    This is intentionally a rules/statistics layer, not a claim that a supervised risk model
    has been trained. It is safe to extend into ML after multiple labeled certification cycles exist.
    """
    if not certified_path or not child_counts_path:
        return pd.DataFrame()
    cert = pd.read_csv(certified_path)
    counts = pd.read_csv(child_counts_path)
    cert_key = _first_existing(cert, ["VendorNumber", "VendorCode", "AgencyCode", "LEACode"])
    count_key = _first_existing(counts, ["VendorNumber", "VendorCode", "AgencyCode", "LEACode"])
    official = _first_existing(cert, ["TotalEnrollment", "CertifiedEnrollmentOfficialCount", "OfficialCount"])
    child = _first_existing(counts, ["ChildCount", "EnrollmentCount"])
    monthly = _first_existing(counts, ["MonthlyEnrollmentYCount", "MonthlyEnrollmentCount"])
    if not all([cert_key, count_key, official, child]):
        raise ValueError("Optional reconciliation files do not expose recognizable agency/count columns.")
    c = cert[[cert_key, official]].copy().rename(columns={cert_key: "AgencyKey", official: "OfficialCertifiedCount"})
    keep = [count_key, child] + ([monthly] if monthly else [])
    x = counts[keep].copy().rename(columns={count_key: "AgencyKey", child: "ChildCount"})
    if monthly:
        x = x.rename(columns={monthly: "MonthlyEnrollmentYCount"})
    out = c.merge(x, on="AgencyKey", how="outer")
    for col in ["OfficialCertifiedCount", "ChildCount", "MonthlyEnrollmentYCount"]:
        if col in out:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)
    out["OfficialVsChildDifference"] = out["OfficialCertifiedCount"] - out["ChildCount"]
    denom = out[["OfficialCertifiedCount", "ChildCount"]].max(axis=1).clip(lower=1)
    out["AbsoluteDifferencePct"] = out["OfficialVsChildDifference"].abs() / denom
    if "MonthlyEnrollmentYCount" in out:
        out["OfficialVsMonthlyDifference"] = out["OfficialCertifiedCount"] - out["MonthlyEnrollmentYCount"]
    out["ReviewPriority"] = np.select(
        [out["AbsoluteDifferencePct"] >= 0.25, out["AbsoluteDifferencePct"] >= 0.10],
        ["High", "Medium"], default="Low"
    )
    out["ReviewReason"] = np.where(out["ReviewPriority"].eq("Low"), "Counts broadly aligned", "Certification/count reconciliation difference")
    return out.sort_values(["ReviewPriority", "AbsoluteDifferencePct"], ascending=[True, False])
