from __future__ import annotations

import pandas as pd
import pytest

from experimentation.ab_test import difference_in_means
from experimentation.bayesian_ab_test import beta_binomial_ab_test
from experimentation.cuped import apply_cuped


def sample_frame() -> pd.DataFrame:
    return pd.DataFrame({"treatment": [0, 0, 1, 1], "outcome": [1.0, 2.0, 3.0, 4.0], "pre": [1.0, 2.0, 1.5, 2.5]})


def test_difference_in_means_returns_expected_lift() -> None:
    result = difference_in_means(sample_frame(), "outcome")
    assert result["absolute_lift"] == pytest.approx(2.0)
    assert result["n_control"] == 2
    assert result["n_treatment"] == 2


def test_difference_in_means_rejects_missing_column() -> None:
    with pytest.raises(ValueError, match="Missing required columns"):
        difference_in_means(sample_frame(), "missing")


def test_cuped_preserves_mean() -> None:
    frame = sample_frame()
    adjusted = apply_cuped(frame, "outcome", "pre")
    assert adjusted.mean() == pytest.approx(frame["outcome"].mean())


def test_cuped_rejects_constant_covariate() -> None:
    frame = sample_frame().assign(pre=1.0)
    with pytest.raises(ValueError, match="positive variance"):
        apply_cuped(frame, "outcome", "pre")


def test_bayesian_probability_bounds() -> None:
    result = beta_binomial_ab_test(60, 100, 50, 100, draws=5_000)
    assert 0 <= result["prob_treatment_better"] <= 1


def test_bayesian_rejects_invalid_counts() -> None:
    with pytest.raises(ValueError, match="Success counts"):
        beta_binomial_ab_test(101, 100, 50, 100)
