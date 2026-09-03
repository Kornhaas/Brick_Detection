# ADR-001: Update-Funktion in einer WebUI

- Status: Akzeptiert
- Datum: 2026-09-03
- Verantwortliche Rollen: Architekt, UX-Experte, Tester

## Kontext

Falls Brick Detection eine WebUI erhält, müssen Betreibende nicht auf einen
externen Konsolenzugang angewiesen sein, um die Anwendung aktuell zu halten.
Gleichzeitig darf eine Update-Funktion weder unbefugt nutzbar sein noch den
laufenden Dienst unbemerkt beschädigen.

## Entscheidung

Jede WebUI enthält im administrativen Bereich eine Update-Funktion. Sie zeigt
die installierte Version, den geprüften verfügbaren Release und einen klaren
Update-Status. Die Ausführung ist nur für authentifizierte, autorisierte
Administratoren möglich und verlangt eine ausdrückliche Bestätigung.

Der Updateprozess lädt ausschließlich ein versioniertes Artefakt aus einer
konfigurierten, vertrauenswürdigen Quelle. Vor der Aktivierung werden Version,
Integrität und Kompatibilität geprüft. Bei Fehlern bleibt die bekannte letzte
funktionierende Version aktiv oder es wird auf sie zurückgerollt. Jeder Versuch
und sein Ergebnis werden ohne Geheimnisse protokolliert.

## Akzeptanzkriterien

- Nicht angemeldete oder nicht autorisierte Nutzende können weder prüfen noch
  installieren.
- Die UI zeigt Version, Quelle, Fortschritt, Erfolg oder einen verständlichen
  Fehlerzustand.
- Vor der Installation ist eine Bestätigung erforderlich.
- Ein fehlgeschlagenes Update beeinträchtigt den laufenden Dienst nicht und ist
  im Logbook bzw. Betriebslog nachvollziehbar.
- Tests decken Berechtigung, erfolgreiche Installation, Integritätsfehler,
  Netzwerkfehler und Rollback ab.

## Konsequenzen

Die konkrete Release-Quelle und das Deploymentverfahren werden mit Einführung
der WebUI in einer weiteren ADR entschieden. Die Funktion wird nicht als
beliebiger Shell-Befehl aus dem Browser implementiert.
