"""Foreground cropping for the fixed, single-part camera box."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any

import numpy as np


@dataclass(frozen=True)
class DetectedComponent:
    """One connected edge component in the downscaled camera image."""

    x: int
    y: int
    width: int
    height: int
    area: int

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2


def select_largest_central_component(
    components: list[DetectedComponent], image_width: int, image_height: int
) -> DetectedComponent | None:
    """Choose the largest component away from camera-frame artefacts at the edge."""
    horizontal_margin = image_width * 0.1
    vertical_margin = image_height * 0.1
    candidates = [
        component
        for component in components
        if component.area >= 100
        and horizontal_margin < component.center_x < image_width - horizontal_margin
        and vertical_margin < component.center_y < image_height - vertical_margin
    ]
    return max(candidates, key=lambda component: component.area, default=None)


def foreground_square_crop(image: Any, padding_ratio: float = 0.25) -> Any:
    """Crop the detected central part with surrounding context, without changing the source file."""
    if padding_ratio < 0:
        raise ValueError("Padding ratio must not be negative.")
    cv2 = import_module("cv2")
    source = np.asarray(image.convert("RGB"))
    source_height, source_width = source.shape[:2]
    scale = min(1.0, 1164 / source_width)
    preview = cv2.resize(
        source,
        (round(source_width * scale), round(source_height * scale)),
        interpolation=cv2.INTER_AREA,
    )
    grayscale = cv2.cvtColor(preview, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(grayscale, 40, 120)
    joined_edges = cv2.dilate(edges, np.ones((9, 9), dtype=np.uint8), iterations=2)
    count, _, statistics, _ = cv2.connectedComponentsWithStats(joined_edges)
    components = [
        DetectedComponent(
            x=int(statistics[index, cv2.CC_STAT_LEFT]),
            y=int(statistics[index, cv2.CC_STAT_TOP]),
            width=int(statistics[index, cv2.CC_STAT_WIDTH]),
            height=int(statistics[index, cv2.CC_STAT_HEIGHT]),
            area=int(statistics[index, cv2.CC_STAT_AREA]),
        )
        for index in range(1, count)
    ]
    selected = select_largest_central_component(components, preview.shape[1], preview.shape[0])
    if selected is None:
        return central_square_crop(image, fraction=0.4)
    center_x = selected.center_x / scale
    center_y = selected.center_y / scale
    side = max(selected.width, selected.height) / scale * (1 + 2 * padding_ratio)
    side = min(round(side), source_width, source_height)
    left = min(max(round(center_x - side / 2), 0), source_width - side)
    top = min(max(round(center_y - side / 2), 0), source_height - side)
    return image.crop((left, top, left + side, top + side))


def central_square_crop(image: Any, fraction: float) -> Any:
    """Return the configured central placement area as a safe detection fallback."""
    if not 0 < fraction <= 1:
        raise ValueError("Crop fraction must be between zero and one.")
    width, height = image.size
    side = round(min(width, height) * fraction)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side))
