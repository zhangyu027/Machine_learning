"""Streamlit application for the medical-imaging clinical AI demo."""

from __future__ import annotations

import io
import json
import time
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import torch
from PIL import Image
from torch import nn
from torchvision import models, transforms


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "outputs" / "figures"
TABLE_DIR = ROOT / "outputs" / "tables"
DOC_PATH = ROOT / "docs" / "CLINICAL_INTERPRETATION.md"
CHECKPOINT = (
    ROOT
    / "models"
    / "checkpoints"
    / "efficientnet_b0"
    / "best_model.pt"
)
RUN_SUMMARY = CHECKPOINT.parent / "run_summary.json"
BEST_METRICS = CHECKPOINT.parent / "best_metrics.json"

st.set_page_config(
    page_title="Medical Imaging Clinical AI",
    page_icon="🩻",
    layout="wide",
)


def select_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def build_model(
    architecture: str,
    num_classes: int,
) -> nn.Module:
    if architecture == "resnet18":
        model = models.resnet18(weights=None)
        model.fc = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(model.fc.in_features, num_classes),
        )
    elif architecture == "resnet50":
        model = models.resnet50(weights=None)
        model.fc = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(model.fc.in_features, num_classes),
        )
    elif architecture == "efficientnet_b0":
        model = models.efficientnet_b0(weights=None)
        model.classifier = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(model.classifier[1].in_features, num_classes),
        )
    elif architecture == "efficientnet_v2_s":
        model = models.efficientnet_v2_s(weights=None)
        model.classifier = nn.Sequential(
            nn.Dropout(0.30),
            nn.Linear(model.classifier[1].in_features, num_classes),
        )
    else:
        raise ValueError(f"Unsupported architecture: {architecture}")

    return model


@st.cache_resource
def load_model():
    if not CHECKPOINT.is_file():
        raise FileNotFoundError(
            f"Checkpoint not found: {CHECKPOINT}"
        )

    device = select_device()
    checkpoint = torch.load(CHECKPOINT, map_location=device)

    architecture = str(
        checkpoint.get("architecture", "efficientnet_b0")
    )
    class_names = checkpoint.get(
        "class_names",
        checkpoint.get("classes", ["NORMAL", "PNEUMONIA"]),
    )
    image_size = int(checkpoint.get("image_size", 224))

    model = build_model(
        architecture=architecture,
        num_classes=len(class_names),
    )
    model.load_state_dict(checkpoint["state_dict"])
    model.to(device)
    model.eval()

    metadata = {
        "architecture": architecture,
        "class_names": list(class_names),
        "image_size": image_size,
        "best_validation_score": checkpoint.get(
            "best_validation_score"
        ),
    }

    return model, metadata, device


def build_inference_transform(image_size: int):
    return transforms.Compose(
        [
            transforms.Grayscale(num_output_channels=3),
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )


def predict_image(image: Image.Image) -> dict[str, Any]:
    model, metadata, device = load_model()
    transform = build_inference_transform(metadata["image_size"])
    tensor = transform(image.convert("RGB")).unsqueeze(0).to(device)

    started = time.perf_counter()
    with torch.inference_mode():
        logits = model(tensor)
        probabilities = torch.softmax(logits, dim=1)[0]

    probabilities = probabilities.detach().cpu()
    predicted_index = int(probabilities.argmax().item())

    return {
        "predicted_class": metadata["class_names"][predicted_index],
        "confidence": float(probabilities[predicted_index].item()),
        "class_probabilities": {
            class_name: float(probabilities[index].item())
            for index, class_name in enumerate(
                metadata["class_names"]
            )
        },
        "architecture": metadata["architecture"],
        "device": str(device),
        "latency_ms": round(
            (time.perf_counter() - started) * 1000,
            2,
        ),
    }


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


st.title("🩻 Medical Imaging Clinical AI")
st.caption(
    "EfficientNet-B0 chest X-ray classification demo with "
    "model evaluation and local inference."
)

st.warning(
    "Research and portfolio demonstration only. "
    "This application is not for diagnosis or patient care."
)

(
    tab_predict,
    tab_results,
    tab_interpretation,
    tab_run,
) = st.tabs(
    [
        "Predict",
        "Results",
        "Clinical Interpretation",
        "How to Run",
    ]
)


with tab_predict:
    st.subheader("Run local image inference")

    checkpoint_status = "Available" if CHECKPOINT.is_file() else "Missing"
    st.write(f"**Checkpoint:** `{CHECKPOINT}`")
    st.write(f"**Status:** {checkpoint_status}")

    if not CHECKPOINT.is_file():
        st.error(
            "The EfficientNet-B0 checkpoint was not found. "
            "Run training before using inference."
        )
    else:
        try:
            _, metadata, device = load_model()
            col1, col2, col3 = st.columns(3)
            col1.metric("Architecture", metadata["architecture"])
            col2.metric("Image size", f"{metadata['image_size']} × {metadata['image_size']}")
            col3.metric("Device", str(device))
        except Exception as exc:
            st.error(f"Unable to load model: {exc}")

    uploaded_file = st.file_uploader(
        "Upload a chest X-ray image",
        type=["png", "jpg", "jpeg"],
    )

    if uploaded_file is not None:
        try:
            image_bytes = uploaded_file.getvalue()
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

            left, right = st.columns([1, 1])

            with left:
                st.image(
                    image,
                    caption=uploaded_file.name,
                    use_container_width=True,
                )

            with right:
                with st.spinner("Running inference..."):
                    result = predict_image(image)

                st.success(
                    f"Prediction: {result['predicted_class']}"
                )
                st.metric(
                    "Confidence",
                    f"{result['confidence']:.2%}",
                )
                st.write(
                    f"Architecture: `{result['architecture']}`"
                )
                st.write(f"Device: `{result['device']}`")
                st.write(
                    f"Latency: `{result['latency_ms']} ms`"
                )

                probability_table = pd.DataFrame(
                    {
                        "Class": list(
                            result["class_probabilities"].keys()
                        ),
                        "Probability": list(
                            result["class_probabilities"].values()
                        ),
                    }
                )
                st.dataframe(
                    probability_table.style.format(
                        {"Probability": "{:.2%}"}
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
                st.bar_chart(
                    probability_table.set_index("Class")
                )

        except Exception as exc:
            st.error(f"Prediction failed: {exc}")


with tab_results:
    st.subheader("Training summary")

    summary = read_json(RUN_SUMMARY)
    metrics = read_json(BEST_METRICS)

    if summary:
        first, second, third = st.columns(3)
        first.metric(
            "Architecture",
            summary.get("architecture", "Unknown"),
        )
        second.metric(
            "Best validation score",
            f"{summary.get('best_validation_score', 0):.4f}",
        )
        third.metric(
            "Classes",
            ", ".join(summary.get("class_names", [])),
        )

    if metrics:
        selected_metrics = {
            "Accuracy": metrics.get("accuracy"),
            "ROC AUC": metrics.get("roc_auc"),
            "F1": metrics.get("f1"),
            "Sensitivity": metrics.get("sensitivity_recall"),
            "Specificity": metrics.get("specificity"),
            "Average precision": metrics.get("average_precision"),
        }
        metrics_df = pd.DataFrame(
            {
                "Metric": selected_metrics.keys(),
                "Value": selected_metrics.values(),
            }
        )
        st.dataframe(
            metrics_df.style.format({"Value": "{:.4f}"}),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info(
            "Training metrics were not found in the checkpoint directory."
        )

    st.subheader("Evaluation artifacts")
    artifact_files = [
        CHECKPOINT.parent / "confusion_matrix.png",
        CHECKPOINT.parent / "roc_curve.png",
        FIGURE_DIR / "gradcam_heatmap.png",
        FIGURE_DIR / "roc_curve_comparison.png",
        FIGURE_DIR / "precision_recall_curve_comparison.png",
        FIGURE_DIR / "model_comparison_bar_chart.png",
    ]

    displayed = False
    for artifact_path in artifact_files:
        if artifact_path.is_file():
            st.image(
                str(artifact_path),
                caption=artifact_path.name,
                use_container_width=True,
            )
            displayed = True

    if not displayed:
        st.info(
            "No evaluation figures were found. Run training and "
            "the notebook to generate them."
        )

    table_candidates = [
        TABLE_DIR / "model_comparison.csv",
        TABLE_DIR / "real_evaluation_table.csv",
        TABLE_DIR / "evaluation_metrics.csv",
    ]

    for table_path in table_candidates:
        if table_path.is_file():
            st.subheader(table_path.stem.replace("_", " ").title())
            st.dataframe(
                pd.read_csv(table_path),
                use_container_width=True,
            )


with tab_interpretation:
    if DOC_PATH.is_file():
        st.markdown(DOC_PATH.read_text(encoding="utf-8"))
    else:
        st.warning(
            "Clinical interpretation document not found at "
            f"`{DOC_PATH}`."
        )


with tab_run:
    st.markdown(
        """
        ## 1. Train the EfficientNet-B0 model

        ```bash
        python -m src.train_cnn \
          --architecture efficientnet_b0 \
          --epochs 5
        ```

        ## 2. Start the FastAPI service

        ```bash
        uvicorn api.main:app --reload
        ```

        Test the API:

        ```bash
        curl http://localhost:8000/health
        ```

        ```bash
        curl -X POST http://localhost:8000/predict \
          -F "file=@data/images/test/NORMAL/example.jpeg"
        ```

        Interactive API documentation:

        ```text
        http://localhost:8000/docs
        ```

        ## 3. Start this Streamlit application

        ```bash
        streamlit run app/streamlit_app.py
        ```

        If the Torch file-watcher warning appears:

        ```bash
        streamlit run app/streamlit_app.py \
          --server.fileWatcherType none
        ```
        """
    )
