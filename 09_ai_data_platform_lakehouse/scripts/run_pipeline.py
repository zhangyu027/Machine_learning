from ai_data_platform_lakehouse.config.settings import settings
from ai_data_platform_lakehouse.ingestion.generator import generate_synthetic_public_health_events
from ai_data_platform_lakehouse.transformations.lakehouse import bronze_ingest,silver_clean,gold_certified_tables
from ai_data_platform_lakehouse.quality.checks import run_quality_checks
from ai_data_platform_lakehouse.features.store import build_feature_store
from ai_data_platform_lakehouse.modeling.forecast import train_forecasting_model
from ai_data_platform_lakehouse.visualization.figures import generate_figures

def main():
    o=settings.outputs_dir
    generate_synthetic_public_health_events(10000,settings.raw_path,settings.random_seed)
    bronze_ingest(settings.raw_path,settings.bronze_path)
    silver_clean(settings.bronze_path,settings.silver_path)
    gold_certified_tables(settings.silver_path,settings.gold_path,o/'tables/gold_monthly_program_demand.csv')
    run_quality_checks(settings.silver_path,o/'tables/data_quality_report.csv')
    build_feature_store(settings.gold_path,settings.feature_path,o/'tables/monthly_program_features.csv')
    metrics=train_forecasting_model(settings.feature_path,o/'models/demand_forecast_model.joblib',o/'tables/forecast_model_metrics.json',o/'tables/forecast_predictions.csv')
    generate_figures(output_dir=o/'figures')
    print({"status":"completed","metrics":metrics})
if __name__=='__main__': main()
