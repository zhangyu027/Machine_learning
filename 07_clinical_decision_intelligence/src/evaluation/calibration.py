from __future__ import annotations
import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss

def calibration_report(y_true, probabilities, bins: int = 10) -> dict:
    prob_true, prob_pred = calibration_curve(y_true, probabilities, n_bins=bins, strategy="quantile")
    return {
        "brier_score": float(brier_score_loss(y_true, probabilities)),
        "mean_predicted_probability": float(np.mean(probabilities)),
        "observed_event_rate": float(np.mean(y_true)),
        "curve": [{"predicted": float(p), "observed": float(o)} for p, o in zip(prob_pred, prob_true)],
    }
