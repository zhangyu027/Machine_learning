from pathlib import Path
import sys
import json

import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from gan_model.dataset import SmilesDataset
from gan_model.model import GeneratorModel


DATA_PATH = ROOT / "data" / "demo_smiles.csv"
VOCAB_PATH = ROOT / "data" / "vocab.json"
MODEL_PATH = ROOT / "gan_model" / "generator.pt"
LOSS_PATH = ROOT / "evaluation" / "training_loss.csv"


def train_generator_model(
    data_path=DATA_PATH,
    vocab_path=VOCAB_PATH,
    model_path=MODEL_PATH,
    loss_path=LOSS_PATH,
    max_len=32,
    batch_size=8,
    epochs=20,
    learning_rate=0.001,
):
    vocab = json.loads(Path(vocab_path).read_text())

    dataset = SmilesDataset(data_path, vocab_path, max_len=max_len)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = GeneratorModel(vocab_size=len(vocab))
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()

    losses = []

    model.train()

    for epoch in range(epochs):
        epoch_loss = 0.0

        for x_batch, y_batch in dataloader:
            logits = model(x_batch)

            loss = criterion(
                logits.reshape(-1, logits.shape[-1]),
                y_batch.reshape(-1),
            )

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        losses.append(epoch_loss)

        print(f"Epoch {epoch + 1:02d}/{epochs}, Loss: {epoch_loss:.4f}")

    # Save trained model
    torch.save(model.state_dict(), model_path)
    print(f"Saved trained generator model to: {model_path}")

    # Save training loss history for visualization
    loss_path.parent.mkdir(parents=True, exist_ok=True)

    loss_df = pd.DataFrame({
        "epoch": list(range(1, len(losses) + 1)),
        "loss": losses
    })

    loss_df.to_csv(loss_path, index=False)
    print(f"Saved training loss history to: {loss_path}")

    return model, losses


if __name__ == "__main__":
    train_generator_model()
