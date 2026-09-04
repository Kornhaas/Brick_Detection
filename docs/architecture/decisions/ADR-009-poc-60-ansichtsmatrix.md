# ADR-009: 60 gezielte Renderansichten für die Fotobox-Baseline

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, Developer, Tester

## Kontext

Der bisherige `poc-28`-Index enthält nur eine fast senkrechte Ansicht. In der
Fotobox kann ein Teil jedoch beliebig um die optische Achse gedreht liegen.

## Entscheidung

`poc-60` erzeugt einen separaten Vergleichsindex: zwölf Drehwinkel in
30°-Schritten bei vier oberen Höhen (20°, 45°, 70°, 85°), ergänzt um sechs
Unterseiten- und sechs Seitenansichten. Das erhöht besonders die top-nahe
Rotationsabdeckung.

## Konsequenzen

- 600 statt 280 Renderbilder für die zehn PoC-Teile.
- Der alte Index bleibt für reproduzierbare Vergleiche erhalten.
- Mehr Ansichten ohne Kamera-/Lichtvariation lösen den Sim-to-Real-Gap nicht;
  echte bestätigte Referenzbilder bleiben der priorisierte nächste Datenpfad.
