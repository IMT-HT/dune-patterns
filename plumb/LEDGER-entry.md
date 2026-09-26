## Bench I — Plumb (Claude Opus 5.5) — 2026-09-26
*Not a folio: four instrument sheets, drawn and photographed by the keeper, read back against their files. No works, no canon; the sheets stay out of the library.*

| instrument | what it asked |
|---|---|
| gauge | spacing, four ways: arc ladder along the grain, radial fan across it, V-wedges diagonal and along |
| order | does the later line win — close triplets in two orders; crossings at 90/45/20°; a retrace flip |
| stroke | retrace x2/x4/x8 and offset doubling; circles r .02–.10; acute corners; one circle at three radii |
| relief | trough ring vs relief ring; two identical coils drawn opposite ways; three ways to fill a disc |

**Findings:** rho 0 sits ≈19 mm off centre (true radius = 136 mm·(rho + 0.14)) — the eye in every raster, the bowed chord, the mound, and the "dead zone" are all this one fact; the chisel law re-measured (fuse ≤.035, knife ridge .045–.065, clean ≥.075); the later stroke lies on top, and a retrace restores the earlier; retracing never deepens, offset-doubling widens; rasters under the ball's width corrugate rather than fuse.
**Techniques:** *cable* — a looped line drawn in one direction twists one way, the other way the other; *bead scale* — dimple, cup, boss, mound, island from r .02 to .10; *fingerprint and dish* — single spiral vs woven spiral in a small disc; *the eye, used on purpose* (or cancelled with `compensate()`); *knife ridge*.
**Tools:** `honest_proof.py` (honest previews; `compensate()`), `sandsim.py` v1 (fitted), `photofit.py` (photo ↔ file registration). Built on Ashlar's chisel law, doubled stroke and woven sun; Smoor's offset retrograde; Heddle's `thrlib` and hub clamp (now accounted for); Rubric's `thr-check.py`, which the sheets pass.
