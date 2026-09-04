import numpy as np
import pytest

from brick_detection.search import EmbeddingIndex


def test_query_aggregates_multiple_matching_views_by_part() -> None:
    index = EmbeddingIndex(
        vectors=np.array([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]], dtype=np.float32),
        part_ids=("3001", "3001", "3002"),
        image_paths=("a.png", "b.png", "c.png"),
        model_version="test-v1",
    )

    candidates = index.query(np.array([1.0, 0.0], dtype=np.float32), top_render_k=3)

    assert candidates[0].part_id == "3001"
    assert candidates[0].matching_views == 2
    assert candidates[0].score == pytest.approx(0.95)
    assert candidates[1].part_id == "3002"


def test_query_scores_a_part_using_only_its_strongest_evidence_views() -> None:
    index = EmbeddingIndex(
        vectors=np.array(
            [[1.0, 0.0], [0.8, 0.6], [0.6, 0.8], [0.0, 1.0]], dtype=np.float32
        ),
        part_ids=("3001", "3001", "3001", "3002"),
        image_paths=("a.png", "b.png", "c.png", "d.png"),
        model_version="test-v1",
    )

    candidate = index.query(
        np.array([1.0, 0.0], dtype=np.float32), top_render_k=4, evidence_view_k=2
    )[0]

    assert candidate.part_id == "3001"
    assert candidate.score == pytest.approx(0.9)


def test_query_rejects_wrong_vector_dimension() -> None:
    index = EmbeddingIndex(
        vectors=np.array([[1.0, 0.0]], dtype=np.float32),
        part_ids=("3001",),
        image_paths=("a.png",),
        model_version="test-v1",
    )

    with pytest.raises(ValueError, match="dimension"):
        index.query(np.array([1.0, 0.0, 0.0], dtype=np.float32))


def test_query_can_exclude_the_exact_render_being_evaluated() -> None:
    index = EmbeddingIndex(
        vectors=np.array([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]], dtype=np.float32),
        part_ids=("3001", "3001", "3002"),
        image_paths=("self.png", "other.png", "third.png"),
        model_version="test-v1",
    )

    candidates = index.query(np.array([1.0, 0.0], dtype=np.float32), exclude_image_path="self.png")

    assert candidates[0].part_id == "3001"
    assert candidates[0].matching_views == 1
