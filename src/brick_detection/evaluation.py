"""Metrics used for synthetic and real retrieval evaluation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


def retrieval_metrics(ranks: Sequence[int | None]) -> dict[str, float]:
    """Calculate ranking metrics where ranks are one-based and capped at ten."""
    if not ranks:
        raise ValueError("At least one query result is required.")
    count = len(ranks)
    return {
        "top_1": sum(rank == 1 for rank in ranks) / count,
        "top_3": sum(rank is not None and rank <= 3 for rank in ranks) / count,
        "top_5": sum(rank is not None and rank <= 5 for rank in ranks) / count,
        "mrr_at_10": sum(1 / rank if rank is not None else 0 for rank in ranks) / count,
    }


def metrics_by_part(
    ranks_by_part: Mapping[str, Sequence[int | None]],
) -> dict[str, dict[str, float]]:
    """Calculate retrieval metrics separately for every labeled part."""
    return {part_id: retrieval_metrics(ranks) for part_id, ranks in sorted(ranks_by_part.items())}
