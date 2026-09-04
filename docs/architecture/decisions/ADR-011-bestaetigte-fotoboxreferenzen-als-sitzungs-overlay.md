# ADR-011: Bestaetigte Fotoboxreferenzen als Sitzungs-Overlay

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, Developer, UX-Experte, Tester

## Kontext

Ein manuell bestaetigtes Kamerabild war bisher nur dauerhaft gespeichert. Die
laufende Suche nutzte weiterhin ausschliesslich synthetische Renderbilder und
konnte den soeben bestaetigten Stein daher erneut falsch einordnen.

## Entscheidung

Die Capture-App legt jedes explizit bestaetigte Bild als zusaetzlichen,
in-memory Suchvektor ueber den unveraenderten Renderindex. Beim Start derselben
Sitzung werden vorhandene Manifestbilder erneut geladen. Die Labels bleiben
ausschliesslich menschlich bestaetigt; automatische Vorschlaege werden nie als
Referenz uebernommen.

## Konsequenzen

- Ein gespeicherter Stein wird in derselben Sitzung sofort als echte Referenz
  beruecksichtigt.
- Ein Neustart mit demselben `--output` setzt die Sitzung fort.
- Der versionierte synthetische Index bleibt reproduzierbar; ein spaeterer,
  expliziter Trainings-/Indexbauprozess kann die echten Referenzen dauerhaft
  zusammenfuehren.
