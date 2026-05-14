"""
Visualization for Phase 2 LSTM model outputs.
"""

from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    PrecisionRecallDisplay,
    confusion_matrix,
)


def generate_lstm_figures(
    predictions_path="outputs/tables/lstm_predictions.csv",
    loss_path="outputs/tables/lstm_training_loss.csv",
    metrics_path="outputs/tables/lstm_model_metrics.json",
    output_dir="outputs/figures",
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pred = pd.read_csv(predictions_path)
    loss = pd.read_csv(loss_path)
    metrics = json.loads(Path(metrics_path).read_text(encoding="utf-8"))

    # LSTM training loss
    plt.figure(figsize=(8, 5))
    plt.plot(loss["epoch"], loss["loss"], marker="o", label="total loss")
    plt.plot(loss["epoch"], loss["classification_loss"], label="classification loss")
    plt.title("LSTM Training Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.legend()
    plt.savefig(output_dir / "lstm_training_loss_curve.png", bbox_inches="tight")
    plt.close()

    # Confusion matrix
    cm = confusion_matrix(pred["actual_delay_risk"], pred["predicted_delay_risk"])
    disp = ConfusionMatrixDisplay(cm, display_labels=["Low Risk", "Delay Risk"])
    disp.plot()
    plt.title("LSTM Delay Risk Confusion Matrix")
    plt.savefig(output_dir / "lstm_confusion_matrix_delay_risk.png", bbox_inches="tight")
    plt.close()

    # ROC
    RocCurveDisplay.from_predictions(
        pred["actual_delay_risk"],
        pred["predicted_delay_probability"],
        name="LSTM delay risk",
    )
    plt.title("LSTM ROC Curve: Delay Risk Prediction")
    plt.savefig(output_dir / "lstm_roc_curve_delay_risk.png", bbox_inches="tight")
    plt.close()

    # PR
    PrecisionRecallDisplay.from_predictions(
        pred["actual_delay_risk"],
        pred["predicted_delay_probability"],
        name="LSTM delay risk",
    )
    plt.title("LSTM Precision-Recall Curve")
    plt.savefig(output_dir / "lstm_precision_recall_delay_risk.png", bbox_inches="tight")
    plt.close()

    # Actual vs predicted delay minutes
    plt.figure(figsize=(8, 5))
    plt.scatter(
        pred["actual_delay_minutes"],
        pred["predicted_delay_minutes"],
        alpha=0.4,
    )
    plt.title("LSTM Actual vs Predicted Delay Minutes")
    plt.xlabel("Actual Delay Minutes")
    plt.ylabel("Predicted Delay Minutes")
    plt.grid(True)
    plt.savefig(output_dir / "lstm_actual_vs_predicted_delay_minutes.png", bbox_inches="tight")
    plt.close()

    # Metrics bar chart
    metric_df = pd.DataFrame({
        "metric": ["accuracy", "f1", "auc"],
        "value": [metrics["accuracy"], metrics["f1"], metrics["auc"]],
    })

    plt.figure(figsize=(7, 5))
    plt.bar(metric_df["metric"], metric_df["value"])
    plt.title("LSTM Classification Metrics")
    plt.ylim(0, 1)
    plt.grid(axis="y")
    plt.savefig(output_dir / "lstm_classification_metrics_bar_chart.png", bbox_inches="tight")
    plt.close()

    return list(output_dir.glob("lstm_*.png"))


if __name__ == "__main__":
    files = generate_lstm_figures()
    print("Generated LSTM figures:")
    for file in files:
        print(file)
