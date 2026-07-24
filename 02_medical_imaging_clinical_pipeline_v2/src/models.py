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
    """ResNet50 or EfficientNet-B0 classifier with configurable input channels.

    Pretrained weights are optional so the project can run in offline environments.
    """

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
            raise ImportError("torchvision is required for TransferLearningCNN") from exc

        architecture = architecture.lower()
        if architecture == "resnet50":
            weights = models.ResNet50_Weights.DEFAULT if pretrained else None
            backbone = models.resnet50(weights=weights)
            if in_channels != 3:
                backbone.conv1 = nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)
            feature_dim = backbone.fc.in_features
            backbone.fc = nn.Identity()
        elif architecture in {"efficientnet", "efficientnet_b0"}:
            weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
            backbone = models.efficientnet_b0(weights=weights)
            if in_channels != 3:
                old = backbone.features[0][0]
                backbone.features[0][0] = nn.Conv2d(
                    in_channels, old.out_channels, old.kernel_size, old.stride, old.padding, bias=False
                )
            feature_dim = backbone.classifier[1].in_features
            backbone.classifier = nn.Identity()
        else:
            raise ValueError("architecture must be 'resnet50' or 'efficientnet_b0'")

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
    def __init__(self, metadata_dim: int = 4, num_classes: int = 2):
        super().__init__()
        self.image_encoder = SimpleCNN(num_classes=64)
        self.meta_encoder = nn.Sequential(
            nn.Linear(metadata_dim, 16), nn.ReLU(), nn.Linear(16, 16), nn.ReLU()
        )
        self.classifier = nn.Sequential(nn.Linear(80, 64), nn.ReLU(), nn.Linear(64, num_classes))

    def forward(self, image: torch.Tensor, metadata: torch.Tensor) -> torch.Tensor:
        return self.classifier(torch.cat([self.image_encoder(image), self.meta_encoder(metadata)], dim=1))


class GradCAM:
    """Minimal Grad-CAM helper for image-level explainability."""

    def __init__(self, model: nn.Module, target_layer: nn.Module):
        self.model = model
        self.gradients = None
        self.activations = None
        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, inputs, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(self, image_tensor: torch.Tensor, class_idx: int | None = None) -> torch.Tensor:
        self.model.eval()
        output = self.model(image_tensor)
        class_idx = output.argmax(dim=1).item() if class_idx is None else class_idx
        self.model.zero_grad()
        output[:, class_idx].backward()
        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = F.relu((weights * self.activations).sum(dim=1, keepdim=True))
        cam = F.interpolate(cam, size=image_tensor.shape[2:], mode="bilinear", align_corners=False)
        cam = cam.squeeze().cpu()
        return (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
