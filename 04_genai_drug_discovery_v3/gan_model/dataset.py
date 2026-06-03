from pathlib import Path
import json
import pandas as pd
import torch
from torch.utils.data import Dataset


class SmilesDataset(Dataset):
    def __init__(self, csv_path, vocab_path, max_len=32):
        self.df = pd.read_csv(csv_path)
        self.vocab = json.loads(Path(vocab_path).read_text())
        self.max_len = max_len
        self.smiles = self.df["smiles"].astype(str).tolist()

    def encode(self, smiles):
        token_ids = [self.vocab["<START>"]]

        for ch in smiles:
            if ch in self.vocab:
                token_ids.append(self.vocab[ch])

        token_ids.append(self.vocab["<END>"])
        token_ids = token_ids[: self.max_len]

        while len(token_ids) < self.max_len:
            token_ids.append(self.vocab["<PAD>"])

        return torch.tensor(token_ids, dtype=torch.long)

    def __len__(self):
        return len(self.smiles)

    def __getitem__(self, idx):
        encoded = self.encode(self.smiles[idx])
        return encoded[:-1], encoded[1:]
