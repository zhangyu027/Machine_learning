from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
GENERATED_PATH = ROOT / "molecule_generation" / "generated_candidates.csv"
SCREENED_PATH = ROOT / "molecule_generation" / "screened_candidates.csv"


def simple_smiles_validity(smiles):
    if not isinstance(smiles, str):
        return False

    if len(smiles.strip()) == 0:
        return False

    allowed_chars = set("CONSBrlc123456789=()[]#")
    return all(ch in allowed_chars for ch in smiles)


def simple_druglikeness_score(smiles):
    if not isinstance(smiles, str):
        return 0.0

    if len(smiles.strip()) == 0:
        return 0.0

    score = 0.0

    if "N" in smiles:
        score += 0.5

    if "O" in smiles:
        score += 0.5

    if 3 <= len(smiles) <= 20:
        score += 0.5

    if "c1" in smiles:
        score += 0.5

    return score

    return score


def screen_candidates(generated_path=GENERATED_PATH, output_path=SCREENED_PATH):
    df = pd.read_csv(generated_path)
    df["generated_smiles"] = df["generated_smiles"].fillna("").astype(str)

    df["is_valid"] = df["generated_smiles"].apply(simple_smiles_validity)
    df["length"] = df["generated_smiles"].astype(str).apply(len)
    df["druglikeness_proxy"] = df["generated_smiles"].apply(simple_druglikeness_score)

    screened = df.sort_values(
        ["is_valid", "druglikeness_proxy", "length"],
        ascending=[False, False, True],
    ).reset_index(drop=True)

    screened.to_csv(output_path, index=False)
    print(f"Saved screened candidates to: {output_path}")

    return screened


if __name__ == "__main__":
    screen_candidates()
