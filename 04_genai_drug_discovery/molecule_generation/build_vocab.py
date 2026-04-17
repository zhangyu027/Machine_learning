from pathlib import Path
import json
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "demo_smiles.csv"
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "vocab.json"

def main() -> None:
    df = pd.read_csv(DATA_PATH)
    chars = sorted(set("".join(df["smiles"].astype(str).tolist())))
    vocab = {"<PAD>": 0, "<START>": 1, "<END>": 2}
    for i, ch in enumerate(chars, start=3):
        vocab[ch] = i
    OUT_PATH.write_text(json.dumps(vocab, indent=2))
    print(f"Saved vocab to {OUT_PATH}")

if __name__ == "__main__":
    main()