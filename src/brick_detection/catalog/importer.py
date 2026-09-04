"""Persist parsed LDraw part metadata in a small SQLite catalogue."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from pathlib import Path

from brick_detection.catalog.parser import PartRecord, parse_part_file


def create_schema(connection: sqlite3.Connection) -> None:
    """Create the deliberately small first catalogue schema."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS parts (
            part_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT,
            keywords_json TEXT NOT NULL,
            source_path TEXT NOT NULL UNIQUE
        )
        """
    )


def import_parts(
    library_root: Path, part_filenames: Iterable[str], database_path: Path
) -> list[PartRecord]:
    """Import listed LDraw files and return the records persisted to SQLite."""
    records = [
        parse_part_file(library_root / "parts" / filename, library_root)
        for filename in part_filenames
    ]
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        create_schema(connection)
        connection.executemany(
            """
            INSERT INTO parts (part_id, title, category, keywords_json, source_path)
            VALUES (:part_id, :title, :category, :keywords_json, :source_path)
            ON CONFLICT(part_id) DO UPDATE SET
                title = excluded.title,
                category = excluded.category,
                keywords_json = excluded.keywords_json,
                source_path = excluded.source_path
            """,
            [
                {
                    "part_id": record.part_id,
                    "title": record.title,
                    "category": record.category,
                    "keywords_json": json.dumps(record.keywords),
                    "source_path": record.source_path,
                }
                for record in records
            ],
        )
    return records
