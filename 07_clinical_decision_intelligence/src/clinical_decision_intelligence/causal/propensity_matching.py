import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

def estimate_propensity_scores(df: pd.DataFrame, treatment_col: str, covariates: list[str]):
    X = pd.get_dummies(df[covariates], drop_first=True)
    model = LogisticRegression(max_iter=1000)
    model.fit(X, df[treatment_col])
    return model, pd.Series(model.predict_proba(X)[:, 1], index=df.index), list(X.columns)

def nearest_neighbor_att(df: pd.DataFrame, outcome_col: str, treatment_col: str, propensity_scores: pd.Series):
    treated_idx = df.index[df[treatment_col] == 1].to_numpy()
    control_idx = df.index[df[treatment_col] == 0].to_numpy()
    nn = NearestNeighbors(n_neighbors=1).fit(propensity_scores.loc[control_idx].to_numpy().reshape(-1, 1))
    _, matched_pos = nn.kneighbors(propensity_scores.loc[treated_idx].to_numpy().reshape(-1, 1))
    matched_control_idx = control_idx[matched_pos.flatten()]
    att = df.loc[treated_idx, outcome_col].mean() - df.loc[matched_control_idx, outcome_col].mean()
    return {"att": float(att), "matched_pairs": int(len(treated_idx))}
