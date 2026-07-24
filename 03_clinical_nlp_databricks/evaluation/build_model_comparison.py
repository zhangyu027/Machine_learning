"""Build an honest model-comparison table from actually generated metric artifacts."""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def read_metrics(filename: str) -> dict:
    path = OUT / filename
    if not path.exists():
        return {"status": "not_run"}
    return json.loads(path.read_text())


def display_number(value, digits=4):
    return "Not run" if value is None else round(float(value), digits)


def main() -> None:
    baseline = read_metrics("model_metrics.json")
    distilbert = read_metrics("distilbert_metrics.json")
    gpt = read_metrics("gpt_metrics.json")
    specs = [
        ("TF-IDF", baseline, "Low", "High"),
        ("DistilBERT", distilbert, "Medium", "Medium"),
        ("GPT", gpt, "High", "Medium"),
    ]
    rows = []
    for name, metrics, default_cost, default_explainability in specs:
        rows.append({
            "Model": name,
            "Status": metrics.get("status", "not_run"),
            "Macro-F1": display_number(metrics.get("macro_f1")),
            "Eligible recall": display_number(metrics.get("eligible_recall")),
            "Latency (ms/note)": display_number(metrics.get("latency_ms_per_note"), 2),
            "Cost": metrics.get("cost_tier", default_cost),
            "Explainability": metrics.get("explainability", default_explainability),
        })
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "model_comparison.csv", index=False)
    markdown = "# Model Comparison\n\n" + table.to_markdown(index=False) + "\n\n"
    markdown += (
        "Only completed runs populate metrics. `Not run` is deliberately retained when "
        "transformer weights or GPT credentials were unavailable; no values are fabricated.\n"
    )
    (OUT / "model_comparison.md").write_text(markdown)
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
