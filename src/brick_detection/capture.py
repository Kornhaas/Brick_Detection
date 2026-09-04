"""File and manifest handling for labeled camera captures."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

PART_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


@dataclass(frozen=True)
class CaptureRecord:
    """One labeled image relative to the validation directory."""

    image_path: str
    part_id: str


def validate_part_id(part_id: str) -> str:
    """Return a safe, non-empty part ID suitable for local filenames."""
    normalized = part_id.strip()
    if not PART_ID_PATTERN.fullmatch(normalized):
        raise ValueError("Part ID may contain only letters, digits, hyphens, and underscores.")
    return normalized


def capture_path(validation_root: Path, part_id: str, captured_at: datetime) -> Path:
    """Build a collision-resistant JPEG path below the validation image folder."""
    safe_part_id = validate_part_id(part_id)
    timestamp = captured_at.strftime("%Y%m%dT%H%M%S%f")
    return validation_root / "images" / f"{safe_part_id}_{timestamp}.jpg"


def append_manifest_record(validation_root: Path, record: CaptureRecord) -> None:
    """Append one relative image path and its known part ID to the CSV manifest."""
    manifest_path = validation_root / "manifest.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not manifest_path.exists()
    with manifest_path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["image_path", "part_id"])
        if new_file:
            writer.writeheader()
        writer.writerow(
            {"image_path": record.image_path, "part_id": validate_part_id(record.part_id)}
        )
