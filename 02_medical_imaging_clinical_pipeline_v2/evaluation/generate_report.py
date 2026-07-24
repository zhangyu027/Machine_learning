"""Generate plots, subgroup metrics, and misclassification artifacts."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import ConfusionMatrixDisplay, PrecisionRecallDisplay, RocCurveDisplay


def generate_evaluation_report(y_true, y_pred, y_prob, case_ids=None, output_dir="evaluation/reports"):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    RocCurveDisplay.from_predictions(y_true, y_prob)
    plt.tight_layout(); plt.savefig(output / "roc_curve.png", dpi=160); plt.close()
    PrecisionRecallDisplay.from_predictions(y_true, y_prob)
    plt.tight_layout(); plt.savefig(output / "precision_recall_curve.png", dpi=160); plt.close()
    ConfusionMatrixDisplay.from_predictions(y_true, y_pred)
    plt.tight_layout(); plt.savefig(output / "confusion_matrix.png", dpi=160); plt.close()

    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=8, strategy="quantile")
    plt.figure(); plt.plot(prob_pred, prob_true, marker="o"); plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("Mean predicted probability"); plt.ylabel("Observed positive rate")
    plt.tight_layout(); plt.savefig(output / "calibration_curve.png", dpi=160); plt.close()

    case_ids = list(range(len(y_true))) if case_ids is None else list(case_ids)
    errors = pd.DataFrame({"case_id": case_ids, "actual": y_true, "predicted": y_pred, "probability": y_prob})
    errors = errors[errors.actual != errors.predicted].copy()
    errors["error_type"] = errors.apply(lambda r: "false_negative" if r.actual == 1 else "false_positive", axis=1)
    errors.sort_values("probability", ascending=False).to_csv(output / "misclassified_cases.csv", index=False)
    return {"misclassified_cases": int(len(errors)), "report_dir": str(output)}


if __name__ == "__main__":
    raise SystemExit("Import generate_evaluation_report from a training/evaluation script.")
