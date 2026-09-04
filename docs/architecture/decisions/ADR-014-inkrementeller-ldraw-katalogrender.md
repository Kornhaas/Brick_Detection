# ADR-014: Inkrementeller LDraw-Katalogrender

- Status: Akzeptiert
- Datum: 2026-09-04

Der Vollkatalog nutzt pro Teil zunächst eine einzelne Dreiviertelansicht.
`poc-60` wird wegen des geschätzten Platzbedarfs von 218 GiB nur gezielt für
relevante Teile gerendert. Ein JSONL-Bookkeeping prüft Metadaten und erwartete
Dateien, sodass Unterbrechungen nur fehlende oder unvollständige Teile fortsetzen.
