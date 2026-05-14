import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.data_generator import generate_synthetic_telemetry
from src.pipeline import run_pipeline
from src.model import train_model
from src.visualization import generate_figures


def main():
    print("Step 1: Generate synthetic train telemetry")
    generate_synthetic_telemetry(n_events=5000, output_path=ROOT / "data/raw/train_telemetry_events.csv")

    print("Step 2: Run Bronze/Silver/Gold pipeline")
    run_pipeline()

    print("Step 3: Train neural network predictive timing model")
    metrics = train_model()
    print(metrics)

    print("Step 4: Generate figures")
    generate_figures()

    print("Done.")


if __name__ == "__main__":
    main()
