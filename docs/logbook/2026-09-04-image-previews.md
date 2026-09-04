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

## Nachsteuerung: Erkennbare Katalogansichten

- **Aufgabe:** Die erste Umsetzung war zu klein und nutzte teilweise unguenstige
  Retrieval-Perspektiven; die direkte Nutzerrueckmeldung wird umgesetzt.
- **Architekt:** ADR-010 trennt Katalogdarstellung verbindlich vom Ranking.
- **Developer:** Bevorzugte 45-Grad-Dreiviertelansicht, lokaler Zuschnitt auf
  das Teil und eine Vorschaugroesse von bis zu 180 Pixeln umgesetzt.
- **UX:** Jede Bildkarte bleibt gemeinsam mit ID und Aehnlichkeitswert klickbar;
  die Teilform statt der leeren Renderflaeche steht im Vordergrund.
- **Tester:** Der reale Render `3002/upper_030_45.png` wird von 512 auf einen
  193-Pixel-Teilausschnitt reduziert. Alle lokalen Qualitaetschecks erfolgreich.

## Echtbild nach manueller Bestaetigung sofort verwenden

- **Aufgabe:** Ein korrekt manuell gespeicherter Stein muss bei der naechsten
  Suche derselben Aufnahme-Sitzung beruecksichtigt werden.
- **Architekt:** ADR-011 definiert einen in-memory Overlay ueber dem
  unveraenderten, reproduzierbaren Renderindex.
- **Developer:** Manifestbilder werden beim Sitzungsstart geladen; jedes neue
  bestaetigte Bild wird direkt als Kamera-Embedding hinzugefuegt.
- **UX:** Manuelles Speichern meldet sichtbar, dass die echte Referenz aktiv
  ist; nur ausdruecklich bestaetigte Labels beeinflussen Vorschlaege.
- **Tester:** Persistenz des Manifests und die Suche nach einer hinzugefuegten
  Referenz automatisiert getestet.

## Aktivitaetslog der Fotobox

- **Aufgabe:** Bedienpersonen sollen sehen, ob die Kamera, die Erkennung oder
  das Speichern gerade arbeitet, statt auf eine scheinbar eingefrorene UI zu
  warten.
- **Developer:** Ein kompaktes, zeitgestempeltes Fensterlog ergaenzt die
  Statuszeile fuer die relevanten Arbeitsschritte.
- **UX:** Das Log nennt klar die gestartete Operation, Trefferzahl und den
  notwendigen menschlichen Bestaetigungsschritt; Bild-Frames erzeugen keinen
  unlesbaren Protokollstrom.
- **Tester:** GUI-Import und die regulaeren Qualitaetschecks werden vor dem
  Push ausgefuehrt.

## Automatische Erkennung nach stabilem Flaechenwechsel

- **Aufgabe:** Einlegen und Herausnehmen eines Steins sollen ohne fixe
  Wartezeit automatisch analysiert werden.
- **Architekt:** ADR-012 trennt erkannte Bewegung von stabiler Flaeche und nutzt
  die anfaengliche Leerflaeche fuer eine explizite "kein Teil erkannt"-Meldung.
- **Developer:** Entprellte Bildsignaturen, eine stabile Dreiproben-Regel und
  das Zuruecksetzen veralteter Vorschlaege umgesetzt.
- **UX:** Das Log sagt erst "Aenderung erkannt", dann "Flaeche stabil" und bei
  leerer Flaeche klar "Kein Teil erkannt".
- **Tester:** Rausch- und Aenderungsentscheidung automatisiert getestet;
  vollstaendiger Qualitaetslauf folgt vor dem Push.

## Wartung: Optionale DINOv2-xFormers-Warnung

- **Architekt:** xFormers bleibt keine Projektabhaengigkeit, weil die Fotobox
  einzelne Bilder verarbeitet und die optionale Beschleunigung nicht benoetigt.
- **Developer:** Die bekannte, harmlose Drittanbieterwarnung wird nur waehrend
  des DINOv2-Ladens gezielt ausgeblendet; andere Warnungen bleiben sichtbar.
- **UX:** Die lokale Konsole zeigt keine irrefuehrende Fehlermeldung mehr.
- **Tester:** Der reguläre Test- und Qualitaetslauf wird vor dem Push ausgefuehrt.
