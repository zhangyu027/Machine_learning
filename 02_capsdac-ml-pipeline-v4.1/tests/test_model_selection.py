import pandas as pd

from src.capsdac_ml.feature_engineering import build_monthly_features
from src.capsdac_ml.model_selection import expanding_window_splits, run_model_selection
from src.capsdac_ml.monitoring import drift_report


def load_demo_features():
    raw = pd.read_csv("data/demo/capsdac_12month_site_demo.csv", dtype={"VendorNumber": str, "PreschoolCDSCode": str})
    return build_monthly_features(raw)


def test_expanding_window_splits_and_model_selection_run():
    features = load_demo_features()
    splits = expanding_window_splits(features)
    assert len(splits) >= 4
    model, report, leaderboard = run_model_selection(features, max_param_sets_per_model=1)
    assert report["selected_model"]["model_name"] in set(leaderboard["model_name"])
    assert hasattr(model, "predict")


def test_drift_report_has_status():
    features = load_demo_features()
    report = drift_report(features)
    assert report["overall_status"] in {"stable", "moderate", "high"}
    assert len(report["features"]) > 0
