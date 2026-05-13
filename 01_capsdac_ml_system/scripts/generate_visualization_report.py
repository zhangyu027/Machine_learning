"""
Generate a visualization inventory report for CAPSDAC ML System.

Run from project root:

    python scripts/generate_visualization_report.py
"""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "outputs" / "figures"
REPORT_DIR = ROOT / "outputs" / "reports"


FIGURE_DESCRIPTIONS = {
    "cspp_enrollment_growth.jpg": "Historical and predicted statewide CSPP enrollment trend.",
    "geomap_county_enrollment.jpg": "County-level enrollment contribution heat map.",
    "top_20_sites_heatmap.jpg": "Top 20 site monthly contribution heatmap.",
    "top_sites_contribution.jpg": "Top site contribution percentage.",
    "top_vendor_contribution.jpg": "Top vendor contribution percentage.",
    "top_10_sites_forecast_enrollment.jpg": "Top sites by forecast enrollment.",
    "top_10_sites_growth_forecast.jpg": "Top preschool enrollment growth forecast.",
    "top_10_vendor_forecast_enrollment.jpg": "Top vendors by forecast enrollment.",
    "top_10_vendor_growth_forecast.jpg": "Top vendor enrollment growth forecast.",
}


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []

    figures = sorted(list(FIGURE_DIR.glob("*.jpg")) + list(FIGURE_DIR.glob("*.png")))

    for fig in figures:
        rows.append({
            "figure_file": fig.name,
            "description": FIGURE_DESCRIPTIONS.get(fig.name, "CAPSDAC visualization output."),
            "relative_path": str(fig.relative_to(ROOT)),
        })

    out_df = pd.DataFrame(rows)

    csv_path = REPORT_DIR / "visualization_inventory.csv"
    out_df.to_csv(csv_path, index=False)

    md_lines = ["# Visualization Inventory", ""]

    for _, row in out_df.iterrows():
        md_lines.append(f"## {row['figure_file']}")
        md_lines.append("")
        md_lines.append(row["description"])
        md_lines.append("")
        md_lines.append(f"`{row['relative_path']}`")
        md_lines.append("")

    md_path = REPORT_DIR / "visualization_inventory.md"
    md_path.write_text("\\n".join(md_lines), encoding="utf-8")

    print(f"Saved visualization inventory CSV: {csv_path}")
    print(f"Saved visualization inventory markdown: {md_path}")


if __name__ == "__main__":
    main()
