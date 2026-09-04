import json
from pathlib import Path

from brick_detection.rendering.bookkeeping import expected_view_files, is_completed_render


def test_completed_render_requires_matching_metadata_and_every_view(tmp_path: Path) -> None:
    target = tmp_path / "3001"
    target.mkdir()
    (target / "render_metadata.json").write_text(
        json.dumps({"view_set": "single"}), encoding="utf-8"
    )

    assert not is_completed_render(target, "single")

    for filename in expected_view_files("single"):
        (target / filename).touch()

    assert is_completed_render(target, "single")
    assert not is_completed_render(target, "poc-60")
