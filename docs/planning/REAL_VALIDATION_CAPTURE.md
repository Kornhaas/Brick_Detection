# Reale Validierungsaufnahmen

## Ziel

Messen, ob die aktuelle Render-Referenzdatenbank echte Fotos korrekt zuordnet.
Diese Bilder sind ausschließlich Evaluation und bleiben von Training sowie
Referenzindex getrennt.

## Minimaler erster Satz

- Die 10 Teile aus `configs/poc_parts.txt`, sofern physisch vorhanden.
- Pro Teil mindestens 3 unterschiedliche Ansichten.
- Neutrale, matte Unterlage; genau ein Teil pro Bild.
- Gleichmäßiges Licht, keine starken Spiegelungen, keine Hände im Bild.
- Originaldateien unverändert in `data/validation/images/` ablegen.

## Manifest

Für jedes Bild eine Zeile in `data/validation/manifest.csv` anlegen:

```csv
image_path,part_id
images/3001_top.jpg,3001
images/3001_side.jpg,3001
```

`part_id` ist die bekannte LDraw-ID. Das Manifest wird nicht eingecheckt, weil
es lokale Bilddaten referenziert. Unklare oder nicht sicher identifizierte Teile
gehören nicht in die erste Messung.

## Abnahme

- Alle Manifestpfade existieren, jedes Bild enthält genau ein Teil.
- Das Evaluationsscript berechnet Top-1/3/5 und MRR getrennt vom
  synthetischen Ergebnis.
- Fehlerfälle werden mit Bild, tatsächlicher ID und Top-5 dokumentiert.
