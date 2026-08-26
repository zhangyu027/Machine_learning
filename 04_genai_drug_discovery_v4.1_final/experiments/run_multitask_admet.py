"""Train a multi-task ADMET classifier on hERG, BBBP, ClinTox, and Tox21.

Design goals
------------
- Keep the frozen classical benchmark untouched.
- Reuse the same scaffold-aware split logic per endpoint.
- Merge molecules across endpoints by canonical input SMILES string.
- Use a shared Morgan-fingerprint backbone with four endpoint-specific heads.
- Support missing labels through a masked binary-cross-entropy loss.
- Use endpoint-specific positive-class weighting estimated from TRAIN data only.
- Report per-endpoint test metrics using the same core metrics as the classical benchmark.

Outputs
-------
reports/multitask_admet_metrics.csv
reports/multitask_admet_predictions.csv
reports/multitask_admet_training_history.csv
models/multitask_admet.pt

Example
-------
python experiments/run_multitask_admet.py

Optional:
python experiments/run_multitask_admet.py \
    --epochs 100 \
    --batch-size 128 \
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
from torch.utils.data import DataLoader, Dataset

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
from pharma_genai.models.classical_baselines import fingerprint_matrix


TASKS = ["hERG", "BBBP", "ClinTox", "Tox21"]

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
    if torch.backends.mps.is_available():
        torch.mps.manual_seed(seed)


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
        raise FileNotFoundError(
            f"Required dataset not found: {p}\n"
            "Complete the endpoint data preparation before running multi-task ADMET."
        )
    return p


def load_endpoint_splits() -> tuple[dict[str, dict[str, pd.DataFrame]], pd.DataFrame]:
    """Load each endpoint, remove conflicting duplicate labels, then scaffold split.

    Identical SMILES with the same label are deduplicated.
    Identical SMILES with conflicting 0/1 labels are excluded entirely and recorded
    in reports/multitask_conflicting_labels.csv.
    """
    result: dict[str, dict[str, pd.DataFrame]] = {}
    conflict_rows = []

    for task, path in ENDPOINTS.items():
        raw = (
            pd.read_csv(require_file(path))
            .dropna(subset=["smiles", "target"])
            .reset_index(drop=True)
        )
        raw["smiles"] = raw["smiles"].astype(str)
        raw["target"] = raw["target"].astype(int)

        labels = set(raw["target"].unique().tolist())
        if not labels.issubset({0, 1}):
            raise ValueError(f"{task}: expected binary 0/1 labels, found {sorted(labels)}")

        # Audit duplicate SMILES before splitting.
        grouped = (
            raw.groupby("smiles")["target"]
            .agg(["count", "nunique", "min", "max"])
            .reset_index()
        )

        conflicting_smiles = grouped.loc[grouped["nunique"] > 1, "smiles"].tolist()

        for smi in conflicting_smiles:
            vals = raw.loc[raw["smiles"] == smi, "target"].tolist()
            conflict_rows.append({
                "endpoint": task,
                "smiles": smi,
                "n_rows": len(vals),
                "labels": "|".join(map(str, sorted(vals))),
                "action": "excluded_conflicting_duplicate",
            })

        # Remove conflicting duplicates completely.
        clean = raw[~raw["smiles"].isin(conflicting_smiles)].copy()

        # Collapse repeated identical SMILES when the label agrees.
        clean = clean.drop_duplicates(subset=["smiles", "target"]).reset_index(drop=True)

        print(
            f"{task}: raw={len(raw)}, "
            f"conflicting_smiles_removed={len(conflicting_smiles)}, "
            f"clean_unique={len(clean)}"
        )

        smiles = clean["smiles"].tolist()
        tr, va, te = scaffold_split_indices(smiles)
        assert_no_scaffold_overlap(smiles, [tr, va, te])

        result[task] = {
            "train": clean.iloc[tr][["smiles", "target"]].copy(),
            "validation": clean.iloc[va][["smiles", "target"]].copy(),
            "test": clean.iloc[te][["smiles", "target"]].copy(),
        }

    return result, pd.DataFrame(conflict_rows)


def merge_split(
    endpoint_splits: dict[str, dict[str, pd.DataFrame]],
    split_name: str,
) -> pd.DataFrame:
    """Create one molecule table with sparse task labels for a given split."""
    rows: dict[str, dict[str, float | str]] = {}

    for task in TASKS:
        df = endpoint_splits[task][split_name]
        for row in df.itertuples(index=False):
            smi = str(row.smiles)
            if smi not in rows:
                rows[smi] = {"smiles": smi, **{t: np.nan for t in TASKS}}

            current = rows[smi][task]
            if not pd.isna(current) and int(current) != int(row.target):
                raise ValueError(
                    f"Conflicting duplicate labels for {task} and SMILES {smi}"
                )
            rows[smi][task] = int(row.target)

    merged = pd.DataFrame(rows.values()).reset_index(drop=True)
    return merged


class MultiTaskDataset(Dataset):
    def __init__(self, df: pd.DataFrame):
        self.smiles = df["smiles"].astype(str).tolist()
        self.X = fingerprint_matrix(self.smiles).astype(np.float32)

        y = df[TASKS].to_numpy(dtype=np.float32)
        self.mask = (~np.isnan(y)).astype(np.float32)
        self.y = np.nan_to_num(y, nan=0.0).astype(np.float32)

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, idx: int):
        return (
            torch.from_numpy(self.X[idx]),
            torch.from_numpy(self.y[idx]),
            torch.from_numpy(self.mask[idx]),
        )


class MultiTaskADMET(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 128, dropout: float = 0.20):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        self.head = nn.Linear(hidden_dim // 2, len(TASKS))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.backbone(x))


def compute_pos_weights(train_df: pd.DataFrame) -> torch.Tensor:
    """Compute neg/pos ratio per task using TRAIN labels only."""
    weights = []
    for task in TASKS:
        labels = train_df[task].dropna().astype(int)
        n_pos = int((labels == 1).sum())
        n_neg = int((labels == 0).sum())

        if n_pos == 0:
            weight = 1.0
        else:
            weight = n_neg / n_pos

        # Avoid pathological numerical extremes while retaining imbalance correction.
        weights.append(float(np.clip(weight, 0.05, 50.0)))

    return torch.tensor(weights, dtype=torch.float32)


def masked_bce_loss(
    logits: torch.Tensor,
    y: torch.Tensor,
    mask: torch.Tensor,
    pos_weight: torch.Tensor,
) -> torch.Tensor:
    loss_fn = nn.BCEWithLogitsLoss(
        reduction="none",
        pos_weight=pos_weight,
    )
    raw = loss_fn(logits, y)
    masked = raw * mask
    denom = mask.sum().clamp_min(1.0)
    return masked.sum() / denom


def run_epoch(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    pos_weight: torch.Tensor,
    optimizer: torch.optim.Optimizer | None = None,
) -> float:
    training = optimizer is not None
    model.train(training)

    total_loss = 0.0
    total_batches = 0

    for X, y, mask in loader:
        X = X.to(device)
        y = y.to(device)
        mask = mask.to(device)

        if training:
            optimizer.zero_grad()

        logits = model(X)
        loss = masked_bce_loss(logits, y, mask, pos_weight)

        if training:
            loss.backward()
            optimizer.step()

        total_loss += float(loss.detach().cpu())
        total_batches += 1

    return total_loss / max(total_batches, 1)


@torch.no_grad()
def predict(
    model: nn.Module,
    dataset: MultiTaskDataset,
    df: pd.DataFrame,
    device: torch.device,
    batch_size: int,
) -> pd.DataFrame:
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    model.eval()

    probs = []
    for X, _, _ in loader:
        logits = model(X.to(device))
        probs.append(torch.sigmoid(logits).cpu().numpy())

    p = np.vstack(probs)
    out = df[["smiles", *TASKS]].copy()

    for i, task in enumerate(TASKS):
        out[f"{task}_prob"] = p[:, i]

    return out


def safe_metrics(y_true: np.ndarray, y_prob: np.ndarray) -> dict[str, float]:
    pred = (y_prob >= 0.5).astype(int)

    metrics = {
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, pred)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
        "brier_score": float(brier_score_loss(y_true, y_prob)),
    }

    if len(np.unique(y_true)) < 2:
        metrics["roc_auc"] = np.nan
        metrics["average_precision"] = np.nan
    else:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
        metrics["average_precision"] = float(
            average_precision_score(y_true, y_prob)
        )

    return metrics


def evaluate_test_predictions(pred_df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for task in TASKS:
        subset = pred_df.dropna(subset=[task]).copy()
        y_true = subset[task].astype(int).to_numpy()
        y_prob = subset[f"{task}_prob"].astype(float).to_numpy()

        stats = safe_metrics(y_true, y_prob)

        rows.append({
            "endpoint": task,
            "model": "multitask_morgan_mlp",
            "representation": "morgan_256",
            "n_test": int(len(subset)),
            "n_positive": int((y_true == 1).sum()),
            "n_negative": int((y_true == 0).sum()),
            "positive_rate": float((y_true == 1).mean()) if len(y_true) else np.nan,
            **stats,
        })

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--dropout", type=float, default=0.20)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-5)
    parser.add_argument("--patience", type=int, default=15)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--device",
        default="auto",
        help="auto, cpu, mps, cuda, etc.",
    )
    parser.add_argument(
        "--metrics-output",
        default="reports/multitask_admet_metrics.csv",
    )
    parser.add_argument(
        "--predictions-output",
        default="reports/multitask_admet_predictions.csv",
    )
    parser.add_argument(
        "--history-output",
        default="reports/multitask_admet_training_history.csv",
    )
    parser.add_argument(
        "--model-output",
        default="models/multitask_admet.pt",
    )
    args = parser.parse_args()

    set_seed(args.seed)
    device = choose_device(args.device)
    print(f"Device: {device}")

    endpoint_splits, conflict_df = load_endpoint_splits()

    conflict_out = Path("reports/multitask_conflicting_labels.csv")
    conflict_out.parent.mkdir(parents=True, exist_ok=True)
    conflict_df.to_csv(conflict_out, index=False)

    train_df = merge_split(endpoint_splits, "train")
    val_df = merge_split(endpoint_splits, "validation")
    test_df = merge_split(endpoint_splits, "test")

    print(
        f"Merged molecules: train={len(train_df)}, "
        f"validation={len(val_df)}, test={len(test_df)}"
    )

    print("\nTraining labels by endpoint:")
    for task in TASKS:
        labels = train_df[task].dropna().astype(int)
        print(
            f"  {task:8s} n={len(labels):5d} "
            f"positive_rate={labels.mean():.4f}"
        )

    train_ds = MultiTaskDataset(train_df)
    val_ds = MultiTaskDataset(val_df)
    test_ds = MultiTaskDataset(test_df)

    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size,
        shuffle=True,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=args.batch_size,
        shuffle=False,
    )

    model = MultiTaskADMET(
        input_dim=train_ds.X.shape[1],
        hidden_dim=args.hidden_dim,
        dropout=args.dropout,
    ).to(device)

    pos_weight = compute_pos_weights(train_df).to(device)
    print("\nTask positive-class weights:")
    for task, w in zip(TASKS, pos_weight.detach().cpu().tolist()):
        print(f"  {task:8s} {w:.4f}")

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
            pos_weight,
            optimizer=optimizer,
        )
        val_loss = run_epoch(
            model,
            val_loader,
            device,
            pos_weight,
            optimizer=None,
        )

        history.append({
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
        raise RuntimeError("Training finished without a valid model state.")

    model.load_state_dict(best_state)
    model.to(device)

    pred_df = predict(
        model,
        test_ds,
        test_df,
        device=device,
        batch_size=args.batch_size,
    )
    metrics_df = evaluate_test_predictions(pred_df)

    metrics_out = Path(args.metrics_output)
    preds_out = Path(args.predictions_output)
    history_out = Path(args.history_output)
    model_out = Path(args.model_output)

    for path in [metrics_out, preds_out, history_out, model_out]:
        path.parent.mkdir(parents=True, exist_ok=True)

    metrics_df.to_csv(metrics_out, index=False)
    pred_df.to_csv(preds_out, index=False)
    pd.DataFrame(history).to_csv(history_out, index=False)

    torch.save({
        "state_dict": best_state,
        "tasks": TASKS,
        "input_dim": int(train_ds.X.shape[1]),
        "hidden_dim": args.hidden_dim,
        "dropout": args.dropout,
        "seed": args.seed,
        "best_validation_loss": best_val_loss,
        "pos_weight": pos_weight.detach().cpu(),
    }, model_out)

    print("\n=== Multi-task ADMET test metrics ===")
    print(
        metrics_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print("\nSaved:")
    print(f"  {metrics_out}")
    print(f"  {preds_out}")
    print(f"  {history_out}")
    print(f"  {model_out}")
    print(f"  {conflict_out}")


if __name__ == "__main__":
    main()
