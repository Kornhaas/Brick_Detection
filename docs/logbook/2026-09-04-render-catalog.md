# Logbook - Inkrementeller LDraw-Katalogrender

- **Aufgabe:** Alle LDraw-Teile ohne Wiederholungen im Hintergrund rendern.
- **Architekt:** ADR-014 trennt den platzsparenden Vollkatalog (`single`) von
  gezielten `poc-60`-Erkennungsansichten.
- **Developer:** Resumierbarer Batch und append-only JSONL-Bookkeeping erstellt.
- **UX:** Status ist mit `scripts/render_status.py` jederzeit ohne Logsuche
  nachvollziehbar.
- **Tester:** Ein echter Render von `3001.dat` erfolgreich; Metadaten und Bild
  als vollständig erkannt. 28 Tests erfolgreich.
- **Risiko:** Ein einzelner Prozess benötigt grob zwei Tage; er setzt nach
  Unterbrechung nur fehlende Teile fort.
