from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "data" / "demo_smiles.csv"
CANDIDATE_PATH = ROOT / "molecule_generation" / "generated_candidates.csv"
OUT_PATH = ROOT / "evaluation" / "evaluation_report.csv"

def novelty_score(smiles: str, training_set: set[str]) -> int:
    return 0 if smiles in training_set else 1

def diversity_proxy(smiles: str) -> int:
    return len(set(smiles))

def simple_druglikeness_proxy(smiles: str) -> float:
    score = 0.0
    if "N" in smiles:
        score += 0.5
    if "O" in smiles:
        score += 0.5
    if len(smiles) <= 20:
        score += 0.5
    if "c1ccccc1" in smiles:
        score += 0.5
    return score

def main() -> None:
    train_df = pd.read_csv(TRAIN_PATH)
    cand_df = pd.read_csv(CANDIDATE_PATH)

    training_set = set(train_df["smiles"].astype(str).tolist())
    cand_df["novelty"] = cand_df["smiles"].astype(str).apply(lambda s: novelty_score(s, training_set))
    cand_df["diversity_proxy"] = cand_df["smiles"].astype(str).apply(diversity_proxy)
    cand_df["druglikeness_proxy"] = cand_df["smiles"].astype(str).apply(simple_druglikeness_proxy)

    ranked = cand_df.sort_values(
        ["is_valid", "novelty", "druglikeness_proxy", "diversity_proxy"],
        ascending=[False, False, False, False],
    )
    ranked.to_csv(OUT_PATH, index=False)
    print(f"Saved evaluation report to {OUT_PATH}")
    print(ranked.head(10).to_string(index=False))

if __name__ == "__main__":
    main()