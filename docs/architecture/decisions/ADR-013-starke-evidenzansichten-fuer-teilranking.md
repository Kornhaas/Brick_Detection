# ADR-013: Starke Evidenzansichten fuer das Teilranking

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, Developer, Tester

## Entscheidung

Der Teilscore wird aus den drei staerksten passenden Referenzansichten
gemittelt, nicht aus allen Ansichten eines Teils innerhalb der globalen
Trefferliste. Die Anzahl aller passenden Ansichten bleibt als Diagnosesignal
erhalten.

## Konsequenzen

- Viele schwache Ansichten eines ansonsten passenden Teils druecken den
  Kandidatenwert nicht mehr kuenstlich.
- Der Score bleibt eine Aehnlichkeit, keine kalibrierte Wahrscheinlichkeit.
- Vergleichsmessungen werden nach dieser Aenderung erneut dokumentiert.
