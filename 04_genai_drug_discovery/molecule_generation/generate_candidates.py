from pathlib import Path
import json
import random
import pandas as pd
import torch

from gan_model.model import GeneratorModel

ROOT = Path(__file__).resolve().parents[1]
VOCAB_PATH = ROOT / "data" / "vocab.json"
MODEL_PATH = ROOT / "gan_model" / "generator.pt"
OUT_PATH = ROOT / "molecule_generation" / "generated_candidates.csv"

def decode(ids, inv_vocab):
    chars = []
    for idx in ids:
        tok = inv_vocab.get(int(idx), "")
        if tok in ["<PAD>", "<START>"]:
            continue
        if tok == "<END>":
            break
        chars.append(tok)
    return "".join(chars)

def simple_validity(smiles: str) -> bool:
    allowed = set("CONSBrlc123456789=()[]#")
    return bool(smiles) and all(ch in allowed for ch in smiles)

def main() -> None:
    vocab = json.loads(VOCAB_PATH.read_text())
    inv_vocab = {v: k for k, v in vocab.items()}
    model = GeneratorModel(vocab_size=len(vocab))
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()

    start_id = vocab["<START>"]
    rows = []
    for _ in range(50):
        seq = [start_id]
        x = torch.tensor([seq], dtype=torch.long)
        for _ in range(20):
            with torch.no_grad():
                logits = model(x)
                probs = torch.softmax(logits[0, -1], dim=-1).numpy()
            next_id = random.choices(range(len(probs)), weights=probs, k=1)[0]
            seq.append(next_id)
            x = torch.tensor([seq], dtype=torch.long)
            if inv_vocab.get(next_id) == "<END>":
                break
        smiles = decode(seq, inv_vocab)
        rows.append({
            "smiles": smiles,
            "is_valid": simple_validity(smiles),
            "length": len(smiles),
        })

    df = pd.DataFrame(rows).drop_duplicates()
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved candidates to {OUT_PATH}")

if __name__ == "__main__":
    main()