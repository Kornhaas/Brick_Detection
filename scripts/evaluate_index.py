"""Evaluate a reference index without querying a render against itself."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from brick_detection.evaluation import retrieval_metrics
from brick_detection.search import EmbeddingIndex


def rank_of(part_id: str, candidates: list[str]) -> int | None:
    """Return the one-based rank of a part, if present."""
    try:
        return candidates.index(part_id) + 1
    except ValueError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/evaluations/poc-v1.json"))
    arguments = parser.parse_args()
    index = EmbeddingIndex.load(arguments.index)
    ranks: list[int | None] = []
    for vector, part_id, image_path in zip(
        index.vectors, index.part_ids, index.image_paths, strict=True
    ):
        candidates = index.query(vector, top_part_k=10, exclude_image_path=image_path)
        ranks.append(rank_of(part_id, [candidate.part_id for candidate in candidates]))

    count = len(ranks)
    result: dict[str, object] = {
        "index_model_version": index.model_version,
        "queries": count,
        "protocol": "leave-one-render-out within synthetic reference set",
    }
    result.update(retrieval_metrics(ranks))
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
