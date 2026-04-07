from torch import nn
from torchvision import models

from config import MODEL_NAME, USE_PRETRAINED

class CNNBackbone(nn.Module):
    def __init__(self, model_name: str = MODEL_NAME):
        super().__init__()

        if model_name == "resnet18":
            weights = models.ResNet18_Weights.DEFAULT if USE_PRETRAINED else None
            backbone = models.resnet18(weights=weights)
            self.output_dim = backbone.fc.in_features
            backbone.fc = nn.Identity()
            self.encoder = backbone
        else:
            raise ValueError(f"Unsupported MODEL_NAME={model_name}")

    def forward(self, x):
        return self.encoder(x)
