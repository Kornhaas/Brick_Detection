# ADR-007: Optionaler Vordergrund-Zuschnitt für die Fotobox

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, UX-Experte, Tester

## Kontext

Die U20-Fotobox erzeugt hochauflösende Bilder mit viel gleichförmiger Umgebung;
die LDraw-Referenzbilder zeigen dagegen das Teil formatfüllend. Die erste reale
Messung erreicht ohne Vorverarbeitung nur 61,7 % Top-5.

## Entscheidung

Die Recognition- und Evaluierungs-CLIs erhalten den expliziten Schalter
`--foreground-crop`. Er sucht im zentralen Einlegebereich die größte
Kantenkomponente und erzeugt daraus nur im Speicher einen quadratischen
Zuschnitt. Wenn der Kontrast nicht ausreicht, fällt die Verarbeitung auf den
festen zentralen Einlegebereich (40 % der kürzeren Bildseite) zurück. Die
Rohbilder und der Referenzindex bleiben unverändert.

Der Zuschnitt ist vorerst **nicht** Standard und wird in den Ergebnissen im
Protokoll kenntlich gemacht. Seine Auswahl wurde auf dem ersten echten Satz
untersucht; ein unabhängiger, frischer Satz ist vor einer Abnahme erforderlich.

## Konsequenzen

- Die Fotobox braucht nur einen zentralen, einzelnen Stein; mehrere Teile oder
  ein Stein am Bildrand sind explizite Fehlerfälle.
- Fehlt der Kontrast, bleibt ein reproduzierbarer Fallback verfügbar, aber die
  spätere UI muss dies als geringere Zuversicht anzeigen.
- OpenCV wird nur bei Nutzung des optionalen Capture-/Crop-Pfads benötigt.
