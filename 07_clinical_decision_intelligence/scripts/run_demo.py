from pathlib import Path
import pandas as pd
from clinical_decision.data_contracts import ClinicalContract
from clinical_decision.features import build_features
from clinical_decision.risk_model import train_risk_model
from clinical_decision.propensity import estimate_propensity_scores, propensity_match, average_treatment_effect_on_treated
from clinical_decision.causal_forest import estimate_heterogeneous_treatment_effects
from clinical_decision.reporting import build_clinical_report
root=Path(__file__).resolve().parents[1]
p=root/"data"/"sample_clinical.csv"
if not p.exists():
    raise SystemExit("Run scripts/generate_sample_clinical_data.py first")
df=pd.read_csv(p)
ClinicalContract().validate(df)
df=build_features(df)
risk=train_risk_model(df)
ps=estimate_propensity_scores(df)
matched=propensity_match(ps, caliper=.05)
att=average_treatment_effect_on_treated(matched)
cate=estimate_heterogeneous_treatment_effects(df)
summary=cate.groupby("site_id").cate.mean().round(4).to_dict()
report=build_clinical_report(risk, att, summary)
out=root/"outputs"/"clinical_decision_report.md"
out.parent.mkdir(exist_ok=True)
out.write_text(report, encoding="utf-8")
print(report)
