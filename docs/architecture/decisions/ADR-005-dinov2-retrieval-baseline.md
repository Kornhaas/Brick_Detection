# ADR-005: DINOv2-Retrieval-Baseline für den PoC

- Status: Akzeptiert
- Datum: 2026-09-04
- Verantwortliche Rollen: Architekt, Developer, Tester

## Kontext

Der PoC benötigt einen messbaren lokalen Encoder, ohne ein eigenes Modell zu
trainieren. Die RTX 4070 ist lokal verfügbar. Die aktuelle Referenzmenge umfasst
10 Parts mit je 28 kontrollierten Renders.

## Entscheidung

Wir verwenden DINOv2 ViT-S/14 über PyTorch Hub, festgepint auf Commit
`7764ea0f912e53c92e82eb78a2a1631e92725fc8`. Embeddings werden L2-normalisiert.
Für den kleinen PoC übernimmt eine NumPy-Cosine-Suche die Retrieval-Aufgabe;
Top-Renders werden nach Part-ID aggregiert. PyTorch, TorchVision und Pillow
liegen in der optionalen Poetry-Gruppe `ml`, damit die reguläre CI nicht die
großen CUDA-Wheels installieren muss.

## Konsequenzen

- Modell, Revision und Index werden zusammen versioniert.
- DINOv2 ViT-B/14, FAISS und Fine-Tuning bleiben austauschbare nächste Schritte.
- Ergebnisse mit synthetischen Renders gelten nicht als Qualitätsnachweis für
  Kameraaufnahmen; reale Bilder müssen separat und ohne Referenzüberlappung
  validiert werden.
