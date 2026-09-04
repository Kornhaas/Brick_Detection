# ADR-004: LDraw-Snapshot nur als lokaler PoC-Datensatz

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, Tester

## Kontext

Ein lokaler LDraw-Ordner ist vorhanden und ermöglicht bereits Render- und
Katalogspikes. Seine ursprüngliche Download-URL und Archiv-Prüfsumme wurden
jedoch nicht erfasst. Die Part-Dateien weisen unterschiedliche
CC-BY-Lizenzhinweise auf.

## Entscheidung

Der vorhandene Ordner darf für den lokalen, nicht veröffentlichten PoC verwendet
werden. Erweiterte oder veröffentlichte Datensätze werden ausschließlich aus
einem ausdrücklich dokumentierten offiziellen LDraw-Release erzeugt. Archivhash,
Release-Kennung, Attribution und importierte Partanzahl sind dann Pflicht.

## Konsequenzen

- Die existierenden 10 PoC-Parts bleiben ein technischer Render- und
  Katalognachweis, kein veröffentlichbarer Trainingsdatensatz.
- `docs/data-sources/LDRAW.md` ist die zentrale Nachweisdokumentation.
- Der Katalog speichert die Quelldatei pro Part; er speichert keine ungesicherte
  globale Lizenzbehauptung.
