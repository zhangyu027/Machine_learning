from __future__ import annotations
import numpy as np

def population_stability_index(reference, current, bins=10) -> float:
    edges=np.quantile(reference, np.linspace(0,1,bins+1)); edges[0],edges[-1]=-np.inf,np.inf
    r=np.histogram(reference,bins=edges)[0]/len(reference)
    c=np.histogram(current,bins=edges)[0]/len(current)
    r=np.clip(r,1e-6,None); c=np.clip(c,1e-6,None)
    return float(np.sum((c-r)*np.log(c/r)))
