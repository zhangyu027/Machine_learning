import pandas as pd
from .bayesian_ab_test import beta_binomial_ab_test

def sequential_conversion_monitor(df: pd.DataFrame, day_col="event_day", treatment_col="treatment", outcome_col="converted"):
    rows = []
    for day in sorted(df[day_col].unique()):
        tmp = df[df[day_col] <= day]
        st = int(tmp.loc[tmp[treatment_col] == 1, outcome_col].sum())
        nt = int((tmp[treatment_col] == 1).sum())
        sc = int(tmp.loc[tmp[treatment_col] == 0, outcome_col].sum())
        nc = int((tmp[treatment_col] == 0).sum())
        if nt > 0 and nc > 0:
            out = beta_binomial_ab_test(st, nt, sc, nc, draws=20000, seed=int(day))
            rows.append({"day": int(day), "n_treatment": nt, "n_control": nc, **out})
    return pd.DataFrame(rows)
