from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.data_generator import generate_synthetic_public_health_events
from src.lakehouse_pipeline import run_lakehouse_pipeline
from src.quality import run_quality_checks
from src.feature_store import build_feature_store
from ml.train_forecast_model import train_forecasting_model
from src.visualization import generate_figures


def main():
    print("Step 1: Generate synthetic healthcare/public-sector events")
    generate_synthetic_public_health_events(
        n_records=10000,
        output_path=ROOT / "data/raw/public_health_events.csv",
    )

    print("Step 2: Run Bronze/Silver/Gold lakehouse pipeline")
    run_lakehouse_pipeline()

    print("Step 3: Run data quality checks")
    run_quality_checks()

    print("Step 4: Build feature store")
    build_feature_store()

    print("Step 5: Train forecasting model")
    metrics = train_forecasting_model()
    print(metrics)

    print("Step 6: Generate visual outputs")
    generate_figures()

    print("Done. Review outputs/tables and outputs/figures.")


if __name__ == "__main__":
    main()
