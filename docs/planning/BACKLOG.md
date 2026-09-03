# Produkt-Backlog

Priorität bedeutet Reihenfolge, nicht parallele Umsetzung. Jeder Eintrag wird
vor Beginn als GitHub Issue angelegt, erhält Akzeptanzkriterien und nach Abschluss
einen Verweis ins Logbook.

## Jetzt: PoC (P0)

- [ ] **BV-001 – Domänen- und Konfigurationsgrundlage:** Verzeichnisgrenzen,
  Settings, strukturiertes Logging und lokale Datenpfade anlegen.
- [ ] **BV-002 – LDraw-Quelle und Lizenz prüfen:** konkrete Library-Version,
  Lizenz/Attribution und Importpfad dokumentieren.
- [ ] **BV-003 – Part-Katalog importieren:** Part-ID, Name, Kategorie und
  Quelldatei für 100 PoC-Teile in SQLite erfassen.
- [ ] **BV-004 – Render-Vertrag definieren:** 28 feste Perspektiven,
  Kamera-, Licht- und Hintergrundprofil als versionierte Konfiguration.
- [ ] **BV-005 – Headless-Render-Spike:** einen Teil reproduzierbar rendern;
  anschließend alle 100 Teile rendern und Metadaten speichern.
- [ ] **BV-006 – Embedding-Spike:** lizenzierten vortrainierten Encoder laden,
  Renders einbetten und Modellversion speichern.
- [ ] **BV-007 – Suche und Aggregation:** FAISS-Index aufbauen, Top-50 Renders
  nach Part-ID aggregieren und Top-5 Parts ausgeben.
- [ ] **BV-008 – Echtes Testset:** mindestens 20 reale Fotos mit Ground Truth,
  ohne Überlappung zum Trainings-/Referenzmaterial.
- [ ] **BV-009 – Benchmark und Go/No-Go:** Top-1/3/5 sowie MRR berechnen,
  Fehlermatrix erstellen und Entscheidung als ADR festhalten.

## Danach: Baseline und WebUI (P1)

- [ ] **BV-010 – Katalog auf häufige Teile erweitern.**
- [ ] **BV-011 – FastAPI-Vertrag:** `/recognize`, `/parts/{id}`, `/feedback`,
  `/health` und `/model/info` als versionierte API.
- [ ] **BV-012 – Scan-WebUI:** Kameraaufnahme und Bild-Upload, Ergebnis mit
  verständlicher Sicherheitsstufe statt Scheingenauigkeit.
- [ ] **BV-013 – Kandidatenauswahl und Feedback:** Top-5 mit Referenzbildern;
  korrekt/falsch/Alternativteil speichern.
- [ ] **BV-014 – Historie und Datenschutz:** lokale Speicherung, Löschkonzept
  und Export der Feedbackdaten.
- [ ] **BV-015 – Update-Ansicht:** gemäß ADR-001 als Administratorfunktion.

## Später: Qualität und Betrieb (P2)

- [ ] Multi-View-Erkennung und Konsens-Ranking.
- [ ] Active-Learning-Export mit Dataset-Versionierung.
- [ ] Fine-Tuning mit Hard Negatives und getrenntem Benchmark.
- [ ] Geometrisches Re-Ranking aus LDraw-Eigenschaften.
- [ ] Containerisierung, CPU/GPU-Erkennung, Backup und Betriebsmetriken.
