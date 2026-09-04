import pytest

from brick_detection.evaluation import metrics_by_part, retrieval_metrics
from brick_detection.vision.preprocess import (
    DetectedComponent,
    central_square_crop,
    select_largest_central_component,
)


def test_retrieval_metrics_calculates_top_k_and_mrr() -> None:
    metrics = retrieval_metrics([1, 2, None, 5])

    assert metrics == {"top_1": 0.25, "top_3": 0.5, "top_5": 0.75, "mrr_at_10": 0.425}


def test_retrieval_metrics_requires_queries() -> None:
    with pytest.raises(ValueError, match="At least"):
        retrieval_metrics([])


def test_metrics_by_part_reports_each_part_independently() -> None:
    metrics = metrics_by_part({"3002": [2, None], "3001": [1, 1]})

    assert metrics["3001"]["top_1"] == 1.0
    assert metrics["3002"]["top_1"] == 0.0
    assert metrics["3002"]["top_3"] == 0.5


def test_select_largest_central_component_ignores_frame_edge_noise() -> None:
    selected = select_largest_central_component(
        [
            DetectedComponent(x=0, y=0, width=200, height=200, area=50_000),
            DetectedComponent(x=400, y=300, width=50, height=60, area=3_000),
            DetectedComponent(x=500, y=300, width=40, height=40, area=2_000),
        ],
        image_width=1000,
        image_height=800,
    )

    assert selected == DetectedComponent(x=400, y=300, width=50, height=60, area=3_000)


def test_central_square_crop_uses_the_configured_middle_area() -> None:
    class TestImage:
        size = (1000, 800)

        def crop(self, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
            return box

    assert central_square_crop(TestImage(), fraction=0.5) == (300, 200, 700, 600)
