# Brick Detection

BrickVision ist ein lokales System zur Erkennung von LEGO-Teilen. Die technische
Umsetzung folgt den Vereinbarungen in [AGENTS.md](AGENTS.md).

Der abgestimmte Projektauftrag und der Startplan stehen in
[docs/planning](docs/planning/PROJECT_BRIEF.md). Wir beginnen mit einem kleinen,
messbaren Embedding-PoC – nicht mit Modelltraining oder einer großen WebUI.

## Schnellstart

```powershell
poetry install --with dev
poetry run pytest
```

Poetry verwaltet die virtuelle Umgebung und die reproduzierbaren Abhängigkeiten
über `poetry.lock`. Neue oder aktualisierte Abhängigkeiten werden ausschließlich
mit `poetry add` beziehungsweise `poetry update` vorgenommen und zusammen mit
der Lockdatei eingecheckt.

## Erkennungs-PoC

Die GPU- und Modellabhängigkeiten sind bewusst optional, damit die reguläre
Qualitätspipeline schlank bleibt. Für Indexaufbau, Bildsuche oder die reale
Evaluation einmalig installieren:

```powershell
poetry install --with dev,ml
poetry run python scripts/build_embedding_index.py --renders data/renders/poc --output data/indexes/poc-v1.npz
poetry run python scripts/recognize_image.py --index data/indexes/poc-v1.npz --image <bilddatei>
```

Die aktuelle synthetische Messung und das Protokoll für die noch ausstehende
Kameravalidierung stehen in [BASELINE_RESULTS.md](docs/planning/BASELINE_RESULTS.md)
und [REAL_VALIDATION_CAPTURE.md](docs/planning/REAL_VALIDATION_CAPTURE.md).

## Qualität und Zusammenarbeit

- Rollen, Arbeitsablauf und Qualitätsregeln: [AGENTS.md](AGENTS.md)
- Architekturentscheidungen: `docs/architecture/decisions/`
- Arbeitsnachweise: `docs/logbook/`
- GitHub überprüft bei Pull Requests Formatierung, Linting, Typen, Tests und
  bekannte Python-Abhängigkeitsschwachstellen.
- Eine spätere WebUI enthält eine sichere Update-Funktion gemäß
  [ADR-001](docs/architecture/decisions/ADR-001-webui-update-funktion.md).

Jede abgeschlossene Arbeit ergänzt das monatliche Logbook nach dessen Vorlage.
