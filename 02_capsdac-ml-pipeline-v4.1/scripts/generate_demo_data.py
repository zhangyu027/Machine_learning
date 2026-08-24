from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    rng = np.random.default_rng(2026)
    months = pd.date_range("2025-07-01", periods=12, freq="MS")
    rows = []
    for site_idx in range(1, 41):
        vendor = 6000 + (site_idx - 1) // 5
        base = 20 + (site_idx % 12) * 4
        county = ["Orange", "Los Angeles", "Sacramento", "Alameda"][site_idx % 4]
        for t, month in enumerate(months):
            season = 4 * np.sin(2 * np.pi * month.month / 12)
            enrollment = max(3, int(round(base + 1.1 * t + season + rng.normal(0, 3))))
            rows.append({
                "SnapshotMonth": month.strftime("%Y-%m"),
                "MonthDate": month,
                "VendorNumber": vendor,
                "LEAID": f"D{vendor}",
                "LEAName": f"Demo LEA {vendor}",
                "County": county,
                "PreschoolID": site_idx,
                "PreschoolCDSCode": f"DEMO{site_idx:04d}",
                "SiteName": f"Demo Site {site_idx}",
                "EnrollmentCount": enrollment,
                "FTShare": float(np.clip(0.35 + rng.normal(0, 0.05), 0.1, 0.8)),
                "IEPShare": float(np.clip(0.10 + rng.normal(0, 0.02), 0, 0.3)),
                "DLLShare": float(np.clip(0.50 + rng.normal(0, 0.08), 0.1, 0.9)),
                "HomelessEligibilityShare": float(np.clip(0.02 + rng.normal(0, 0.01), 0, 0.1)),
                "MedianFamilyMonthlyIncome": float(max(500, 2800 + rng.normal(0, 500))),
                "MeanFamilySize": float(np.clip(3.5 + rng.normal(0, 0.3), 2, 6)),
                "FundingType": "CSPP",
                "DataSource": "synthetic demo",
            })
    df = pd.DataFrame(rows)
    agency = df.groupby(["MonthDate", "VendorNumber"], as_index=False).agg(
        AgencyEnrollment=("EnrollmentCount", "sum"),
        AgencyActiveSites=("PreschoolCDSCode", "nunique"),
    )
    df = df.merge(agency, on=["MonthDate", "VendorNumber"], how="left")
    out = ROOT / "data/demo/capsdac_12month_site_demo.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(out)


if __name__ == "__main__":
    main()
