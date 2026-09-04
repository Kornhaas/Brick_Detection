from datetime import datetime
from pathlib import Path

import pytest

from brick_detection.assisted_capture import (
    new_reference_root,
    suggestion_preview_paths,
    visible_suggestions,
)
from brick_detection.capture import (
    CaptureRecord,
    append_manifest_record,
    capture_path,
    new_holdout_root,
    validate_part_id,
)
from brick_detection.search import PartCandidate


def test_capture_path_is_below_images_directory_and_uses_safe_part_id(tmp_path: Path) -> None:
    path = capture_path(tmp_path, "3001", datetime(2026, 9, 4, 12, 30, 15, 123456))

    assert path == tmp_path / "images" / "3001_20260904T123015123456.jpg"


def test_new_holdout_root_is_distinct_and_date_stamped(tmp_path: Path) -> None:
    path = new_holdout_root(tmp_path, datetime(2026, 9, 4, 13, 30, 15))

    assert path == tmp_path / "holdout-20260904-133015"


def test_visible_suggestions_filters_by_similarity_and_limits_count() -> None:
    candidates = [
        PartCandidate("3001", 0.61, 12),
        PartCandidate("3002", 0.59, 10),
        PartCandidate("3003", 0.52, 9),
    ]

    assert visible_suggestions(candidates, minimum_score=0.55, maximum_count=2) == candidates[:2]


def test_new_reference_root_is_separate_from_holdout_root(tmp_path: Path) -> None:
    assert new_reference_root(tmp_path, datetime(2026, 9, 4, 13, 30, 15)) == (
        tmp_path / "session-20260904-133015"
    )


@pytest.mark.parametrize("part_id", ["", "  ", "3001/other", "3001.csv", "part id"])
def test_validate_part_id_rejects_unsafe_names(part_id: str) -> None:
    with pytest.raises(ValueError):
        validate_part_id(part_id)


def test_suggestion_preview_paths_prefer_a_consistent_three_quarter_render() -> None:
    previews = suggestion_preview_paths(
        [PartCandidate("3002", 0.8, 1), PartCandidate("3001", 0.7, 1)],
        (
            "/renders/3001/lower_000.png",
            "/renders/3001/upper_030_45.png",
            "/renders/3002/orbit_045_45.png",
        ),
        ("3001", "3001", "3002"),
    )

    assert previews == {
        "3001": Path("/renders/3001/upper_030_45.png"),
        "3002": Path("/renders/3002/orbit_045_45.png"),
    }


def test_append_manifest_record_creates_a_valid_csv(tmp_path: Path) -> None:
    append_manifest_record(tmp_path, CaptureRecord("images/3001_test.jpg", "3001"))
    append_manifest_record(tmp_path, CaptureRecord("images/3002_test.jpg", "3002"))

    assert (tmp_path / "manifest.csv").read_text(encoding="utf-8") == (
        "image_path,part_id\nimages/3001_test.jpg,3001\nimages/3002_test.jpg,3002\n"
    )
