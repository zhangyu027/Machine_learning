from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from bandits.thompson_sampling import simulate_thompson_sampling
from causal.uplift_t_learner import TLearnerUpliftModel


def test_t_learner_fit_and_predict() -> None:
    frame = pd.DataFrame({"x": [0, 1, 2, 3, 4, 5], "t": [0, 0, 0, 1, 1, 1], "y": [0, 1, 2, 2, 4, 6]})
    model = TLearnerUpliftModel(n_estimators=10).fit(frame[["x"]], frame["y"], frame["t"])
    predictions = model.predict_cate(frame[["x"]])
    assert len(predictions) == len(frame)
    assert np.isfinite(predictions).all()


def test_t_learner_requires_both_arms() -> None:
    frame = pd.DataFrame({"x": [1, 2], "y": [1, 2], "t": [1, 1]})
    with pytest.raises(ValueError, match="both control"):
        TLearnerUpliftModel(n_estimators=5).fit(frame[["x"]], frame["y"], frame["t"])


def test_thompson_sampling_returns_snapshots() -> None:
    result = simulate_thompson_sampling([0.1, 0.2], steps=250, snapshot_every=100)
    assert result.iloc[-1]["step"] == 250
    assert {"pulls_arm_0", "pulls_arm_1"} <= set(result.columns)


def test_thompson_sampling_validates_rates() -> None:
    with pytest.raises(ValueError, match="between zero and one"):
        simulate_thompson_sampling([0.2, 1.2])
