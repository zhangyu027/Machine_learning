from pathlib import Path
import json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from gan_model.dataset import SmilesDataset
from gan_model.model import GeneratorModel

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "demo_smiles.csv"
VOCAB_PATH = ROOT / "data" / "vocab.json"
MODEL_PATH = ROOT / "gan_model" / "generator.pt"

def main() -> None:
    vocab = json.loads(VOCAB_PATH.read_text())
    ds = SmilesDataset(str(DATA_PATH), str(VOCAB_PATH), max_len=32)
    dl = DataLoader(ds, batch_size=8, shuffle=True)

    model = GeneratorModel(vocab_size=len(vocab))
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(20):
        total_loss = 0.0
        for x, y in dl:
            logits = model(x)
            loss = criterion(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"epoch={epoch+1} loss={total_loss:.4f}")

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")

if __name__ == "__main__":
    main()