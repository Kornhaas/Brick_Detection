# UX-Anforderungen für BrickVision

## Primäre Aufgabe

Eine Person fotografiert ein einzelnes Teil, bestätigt den vorgeschlagenen Part
oder wählt einen passenden Kandidaten. Die Bedienung optimiert schnelles,
fehlerarmes Sortieren – nicht die Darstellung einer unkalibrierten Dezimalzahl.

## Akzeptanzkriterien für die erste WebUI

- Aufnahme per Kamera und Bild-Upload funktionieren auf Desktop und Mobilgerät.
- Das Ergebnis zeigt Part-ID, Name und ein Referenzbild.
- Die besten fünf Kandidaten sind bei Unsicherheit direkt vergleichbar.
- Sicherheit wird als **sehr sicher**, **sicher** oder **unsicher** dargestellt;
  die numerische Bewertung bleibt für Diagnosezwecke verfügbar.
- „Richtig“ und „Anderes Teil auswählen“ sind ohne Scrollen erreichbar.
- Fehler erklären den nächsten Schritt (z. B. „Teil einzeln vor neutralem
  Hintergrund fotografieren“), statt nur einen technischen Fehlercode zu zeigen.
- Feedback wird erst gespeichert, nachdem die Person ihre Wahl bestätigt hat.

## Sicherheitskritische Interaktion

Automatisches Sortieren ist erst zulässig, wenn ein später festgelegter,
kalibrierter Schwellenwert, ausreichender Abstand zum zweiten Kandidaten und
übereinstimmende Mehrfachansichten vorliegen. Andernfalls verlangt das System
eine menschliche Auswahl.
