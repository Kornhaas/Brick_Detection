"""Render only missing LDraw parts with durable local progress bookkeeping."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from brick_detection.rendering.bookkeeping import append_event, is_completed_render


def parts_from_file(path: Path) -> list[str]:
    """Read a stable, comment-friendly list of LDraw part filenames."""
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def library_parts(library: Path) -> list[str]:
    """Return all official direct part files in deterministic order."""
    return [path.name for path in sorted((library / "parts").glob("*.dat"))]


def timestamp() -> str:
    """Return one portable UTC timestamp for the append-only job history."""
    return datetime.now(UTC).isoformat(timespec="seconds")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blender", type=Path, required=True)
    parser.add_argument("--library", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--view-set", default="single")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all", action="store_true", help="Render every official LDraw part.")
    scope.add_argument(
        "--parts", type=Path, help="Render only part filenames listed in a text file."
    )
    parser.add_argument("--limit", type=int, help="Maximum missing parts to process in this run.")
    parser.add_argument("--minimum-free-gib", type=float, default=20.0)
    parser.add_argument(
        "--bookkeeping", type=Path, help="Append-only JSONL state file; defaults below output."
    )
    arguments = parser.parse_args()
    library = arguments.library.resolve()
    blender = arguments.blender.resolve()
    output = arguments.output.resolve()
    if not blender.is_file() or not (library / "parts").is_dir() or not (library / "p").is_dir():
        raise SystemExit("Blender executable or LDraw library is invalid.")
    parts = library_parts(library) if arguments.all else parts_from_file(arguments.parts.resolve())
    unknown = [part for part in parts if not (library / "parts" / part).is_file()]
    if unknown:
        raise SystemExit(f"Unknown LDraw parts: {', '.join(unknown[:5])}")
    state_path = arguments.bookkeeping or output / "render_bookkeeping.jsonl"
    missing = [
        part
        for part in parts
        if not is_completed_render(output / Path(part).stem, arguments.view_set)
    ]
    if arguments.limit is not None:
        missing = missing[: arguments.limit]
    append_event(
        state_path,
        {
            "at": timestamp(),
            "event": "run_started",
            "view_set": arguments.view_set,
            "requested": len(parts),
            "missing": len(missing),
        },
    )
    repository_root = Path(__file__).resolve().parents[1]
    for position, part in enumerate(missing, start=1):
        free_gib = shutil.disk_usage(output.parent).free / 1024**3
        if free_gib < arguments.minimum_free_gib:
            append_event(
                state_path, {"at": timestamp(), "event": "stopped_low_disk", "free_gib": free_gib}
            )
            raise SystemExit(f"Stopped: only {free_gib:.1f} GiB free space remains.")
        destination = output / Path(part).stem
        command = [
            str(blender),
            "--background",
            "--factory-startup",
            "--python",
            str(repository_root / "scripts" / "render_part.py"),
            "--",
            "--library",
            str(library),
            "--part",
            part,
            "--output",
            str(destination),
            "--view-set",
            arguments.view_set,
        ]
        append_event(state_path, {"at": timestamp(), "event": "part_started", "part": part})
        print(f"[{position}/{len(missing)}] Rendering {part}", flush=True)
        result = subprocess.run(command, check=False)
        event = (
            "part_completed"
            if result.returncode == 0 and is_completed_render(destination, arguments.view_set)
            else "part_failed"
        )
        append_event(
            state_path,
            {"at": timestamp(), "event": event, "part": part, "returncode": result.returncode},
        )
    append_event(
        state_path, {"at": timestamp(), "event": "run_completed", "processed": len(missing)}
    )


if __name__ == "__main__":
    main()
