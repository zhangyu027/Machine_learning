from pathlib import Path
import pandas as pd
import pytest
from ai_data_platform_lakehouse.ingestion.generator import generate_synthetic_public_health_events
from ai_data_platform_lakehouse.transformations.lakehouse import bronze_ingest,silver_clean,gold_certified_tables
from ai_data_platform_lakehouse.quality.checks import run_quality_checks,DataQualityError
from ai_data_platform_lakehouse.features.store import build_feature_store
from ai_data_platform_lakehouse.modeling.forecast import chronological_split,train_forecasting_model

def test_generator_is_deterministic(tmp_path):
    a=generate_synthetic_public_health_events(100,tmp_path/'a.csv',7); b=generate_synthetic_public_health_events(100,tmp_path/'b.csv',7); pd.testing.assert_frame_equal(a,b)
def test_full_pipeline_and_no_feature_leakage(tmp_path):
    raw=tmp_path/'raw.csv'; bronze=tmp_path/'bronze.parquet'; silver=tmp_path/'silver.parquet'; gold=tmp_path/'gold.parquet'; feat=tmp_path/'feat.parquet'; out=tmp_path/'out'
    generate_synthetic_public_health_events(1500,raw); bronze_ingest(raw,bronze); s=silver_clean(bronze,silver); assert s.event_id.is_unique
    g=gold_certified_tables(silver,gold,out/'gold.csv'); f=build_feature_store(gold,feat,out/'feat.csv')
    first_months = g.groupby(['county','program'])['event_month'].min().reset_index()
    merged = f.merge(first_months, on=['county','program'], suffixes=('', '_first'))
    assert (merged['event_month'] > merged['event_month_first']).all()
    report=run_quality_checks(silver,out/'quality.csv'); assert report.passed.all()
    metrics=train_forecasting_model(feat,out/'model.joblib',out/'metrics.json',out/'pred.csv'); assert metrics['train_end'] < metrics['test_start']; assert 'baseline_mae' in metrics; assert 'backtest_summary' in metrics
def test_chronological_split():
    df=pd.DataFrame({'event_month':pd.date_range('2024-01-01',periods=20,freq='MS')}); tr,te=chronological_split(df); assert tr.event_month.max()<te.event_month.min()
def test_quality_failure(tmp_path):
    p=tmp_path/'bad.parquet'; pd.DataFrame({'event_id':['a','a'],'event_month':pd.to_datetime(['2024-01-01']*2),'county':['x']*2,'program':['p']*2,'site_id':['s']*2,'risk_score':[2.0,2.0],'service_count':[1,1],'prior_utilization':[1,1],'social_need_index':[.2,.2],'target_next_month_demand':[1,1]}).to_parquet(p,index=False)
    with pytest.raises(DataQualityError): run_quality_checks(p,tmp_path/'q.csv')


def test_split_keeps_entire_months():
    months=pd.date_range("2025-01-01",periods=12,freq="MS")
    df=pd.DataFrame({"event_month":list(months)*3})
    train,test=chronological_split(df)
    assert set(train.event_month).isdisjoint(set(test.event_month))
    assert len(test)%3==0


def test_missing_future_target_not_plotted_as_zero():
    import numpy as np
    gold=pd.DataFrame({"event_month":["2026-01-01","2026-02-01"],"target_next_month_demand":[10.0,np.nan]})
    monthly=gold.dropna(subset=["target_next_month_demand"]).groupby("event_month",as_index=False)["target_next_month_demand"].sum(min_count=1)
    assert len(monthly)==1
    assert monthly.iloc[0]["target_next_month_demand"]==10.0

def test_backtest_summary_consistency(tmp_path):
    raw=tmp_path/"raw.csv"; bronze=tmp_path/"bronze.parquet"; silver=tmp_path/"silver.parquet"; gold=tmp_path/"gold.parquet"; features=tmp_path/"features.parquet"
    generate_synthetic_public_health_events(100,raw)
    bronze_ingest(raw,bronze);silver_clean(bronze,silver)
    gold_certified_tables(silver,gold,tmp_path/"gold.csv")
    build_feature_store(gold,features,tmp_path/"features.csv")
    metrics=train_forecasting_model(features,tmp_path/"model.joblib",tmp_path/"metrics.json",tmp_path/"pred.csv")
    summary=metrics["backtest_summary"]
    assert summary["folds"]>0
    assert 0<=summary["model_wins"]<=summary["folds"]
    assert metrics["baseline_improvement_pct"]==pytest.approx(100*(metrics["baseline_mae"]-metrics["mae"])/metrics["baseline_mae"])
