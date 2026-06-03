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
    classification_report,
    confusion_matrix,
    brier_score_loss,
)

from src.model import MultimodalRiskModel


def train_multimodal_model(
    feature_path="data/processed/multimodal_features.npz",
    model_path="outputs/models/multimodal_risk_model.pt",
    metrics_path="outputs/tables/model_metrics.json",
    predictions_path="outputs/tables/predictions.csv",
    report_path="outputs/tables/classification_report.csv",
    epochs=30,
    seed=42,
):
    torch.manual_seed(seed)
    np.random.seed(seed)

    model_path = Path(model_path)
    metrics_path = Path(metrics_path)
    predictions_path = Path(predictions_path)
    report_path = Path(report_path)

    for p in [model_path.parent, metrics_path.parent, predictions_path.parent, report_path.parent]:
        p.mkdir(parents=True, exist_ok=True)

    data = np.load(feature_path)

    images = data["images"].astype("float32")
    structured = data["structured"].astype("float32")
    labs = data["labs"].astype("float32")
    text = data["text"].astype("float32")
    y = data["y"].astype("float32")
    subgroup_sex = data["subgroup_sex"]
    subgroup_site = data["subgroup_site"]

    indices = np.arange(len(y))
    train_idx, test_idx = train_test_split(
        indices,
        test_size=0.25,
        random_state=seed,
        stratify=y,
    )

    model = MultimodalRiskModel(
        structured_dim=structured.shape[1],
        lab_dim=labs.shape[1],
        text_dim=text.shape[1],
    )

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.BCEWithLogitsLoss()

    X_img_train = torch.tensor(images[train_idx])
    X_struct_train = torch.tensor(structured[train_idx])
    X_lab_train = torch.tensor(labs[train_idx])
    X_text_train = torch.tensor(text[train_idx])
    y_train = torch.tensor(y[train_idx])

    history = []

    for epoch in range(epochs):
        model.train()

        logits = model(X_img_train, X_struct_train, X_lab_train, X_text_train)
        loss = loss_fn(logits, y_train)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        history.append({"epoch": epoch + 1, "loss": float(loss.detach().numpy())})
        print(f"Epoch {epoch+1:02d}/{epochs} | Loss={loss.item():.4f}")

    model.eval()

    with torch.no_grad():
        logits = model(
            torch.tensor(images[test_idx]),
            torch.tensor(structured[test_idx]),
            torch.tensor(labs[test_idx]),
            torch.tensor(text[test_idx]),
        )
        probs = torch.sigmoid(logits).numpy()

    preds = (probs >= 0.5).astype(int)
    y_test = y[test_idx]

    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "f1": float(f1_score(y_test, preds, zero_division=0)),
        "auc": float(roc_auc_score(y_test, probs)),
        "brier_score": float(brier_score_loss(y_test, probs)),
        "n_test": int(len(y_test)),
        "model_type": "multimodal image_text_labs_structured_fusion",
    }

    torch.save(model.state_dict(), model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    pd.DataFrame(history).to_csv(metrics_path.parent / "training_loss.csv", index=False)

    pd.DataFrame(
        classification_report(y_test, preds, output_dict=True, zero_division=0)
    ).transpose().to_csv(report_path)

    pd.DataFrame(confusion_matrix(y_test, preds)).to_csv(
        metrics_path.parent / "confusion_matrix.csv",
        index=False,
    )

    pred_df = pd.DataFrame({
        "actual_high_risk": y_test,
        "predicted_high_risk": preds,
        "predicted_probability": probs,
        "sex": subgroup_sex[test_idx],
        "site_id": subgroup_site[test_idx],
    })
    pred_df.to_csv(predictions_path, index=False)

    return metrics


if __name__ == "__main__":
    print(train_multimodal_model())
