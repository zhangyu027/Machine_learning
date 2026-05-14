from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, ConfusionMatrixDisplay, confusion_matrix


def generate_figures(
    predictions_path="outputs/tables/predictions.csv",
    loss_path="outputs/tables/training_loss.csv",
    metrics_path="outputs/tables/model_metrics.json",
    output_dir="outputs/figures",
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pred = pd.read_csv(predictions_path)
    loss = pd.read_csv(loss_path)
    metrics = json.loads(Path(metrics_path).read_text())

    plt.figure(figsize=(8, 5))
    plt.plot(loss["epoch"], loss["loss"], marker="o")
    plt.title("Neural Network Training Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.savefig(output_dir / "training_loss_curve.png", bbox_inches="tight")
    plt.close()

    cm = confusion_matrix(pred["actual_delay_risk"], pred["predicted_delay_risk"])
    disp = ConfusionMatrixDisplay(cm, display_labels=["Low Risk", "Delay Risk"])
    disp.plot()
    plt.title("Delay Risk Confusion Matrix")
    plt.savefig(output_dir / "confusion_matrix_delay_risk.png", bbox_inches="tight")
    plt.close()

    RocCurveDisplay.from_predictions(pred["actual_delay_risk"], pred["predicted_delay_probability"], name="Delay risk NN")
    plt.title("ROC Curve: Delay Risk Prediction")
    plt.savefig(output_dir / "roc_curve_delay_risk.png", bbox_inches="tight")
    plt.close()

    PrecisionRecallDisplay.from_predictions(pred["actual_delay_risk"], pred["predicted_delay_probability"], name="Delay risk NN")
    plt.title("Precision-Recall Curve: Delay Risk Prediction")
    plt.savefig(output_dir / "precision_recall_delay_risk.png", bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(pred["actual_delay_minutes"], pred["predicted_delay_minutes"], alpha=0.4)
    plt.title("Actual vs Predicted Delay Minutes")
    plt.xlabel("Actual Delay Minutes")
    plt.ylabel("Predicted Delay Minutes")
    plt.grid(True)
    plt.savefig(output_dir / "actual_vs_predicted_delay_minutes.png", bbox_inches="tight")
    plt.close()

    metric_df = pd.DataFrame({
        "metric": ["accuracy", "f1", "auc"],
        "value": [metrics["accuracy"], metrics["f1"], metrics["auc"]]
    })
    plt.figure(figsize=(7, 5))
    plt.bar(metric_df["metric"], metric_df["value"])
    plt.title("Classification Metrics")
    plt.ylim(0, 1)
    plt.grid(axis="y")
    plt.savefig(output_dir / "classification_metrics_bar_chart.png", bbox_inches="tight")
    plt.close()

    return list(output_dir.glob("*.png"))


if __name__ == "__main__":
    print(generate_figures())
