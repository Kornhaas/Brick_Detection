# ADR-008: Menschlich bestätigte reale Referenzbilder

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, UX-Experte, Tester

## Kontext

Der Renderindex liefert für echte Fotoboxbilder oft passende Kandidaten, aber
noch keine zuverlässige automatische Top-1-Entscheidung. Gleichzeitig sind
echte, gelabelte Fotoboxbilder der schnellste Weg, die Sim-to-Real-Lücke zu
schließen.

## Entscheidung

Die Capture-App erhält mit `--index` einen assistierten Referenzmodus. Sie
berechnet eine Vordergrund-zugeschnittene Anfrage, zeigt Kandidaten samt
**Similarity** und speichert ein Bild nur, wenn eine Bedienperson einen
Kandidaten bestätigt oder eine bekannte ID manuell einträgt. Similarity wird
nicht als Wahrscheinlichkeit bezeichnet.

Ohne explizites `--output` speichert dieser Modus in einem getrennten,
zeitgestempelten Ordner unter `data/references/real/`. Validierungs- und
Holdout-Bilder dürfen niemals automatisch in diesen Referenzsatz einfließen.

## Konsequenzen

- Der Renderindex bleibt Vorschlagsquelle, nicht Labelautorität.
- Der anfängliche Filter von 50 % Similarity ist eine Bedienhilfe und wird erst
  nach ausreichenden Bestätigungen anhand gemessener Fehlerraten kalibriert.
- Jeder bestätigte Satz kann später als echte Stützdatenbank oder für einen
  getrennt validierten Klassifikator dienen.
