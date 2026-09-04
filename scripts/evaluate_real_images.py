"""Evaluate labeled camera images against a local DINOv2 retrieval index."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from brick_detection.evaluation import metrics_by_part, retrieval_metrics
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
    parser.add_argument(
        "--foreground-crop",
        action="store_true",
        help="Detect and crop the central part before embedding",
    )
    arguments = parser.parse_args()
    manifest = arguments.manifest.resolve()
    # utf-8-sig accepts both app-generated UTF-8 and the BOM written by Excel/PowerShell.
    with manifest.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    paths = [manifest.parent / row["image_path"] for row in rows]
    if not rows or any(not path.is_file() for path in paths):
        raise SystemExit("Manifest must contain existing image paths.")

    index = EmbeddingIndex.load(arguments.index)
    encoder = DINOv2Encoder()
    if index.model_version != encoder.version:
        raise SystemExit(f"Index expects {index.model_version}, encoder is {encoder.version}.")
    vectors = encoder.embed_paths(paths, crop_foreground=arguments.foreground_crop)
    ranks: list[int | None] = []
    ranks_by_part: dict[str, list[int | None]] = {}
    details: list[dict[str, object]] = []
    for row, vector in zip(rows, vectors, strict=True):
        candidates = index.query(vector, top_part_k=10)
        candidate_ids = [candidate.part_id for candidate in candidates]
        rank = rank_of(row["part_id"], candidate_ids)
        ranks.append(rank)
        ranks_by_part.setdefault(row["part_id"], []).append(rank)
        details.append(
            {
                "image_path": row["image_path"],
                "part_id": row["part_id"],
                "rank": rank,
                "top_candidates": candidate_ids,
            }
        )
    result: dict[str, object] = {
        "index_model_version": index.model_version,
        "queries": len(rows),
        "protocol": "labeled real camera images, separate from reference renders"
        + ("; central foreground crop" if arguments.foreground_crop else ""),
    }
    result.update(retrieval_metrics(ranks))
    result["per_part"] = metrics_by_part(ranks_by_part)
    result["failures"] = [detail for detail in details if detail["rank"] != 1]
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
