from src.healthcare_mm.ingestion.load_sources import load_sample_sources
from src.healthcare_mm.lakehouse.build_gold import build_gold_patient_encounter_table
from src.healthcare_mm.features.multimodal_features import build_feature_frame

def test_gold_and_feature_pipeline():
    sources = load_sample_sources()
    gold = build_gold_patient_encounter_table(sources)
    features = build_feature_frame(gold)
    assert len(gold) > 0
    assert "readmitted_30d" in features.columns
    assert features.shape[1] > 10
