"""Deep-learning model definitions for medical imaging classification."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleCNN(nn.Module):
    """Small CNN used for smoke tests and CPU-only demonstrations."""

    def __init__(self, num_classes: int = 2, in_channels: int = 1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.avg = nn.AdaptiveAvgPool2d((4, 4))
        self.fc1 = nn.Linear(64 * 4 * 4, 64)
        self.fc2 = nn.Linear(64, num_classes)

    def forward_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = F.relu(self.conv3(x))
        x = self.avg(x)
        x = torch.flatten(x, 1)
        return F.relu(self.fc1(x))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc2(self.forward_features(x))


class TransferLearningCNN(nn.Module):
    """ResNet50 or EfficientNet-B0 classifier with configurable input channels."""

    def __init__(
        self,
        architecture: str = "resnet50",
        num_classes: int = 2,
        in_channels: int = 1,
        pretrained: bool = False,
        freeze_backbone: bool = False,
    ):
        super().__init__()

        try:
            from torchvision import models
        except ImportError as exc:
            raise ImportError(
                "torchvision is required for TransferLearningCNN"
            ) from exc

        architecture = architecture.lower()

        if architecture == "resnet50":
            weights = models.ResNet50_Weights.DEFAULT if pretrained else None
            backbone = models.resnet50(weights=weights)

            if in_channels != 3:
                backbone.conv1 = nn.Conv2d(
                    in_channels,
                    64,
                    kernel_size=7,
                    stride=2,
                    padding=3,
                    bias=False,
                )

            feature_dim = backbone.fc.in_features
            backbone.fc = nn.Identity()

        elif architecture in {"efficientnet", "efficientnet_b0"}:
            weights = (
                models.EfficientNet_B0_Weights.DEFAULT
                if pretrained
                else None
            )
            backbone = models.efficientnet_b0(weights=weights)

            if in_channels != 3:
                old_layer = backbone.features[0][0]
                backbone.features[0][0] = nn.Conv2d(
                    in_channels,
                    old_layer.out_channels,
                    old_layer.kernel_size,
                    old_layer.stride,
                    old_layer.padding,
                    bias=False,
                )

            feature_dim = backbone.classifier[1].in_features
            backbone.classifier = nn.Identity()

        else:
            raise ValueError(
                "architecture must be 'resnet50' or 'efficientnet_b0'"
            )

        self.architecture = architecture
        self.backbone = backbone
        self.classifier = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(feature_dim, num_classes),
        )

        if freeze_backbone:
            for parameter in self.backbone.parameters():
                parameter.requires_grad = False

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.backbone(x))


class MultimodalClinicalModel(nn.Module):
    """Combine image features with structured clinical metadata."""

    def __init__(
        self,
        metadata_dim: int = 4,
        num_classes: int = 2,
        in_channels: int = 1,
    ):
        super().__init__()

        self.image_encoder = SimpleCNN(
            num_classes=num_classes,
            in_channels=in_channels,
        )
        self.meta_encoder = nn.Sequential(
            nn.Linear(metadata_dim, 16),
            nn.ReLU(),
            nn.Dropout(0.10),
            nn.Linear(16, 16),
            nn.ReLU(),
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 + 16, 64),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(64, num_classes),
        )

    def forward(
        self,
        image: torch.Tensor,
        metadata: torch.Tensor,
    ) -> torch.Tensor:
        image_features = self.image_encoder.forward_features(image)
        metadata_features = self.meta_encoder(metadata.float())
        combined_features = torch.cat(
            [image_features, metadata_features],
            dim=1,
        )
        return self.classifier(combined_features)


class GradCAM:
    """Minimal Grad-CAM helper for image-level explainability."""

    def __init__(self, model: nn.Module, target_layer: nn.Module):
        self.model = model
        self.gradients: torch.Tensor | None = None
        self.activations: torch.Tensor | None = None
        self._forward_handle = target_layer.register_forward_hook(
            self._save_activation
        )
        self._backward_handle = target_layer.register_full_backward_hook(
            self._save_gradient
        )

    def _save_activation(self, module, inputs, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(
        self,
        image_tensor: torch.Tensor,
        class_idx: int | None = None,
    ) -> torch.Tensor:
        self.model.eval()
        output = self.model(image_tensor)

        if class_idx is None:
            class_idx = int(output.argmax(dim=1).item())

        self.model.zero_grad(set_to_none=True)
        output[:, class_idx].sum().backward()

        if self.gradients is None or self.activations is None:
            raise RuntimeError(
                "Grad-CAM hooks did not capture gradients and activations."
            )

        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = F.relu(
            (weights * self.activations).sum(dim=1, keepdim=True)
        )
        cam = F.interpolate(
            cam,
            size=image_tensor.shape[2:],
            mode="bilinear",
            align_corners=False,
        )
        cam = cam.squeeze().detach().cpu()

        return (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)

    def close(self) -> None:
        """Remove registered hooks when Grad-CAM is no longer needed."""
        self._forward_handle.remove()
        self._backward_handle.remove()
