from pathlib import Path
import json
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "demo_smiles.csv"
VOCAB_PATH = ROOT / "data" / "vocab.json"


def build_vocab(data_path=DATA_PATH, vocab_path=VOCAB_PATH):
    df = pd.read_csv(data_path)
    all_smiles = df["smiles"].astype(str).tolist()
    unique_chars = sorted(set("".join(all_smiles)))

    vocab = {
        "<PAD>": 0,
        "<START>": 1,
        "<END>": 2,
    }

    for char in unique_chars:
        vocab[char] = len(vocab)

    vocab_path.write_text(json.dumps(vocab, indent=2))
    print(f"Vocabulary size: {len(vocab)}")
    print(f"Saved vocabulary to: {vocab_path}")

    return vocab


if __name__ == "__main__":
    build_vocab()
