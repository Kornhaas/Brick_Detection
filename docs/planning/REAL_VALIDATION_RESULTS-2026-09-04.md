# Reale Validierung – 2026-09-04

## Datensatz und Protokoll

- 60 getrennte Kamerabilder aus der U20-16MP-AF-Fotobox, 4656×3496 Pixel.
- 9 der 10 PoC-Teil-IDs sind vertreten; `3010` fehlt im aktuellen Satz.
- Die Bilder wurden nicht in den Renderindex, in Embeddings des Index oder in
  Training übernommen.
- Encoder und Index: DINOv2 ViT-S/14, `dinov2_vits14@7764ea0f912e`.

## Ergebnis ohne kamerabildspezifische Vorverarbeitung

| Kennzahl | Ergebnis |
| --- | ---: |
| Top-1 | 16,7 % |
| Top-3 | 43,3 % |
| Top-5 | 61,7 % |
| MRR@10 | 0,356 |

Die synthetische Leave-one-render-out-Messung ist damit erwartungsgemäß nicht
auf die Fotobox übertragbar. Besonders die Teile `3001` und `3002` wurden in
diesem Satz nicht innerhalb der Top-5 gefunden. `3005` war mit 66,7 % Top-1
die stärkste Teil-ID.

## Befund

Die Fotos enthalten sehr viel einfarbige Umgebung, das Teil selbst ist klein.
Die LDraw-Referenzbilder dagegen zeigen ein formatfüllendes Teil. Ein reiner,
nicht persistierter zentraler Testausschnitt erhöhte auf demselben Satz Top-5
auf bis zu 81,7 %. Dieses Ergebnis ist nur ein Diagnosewert und darf nicht als
Abnahme gelten, weil der Ausschnitt anhand dieses Satzes untersucht wurde.

## Nächste Arbeit

1. Zuschneide-/Objekterkennung als explizite, getestete Vorverarbeitungsstufe
   implementieren; Originalbilder bleiben unverändert.
2. Einen frischen, zuvor nicht betrachteten Satz mit allen 10 Teilen erfassen.
3. Erst auf diesem unabhängigen Satz die Abnahmewerte für die Fotobox festlegen.

## Diagnose: optionaler Vordergrund-Zuschnitt

Die nun implementierte, explizit aktivierte Kanten-/Zentrums-Vorverarbeitung
ergab auf diesem selben Satz:

| Kennzahl | Rohbild | Vordergrund-Zuschnitt |
| --- | ---: | ---: |
| Top-1 | 16,7 % | 23,3 % |
| Top-3 | 43,3 % | 56,7 % |
| Top-5 | 61,7 % | 80,0 % |
| MRR@10 | 0,356 | 0,442 |

Das belegt den Bildausschnitt als wesentlichen Hebel, ist aber weiterhin ein
Diagnoseergebnis und keine Abnahme auf unabhängigen Daten.

## Unabhängige Holdout-Abnahme

Ein zweiter, getrennt angelegter Fotobox-Satz umfasst 83 Bilder aller 10
PoC-Teil-IDs. Er wurde erst nach der Wahl der Vorverarbeitung aufgenommen und
lief mit derselben, expliziten Vordergrund-Zuschnittsoption.

| Kennzahl | Holdout-Ergebnis |
| --- | ---: |
| Top-1 | 24,1 % |
| Top-3 | 60,2 % |
| Top-5 | 77,1 % |
| MRR@10 | 0,454 |

Damit bestätigt der unabhängige Satz die Verbesserung gegenüber der Rohbild-
Baseline, erreicht aber noch nicht die Qualität für automatische
Lagerzuordnungen. Besonders `3710` (Top-5 12,5 %) und `3068b` (Top-5 60,0 %)
benötigen gezielte Verbesserungen an Referenzansichten oder Modellstrategie.
