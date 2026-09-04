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

### Aufnahmen mit der Fotobox

Die USB-Kamera-App benötigt die optionale Aufnahmegruppe und startet lokal mit:

```powershell
poetry install --with dev,capture
poetry run python scripts/capture_validation_images.py --camera 0
```

Für die verwendete InnoMaker U20-16MP-AF fordert die App standardmäßig MJPEG
mit `4656×3496` bei 15 fps an; die Live-Anzeige nennt die tatsächlich gelieferte
Auflösung. Für einen schnelleren Einrichtungscheck kann sie etwa mit
`--width 1920 --height 1080 --fps 30` gestartet werden.

Teil-ID eingeben, den Stein zentrieren und „Foto aufnehmen“ (oder Enter)
wählen. Bilder und `manifest.csv` bleiben unter `data/validation/` lokal und
werden nicht eingecheckt. Die erkannten Bilder können anschließend gemessen
werden:

```powershell
poetry install --with dev,ml,capture
poetry run python scripts/evaluate_real_images.py --index data/indexes/poc-v1.npz --manifest data/validation/manifest.csv
```

Bei Bildern aus der festen Fotobox kann der explizite, noch zu validierende
Vordergrund-Zuschnitt verwendet werden: `--foreground-crop`. Derselbe Schalter
steht bei `recognize_image.py` zur Verfügung. Details und Grenzen stehen in
[ADR-007](docs/architecture/decisions/ADR-007-fotobox-vordergrund-zuschnitt.md).

## Qualität und Zusammenarbeit

- Rollen, Arbeitsablauf und Qualitätsregeln: [AGENTS.md](AGENTS.md)
- Architekturentscheidungen: `docs/architecture/decisions/`
- Arbeitsnachweise: `docs/logbook/`
- GitHub überprüft bei Pull Requests Formatierung, Linting, Typen, Tests und
  bekannte Python-Abhängigkeitsschwachstellen.
- Eine spätere WebUI enthält eine sichere Update-Funktion gemäß
  [ADR-001](docs/architecture/decisions/ADR-001-webui-update-funktion.md).

Jede abgeschlossene Arbeit ergänzt das monatliche Logbook nach dessen Vorlage.
