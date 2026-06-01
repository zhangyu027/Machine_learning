from pathlib import Path
import numpy as np
import pandas as pd
rng = np.random.default_rng(7)
n=4000
age = rng.integers(25, 90, n)
sex = rng.choice(["Female","Male"], size=n)
comorbidity = rng.poisson(2.2, n)
baseline = rng.beta(2,5,n)
prior = rng.poisson(1.5,n)
lab = rng.normal(0,1,n)
site = rng.choice(["S1","S2","S3","S4"], size=n)
# confounded treatment assignment
ps = 1/(1+np.exp(-(-1.0 + .02*age + .35*comorbidity + .6*baseline + .2*(site=="S1"))))
treatment = rng.binomial(1, ps)
# treatment has greater benefit for high baseline risk
true_effect = -0.10 - 0.15*(baseline > .45) + 0.05*(comorbidity > 4)
readmit_prob = 1/(1+np.exp(-(-2.0 + .025*age + .28*comorbidity + 1.4*baseline + .2*prior + true_effect*treatment)))
readmission = rng.binomial(1, readmit_prob)
los = np.maximum(1, rng.normal(3 + .4*comorbidity + 2*readmission - .5*treatment, 1.2, n))
df=pd.DataFrame({"patient_id": range(n), "age":age, "sex":sex, "comorbidity_score":comorbidity, "baseline_risk_score":baseline, "prior_visits":prior, "lab_abnormality_score":lab, "site_id":site, "treatment":treatment, "readmission_30d":readmission, "length_of_stay":los})
out=Path(__file__).resolve().parents[1]/"data"/"sample_clinical.csv"
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out,index=False)
print(out)
