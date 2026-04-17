from pathlib import Path
import json
import pandas as pd
import torch
from torch.utils.data import Dataset

class SmilesDataset(Dataset):
    def __init__(self, csv_path: str, vocab_path: str, max_len: int = 32):
        self.df = pd.read_csv(csv_path)
        self.vocab = json.loads(Path(vocab_path).read_text())
        self.max_len = max_len
        self.samples = [self.encode(x) for x in self.df["smiles"].astype(str).tolist()]

    def encode(self, smiles: str):
        ids = [self.vocab["<START>"]]
        ids.extend([self.vocab[ch] for ch in smiles if ch in self.vocab])
        ids.append(self.vocab["<END>"])
        ids = ids[: self.max_len]
        if len(ids) < self.max_len:
            ids.extend([self.vocab["<PAD>"]] * (self.max_len - len(ids)))
        return torch.tensor(ids, dtype=torch.long)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        x = self.samples[idx]
        return x[:-1], x[1:]