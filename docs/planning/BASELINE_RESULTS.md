# DINOv2-Retrieval-Baseline – 2026-09-04

## Aufbau

- 10 LDraw-Parts, je 28 Workbench-Renders, insgesamt 280 Referenzbilder.
- Encoder: DINOv2 ViT-S/14, Revision `7764ea0f912e`.
- Suche: L2-normalisierte Embeddings, Cosine Similarity, Aggregation nach
  Part-ID.
- Ausführung: lokale NVIDIA GeForce RTX 4070.

## Synthetische Leave-one-render-out-Messung

| Kennzahl | Ergebnis |
| --- | ---: |
| Top-1 | 57,1 % |
| Top-3 | 87,9 % |
| Top-5 | 94,3 % |
| MRR@10 | 0,726 |

Das jeweils angefragte Referenzbild wurde aus der Suche ausgeschlossen. Die
Messung zeigt daher, ob andere Ansichten desselben synthetischen Parts gefunden
werden. Sie misst **nicht** die Übertragbarkeit auf echte Fotos.

## Nächster Qualitätsnachweis

Der nächste Schritt ist ein festes, reales Testset nach
[REAL_VALIDATION_CAPTURE.md](REAL_VALIDATION_CAPTURE.md). Seine Bilder dürfen
nicht in Renders, Embeddings, Fine-Tuning oder Feedback-Training einfließen.

## Quellen

- https://github.com/facebookresearch/dinov2
- https://pytorch.org/get-started/locally/
