"""
Sequential telemetry feature engineering.

This module converts Gold telemetry records into rolling train-level sequences
for LSTM modeling. The goal is to move beyond a row-level feedforward neural
network and model temporal train movement history.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler


SEQUENCE_FEATURE_COLS = [
    "scheduled_minutes",
    "distance_miles",
    "avg_speed_mph",
    "brake_pressure",
    "engine_temp",
    "vibration_score",
    "weather_severity",
    "route_congestion",
    "cargo_weight_tons",
    "hour",
    "day_of_week",
]


def create_lstm_sequences(
    gold_path="data/gold/train_delay_features.parquet",
    sequence_path="data/gold/train_delay_sequences.npz",
    scaler_path="outputs/models/lstm_sequence_scaler.joblib",
    metadata_path="outputs/tables/lstm_sequence_metadata.json",
    sequence_length=8,
):
    """
    Create train-level rolling sequences.

    For each train_id, records are sorted by event_time. A sequence of previous
    telemetry observations predicts the current delay risk and delay minutes.
    """

    gold_path = Path(gold_path)
    sequence_path = Path(sequence_path)
    scaler_path = Path(scaler_path)
    metadata_path = Path(metadata_path)

    sequence_path.parent.mkdir(parents=True, exist_ok=True)
    scaler_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(gold_path)
    df["event_time"] = pd.to_datetime(df["event_time"])
    df = df.sort_values(["train_id", "event_time"]).reset_index(drop=True)

    required_cols = ["train_id", "event_time", "delay_risk", "delay_minutes"] + SEQUENCE_FEATURE_COLS
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for sequence modeling: {missing}")

    scaler = StandardScaler()
    df[SEQUENCE_FEATURE_COLS] = scaler.fit_transform(df[SEQUENCE_FEATURE_COLS]).astype("float32")

    X_seq = []
    y_risk = []
    y_delay = []
    sequence_info = []

    for train_id, group in df.groupby("train_id"):
        group = group.sort_values("event_time").reset_index(drop=True)

        if len(group) <= sequence_length:
            continue

        values = group[SEQUENCE_FEATURE_COLS].values.astype("float32")

        for idx in range(sequence_length, len(group)):
            X_seq.append(values[idx-sequence_length:idx])
            y_risk.append(float(group.loc[idx, "delay_risk"]))
            y_delay.append(float(group.loc[idx, "delay_minutes"]))
            sequence_info.append({
                "train_id": train_id,
                "target_event_time": str(group.loc[idx, "event_time"]),
                "route_id": str(group.loc[idx, "route_id"]),
            })

    X_seq = np.array(X_seq, dtype="float32")
    y_risk = np.array(y_risk, dtype="float32")
    y_delay = np.array(y_delay, dtype="float32")

    if len(X_seq) == 0:
        raise ValueError(
            "No sequences were created. Increase synthetic data volume or reduce sequence_length."
        )

    np.savez_compressed(
        sequence_path,
        X_seq=X_seq,
        y_risk=y_risk,
        y_delay=y_delay,
    )

    joblib.dump(scaler, scaler_path)

    metadata = {
        "sequence_length": sequence_length,
        "feature_columns": SEQUENCE_FEATURE_COLS,
        "n_sequences": int(len(X_seq)),
        "sequence_shape": list(X_seq.shape),
        "target_description": "Predict current delay risk and delay minutes from prior telemetry sequence.",
        "sequence_info_sample": sequence_info[:10],
    }

    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Created sequences: {X_seq.shape}")
    print(f"Saved sequence data to: {sequence_path}")

    return X_seq, y_risk, y_delay, metadata


if __name__ == "__main__":
    create_lstm_sequences()
