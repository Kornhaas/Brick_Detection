# ADR-006: Lokale GUI für Validierungsaufnahmen

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, UX-Experte, Tester

## Kontext

Die Fotobox mit USB-Kamera soll reale, gelabelte Bilder für die Bewertung der
Erkennung erzeugen. Manuell verschobene Dateien und handgeschriebene CSV-Zeilen
sind fehleranfällig und gefährden die Trennung zwischen Evaluation und
Referenzdaten.

## Entscheidung

Eine kleine lokale Tkinter-Anwendung zeigt die Live-Vorschau einer gewählten
USB-Kamera. Ein Foto kann ausschließlich nach Eingabe einer sicheren, bekannten
LDraw-Teil-ID gespeichert werden. Das Bild landet in
`data/validation/images/`; die App ergänzt unmittelbar die zugehörige Zeile in
`data/validation/manifest.csv`. Beide Pfade bleiben durch `.gitignore` lokal.

Ohne explizites `--output` erzeugt jeder App-Start einen neuen, zeitgestempelten
Holdout-Ordner unter `data/validation/`. Ein vorhandener Satz wird nur mit
einem ausdrücklich angegebenen `--output` fortgesetzt.

OpenCV und Pillow liegen in der optionalen Poetry-Gruppe `capture`. Die App
hat weder Netzwerkzugriff noch Zugriff auf Brick Manager oder eine
Lagerzuordnung.

Für die InnoMaker U20-16MP-AF fragt die Anwendung MJPEG mit `4656×3496` bei
15 fps an. Die tatsächlich gelieferte Auflösung wird aus dem ersten Bild
ermittelt und sichtbar angezeigt, da UVC-Geräte die angeforderte Einstellung
ablehnen oder auf eine unterstützte Variante zurückfallen können.

## Konsequenzen

- Aufnahmen sind direkt mit `evaluate_real_images.py` auswertbar.
- Eine falsche ID kann technisch nicht erkannt werden; die Bedienperson muss
  das Teil vor dem Auslösen kennen und die Eingabe prüfen.
- Kameraindex, Licht und physische Positionierung bleiben konfigurierbare
  Betriebsparameter und werden mit der Messung festgehalten.
