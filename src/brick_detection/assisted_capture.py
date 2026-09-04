"""Pure policy helpers for human-confirmed reference capture."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

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
    first_path_by_part: dict[str, Path] = {}
    for image_path, part_id in zip(image_paths, part_ids, strict=True):
        first_path_by_part.setdefault(part_id, Path(image_path))
    return {
        candidate.part_id: first_path_by_part[candidate.part_id]
        for candidate in candidates
        if candidate.part_id in first_path_by_part
    }
