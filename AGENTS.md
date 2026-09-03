# AI-Arbeitsvereinbarung

Dieses Repository wird von Menschen und AI-Agenten gemeinsam gepflegt. Jede
Änderung muss klein, nachvollziehbar und überprüfbar sein.

## Rollen

| Rolle | Verantwortung | Ergebnis vor der Umsetzung |
| --- | --- | --- |
| Architekt | Grenzen, Datenflüsse, Abhängigkeiten und technische Entscheidungen | Eintrag in `docs/architecture/decisions/` bei relevanten Entscheidungen |
| Developer | Implementierung, verständlicher Code, Tests und Dokumentation | Änderung mit passenden Tests |
| UX-Experte | Nutzeraufgaben, Verständlichkeit, Zugänglichkeit und Fehlermeldungen | UX-Notiz oder Akzeptanzkriterien im Logbook |
| Tester | Risiken, Testfälle, Regressionen und Abnahme | Testnachweis im Logbook und im Pull Request |

Eine Person oder ein Agent darf mehrere Rollen übernehmen, muss die jeweilige
Sicht aber explizit im Logbook berücksichtigen. Sicherheits- oder
Architekturentscheidungen werden nicht stillschweigend im Code versteckt.

## Verbindlicher Ablauf

1. Aufgabe und Akzeptanzkriterien verstehen.
2. Vor jeder fachlich oder technisch dauerhaften Entscheidung die Architektursicht
   prüfen; bei Folgen für Nutzende die UX-Sicht einbeziehen.
3. Implementieren, testen und die lokalen Qualitätschecks ausführen.
4. Einen Eintrag in `docs/logbook/` ergänzen. Ohne Logbook-Eintrag ist Arbeit
   nicht abgeschlossen.
5. Pull Request erstellen; die GitHub-Checks müssen erfolgreich sein.

## Code- und Qualitätsregeln

- Python-Code liegt in `src/`, Tests in `tests/`.
- Neue Logik hat mindestens einen passenden Test.
- Keine Geheimnisse, Zugangsdaten oder personenbezogenen Testdaten einchecken.
- Abhängigkeiten werden mit Poetry in `pyproject.toml` und `poetry.lock`
  gepflegt; keine direkte `pip install`-Änderung am Projektzustand.
- Vermeide große, unverbundene Änderungen in einem Pull Request.

## Nützliche Befehle

```powershell
poetry install --with dev
poetry run ruff format --check .
poetry run ruff check .
poetry run mypy src
poetry run pytest
```
