"""
CAPSDAC pipeline helper script.

This script validates the package structure, checks raw data availability,
summarizes tables/figures, and writes a pipeline summary report.

Run from project root:

    python scripts/run_capsdac_pipeline.py
"""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "Child_April_deidentified_sample.csv"
FIGURE_DIR = ROOT / "outputs" / "figures"
TABLE_DIR = ROOT / "outputs" / "tables"
REPORT_DIR = ROOT / "outputs" / "reports"


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    lines = ["# CAPSDAC Pipeline Summary", ""]

    lines.append("## Raw Data Check")

    if RAW_DATA.exists():
        df = pd.read_csv(RAW_DATA)
        lines.append(f"- Raw data found: `{RAW_DATA}`")
        lines.append(f"- Rows: {len(df):,}")
        lines.append(f"- Columns: {len(df.columns):,}")

        schema = pd.DataFrame({
            "column": df.columns,
            "dtype": [str(df[c].dtype) for c in df.columns],
            "missing_count": [df[c].isna().sum() for c in df.columns],
        })

        schema_path = TABLE_DIR / "deidentified_sample_schema_from_pipeline.csv"
        schema.to_csv(schema_path, index=False)
        lines.append(f"- Schema saved to: `{schema_path}`")
    else:
        lines.append(f"- Raw data missing: `{RAW_DATA}`")

    lines.append("")
    lines.append("## Figure Inventory")

    figures = sorted(list(FIGURE_DIR.glob("*.jpg")) + list(FIGURE_DIR.glob("*.png")))

    if figures:
        for fig in figures:
            lines.append(f"- `{fig.name}`")
    else:
        lines.append("- No figures found.")

    lines.append("")
    lines.append("## Table Inventory")

    tables = sorted(TABLE_DIR.glob("*.csv"))

    if tables:
        for table in tables:
            lines.append(f"- `{table.name}`")
    else:
        lines.append("- No tables found.")

    lines.append("")
    lines.append("## Recommended Notebook Order")
    lines.append("1. `notebooks/01_capsdac_child_monthly_snapshots.ipynb`")
    lines.append("2. `notebooks/02_capsdac_3_5_month_recursive_forecast.ipynb`")
    lines.append("3. `notebooks/03_capsdac_geo_heatmaps_printable.ipynb`")

    report_path = REPORT_DIR / "pipeline_summary.md"
    report_path.write_text("\\n".join(lines), encoding="utf-8")

    print(f"Pipeline summary written to: {report_path}")


if __name__ == "__main__":
    main()
