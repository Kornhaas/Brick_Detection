# ADR-002: Embedding-basierter lokaler Recognition-PoC

- Status: Akzeptiert
- Datum: 2026-09-03
- Verantwortliche Rollen: Architekt, Developer, UX-Experte, Tester

## Kontext

Das System soll ohne externe Erkennungs-API skalierbar arbeiten. Ein klassischer
Klassifikator müsste für jede Part-ID umfangreiche gelabelte Bilddaten besitzen.
Die Startinformationen schlagen daher synthetische LDraw-Renders und einen
vortrainierten Bildencoder mit Ähnlichkeitssuche vor.

## Entscheidung

Der PoC trennt strikt Datenpipeline und Recognition Engine:

```text
LDraw → Katalog/Render → Embeddings/FAISS-Index
Kamerabild → Freistellung → Encoder → Suche → Part-Aggregation → Top-5
```

Wir starten mit einem lizenzierten vortrainierten Encoder und FAISS. Für jede
Embedding-Zeile werden Modellversion und Indexversion gespeichert. Treffer von
Renders werden nach Part-ID aggregiert; die UI erhält Parts, nicht nur die
nächsten Einzelbilder.

## Konsequenzen

- Encoder, Index und Renders sind austauschbar und versioniert.
- SQLite ist für den PoC ausreichend; eine Vektordatenbank wird erst bei
  Mehrbenutzerbetrieb oder komplexen Filtern bewertet.
- Segmentierung, Multi-View, Fine-Tuning und Geometrie-Reranking sind
  Erweiterungen, keine Voraussetzung für den ersten Messpunkt.
