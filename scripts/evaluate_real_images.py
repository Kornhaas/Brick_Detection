"""Evaluate labeled camera images against a local DINOv2 retrieval index."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from brick_detection.evaluation import retrieval_metrics
from brick_detection.search import EmbeddingIndex
from brick_detection.vision import DINOv2Encoder


def rank_of(part_id: str, candidates: list[str]) -> int | None:
    """Return a one-based target rank, if it occurs in the candidates."""
    try:
        return candidates.index(part_id) + 1
    except ValueError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/evaluations/real-v1.json"))
    arguments = parser.parse_args()
    manifest = arguments.manifest.resolve()
    with manifest.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    paths = [manifest.parent / row["image_path"] for row in rows]
    if not rows or any(not path.is_file() for path in paths):
        raise SystemExit("Manifest must contain existing image paths.")

    index = EmbeddingIndex.load(arguments.index)
    encoder = DINOv2Encoder()
    if index.model_version != encoder.version:
        raise SystemExit(f"Index expects {index.model_version}, encoder is {encoder.version}.")
    vectors = encoder.embed_paths(paths)
    ranks = [
        rank_of(
            row["part_id"], [candidate.part_id for candidate in index.query(vector, top_part_k=10)]
        )
        for row, vector in zip(rows, vectors, strict=True)
    ]
    result: dict[str, object] = {
        "index_model_version": index.model_version,
        "queries": len(rows),
        "protocol": "labeled real camera images, separate from reference renders",
    }
    result.update(retrieval_metrics(ranks))
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
