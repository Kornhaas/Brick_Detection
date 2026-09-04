import pytest

from brick_detection.evaluation import retrieval_metrics


def test_retrieval_metrics_calculates_top_k_and_mrr() -> None:
    metrics = retrieval_metrics([1, 2, None, 5])

    assert metrics == {"top_1": 0.25, "top_3": 0.5, "top_5": 0.75, "mrr_at_10": 0.425}


def test_retrieval_metrics_requires_queries() -> None:
    with pytest.raises(ValueError, match="At least"):
        retrieval_metrics([])
