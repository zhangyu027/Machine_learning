import numpy as np
import pandas as pd

def apply_cuped(df: pd.DataFrame, outcome: str, pre_period_metric: str) -> pd.Series:
    theta = np.cov(df[outcome], df[pre_period_metric])[0, 1] / np.var(df[pre_period_metric])
    return df[outcome] - theta * (df[pre_period_metric] - df[pre_period_metric].mean())
