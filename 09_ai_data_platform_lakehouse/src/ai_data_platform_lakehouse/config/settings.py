from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    project_root: Path = Path(__file__).resolve().parents[3]
    random_seed: int = 42

    @property
    def raw_path(self) -> Path: return self.project_root / "data/raw/public_health_events.csv"
    @property
    def bronze_path(self) -> Path: return self.project_root / "data/bronze/events_bronze.parquet"
    @property
    def silver_path(self) -> Path: return self.project_root / "data/silver/events_silver.parquet"
    @property
    def gold_path(self) -> Path: return self.project_root / "data/gold/gold_monthly_program_demand.parquet"
    @property
    def feature_path(self) -> Path: return self.project_root / "data/feature_store/monthly_program_features.parquet"
    @property
    def outputs_dir(self) -> Path: return self.project_root / "outputs"

settings = Settings()
