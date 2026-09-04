import json
import sqlite3
from pathlib import Path

from brick_detection.catalog import import_parts, parse_part_file


def write_part(library: Path, filename: str, body: str) -> Path:
    part_path = library / "parts" / filename
    part_path.parent.mkdir(parents=True)
    part_path.write_text(body, encoding="utf-8")
    return part_path


def test_parser_extracts_title_category_keywords_and_relative_path(tmp_path: Path) -> None:
    library = tmp_path / "ldraw"
    part = write_part(
        library,
        "3001.dat",
        """0 Brick 2 x 4
0 Name: 3001.dat
0 !CATEGORY Brick
0 !KEYWORDS basic, rectangular
0 BFC CERTIFY CCW
""",
    )

    record = parse_part_file(part, library)

    assert record.part_id == "3001"
    assert record.title == "Brick 2 x 4"
    assert record.category == "Brick"
    assert record.keywords == ("basic", "rectangular")
    assert record.source_path == "parts/3001.dat"


def test_importer_persists_and_updates_catalogue_records(tmp_path: Path) -> None:
    library = tmp_path / "ldraw"
    write_part(library, "3001.dat", "0 Brick 2 x 4\n0 !KEYWORDS basic\n")
    database = tmp_path / "catalog.sqlite3"

    import_parts(library, ["3001.dat"], database)
    import_parts(library, ["3001.dat"], database)

    with sqlite3.connect(database) as connection:
        row = connection.execute(
            "SELECT part_id, title, category, keywords_json, source_path FROM parts"
        ).fetchone()
    assert row == ("3001", "Brick 2 x 4", None, json.dumps(["basic"]), "parts/3001.dat")
