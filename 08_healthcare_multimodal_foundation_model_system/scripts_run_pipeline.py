from src.healthcare_mm.ingestion.load_sources import load_sample_sources
from src.healthcare_mm.lakehouse.build_gold import build_gold_patient_encounter_table
from src.healthcare_mm.features.multimodal_features import build_feature_frame
from src.healthcare_mm.models.train_readmission_model import train_model
from src.healthcare_mm.mlops.model_card import write_model_card

def main():
    sources = load_sample_sources()
    gold = build_gold_patient_encounter_table(sources)
    gold.to_csv("data/sample/gold_patient_encounter.csv", index=False)
    features = build_feature_frame(gold)
    features.to_csv("data/sample/model_features.csv", index=False)
    metrics = train_model(features)
    write_model_card(metrics)
    print(metrics)

if __name__ == "__main__":
    main()
