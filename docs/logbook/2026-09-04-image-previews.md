# Logbook - 2026-09-04 Bildvorschauen

- **Aufgabe:** Die vorgeschlagenen Teilenummern in der Fotobox schneller und
  sicherer mit dem echten Stein vergleichbar machen.
- **Architekt:** Die Vorschau stammt ausschliesslich aus dem bestehenden
  Renderindex und beeinflusst weder Ranking noch gespeicherte Labels. Fehlt
  eine lokale Renderdatei, bleibt der Textvorschlag funktional.
- **Developer:** Jeder Vorschlagsbutton zeigt eine kompakte, stabile
  Renderansicht der zugehoerigen Teil-ID; die Bildreferenzen werden nach jeder
  neuen Suche sauber ersetzt.
- **UX:** Teilenummer, Aehnlichkeitswert und Bild sind gemeinsam auswaehlbar.
  Die ausdrueckliche menschliche Bestaetigung vor dem Speichern bleibt erhalten.
- **Tester:** Auswahl der stabilen Vorschauansicht automatisiert getestet.
  `ruff format --check`, `ruff check`, `mypy src` und `pytest` (24 Tests)
  erfolgreich ausgefuehrt.
