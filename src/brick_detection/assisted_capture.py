"""Pure policy helpers for human-confirmed reference capture."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np

from brick_detection.search import PartCandidate


def new_reference_root(base_directory: Path, created_at: datetime) -> Path:
    """Return a distinct directory for human-confirmed real reference images."""
    return base_directory / f"session-{created_at.strftime('%Y%m%d-%H%M%S')}"


def visible_suggestions(
    candidates: list[PartCandidate], minimum_score: float, maximum_count: int
) -> list[PartCandidate]:
    """Keep only the best candidates whose cosine similarity meets the UI threshold."""
    if not 0 <= minimum_score <= 1:
        raise ValueError("Minimum similarity must be between zero and one.")
    if maximum_count < 1:
        raise ValueError("Maximum candidate count must be positive.")
    return [candidate for candidate in candidates if candidate.score >= minimum_score][
        :maximum_count
    ]


def suggestion_preview_paths(
    candidates: list[PartCandidate], image_paths: tuple[str, ...], part_ids: tuple[str, ...]
) -> dict[str, Path]:
    """Choose one stable rendered preview image for every visible part suggestion."""
    if len(image_paths) != len(part_ids):
        raise ValueError("Image paths and part IDs must have matching lengths.")
    paths_by_part: dict[str, list[Path]] = {}
    for image_path, part_id in zip(image_paths, part_ids, strict=True):
        paths_by_part.setdefault(part_id, []).append(Path(image_path))
    return {
        candidate.part_id: min(paths_by_part[candidate.part_id], key=presentation_view_priority)
        for candidate in candidates
        if candidate.part_id in paths_by_part
    }


def presentation_view_priority(path: Path) -> tuple[int, str]:
    """Prioritize the consistent three-quarter render made for human confirmation."""
    preferred_names = ("upper_030_45.png", "orbit_045_45.png", "view_00.png")
    try:
        return (preferred_names.index(path.name), path.name)
    except ValueError:
        return (len(preferred_names), path.name)


def scene_has_changed(
    previous: np.ndarray,
    current: np.ndarray,
    pixel_difference: int = 25,
    minimum_changed_ratio: float = 0.004,
) -> bool:
    """Detect a meaningful change while ignoring small camera and compression noise."""
    if previous.shape != current.shape:
        raise ValueError("Scene signatures must have matching shapes.")
    if pixel_difference < 1 or not 0 < minimum_changed_ratio <= 1:
        raise ValueError("Change thresholds must be positive and the ratio must be at most one.")
    changed = np.abs(previous.astype(np.int16) - current.astype(np.int16)) >= pixel_difference
    return float(np.count_nonzero(changed)) / changed.size >= minimum_changed_ratio
