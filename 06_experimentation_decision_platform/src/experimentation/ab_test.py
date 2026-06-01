import numpy as np
import pandas as pd

def difference_in_means(df: pd.DataFrame, outcome: str, treatment_col: str = "treatment") -> dict:
    t = df.loc[df[treatment_col] == 1, outcome]
    c = df.loc[df[treatment_col] == 0, outcome]
    lift = t.mean() - c.mean()
    se = np.sqrt(t.var(ddof=1) / len(t) + c.var(ddof=1) / len(c))
    return {
        "control_mean": float(c.mean()),
        "treatment_mean": float(t.mean()),
        "absolute_lift": float(lift),
        "relative_lift_pct": float(lift / (c.mean() + 1e-9) * 100),
        "ci_95": [float(lift - 1.96 * se), float(lift + 1.96 * se)],
    }
