"""Embed rendered parts and persist the first local retrieval index."""

from __future__ import annotations

import argparse
from pathlib import Path

from brick_detection.search import EmbeddingIndex
from brick_detection.vision import DINOv2Encoder


def render_paths(root: Path) -> tuple[list[Path], list[str]]:
    """Return rendered PNGs and their containing part IDs in stable order."""
    paths = sorted(path for path in root.glob("*/*.png") if path.name != "render.png")
    return paths, [path.parent.name for path in paths]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renders", type=Path, default=Path("data/renders/poc"))
    parser.add_argument("--output", type=Path, default=Path("data/indexes/poc-v1.npz"))
    parser.add_argument("--batch-size", type=int, default=32)
    arguments = parser.parse_args()
    paths, part_ids = render_paths(arguments.renders.resolve())
    if not paths:
        raise SystemExit(f"No renders found below {arguments.renders}")
    encoder = DINOv2Encoder()
    vectors = encoder.embed_paths(paths, arguments.batch_size)
    EmbeddingIndex(
        vectors, tuple(part_ids), tuple(str(path) for path in paths), encoder.version
    ).save(arguments.output)
    print(f"Indexed {len(paths)} renders for {len(set(part_ids))} parts using {encoder.version}")


if __name__ == "__main__":
    main()
