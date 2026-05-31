from pathlib import Path
import sys
import json
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from gan_model.model import GeneratorModel


VOCAB_PATH = ROOT / "data" / "vocab.json"
MODEL_PATH = ROOT / "gan_model" / "generator.pt"
GENERATED_PATH = ROOT / "molecule_generation" / "generated_candidates.csv"


def decode_token_ids(token_ids, idx_to_token):
    tokens = []

    for idx in token_ids:
        token = idx_to_token.get(int(idx), "")

        if token in ["<PAD>", "<START>"]:
            continue

        if token == "<END>":
            break

        tokens.append(token)

    return "".join(tokens)


def generate_molecules(
    model_path=MODEL_PATH,
    vocab_path=VOCAB_PATH,
    output_path=GENERATED_PATH,
    n_molecules=100,
    max_new_tokens=25,
):
    vocab = json.loads(Path(vocab_path).read_text())
    idx_to_token = {idx: token for token, idx in vocab.items()}

    model = GeneratorModel(vocab_size=len(vocab))
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    generated = []

    for _ in range(n_molecules):
        sequence = [vocab["<START>"]]

        for _ in range(max_new_tokens):
            x = torch.tensor([sequence], dtype=torch.long)

            with torch.no_grad():
                logits = model(x)

            probabilities = torch.softmax(logits[0, -1], dim=0)
            next_token_id = torch.multinomial(probabilities, num_samples=1).item()

            sequence.append(next_token_id)

            if idx_to_token.get(next_token_id) == "<END>":
                break

        generated.append(decode_token_ids(sequence, idx_to_token))

    generated_df = pd.DataFrame({"generated_smiles": generated})
    generated_df = generated_df.drop_duplicates().reset_index(drop=True)
    generated_df.to_csv(output_path, index=False)

    print(f"Saved generated molecules to: {output_path}")
    return generated_df


if __name__ == "__main__":
    generate_molecules()
