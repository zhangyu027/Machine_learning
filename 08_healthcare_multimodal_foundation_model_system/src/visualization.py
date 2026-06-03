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


def generate_figures(
    predictions_path="outputs/tables/predictions.csv",
    loss_path="outputs/tables/training_loss.csv",
    metrics_path="outputs/tables/model_metrics.json",
    fairness_path="outputs/tables/fairness_subgroup_metrics.csv",
    output_dir="outputs/figures",
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pred = pd.read_csv(predictions_path)
    loss = pd.read_csv(loss_path)
    metrics = json.loads(Path(metrics_path).read_text())

    plt.figure(figsize=(8, 5))
    plt.plot(loss["epoch"], loss["loss"], marker="o")
    plt.title("Multimodal Model Training Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.savefig(output_dir / "training_loss_curve.png", bbox_inches="tight")
    plt.close()

    cm = confusion_matrix(pred["actual_high_risk"], pred["predicted_high_risk"])
    disp = ConfusionMatrixDisplay(cm, display_labels=["Low Risk", "High Risk"])
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig(output_dir / "confusion_matrix.png", bbox_inches="tight")
    plt.close()

    RocCurveDisplay.from_predictions(
        pred["actual_high_risk"],
        pred["predicted_probability"],
        name="Multimodal risk model",
    )
    plt.title("ROC Curve")
    plt.savefig(output_dir / "roc_curve.png", bbox_inches="tight")
    plt.close()

    PrecisionRecallDisplay.from_predictions(
        pred["actual_high_risk"],
        pred["predicted_probability"],
        name="Multimodal risk model",
    )
    plt.title("Precision-Recall Curve")
    plt.savefig(output_dir / "precision_recall_curve.png", bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7, 5))
    plt.bar(["accuracy", "f1", "auc"], [metrics["accuracy"], metrics["f1"], metrics["auc"]])
    plt.title("Model Performance Metrics")
    plt.ylim(0, 1)
    plt.grid(axis="y")
    plt.savefig(output_dir / "model_metrics_bar_chart.png", bbox_inches="tight")
    plt.close()

    if Path(fairness_path).exists():
        fair = pd.read_csv(fairness_path)
        plt.figure(figsize=(9, 5))
        plot_df = fair[fair["subgroup_variable"] == "sex"]
        plt.bar(plot_df["subgroup_value"].astype(str), plot_df["accuracy"])
        plt.title("Fairness Check: Accuracy by Sex")
        plt.xlabel("Sex subgroup")
        plt.ylabel("Accuracy")
        plt.ylim(0, 1)
        plt.grid(axis="y")
        plt.savefig(output_dir / "fairness_accuracy_by_sex.png", bbox_inches="tight")
        plt.close()

    return list(output_dir.glob("*.png"))


if __name__ == "__main__":
    print(generate_figures())
