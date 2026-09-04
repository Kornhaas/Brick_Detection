"""Summarize append-only local render bookkeeping."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bookkeeping", type=Path, required=True)
    arguments = parser.parse_args()
    events = [
        json.loads(line) for line in arguments.bookkeeping.read_text(encoding="utf-8").splitlines()
    ]
    counts = Counter(event["event"] for event in events)
    print(json.dumps(dict(sorted(counts.items())), indent=2))


if __name__ == "__main__":
    main()
