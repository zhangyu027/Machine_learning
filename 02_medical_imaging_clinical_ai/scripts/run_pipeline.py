from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from imaging_pipeline.bronze_ingest import run_bronze
from imaging_pipeline.silver_preprocess import run_silver
from imaging_pipeline.gold_feature_table import run_gold
from imaging_pipeline.train_eval_pipeline import train_and_evaluate


def main():
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "outputs" / "tables"
    bronze = run_bronze(output_dir)
    silver = run_silver(bronze, output_dir)
    gold = run_gold(silver, output_dir)
    metrics = train_and_evaluate(gold, output_dir=output_dir, model_dir=root / "models")
    eval_dir = root / "evaluation"
    eval_dir.mkdir(exist_ok=True)
    summary = {
        "project": "02_medical_imaging_clinical_ai",
        "pipeline_status": "completed_successfully",
        "bronze_table": "outputs/tables/bronze_imaging_metadata.csv",
        "silver_table": "outputs/tables/silver_imaging_features.csv",
        "gold_table": "outputs/tables/gold_patient_imaging_features.csv",
        "metrics": metrics,
        "validation_notes": [
            "End-to-end medical imaging lakehouse pipeline executed successfully.",
            "Bronze, Silver, and Gold data assets were generated from synthetic demo data.",
            "Metrics are for portfolio pipeline validation and are not representative of clinical deployment."
        ]
    }
    (eval_dir / "evaluation_summary.json").write_text(json.dumps(summary, indent=2))
    print("Medical imaging clinical AI pipeline completed successfully.")
    print(f"Gold table: {gold}")
    print(f"Metrics: {metrics}")


if __name__ == "__main__":
    main()
