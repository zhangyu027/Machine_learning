from pathlib import Path
import pandas as pd


def load_child_enrollment(path: str | Path) -> pd.DataFrame:
    """Load de-identified child enrollment sample data."""
    return pd.read_csv(path)


def load_child_family(path: str | Path) -> pd.DataFrame:
    """Load de-identified child family sample data."""
    return pd.read_csv(path)
