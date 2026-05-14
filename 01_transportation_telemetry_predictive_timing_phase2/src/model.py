from pathlib import Path
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import joblib
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, mean_absolute_error, mean_squared_error, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


FEATURE_COLS = [
    "scheduled_minutes", "distance_miles", "avg_speed_mph", "brake_pressure",
    "engine_temp", "vibration_score", "weather_severity", "route_congestion",
    "cargo_weight_tons", "hour", "day_of_week"
]


class DelayTimingNN(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.15),
            nn.Linear(64, 32),
            nn.ReLU(),
        )
        self.classifier = nn.Linear(32, 1)
        self.regressor = nn.Linear(32, 1)

    def forward(self, x):
        h = self.shared(x)
        risk_logit = self.classifier(h).squeeze(1)
        delay_pred = self.regressor(h).squeeze(1)
        return risk_logit, delay_pred


def train_model(
    gold_path="data/gold/train_delay_features.parquet",
    model_path="outputs/models/delay_timing_nn.pt",
    scaler_path="outputs/models/scaler.joblib",
    metrics_path="outputs/tables/model_metrics.json",
    report_path="outputs/tables/classification_report.csv",
    predictions_path="outputs/tables/predictions.csv",
    epochs=30,
    seed=42,
):
    torch.manual_seed(seed)
    np.random.seed(seed)

    df = pd.read_parquet(gold_path)

    X = df[FEATURE_COLS].values.astype("float32")
    y_class = df["delay_risk"].values.astype("float32")
    y_reg = df["delay_minutes"].values.astype("float32")

    X_train, X_test, yc_train, yc_test, yr_train, yr_test = train_test_split(
        X, y_class, y_reg, test_size=0.25, random_state=seed, stratify=y_class
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train).astype("float32")
    X_test = scaler.transform(X_test).astype("float32")

    model = DelayTimingNN(input_dim=X_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    bce = nn.BCEWithLogitsLoss()
    mse = nn.MSELoss()

    X_train_t = torch.tensor(X_train)
    yc_train_t = torch.tensor(yc_train)
    yr_train_t = torch.tensor(yr_train)

    history = []

    for epoch in range(epochs):
        model.train()
        risk_logit, delay_pred = model(X_train_t)
        loss_class = bce(risk_logit, yc_train_t)
        loss_reg = mse(delay_pred, yr_train_t)
        loss = loss_class + 0.02 * loss_reg

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        history.append(float(loss.detach().numpy()))

    model.eval()
    with torch.no_grad():
        risk_logit, delay_pred = model(torch.tensor(X_test))
        risk_prob = torch.sigmoid(risk_logit).numpy()
        delay_pred_np = delay_pred.numpy()

    y_pred = (risk_prob >= 0.5).astype(int)

    metrics = {
        "accuracy": float(accuracy_score(yc_test, y_pred)),
        "f1": float(f1_score(yc_test, y_pred, zero_division=0)),
        "auc": float(roc_auc_score(yc_test, risk_prob)),
        "mae_delay_minutes": float(mean_absolute_error(yr_test, delay_pred_np)),
        "rmse_delay_minutes": float(mean_squared_error(yr_test, delay_pred_np) ** 0.5),
        "n_test": int(len(yc_test)),
    }

    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    Path(metrics_path).parent.mkdir(parents=True, exist_ok=True)

    torch.save(model.state_dict(), model_path)
    joblib.dump(scaler, scaler_path)
    Path(metrics_path).write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    report_df = pd.DataFrame(classification_report(yc_test, y_pred, output_dict=True, zero_division=0)).transpose()
    report_df.to_csv(report_path)

    pred_df = pd.DataFrame({
        "actual_delay_risk": yc_test,
        "predicted_delay_risk": y_pred,
        "predicted_delay_probability": risk_prob,
        "actual_delay_minutes": yr_test,
        "predicted_delay_minutes": delay_pred_np,
    })
    pred_df.to_csv(predictions_path, index=False)

    pd.DataFrame({"epoch": range(1, len(history)+1), "loss": history}).to_csv("outputs/tables/training_loss.csv", index=False)
    pd.DataFrame(confusion_matrix(yc_test, y_pred)).to_csv("outputs/tables/confusion_matrix.csv", index=False)

    return metrics


if __name__ == "__main__":
    print(train_model())
