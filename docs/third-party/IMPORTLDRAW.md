# ImportLDraw

The renderer calls the external Blender add-on ImportLDraw. It is downloaded
into `data/tools/ImportLDraw` and is deliberately not committed to this
repository. The source repository states GPL-2.0-or-later; we do not copy or
modify its code. `scripts/render_part.py` applies a small runtime adapter for
Blender 5.2 because that release no longer guarantees a node display name the
add-on expects.

- Source: https://github.com/TobyLobster/ImportLDraw
- Revision: record the commit hash before a production render batch.
- Purpose: import LDraw `.dat` files into Blender for rendering.
