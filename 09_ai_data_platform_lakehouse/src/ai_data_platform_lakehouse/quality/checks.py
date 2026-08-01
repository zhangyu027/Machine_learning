from pathlib import Path
import pandas as pd
class DataQualityError(RuntimeError): pass

def run_quality_checks(silver_path: str | Path, output_path: str | Path, fail_on_critical: bool=True) -> pd.DataFrame:
    df=pd.read_parquet(silver_path); checks=[]
    def add(name,passed,value,severity="critical"): checks.append({"check_name":name,"severity":severity,"passed":bool(passed),"value":value})
    add("row_count_positive",len(df)>0,len(df)); add("event_id_unique",df.event_id.is_unique,df.event_id.nunique())
    for c in ["county","program","site_id","event_month"]: add(f"{c}_not_null",df[c].notna().all(),int(df[c].isna().sum()))
    for c in ["risk_score","social_need_index"]: add(f"{c}_between_0_and_1",df[c].between(0,1).all(),f"{df[c].min():.3f} - {df[c].max():.3f}")
    add("service_count_non_negative",(df.service_count>=0).all(),float(df.service_count.min()))
    report=pd.DataFrame(checks); p=Path(output_path); p.parent.mkdir(parents=True,exist_ok=True); report.to_csv(p,index=False)
    failed=report[(report.severity=="critical")&(~report.passed)]
    if fail_on_critical and not failed.empty: raise DataQualityError(f"{len(failed)} critical quality checks failed: {failed.check_name.tolist()}")
    return report
