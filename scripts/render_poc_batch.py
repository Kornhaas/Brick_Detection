"""Run the Blender renderer for every part in a simple text manifest."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def parts_from_manifest(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blender", type=Path, required=True)
    parser.add_argument("--library", type=Path, required=True)
    parser.add_argument("--parts", type=Path, default=Path("configs/poc_parts.txt"))
    parser.add_argument("--output", type=Path, default=Path("data/renders/poc"))
    parser.add_argument("--view-set", default="poc-28")
    arguments = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    for part in parts_from_manifest(arguments.parts.resolve()):
        command = [
            str(arguments.blender.resolve()),
            "--background",
            "--factory-startup",
            "--python",
            str(repository_root / "scripts" / "render_part.py"),
            "--",
            "--library",
            str(arguments.library.resolve()),
            "--part",
            part,
            "--output",
            str((arguments.output / Path(part).stem).resolve()),
            "--view-set",
            arguments.view_set,
        ]
        print(f"Rendering {part}")
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
