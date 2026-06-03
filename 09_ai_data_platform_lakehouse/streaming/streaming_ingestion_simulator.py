"""
Streaming ingestion simulator.

This writes small micro-batches from raw data into a landing area.
It represents how Kafka/Kinesis events could be consumed into Bronze.
"""

from pathlib import Path
import pandas as pd
import time


def simulate_micro_batches(
    raw_path="data/raw/public_health_events.csv",
    landing_dir="data/raw/micro_batches",
    batch_size=1000,
    sleep_seconds=0,
):
    df = pd.read_csv(raw_path)
    landing = Path(landing_dir)
    landing.mkdir(parents=True, exist_ok=True)

    batch_files = []
    for i, start in enumerate(range(0, len(df), batch_size)):
        batch = df.iloc[start:start + batch_size]
        out = landing / f"events_batch_{i:03d}.csv"
        batch.to_csv(out, index=False)
        batch_files.append(out)
        print(f"Wrote micro-batch: {out}")
        if sleep_seconds:
            time.sleep(sleep_seconds)

    return batch_files


if __name__ == "__main__":
    simulate_micro_batches()
