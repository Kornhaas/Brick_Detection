"""Import a selected set of LDraw parts into the local SQLite catalogue."""

from __future__ import annotations

import argparse
from pathlib import Path

from brick_detection.catalog import import_parts


def filenames_from_manifest(path: Path) -> list[str]:
    """Read filenames while ignoring comments and empty lines."""
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", type=Path, required=True)
    parser.add_argument("--parts", type=Path, default=Path("configs/poc_parts.txt"))
    parser.add_argument("--database", type=Path, default=Path("data/catalog/brickvision.sqlite3"))
    arguments = parser.parse_args()
    records = import_parts(
        arguments.library.resolve(),
        filenames_from_manifest(arguments.parts.resolve()),
        arguments.database,
    )
    print(f"Imported {len(records)} parts into {arguments.database}")


if __name__ == "__main__":
    main()
