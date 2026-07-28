"""Distributed training configuration helpers for torchrun/DeepSpeed/Ray."""
from __future__ import annotations
import os

def distributed_context() -> dict:
    return {"world_size": int(os.getenv("WORLD_SIZE", "1")), "rank": int(os.getenv("RANK", "0")), "local_rank": int(os.getenv("LOCAL_RANK", "0"))}

def torchrun_command(config: str = "configs/train.yaml", processes: int = 2) -> str:
    return f"torchrun --standalone --nproc_per_node={processes} training/train_multimodal.py --config {config}"
