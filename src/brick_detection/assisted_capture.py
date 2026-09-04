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
