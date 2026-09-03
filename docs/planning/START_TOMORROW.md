# Startplan für den ersten Projekttag

## Tagesziel

Bis zum Ende des ersten Arbeitstags existiert ein nachvollziehbarer,
reproduzierbarer LDraw-Import für eine bewusst kleine PoC-Auswahl. Es wird noch
kein Modell trainiert und keine WebUI gebaut.

## Reihenfolge

1. **Architekt (30–45 min):** LDraw-Quelle, konkrete Version und Lizenz
   festlegen; Entscheidung als ADR dokumentieren. Datenablage außerhalb von Git
   festlegen.
2. **Developer (60–90 min):** Domänenpakete `catalog`, `rendering`, `vision`,
   `search` und `evaluation` als getrennte Grenzen anlegen; Settings und
   strukturiertes Logging ergänzen.
3. **Developer (90–120 min):** importer für eine kleine, dokumentierte
   Teil-Auswahl implementieren; Katalog in SQLite erzeugen.
4. **Tester (30 min):** Parser-Tests mit kleinen LDraw-Fixtures hinzufügen;
   Import wiederholt ausführen und Ergebnis vergleichen.
5. **UX-Experte (30 min):** Scan-Flow und Fehlerzustände als Akzeptanzkriterien
   für BV-012/BV-013 festhalten. Kein High-Fidelity-Design nötig.
6. **Alle Rollen (15 min):** Erkenntnisse, Prüfungen, Risiken und den nächsten
   kleinsten Schritt im Monats-Logbook erfassen.

## Definition of Done für morgen

- LDraw-Quelle und Lizenz sind nachweisbar dokumentiert.
- Mindestens drei Part-Dateien werden deterministisch in einen Katalog
  importiert.
- Der Import hat Unit-Tests und alle Poetry-Qualitätschecks sind grün.
- Rohdaten, Renderings, Modelle und Datenbanken sind von Git ausgeschlossen.
- Ein Logbook-Eintrag enthält Ergebnisse und offene Fragen.

## Vor dem Start bereitzuhalten

- Eine lokale LDraw-Library oder die Entscheidung, welche offizielle Quelle
  heruntergeladen werden soll.
- Drei bis zehn physische Beispielteile mit bekannter Design-ID für den späteren
  Kamera-Test.
- Information, ob eine NVIDIA-GPU für spätere Renders/Embeddings verfügbar ist.

Diese Punkte blockieren die Paket- und Importgrundlage nicht; sie verhindern
aber spätere Annahmen über Lizenz, Daten oder Hardware.
