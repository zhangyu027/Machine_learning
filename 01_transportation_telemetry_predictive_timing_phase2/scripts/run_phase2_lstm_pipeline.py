"""
Run the Phase 2 LSTM transportation telemetry pipeline.

This script runs:
1. synthetic IoT-style train telemetry generation
2. Bronze/Silver/Gold data engineering pipeline
3. sequence-window feature engineering
4. LSTM model training
5. LSTM evaluation figures
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.data_generator import generate_synthetic_telemetry
from src.pipeline import run_pipeline
from src.sequence_features import create_lstm_sequences
from src.lstm_model import train_lstm_model
from src.lstm_visualization import generate_lstm_figures


def main():
    print("Step 1: Generate synthetic IoT-style train telemetry")
    generate_synthetic_telemetry(
        n_events=12000,
        output_path=ROOT / "data/raw/train_telemetry_events.csv",
    )

    print("Step 2: Run Bronze/Silver/Gold pipeline")
    run_pipeline()

    print("Step 3: Create LSTM sequence windows")
    create_lstm_sequences(
        gold_path=ROOT / "data/gold/train_delay_features.parquet",
        sequence_path=ROOT / "data/gold/train_delay_sequences.npz",
        scaler_path=ROOT / "outputs/models/lstm_sequence_scaler.joblib",
        metadata_path=ROOT / "outputs/tables/lstm_sequence_metadata.json",
        sequence_length=8,
    )

    print("Step 4: Train LSTM predictive timing model")
    metrics = train_lstm_model(
        sequence_path=ROOT / "data/gold/train_delay_sequences.npz",
        model_path=ROOT / "outputs/models/lstm_delay_timing.pt",
        metrics_path=ROOT / "outputs/tables/lstm_model_metrics.json",
        report_path=ROOT / "outputs/tables/lstm_classification_report.csv",
        predictions_path=ROOT / "outputs/tables/lstm_predictions.csv",
        loss_path=ROOT / "outputs/tables/lstm_training_loss.csv",
        confusion_matrix_path=ROOT / "outputs/tables/lstm_confusion_matrix.csv",
        epochs=40,
    )

    print("Step 5: Generate LSTM figures")
    generate_lstm_figures(
        predictions_path=ROOT / "outputs/tables/lstm_predictions.csv",
        loss_path=ROOT / "outputs/tables/lstm_training_loss.csv",
        metrics_path=ROOT / "outputs/tables/lstm_model_metrics.json",
        output_dir=ROOT / "outputs/figures",
    )

    print("Phase 2 LSTM pipeline complete.")
    print(metrics)


if __name__ == "__main__":
    main()
