"""Resumable local bookkeeping for LDraw render jobs."""

from __future__ import annotations

import json
from pathlib import Path

from brick_detection.rendering.views import view_definitions


def expected_view_files(view_set: str) -> set[str]:
    """Return the exact image filenames required for one completed part render."""
    return {f"{view['name']}.png" for view in view_definitions(view_set)}


def is_completed_render(output_directory: Path, view_set: str) -> bool:
    """Treat a render as complete only with matching metadata and every expected image."""
    metadata_path = output_directory / "render_metadata.json"
    if not metadata_path.is_file():
        return False
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if metadata.get("view_set") != view_set:
        return False
    return all(
        (output_directory / filename).is_file() for filename in expected_view_files(view_set)
    )


def append_event(path: Path, event: dict[str, object]) -> None:
    """Append an auditable event without rewriting the running job history."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as file:
        file.write(json.dumps(event, sort_keys=True) + "\n")
