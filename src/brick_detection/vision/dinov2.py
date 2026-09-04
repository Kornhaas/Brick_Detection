"""Pinned DINOv2 encoder for local image embedding."""

from __future__ import annotations

from collections.abc import Sequence
from importlib import import_module
from pathlib import Path

import numpy as np

DINOV2_REVISION = "7764ea0f912e53c92e82eb78a2a1631e92725fc8"
MODEL_NAME = "dinov2_vits14"


class DINOv2Encoder:
    """Embed RGB images with the official, revision-pinned DINOv2 ViT-S/14 model."""

    def __init__(self, device: str | None = None) -> None:
        torch = import_module("torch")
        transforms = import_module("torchvision.transforms")

        self._torch = torch
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load(
            f"facebookresearch/dinov2:{DINOV2_REVISION}", MODEL_NAME, trust_repo=True
        ).to(self.device)
        self.model.eval()
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224), antialias=True),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ]
        )

    @property
    def version(self) -> str:
        """Return a stable identifier stored alongside generated embeddings."""
        return f"{MODEL_NAME}@{DINOV2_REVISION[:12]}"

    def embed_paths(self, paths: Sequence[Path], batch_size: int = 32) -> np.ndarray:
        """Return L2-normalized embeddings in the input path order."""
        image_module = import_module("PIL.Image")

        vectors: list[np.ndarray] = []
        with self._torch.inference_mode():
            for start in range(0, len(paths), batch_size):
                images = [
                    self.transform(image_module.open(path).convert("RGB"))
                    for path in paths[start : start + batch_size]
                ]
                output = self.model(self._torch.stack(images).to(self.device))
                normalized = self._torch.nn.functional.normalize(output, dim=1)
                vectors.append(normalized.cpu().numpy().astype(np.float32))
        return np.concatenate(vectors, axis=0) if vectors else np.empty((0, 0), dtype=np.float32)
