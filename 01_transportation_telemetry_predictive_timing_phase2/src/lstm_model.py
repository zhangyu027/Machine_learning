"""
LSTM model for train telemetry predictive timing.

This is the Phase 2 research-grade upgrade. It models sequential telemetry
windows instead of treating every event as an independent row.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    mean_absolute_error,
    mean_squared_error,
    classification_report,
    confusion_matrix,
)


class TelemetryLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim=64, num_layers=1, dropout=0.15):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )

        self.shared = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
        )

        self.classifier = nn.Linear(32, 1)
        self.regressor = nn.Linear(32, 1)

    def forward(self, x):
        output, (hidden, cell) = self.lstm(x)
        last_hidden = output[:, -1, :]

        shared = self.shared(last_hidden)

        risk_logit = self.classifier(shared).squeeze(1)
        delay_pred = self.regressor(shared).squeeze(1)

        return risk_logit, delay_pred


def train_lstm_model(
    sequence_path="data/gold/train_delay_sequences.npz",
    model_path="outputs/models/lstm_delay_timing.pt",
    metrics_path="outputs/tables/lstm_model_metrics.json",
    report_path="outputs/tables/lstm_classification_report.csv",
    predictions_path="outputs/tables/lstm_predictions.csv",
    loss_path="outputs/tables/lstm_training_loss.csv",
    confusion_matrix_path="outputs/tables/lstm_confusion_matrix.csv",
    epochs=40,
    seed=42,
):
    torch.manual_seed(seed)
    np.random.seed(seed)

    sequence_path = Path(sequence_path)
    model_path = Path(model_path)
    metrics_path = Path(metrics_path)
    report_path = Path(report_path)
    predictions_path = Path(predictions_path)
    loss_path = Path(loss_path)
    confusion_matrix_path = Path(confusion_matrix_path)

    for p in [model_path.parent, metrics_path.parent, report_path.parent, predictions_path.parent]:
        p.mkdir(parents=True, exist_ok=True)

    data = np.load(sequence_path)
    X_seq = data["X_seq"].astype("float32")
    y_risk = data["y_risk"].astype("float32")
    y_delay = data["y_delay"].astype("float32")

    X_train, X_test, yrisk_train, yrisk_test, ydelay_train, ydelay_test = train_test_split(
        X_seq,
        y_risk,
        y_delay,
        test_size=0.25,
        random_state=seed,
        stratify=y_risk,
    )

    model = TelemetryLSTM(input_dim=X_seq.shape[2])

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    bce = nn.BCEWithLogitsLoss()
    mse = nn.MSELoss()

    X_train_t = torch.tensor(X_train)
    yrisk_train_t = torch.tensor(yrisk_train)
    ydelay_train_t = torch.tensor(ydelay_train)

    history = []

    for epoch in range(epochs):
        model.train()

        risk_logit, delay_pred = model(X_train_t)

        loss_class = bce(risk_logit, yrisk_train_t)
        loss_reg = mse(delay_pred, ydelay_train_t)
        loss = loss_class + 0.02 * loss_reg

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        history.append({
            "epoch": epoch + 1,
            "loss": float(loss.detach().numpy()),
            "classification_loss": float(loss_class.detach().numpy()),
            "regression_loss": float(loss_reg.detach().numpy()),
        })

        print(
            f"Epoch {epoch+1:02d}/{epochs} | "
            f"Loss={loss.item():.4f} | "
            f"Class={loss_class.item():.4f} | "
            f"Reg={loss_reg.item():.4f}"
        )

    model.eval()

    with torch.no_grad():
        risk_logit, delay_pred = model(torch.tensor(X_test))
        risk_prob = torch.sigmoid(risk_logit).numpy()
        delay_pred_np = delay_pred.numpy()

    y_pred = (risk_prob >= 0.5).astype(int)

    metrics = {
        "model_type": "LSTM sequence model",
        "accuracy": float(accuracy_score(yrisk_test, y_pred)),
        "f1": float(f1_score(yrisk_test, y_pred, zero_division=0)),
        "auc": float(roc_auc_score(yrisk_test, risk_prob)),
        "mae_delay_minutes": float(mean_absolute_error(ydelay_test, delay_pred_np)),
        "rmse_delay_minutes": float(mean_squared_error(ydelay_test, delay_pred_np) ** 0.5),
        "n_test": int(len(yrisk_test)),
        "sequence_length": int(X_seq.shape[1]),
        "n_features": int(X_seq.shape[2]),
    }

    torch.save(model.state_dict(), model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    pd.DataFrame(history).to_csv(loss_path, index=False)

    pd.DataFrame(
        classification_report(
            yrisk_test,
            y_pred,
            output_dict=True,
            zero_division=0,
        )
    ).transpose().to_csv(report_path)

    pd.DataFrame({
        "actual_delay_risk": yrisk_test,
        "predicted_delay_risk": y_pred,
        "predicted_delay_probability": risk_prob,
        "actual_delay_minutes": ydelay_test,
        "predicted_delay_minutes": delay_pred_np,
    }).to_csv(predictions_path, index=False)

    pd.DataFrame(confusion_matrix(yrisk_test, y_pred)).to_csv(confusion_matrix_path, index=False)

    print("\nLSTM training complete.")
    print(json.dumps(metrics, indent=2))

    return metrics


if __name__ == "__main__":
    train_lstm_model()
