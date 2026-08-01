from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

def _safe_auc(y, p):
    return float(roc_auc_score(y, p)) if len(np.unique(y)) > 1 else None

def subgroup_fairness_report(frame: pd.DataFrame, target: str, score: str, group: str, threshold: float=.5) -> dict:
    rows=[]
    for value, part in frame.groupby(group, dropna=False):
        pred=(part[score] >= threshold).astype(int)
        y=part[target].astype(int)
        positive=y==1; negative=y==0
        tpr=float(((pred==1)&positive).sum()/max(positive.sum(),1))
        fpr=float(((pred==1)&negative).sum()/max(negative.sum(),1))
        rows.append({"group":str(value),"n":int(len(part)),"event_rate":float(y.mean()),
                     "selection_rate":float(pred.mean()),"tpr":tpr,"fpr":fpr,"auc":_safe_auc(y,part[score])})
    result={"group_column":group,"threshold":threshold,"subgroups":rows}
    if rows:
        result["equal_opportunity_gap"]=float(max(r['tpr'] for r in rows)-min(r['tpr'] for r in rows))
        result["demographic_parity_gap"]=float(max(r['selection_rate'] for r in rows)-min(r['selection_rate'] for r in rows))
    return result
