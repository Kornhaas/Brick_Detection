# LDraw-Quelle und Lizenzstatus

## Aktuell verwendeter PoC-Snapshot

- Lokaler Pfad: `data/ldraw/` (von Git ausgeschlossen).
- Beobachtete Konfiguration: `LDConfig.ldr` nennt Update `2026-05-29`.
- Beobachtete Anzahl der Dateien direkt unter `parts/`: 24.735 `.dat`-Dateien.
- Referenzdatei: `parts/3001.dat`, SHA-256
  `70968CB5E4BAA92DC6A1939ACA7526B8566A17DBEA49DA9B91182AA864E412C4`.
- Die ursprüngliche Download-URL und Archiv-Prüfsumme des aktuell vorhandenen
  Ordners wurden nicht beim Herunterladen erfasst. Der Snapshot ist daher nur
  für den lokalen PoC zulässig, nicht als reproduzierbare Distributionsquelle.

## Verbindliche Quelle für weitere Datenstände

Vor einer Erweiterung über den lokalen PoC hinaus wird die vollständige Library
aus dem offiziellen LDraw.org-Library-Update bezogen, zusammen mit:

1. Release-Kennung und direkter Download-URL;
2. SHA-256 des heruntergeladenen Archivs;
3. Download-Datum;
4. Anzahl importierter Parts;
5. Lizenz- und Attributionsnachweis.

Die Library und ihre Renders verbleiben außerhalb von Git. Die offizielle
Bibliothek führt ihre Parts unter den Bedingungen der Contributor Agreement
Library; individuelle Part-Header enthalten die jeweilige Lizenzreferenz.
`CAreadme.txt` im lokalen Snapshot nennt CC BY 2.0 und/oder CC BY 4.0 und
verlangt Attribution. Vor Veröffentlichung prüfen wir jede verwendete Datei und
die zugehörigen Lizenzbedingungen erneut.

## Quellen

- https://library.ldraw.org/updates?latest=
- https://www.ldraw.org/article/218.html
- https://creativecommons.org/licenses/by/4.0/
