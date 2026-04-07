from __future__ import annotations

import torch
from torch.utils.data import DataLoader

from config import cfg
from preprocessing.dataset import ImageFolderWithOptionalMetadata
from model.cnn_backbone import CNNClassifier
from model.multimodal_model import MultimodalGraphModel
from model.graph_fusion import SimpleKNNGraphRefiner
from model.utils import compute_classification_metrics, load_pickle, save_json, to_numpy

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def build_model():
    if cfg.model_type == "cnn":
        model = CNNClassifier(num_classes=cfg.num_classes)
    else:
        model = MultimodalGraphModel(metadata_dim=len(cfg.metadata_features), num_classes=cfg.num_classes)
    model.load_state_dict(torch.load(cfg.model_path, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model

def main():
    test_dataset = ImageFolderWithOptionalMetadata(cfg.test_dir, train=False)
    if len(test_dataset) == 0:
        print("No test images found. Add files under data/test/* and rerun.")
        return

    loader = DataLoader(test_dataset, batch_size=cfg.batch_size, shuffle=False)
    model = build_model()

    refiner = None
    if cfg.model_type == "multimodal_graph" and cfg.graph_cache_path.exists():
        refiner = load_pickle(cfg.graph_cache_path)

    y_true, y_pred, y_prob = [], [], []

    with torch.no_grad():
        for batch in loader:
            images = batch["image"].to(DEVICE)
            labels = batch["label"].to(DEVICE)

            if cfg.model_type == "cnn":
                logits, _ = model(images)
                probs = torch.softmax(logits, dim=1)
            else:
                metadata = batch["metadata"].to(DEVICE)
                logits, embeddings = model(images, metadata)
                probs = torch.softmax(logits, dim=1)
                if refiner is not None:
                    refined_probs = []
                    for i in range(probs.shape[0]):
                        result = refiner.refine(
                            query_embedding=to_numpy(embeddings[i]),
                            base_probability=to_numpy(probs[i]),
                        )
                        refined_probs.append(result["final_probability"])
                    probs = torch.tensor(refined_probs, dtype=torch.float32, device=DEVICE)

            preds = torch.argmax(probs, dim=1)
            y_true.extend(labels.cpu().tolist())
            y_pred.extend(preds.cpu().tolist())
            y_prob.extend(probs[:, 1].cpu().tolist())

    metrics = compute_classification_metrics(y_true, y_pred, y_prob)
    save_json(metrics, cfg.artifacts_dir / "evaluation_metrics.json")
    print(metrics)

if __name__ == "__main__":
    main()
