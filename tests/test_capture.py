from datetime import datetime
from pathlib import Path

import pytest

from brick_detection.capture import (
    CaptureRecord,
    append_manifest_record,
    capture_path,
    validate_part_id,
)


def test_capture_path_is_below_images_directory_and_uses_safe_part_id(tmp_path: Path) -> None:
    path = capture_path(tmp_path, "3001", datetime(2026, 9, 4, 12, 30, 15, 123456))

    assert path == tmp_path / "images" / "3001_20260904T123015123456.jpg"


@pytest.mark.parametrize("part_id", ["", "  ", "3001/other", "3001.csv", "part id"])
def test_validate_part_id_rejects_unsafe_names(part_id: str) -> None:
    with pytest.raises(ValueError):
        validate_part_id(part_id)


def test_append_manifest_record_creates_a_valid_csv(tmp_path: Path) -> None:
    append_manifest_record(tmp_path, CaptureRecord("images/3001_test.jpg", "3001"))
    append_manifest_record(tmp_path, CaptureRecord("images/3002_test.jpg", "3002"))

    assert (tmp_path / "manifest.csv").read_text(encoding="utf-8") == (
        "image_path,part_id\nimages/3001_test.jpg,3001\nimages/3002_test.jpg,3002\n"
    )
