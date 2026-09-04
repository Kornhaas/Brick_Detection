"""Read stable metadata from the header of an LDraw part file."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PartRecord:
    """The catalogue metadata needed by the first retrieval PoC."""

    part_id: str
    title: str
    category: str | None
    keywords: tuple[str, ...]
    source_path: str


def parse_part_file(path: Path, library_root: Path) -> PartRecord:
    """Parse title and recognised metadata commands from an LDraw part file."""
    relative_path = path.resolve().relative_to(library_root.resolve()).as_posix()
    title: str | None = None
    category: str | None = None
    keywords: list[str] = []

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("0 Name:"):
            continue
        if line.startswith("0 !CATEGORY "):
            category = line.removeprefix("0 !CATEGORY ").strip() or None
        elif line.startswith("0 !KEYWORDS "):
            keywords.extend(
                keyword.strip()
                for keyword in line.removeprefix("0 !KEYWORDS ").split(",")
                if keyword.strip()
            )
        elif title is None and line.startswith("0 ") and not line.startswith("0 !"):
            title = line.removeprefix("0 ").strip()

    if title is None:
        raise ValueError(f"Missing title in LDraw part: {path}")
    return PartRecord(
        part_id=path.stem,
        title=title,
        category=category,
        keywords=tuple(keywords),
        source_path=relative_path,
    )
