"""Run a molecular GNN benchmark for hERG, BBBP, ClinTox, and Tox21.

This module is intentionally separate from the frozen classical and multi-task
benchmarks. It uses the same endpoint datasets and scaffold-aware split logic.

Architecture
------------
- RDKit molecule -> atom/bond graph
- Two GraphConv layers (PyTorch Geometric)
- Global mean pooling
- Binary classification head

Outputs
-------
reports/gnn_benchmark.csv
reports/gnn_training_history.csv
reports/gnn_predictions.csv
models/gnn_<endpoint>.pt

Examples
--------
python experiments/run_gnn_benchmark.py --endpoint hERG

python experiments/run_gnn_benchmark.py \
    --endpoint BBBP \
    --epochs 100 \
    --hidden-dim 128 \
    --patience 15
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd

import torch
from torch import nn
from torch.utils.data import Dataset

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    brier_score_loss,
    roc_auc_score,
    average_precision_score,
)

from pharma_genai.data.scaffold_split import (
    scaffold_split_indices,
    assert_no_scaffold_overlap,
)

try:
    from rdkit import Chem
except ImportError as exc:
    raise ImportError(
        "RDKit is required for the GNN benchmark. "
        "Install with: conda install -c conda-forge rdkit"
    ) from exc

try:
    from torch_geometric.data import Data
    from torch_geometric.loader import DataLoader
    from torch_geometric.nn import GraphConv, global_mean_pool
except ImportError as exc:
    raise ImportError(
        "PyTorch Geometric is required for the GNN benchmark. "
        "Install with: python -m pip install torch-geometric"
    ) from exc


ENDPOINTS = {
    "hERG": "data/processed/herg.csv",
    "BBBP": "data/BBBP/bbbp.csv",
    "ClinTox": "data/ClinTox/clintox.csv",
    "Tox21": "data/Tox21/tox21_task0.csv",
}


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def choose_device(requested: str) -> torch.device:
    if requested != "auto":
        return torch.device(requested)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def require_file(path: str) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset not found: {p}")
    return p


def atom_features(atom: Chem.Atom) -> list[float]:
    return [
        float(atom.GetAtomicNum()),
        float(atom.GetTotalDegree()),
        float(atom.GetFormalCharge()),
        float(atom.GetTotalNumHs()),
        float(atom.GetIsAromatic()),
        float(atom.GetMass() / 100.0),
    ]


def smiles_to_graph(smiles: str, target: int) -> Data | None:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    x = torch.tensor(
        [atom_features(atom) for atom in mol.GetAtoms()],
        dtype=torch.float32,
    )

    edges = []
    for bond in mol.GetBonds():
        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()
        edges.append([i, j])
        edges.append([j, i])

    if edges:
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    else:
        edge_index = torch.empty((2, 0), dtype=torch.long)

    y = torch.tensor([float(target)], dtype=torch.float32)

    data = Data(
        x=x,
        edge_index=edge_index,
        y=y,
    )
    data.smiles = smiles
    return data


class MoleculeGraphDataset(Dataset):
    def __init__(self, df: pd.DataFrame):
        self.items = []
        skipped = 0

        for row in df.itertuples(index=False):
            graph = smiles_to_graph(str(row.smiles), int(row.target))
            if graph is None:
                skipped += 1
                continue
            self.items.append(graph)

        self.skipped_invalid = skipped

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, idx: int) -> Data:
        return self.items[idx]


class MolecularGNN(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 128, dropout: float = 0.2):
        super().__init__()
        self.conv1 = GraphConv(input_dim, hidden_dim)
        self.conv2 = GraphConv(hidden_dim, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.head = nn.Linear(hidden_dim, 1)

    def forward(self, data: Data) -> torch.Tensor:
        x, edge_index, batch = data.x, data.edge_index, data.batch

        x = torch.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = torch.relu(self.conv2(x, edge_index))
        x = global_mean_pool(x, batch)
        x = self.dropout(x)
        return self.head(x).squeeze(-1)


def load_endpoint(endpoint: str) -> tuple[pd.DataFrame, np.ndarray, np.ndarray, np.ndarray]:
    path = require_file(ENDPOINTS[endpoint])

    df = (
        pd.read_csv(path)
        .dropna(subset=["smiles", "target"])
        .reset_index(drop=True)
    )
    df["smiles"] = df["smiles"].astype(str)
    df["target"] = df["target"].astype(int)

    labels = set(df["target"].unique().tolist())
    if not labels.issubset({0, 1}):
        raise ValueError(f"{endpoint}: labels must be binary 0/1, found {sorted(labels)}")

    smiles = df["smiles"].tolist()
    tr, va, te = scaffold_split_indices(smiles)
    assert_no_scaffold_overlap(smiles, [tr, va, te])

    return df, tr, va, te


def compute_pos_weight(y: np.ndarray) -> float:
    n_pos = int((y == 1).sum())
    n_neg = int((y == 0).sum())

    if n_pos == 0:
        return 1.0

    return float(np.clip(n_neg / n_pos, 0.05, 50.0))


def run_epoch(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    loss_fn: nn.Module,
    optimizer: torch.optim.Optimizer | None = None,
) -> float:
    training = optimizer is not None
    model.train(training)

    total_loss = 0.0
    n_batches = 0

    for batch in loader:
        batch = batch.to(device)

        if training:
            optimizer.zero_grad()

        logits = model(batch)
        y = batch.y.view(-1)
        loss = loss_fn(logits, y)

        if training:
            loss.backward()
            optimizer.step()

        total_loss += float(loss.detach().cpu())
        n_batches += 1

    return total_loss / max(n_batches, 1)


@torch.no_grad()
def predict(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    model.eval()

    y_true = []
    y_prob = []
    smiles_all = []

    for batch in loader:
        batch = batch.to(device)
        logits = model(batch)
        probs = torch.sigmoid(logits)

        y_true.extend(batch.y.view(-1).cpu().numpy().tolist())
        y_prob.extend(probs.cpu().numpy().tolist())

        if hasattr(batch, "smiles"):
            smiles_all.extend(list(batch.smiles))
        else:
            smiles_all.extend([""] * len(probs))

    return (
        np.asarray(y_true, dtype=int),
        np.asarray(y_prob, dtype=float),
        smiles_all,
    )


def classification_metrics(y_true: np.ndarray, y_prob: np.ndarray) -> dict[str, float]:
    pred = (y_prob >= 0.5).astype(int)

    out = {
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, pred)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
        "brier_score": float(brier_score_loss(y_true, y_prob)),
    }

    if len(np.unique(y_true)) < 2:
        out["roc_auc"] = np.nan
        out["average_precision"] = np.nan
    else:
        out["roc_auc"] = float(roc_auc_score(y_true, y_prob))
        out["average_precision"] = float(
            average_precision_score(y_true, y_prob)
        )

    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", choices=ENDPOINTS.keys(), required=True)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--dropout", type=float, default=0.20)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-5)
    parser.add_argument("--patience", type=int, default=15)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="auto")
    args = parser.parse_args()

    set_seed(args.seed)
    device = choose_device(args.device)

    endpoint = args.endpoint
    print(f"Endpoint: {endpoint}")
    print(f"Device: {device}")

    df, tr, va, te = load_endpoint(endpoint)

    train_df = df.iloc[tr][["smiles", "target"]].copy()
    val_df = df.iloc[va][["smiles", "target"]].copy()
    test_df = df.iloc[te][["smiles", "target"]].copy()

    train_ds = MoleculeGraphDataset(train_df)
    val_ds = MoleculeGraphDataset(val_df)
    test_ds = MoleculeGraphDataset(test_df)

    if not train_ds.items:
        raise RuntimeError("No valid training molecules after RDKit graph conversion.")

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False)

    input_dim = train_ds.items[0].x.shape[1]

    model = MolecularGNN(
        input_dim=input_dim,
        hidden_dim=args.hidden_dim,
        dropout=args.dropout,
    ).to(device)

    train_y = train_df["target"].to_numpy()
    pos_weight_value = compute_pos_weight(train_y)
    pos_weight = torch.tensor([pos_weight_value], dtype=torch.float32, device=device)

    print(f"Train positive rate: {train_y.mean():.4f}")
    print(f"Positive-class weight: {pos_weight_value:.4f}")

    loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.learning_rate,
        weight_decay=args.weight_decay,
    )

    best_val_loss = float("inf")
    best_state = None
    patience_left = args.patience
    history = []

    for epoch in range(1, args.epochs + 1):
        train_loss = run_epoch(
            model,
            train_loader,
            device,
            loss_fn,
            optimizer=optimizer,
        )
        val_loss = run_epoch(
            model,
            val_loader,
            device,
            loss_fn,
            optimizer=None,
        )

        history.append({
            "endpoint": endpoint,
            "epoch": epoch,
            "train_loss": train_loss,
            "validation_loss": val_loss,
        })

        print(
            f"Epoch {epoch:03d} "
            f"train_loss={train_loss:.5f} "
            f"val_loss={val_loss:.5f}"
        )

        if val_loss < best_val_loss - 1e-6:
            best_val_loss = val_loss
            best_state = {
                k: v.detach().cpu().clone()
                for k, v in model.state_dict().items()
            }
            patience_left = args.patience
        else:
            patience_left -= 1

        if patience_left <= 0:
            print(f"Early stopping at epoch {epoch}.")
            break

    if best_state is None:
        raise RuntimeError("No valid model state captured.")

    model.load_state_dict(best_state)
    model.to(device)

    y_true, y_prob, smiles = predict(model, test_loader, device)
    metrics = classification_metrics(y_true, y_prob)

    result = {
        "endpoint": endpoint,
        "model": "graphconv_gnn",
        "representation": "molecular_graph",
        "n_train": len(train_ds),
        "n_validation": len(val_ds),
        "n_test": len(test_ds),
        "n_positive": int((y_true == 1).sum()),
        "n_negative": int((y_true == 0).sum()),
        "positive_rate": float((y_true == 1).mean()),
        **metrics,
    }

    reports = Path("reports")
    models_dir = Path("models")
    reports.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    benchmark_path = reports / "gnn_benchmark.csv"
    history_path = reports / "gnn_training_history.csv"
    predictions_path = reports / "gnn_predictions.csv"
    model_path = models_dir / f"gnn_{endpoint.lower()}.pt"

    # Append endpoint result without duplicating an existing endpoint/model row.
    if benchmark_path.exists():
        bench_df = pd.read_csv(benchmark_path)
        bench_df = bench_df[
            ~(
                (bench_df["endpoint"] == endpoint)
                & (bench_df["model"] == result["model"])
            )
        ]
        bench_df = pd.concat([bench_df, pd.DataFrame([result])], ignore_index=True)
    else:
        bench_df = pd.DataFrame([result])

    bench_df.to_csv(benchmark_path, index=False)

    hist_df = pd.DataFrame(history)
    if history_path.exists():
        old_hist = pd.read_csv(history_path)
        old_hist = old_hist[old_hist["endpoint"] != endpoint]
        hist_df = pd.concat([old_hist, hist_df], ignore_index=True)
    hist_df.to_csv(history_path, index=False)

    pred_df = pd.DataFrame({
        "endpoint": endpoint,
        "smiles": smiles,
        "y_true": y_true,
        "y_prob": y_prob,
        "predicted_label": (y_prob >= 0.5).astype(int),
    })
    if predictions_path.exists():
        old_pred = pd.read_csv(predictions_path)
        old_pred = old_pred[old_pred["endpoint"] != endpoint]
        pred_df = pd.concat([old_pred, pred_df], ignore_index=True)
    pred_df.to_csv(predictions_path, index=False)

    torch.save({
        "state_dict": best_state,
        "endpoint": endpoint,
        "input_dim": input_dim,
        "hidden_dim": args.hidden_dim,
        "dropout": args.dropout,
        "seed": args.seed,
        "best_validation_loss": best_val_loss,
        "pos_weight": pos_weight_value,
    }, model_path)

    print("\n=== GNN test metrics ===")
    print(json.dumps(result, indent=2))

    print("\nSaved:")
    print(f"  {benchmark_path}")
    print(f"  {history_path}")
    print(f"  {predictions_path}")
    print(f"  {model_path}")


if __name__ == "__main__":
    main()
