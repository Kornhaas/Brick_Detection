# BrickVision – Nordstern

## Zielbild

BrickVision soll ein lokal betriebenes Assistenzsystem für die Sortierung von
LEGO-Teilen werden. Ein Teil wird in eine Kamera-Box gelegt. Nach einem
Tastendruck oder einer automatischen Auslösung erkennt das System das Teil,
zeigt es auf einem kleinen Bildschirm an und nennt dessen Lagerplatz.

```text
Kamera-Box → Teilidentifikation → Lagerplatzauflösung → Bildschirmhinweis
                                  ↑
                           Brick Manager
```

Das System soll später entweder auf einem lokalen PC als Server oder auf einem
Raspberry Pi laufen können. Die Erkennung und die Daten bleiben dabei lokal;
eine externe Recognition-API ist keine Voraussetzung.

## Produktphasen

| Phase | Ergebnis | Nicht enthalten |
| --- | --- | --- |
| 1. Identifikation | Foto → Top-5-Part-IDs mit nachvollziehbarer Sicherheit | Lagerplatz, Hardware, Brick-Manager-Zugriff |
| 2. Nutzerfluss | Kamera-/Upload-UI, Bestätigung oder Korrektur eines Kandidaten | Automatisches Einsortieren |
| 3. Lagerintegration | Part-ID → Lagerplatz über eine stabile Brick-Manager-Schnittstelle | Direkter Zugriff auf dessen Datenbank |
| 4. Kamera-Box | Feste Kamera, Beleuchtung, Auslöser und kleiner Bildschirm | Mechanische Sortierung |
| 5. Betrieb | Lokaler PC oder Raspberry Pi, Health-Checks, Updates und Backups | Cloudzwang |

## Designprinzipien

- **Erkennung vor Integration:** Erst ein gemessener, brauchbarer Retrieval-PoC;
  erst danach die Anbindung an den Brick Manager.
- **Schnittstellen statt Datenbankkopplung:** BrickVision fragt später eine
  dokumentierte API oder einen Adapter nach Lagerplätzen. Es schreibt nicht
  direkt in die Datenbank des Brick Managers.
- **Lokaler Betrieb:** Kamera, Erkennung, Lagerbestand und Anzeige funktionieren
  im lokalen Netzwerk beziehungsweise offline, soweit die Hardware es erlaubt.
- **Unsicherheit ist ein Ergebnis:** Bei unklaren Teilen zeigt das System
  Kandidaten und fordert Bestätigung, statt einen falschen Lagerplatz auszugeben.
- **Hardware-unabhängiger Kern:** Die Recognition Engine bleibt von Kamera,
  Bildschirm und Raspberry Pi getrennt testbar.

## Spätere offene Entscheidungen

- Welche API, Authentifizierung und Datenfelder der bestehende Brick Manager
  anbietet.
- Exakte Kamera, Beleuchtung, Trigger und Displaygröße der Box.
- Ob die Inferenz auf Raspberry Pi ausreichend schnell und präzise ist oder ein
  lokaler PC-Server verwendet wird.
- Format einer Lagerplatzantwort, etwa `box`, `fach`, `position` und Anzeige-
  text.
