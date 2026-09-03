# BrickVision – Projektauftrag

## Ziel

BrickVision erkennt LEGO-Teile lokal und ohne Abhängigkeit von Brickognize oder
einer anderen externen Erkennungs-API. Zunächst steht die Identifikation eines
einzelnen, freigestellten Teils aus einem Bild im Vordergrund. Eine WebUI zeigt
die besten Kandidaten und sammelt bestätigendes oder korrigierendes Feedback.

## Leitprinzip

Wir validieren zuerst die zentrale Hypothese statt früh eine große Anwendung
oder ein eigenes Modell zu bauen:

> Liefert ein vortrainierter Bildencoder für Fotos realer Teile den korrekten
> LDraw-Part in den Top-5?

Der Proof of Concept (PoC) umfasst 100 ausgewählte Teile, 28 kontrollierte
Renders pro Teil und mindestens 20 reale, gelabelte Testfotos. Das Ergebnis
entscheidet über die nächste Ausbaustufe.

## Nicht-Ziele des PoC

- kein Training eines Modells von Grund auf;
- keine vollständige LDraw-Bibliothek und keine Million Renderings;
- keine Sortierhardware, Mobile App, Microservices oder Cloudzwang;
- keine automatische Sortierentscheidung.

## Erfolgskriterien

| Metrik | PoC-Ziel | Entscheidung |
| --- | ---: | --- |
| Top-5-Trefferquote | mindestens 85 % als Zielwert | Bei deutlich unter 50 % Encoder/Preprocessing prüfen, nicht sofort skalieren. |
| Nachvollziehbarkeit | 100 % | Jedes Testfoto hat Part-ID, Aufnahmebedingungen und Split. |
| Reproduzierbarkeit | 100 % | Render, Index und Messung sind per versionierten Befehl erzeugbar. |

Die Zielwerte sind Projektziele, keine vorab zugesicherten Modellwerte.

## Produktweg

1. **PoC:** LDraw-Import → kontrollierte Renders → Encoder-Embeddings →
   FAISS-Suche → echter Benchmark.
2. **Baseline ausbauen:** häufige Teile, robuste Vorverarbeitung und
   systematische Fehlermatrix.
3. **Interaktion:** WebUI mit Kamera/Upload, Top-5-Auswahl und Feedback.
4. **Verbesserung:** Multi-View, Active Learning, Fine-Tuning und geometrisches
   Re-Ranking.
5. **Betrieb:** Docker, Modell-/Dataset-Versionierung, Monitoring und sichere
   Update-Funktion.

## Grundannahmen und Risiken

- Sehr ähnliche Varianten, Prints, Transparenz und verdeckte Merkmale werden
  den PoC erschweren; der PoC wählt deshalb unterscheidbare Beispielteile.
- Synthetische Renders können von realen Kamerabildern abweichen. Das reale,
  strikt vom Training getrennte Testset ist daher Pflicht.
- LDraw-Dateien und Metadaten werden erst nach dokumentierter Lizenz- und
  Quellenprüfung importiert.
- Modellgewichte und deren Lizenz müssen vor Aufnahme in die Pipeline geprüft
  werden.
