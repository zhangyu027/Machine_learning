from pathlib import Path

from src.healthcare_mm.ingestion.load_sources import load_sample_sources
from src.healthcare_mm.lakehouse.build_gold import build_gold_patient_encounter_table
from src.healthcare_mm.features.multimodal_features import build_feature_frame
from src.healthcare_mm.models.train_readmission_model import train_model
from src.healthcare_mm.mlops.model_card import write_model_card


def test_gold_and_feature_pipeline():
    sources = load_sample_sources()
    gold = build_gold_patient_encounter_table(sources)
    features = build_feature_frame(gold)
    assert len(gold) > 0
    assert "readmitted_30d" in features.columns
    assert features.shape[1] > 10


def test_training_and_model_card_outputs(tmp_path):
    sources = load_sample_sources()
    gold = build_gold_patient_encounter_table(sources)
    features = build_feature_frame(gold)
    metrics = train_model(features, model_dir=tmp_path / "models", output_dir=tmp_path / "outputs")
    write_model_card(metrics, path=tmp_path / "outputs" / "model_card.json")

    assert 0.0 <= metrics["roc_auc"] <= 1.0
    assert 0.0 <= metrics["average_precision"] <= 1.0
    assert (tmp_path / "models" / "readmission_gbm.joblib").exists()
    assert (tmp_path / "outputs" / "model_metrics.json").exists()
    assert (tmp_path / "outputs" / "model_card.json").exists()
