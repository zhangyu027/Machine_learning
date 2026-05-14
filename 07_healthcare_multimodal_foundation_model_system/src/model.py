import torch
import torch.nn as nn


class ImageEncoder(nn.Module):
    def __init__(self, output_dim=32):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 12, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(12, 24, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(24 * 8 * 8, output_dim),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.encoder(x)


class TabularEncoder(nn.Module):
    def __init__(self, input_dim, output_dim=16):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 24),
            nn.ReLU(),
            nn.Linear(24, output_dim),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.encoder(x)


class TextEncoder(nn.Module):
    def __init__(self, input_dim, output_dim=24):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 48),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(48, output_dim),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.encoder(x)


class MultimodalRiskModel(nn.Module):
    def __init__(self, structured_dim, lab_dim, text_dim):
        super().__init__()
        self.image_encoder = ImageEncoder(output_dim=32)
        self.structured_encoder = TabularEncoder(structured_dim, output_dim=16)
        self.lab_encoder = TabularEncoder(lab_dim, output_dim=16)
        self.text_encoder = TextEncoder(text_dim, output_dim=24)

        fusion_dim = 32 + 16 + 16 + 24
        self.fusion = nn.Sequential(
            nn.Linear(fusion_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
        )

        self.classifier = nn.Linear(32, 1)

    def forward(self, image, structured, labs, text):
        image_vec = self.image_encoder(image)
        structured_vec = self.structured_encoder(structured)
        lab_vec = self.lab_encoder(labs)
        text_vec = self.text_encoder(text)

        fused = torch.cat([image_vec, structured_vec, lab_vec, text_vec], dim=1)
        hidden = self.fusion(fused)
        return self.classifier(hidden).squeeze(1)
