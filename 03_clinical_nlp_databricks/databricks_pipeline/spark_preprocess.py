"""Databricks-style preprocessing for clinical NLP notes.

Runs locally with pandas fallback. If PySpark is available, the script uses Spark-style
DataFrame transformations to mirror a Databricks Bronze-to-Silver preprocessing step.
"""
from pathlib import Path
import os
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "sample" / "clinical_notes_raw.csv"
OUT_DIR = ROOT / "outputs"
PROCESSED = OUT_DIR / "clinical_notes_processed.csv"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def run_pandas() -> None:
    df = pd.read_csv(RAW)
    df["clean_text"] = df["note_text"].map(clean_text)
    df["note_length"] = df["clean_text"].str.split().map(len)
    df["source_layer"] = "silver"
    df.to_csv(PROCESSED, index=False)
    print(f"Processed clinical notes: {PROCESSED}")

def run_spark() -> bool:
    try:
        from pyspark.sql import SparkSession, functions as F
    except Exception:
        return False
    spark = SparkSession.builder.master("local[*]").appName("clinical-nlp-preprocess").getOrCreate()
    df = spark.read.option("header", True).csv(str(RAW))
    df = (
        df.withColumn("clean_text", F.lower(F.col("note_text")))
          .withColumn("clean_text", F.regexp_replace(F.col("clean_text"), r"[^a-z0-9\\s]", " "))
          .withColumn("clean_text", F.regexp_replace(F.col("clean_text"), r"\\s+", " "))
          .withColumn("note_length", F.size(F.split(F.col("clean_text"), " ")))
          .withColumn("source_layer", F.lit("silver"))
    )
    # Write through pandas for a single local CSV artifact that is easy to inspect in GitHub demos.
    df.toPandas().to_csv(PROCESSED, index=False)
    spark.stop()
    print(f"Processed clinical notes with Spark-compatible logic: {PROCESSED}")
    return True

if __name__ == "__main__":
    if not RAW.exists():
        raise FileNotFoundError(f"Raw dataset not found. Run: python notebooks/demo_dataset_builder.py")
    if os.getenv("USE_PYSPARK") == "1":
        if not run_spark():
            run_pandas()
    else:
        run_pandas()
