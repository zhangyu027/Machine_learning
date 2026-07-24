"""Fine-tune DistilBERT for three-class clinical eligibility classification.

This is a real Hugging Face training path. It downloads model weights on first run.
For a domain-specific alternative, pass --model-name emilyalsentzer/Bio_ClinicalBERT.
"""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "outputs" / "clinical_notes_processed.csv"
MODEL_DIR = ROOT / "models" / "distilbert_clinical_eligibility"
METRICS_PATH = ROOT / "outputs" / "distilbert_metrics.json"
PREDICTIONS_PATH = ROOT / "outputs" / "distilbert_predictions.csv"
LABELS = ["eligible", "needs_review", "not_eligible"]
LABEL2ID = {label: idx for idx, label in enumerate(LABELS)}
ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", default="distilbert-base-uncased")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        import torch
        from torch.utils.data import Dataset
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            DataCollatorWithPadding,
            Trainer,
            TrainingArguments,
        )
    except ImportError as exc:
        raise SystemExit(
            "Transformer dependencies are missing. Run: pip install -r requirements-transformers.txt"
        ) from exc

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    if not DATA_PATH.exists():
        raise FileNotFoundError("Run preprocessing before transformer training.")

    df = pd.read_csv(DATA_PATH).dropna(subset=["clean_text", "label"])
    train_df, test_df = train_test_split(
        df, test_size=0.25, random_state=args.seed, stratify=df["label"]
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    class ClinicalDataset(Dataset):
        def __init__(self, frame: pd.DataFrame):
            self.texts = frame["clean_text"].astype(str).tolist()
            self.labels = [LABEL2ID[x] for x in frame["label"].tolist()]

        def __len__(self):
            return len(self.labels)

        def __getitem__(self, idx: int):
            item = tokenizer(
                self.texts[idx], truncation=True, max_length=args.max_length
            )
            item["labels"] = self.labels[idx]
            return item

    train_dataset = ClinicalDataset(train_df)
    test_dataset = ClinicalDataset(test_df)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=len(LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )

    def compute_metrics(eval_pred):
        logits, label_ids = eval_pred
        pred_ids = np.argmax(logits, axis=-1)
        y_true = [ID2LABEL[int(x)] for x in label_ids]
        y_pred = [ID2LABEL[int(x)] for x in pred_ids]
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "macro_f1": f1_score(y_true, y_pred, average="macro"),
            "eligible_recall": recall_score(
                y_true, y_pred, labels=["eligible"], average="macro", zero_division=0
            ),
        }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    training_args = TrainingArguments(
        output_dir=str(MODEL_DIR / "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        report_to=[],
        seed=args.seed,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
        compute_metrics=compute_metrics,
    )
    train_start = time.perf_counter()
    trainer.train()
    training_seconds = time.perf_counter() - train_start
    eval_metrics = trainer.evaluate()

    start = time.perf_counter()
    prediction_output = trainer.predict(test_dataset)
    total_inference = time.perf_counter() - start
    pred_ids = np.argmax(prediction_output.predictions, axis=-1)
    pred_labels = [ID2LABEL[int(x)] for x in pred_ids]
    true_labels = test_df["label"].tolist()

    trainer.save_model(str(MODEL_DIR))
    tokenizer.save_pretrained(str(MODEL_DIR))
    pd.DataFrame({
        "note_text": test_df["clean_text"].tolist(),
        "label": true_labels,
        "prediction": pred_labels,
    }).to_csv(PREDICTIONS_PATH, index=False)

    metrics = {
        "status": "completed",
        "model_name": args.model_name,
        "accuracy": float(eval_metrics["eval_accuracy"]),
        "macro_f1": float(eval_metrics["eval_macro_f1"]),
        "eligible_recall": float(eval_metrics["eval_eligible_recall"]),
        "latency_ms_per_note": float(total_inference / max(len(test_dataset), 1) * 1000),
        "training_seconds": float(training_seconds),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "cost_tier": "Medium",
        "explainability": "Medium",
        "data_type": "synthetic_demo_data",
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
