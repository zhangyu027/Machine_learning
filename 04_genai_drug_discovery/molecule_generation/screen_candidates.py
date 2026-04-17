from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "evaluation" / "evaluation_report.csv"
OUT_PATH = ROOT / "molecule_generation" / "top_candidates.csv"

def main() -> None:
    df = pd.read_csv(EVAL_PATH)
    screened = df[
        (df["is_valid"] == True) &
        (df["novelty"] == 1) &
        (df["druglikeness_proxy"] >= 1.0)
    ].copy()
    screened.head(20).to_csv(OUT_PATH, index=False)
    print(f"Saved screened candidates to {OUT_PATH}")

if __name__ == "__main__":
    main()