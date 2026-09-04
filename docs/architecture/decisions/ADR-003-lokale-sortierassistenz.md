# ADR-003: Lokale Sortierassistenz als langfristiges Ziel

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, UX-Experte

## Kontext

Ein bestehender Brick Manager verwaltet bereits den privaten Teilebestand. Das
langfristige Ziel ist eine stationäre Kamera-Box: Teil erkennen, passenden
Lagerplatz auf einem kleinen Bildschirm anzeigen und den Sortiervorgang
unterstützen. Die unmittelbare Arbeit gilt weiterhin dem Erkennungs-PoC.

## Entscheidung

BrickVision wird als lokal betreibbare Recognition Engine mit einer späteren,
entkoppelten Lagerplatzintegration geplant. Die Engine kennt Part-IDs und
Kandidaten; ein Brick-Manager-Adapter löst eine bestätigte Part-ID später in
einen Lagerplatz auf. Kamera, Auslöser und Display werden als Clients der API
behandelt, nicht als Voraussetzung der Engine.

## Konsequenzen

- Die jetzige PoC-Schnittstelle darf keine Annahmen über Brick-Manager-Tabellen
  oder Kamera-Hardware enthalten.
- Eine spätere Integration benötigt eine separate ADR mit API-Vertrag,
  Authentifizierung, Fehlerszenarien und Schreibrechten.
- Raspberry Pi und PC-Server bleiben gleichwertige Deploymentoptionen, bis
  Messwerte für Inferenzzeit und Hardware vorliegen.
