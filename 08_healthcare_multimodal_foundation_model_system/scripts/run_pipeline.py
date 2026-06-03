from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.data_generator import generate_synthetic_healthcare_data
from src.preprocessing import prepare_features
from src.train_eval import train_multimodal_model
from src.fairness_uncertainty import subgroup_metrics, uncertainty_table
from src.visualization import generate_figures

def main():
    print("Step 1: Generate synthetic multimodal healthcare data")
    generate_synthetic_healthcare_data(n_patients=2500)

    print("Step 2: Prepare multimodal features")
    prepare_features()

    print("Step 3: Train multimodal risk model")
    metrics = train_multimodal_model()
    print(metrics)

    print("Step 4: Fairness and uncertainty outputs")
    subgroup_metrics()
    uncertainty_table()

    print("Step 5: Generate figures")
    generate_figures()

    print("Done. Review outputs/tables and outputs/figures.")


if __name__ == "__main__":
    main()
