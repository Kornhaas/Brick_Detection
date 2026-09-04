# ADR-010: Katalogvorschau getrennt von Retrieval-Ansichten

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, Developer, UX-Experte, Tester

## Kontext

Die dichten Renderansichten des Retrieval-Index sind fuer die Bildaehnlichkeit
ausgelegt. Eine beliebige, weit ausgeschnittene Unterseitenansicht hilft
Menschen jedoch nicht verlässlich bei der Teilebestaetigung.

## Entscheidung

Die Auswahloberflaeche nutzt pro Teil eine bevorzugte, einheitliche
Dreiviertelansicht (`upper_030_45`, dann `orbit_045_45`). Sie beschneidet die
neutrale Renderflaeche lokal auf das Teil und zeigt die Vorschau gross an.
Ranking und Embedding-Index bleiben unveraendert.

## Konsequenzen

- Die dargestellte Perspektive ist nachvollziehbar und fuer Menschen
  vergleichbar.
- Eine fehlende bevorzugte Ansicht faellt sicher auf eine vorhandene Ansicht
  zurueck.
- Die spaetere Produktansicht kann durch speziell gerenderte Katalogbilder
  ersetzt werden, ohne das Erkennungsmodell zu aendern.
