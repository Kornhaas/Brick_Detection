# ADR-012: Stabile Fotoboxflaeche triggert die Erkennung

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, Developer, UX-Experte, Tester

## Entscheidung

Die Capture-App vergleicht regelmaessig verkleinerte, geglaettete Kamerabilder.
Eine deutliche Aenderung setzt die Flaeche auf "in Bewegung". Erst nach drei
aufeinanderfolgenden stabilen Proben startet genau eine Erkennung. Eine beim
Start erfasste leere Ausgangsflaeche meldet das Herausnehmen eines Steins als
"kein Teil erkannt" statt als zufaelligen Modellvorschlag.

## Konsequenzen

- Keine fixe Wartezeit; die Ausloesung erfolgt beim Stillstand.
- Beim Start mit bereits eingelegtem Stein bleibt die manuelle Erkennung als
  sicherer Fallback verfuegbar.
