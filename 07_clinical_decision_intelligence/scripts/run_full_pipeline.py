import json
from pathlib import Path
import pandas as pd
from src.ml.train_xgboost_readmission import train_xgboost_readmission, save_model
from src.causal.propensity_matching import estimate_propensity_scores, nearest_neighbor_att

ROOT = Path(__file__).resolve().parents[1]

def main():
    df = pd.read_csv(ROOT / "data/raw/patient_encounters.csv")
    model, cols, metrics = train_xgboost_readmission(df)
    save_model(model, cols, ROOT / "models/xgboost_readmission_model.joblib")
    covariates = ["age","sex","insurance","hospital_id","comorbidity_index","prior_admissions_12m","severity_score"]
    _, ps, _ = estimate_propensity_scores(df, "care_management_program", covariates)
    df["propensity_score"] = ps
    att = nearest_neighbor_att(df, "readmitted_30d", "care_management_program", ps)
    summary = {"xgboost_readmission_model": metrics, "propensity_score_matching": att}
    (ROOT / "reports/model_outputs/model_summary.json").write_text(json.dumps(summary, indent=2))
    df.to_csv(ROOT / "data/processed/clinical_modeling_dataset.csv", index=False)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
