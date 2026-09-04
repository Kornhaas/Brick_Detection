"""Query the local retrieval index with one image."""

from __future__ import annotations

import argparse
from pathlib import Path

from brick_detection.search import EmbeddingIndex
from brick_detection.vision import DINOv2Encoder


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=5)
    arguments = parser.parse_args()
    index = EmbeddingIndex.load(arguments.index)
    encoder = DINOv2Encoder()
    if index.model_version != encoder.version:
        raise SystemExit(f"Index expects {index.model_version}, encoder is {encoder.version}.")
    vector = encoder.embed_paths([arguments.image.resolve()])[0]
    for candidate in index.query(vector, top_part_k=arguments.top_k):
        print(
            f"{candidate.part_id}\t{candidate.score:.4f}\t{candidate.matching_views} matching views"
        )


if __name__ == "__main__":
    main()
