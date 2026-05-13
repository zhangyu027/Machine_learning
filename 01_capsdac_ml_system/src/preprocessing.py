"""
CAPSDAC preprocessing utilities.

These functions provide a reusable preprocessing layer for the CAPSDAC enrollment
forecasting and contribution analysis workflow.
"""

from pathlib import Path
import pandas as pd


def load_child_snapshot(path):
    """
    Load a CAPSDAC child monthly snapshot CSV.
    """
    return pd.read_csv(path)


def standardize_column_names(df):
    """
    Standardize column names for easier downstream modeling.
    """
    out = df.copy()
    out.columns = (
        out.columns
        .str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("/", "_", regex=False)
    )
    return out


def save_schema(df, output_path):
    """
    Save a column schema table.
    """
    schema = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "non_null_count": [df[c].notna().sum() for c in df.columns],
        "missing_count": [df[c].isna().sum() for c in df.columns],
    })
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    schema.to_csv(output_path, index=False)
    return schema


def detect_date_columns(df):
    """
    Return likely date/month columns.
    """
    keywords = ["date", "month", "report", "snapshot", "period"]
    return [c for c in df.columns if any(k in c.lower() for k in keywords)]
