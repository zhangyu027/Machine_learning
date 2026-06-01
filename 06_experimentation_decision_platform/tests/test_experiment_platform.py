import pandas as pd
from experiment_platform.data_contracts import ExperimentContract
from experiment_platform.cuped import apply_cuped
from experiment_platform.ab_testing import t_test


def sample_df():
    return pd.DataFrame({
        "user_id": [1,2,3,4],
        "variant": ["control","control","treatment","treatment"],
        "pre_period_metric": [10,12,11,13],
        "post_period_metric": [20,22,25,27],
        "converted": [0,0,1,1],
        "segment": ["a","a","b","b"],
    })


def test_contract_validates():
    ExperimentContract().validate(sample_df())


def test_cuped_adds_adjusted_column():
    out = apply_cuped(sample_df(), "post_period_metric", "pre_period_metric")
    assert "post_period_metric_cuped" in out.columns


def test_ab_result_has_lift():
    res = t_test(sample_df())
    assert res["absolute_lift"] > 0
