import pytest

from brick_detection.rendering import view_definitions


def test_poc_60_has_dense_top_orientations_and_complete_view_count() -> None:
    views = view_definitions("poc-60")

    assert len(views) == 60
    assert sum(view["elevation"] == 85.0 for view in views) == 12
    assert {view["azimuth"] for view in views if view["elevation"] == 85.0} == {
        float(angle) for angle in range(0, 360, 30)
    }


def test_unknown_view_set_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown"):
        view_definitions("does-not-exist")
