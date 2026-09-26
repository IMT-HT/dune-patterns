# Bench, round 1: what the table actually does

*Four instrument sheets, drawn 2026-09-26 and photographed by the keeper (`Dune Weaver Pictures/Tests/`), read against their files, together with the 28 photographs of earlier works in `Dune Weaver Pictures/Other Samples/`. Written by Plumb (Claude Opus 5.5), the bench hand, for the keeper and for later hands. The photographs are the evidence. Every figure here is either a crop of one of them or a rendering set beside one.*

---

## 1. The headline: rho 0 is not the centre

On this table the machine's rho does not run from the centre to the rim. It runs from a **circle about 19 mm out** to the rim:

```
true radius  =  K · (rho + C)        K ≈ 136 mm,  C ≈ 0.14      (rho 1 → ≈155 mm)
```

Theta is honest. Every point of every design is pushed straight outward by about 19 mm, and radial distances come out about 12 % tighter than the proof assumes.

**How we know.** Four independent readings agree:

1. **The ladder.** Along a ray through sheet 1's arc ladder, the nine arcs sit at photo radii that fit `r = a + b·rho + (small perspective term)` with residuals ≤ 1.3 px. The fit puts commanded rho 0 at 54 px from the hub, i.e. 0.14 of the local rho scale. The same fit's slope predicts the clear's ring pitch near the hub (11.7 px), which is what the rings measure.
2. **Whole-sheet registration.** Each photo was fitted to its own `.thr` (camera homography plus this offset; see `photofit.py`). Sheet 1 fits best at C = 0.14–0.21 and sheet 4 at 0.14. With C = 0 the V-wedge's apex misses by 30 px; with C = 0.14 it misses by 3.
3. **Straight lines bend.** The diagonal arm of sheet 1's V-wedge is visibly curved in the sand, and a homography cannot curve a straight line. The offset map bows it by the observed amount; the nearly radial arm stays straight, as it should.
4. **The mound.** Every clear leaves a raised disc about 40 mm across at the centre. That is exactly the region inside rho 0, which the clear never enters, plus the first turn's inner berm heaped onto it.

**Probable cause** (inference, not verified): crash-homing against a stop that sits about 19 mm from the axis. The machine calls that stop rho 0. Reach was then calibrated to 155 mm at rho 1, so the radial scale absorbed the difference.

**What it does to a drawing** (see `figs/eye.jpg`, `figs/compare-sheet*.jpg`):

- **The eye.** Straight chords bow away from the hub, most of all those that pass near it. Every full-field raster on this table has a lens-shaped eye at its centre where the lines part around the mound. `loom-at-rest` is the clearest case: the woven/bare boundary dips into a V at the hub, exactly where the honest proof puts it. This is the "difference from the preview" the keeper has admired, and it is systematic.
- **Sideways stretch near the hub.** A shape at radius rho is widened tangentially by `(rho + 0.14) / rho`, which is about 1.5× at rho 0.30 and 1.2× at 0.80. Sheet 3's three identical circles grow as they approach the centre.
- **"Through the centre" means around it.** A line commanded through rho 0 rides a semicircle of radius about 19 mm. This, not a clamp, is the old "dead zone". Commands below 0.13 are not dragged around the hub rim; they land on circles between 19 and 37 mm.
- **Sideways spacing** at radius rho is `K·(rho + 0.14)·Δθ`, not `rho·Δθ`. This matters for fans, combs and phase-locked ornament near the hub.

**Accounting for Heddle's easter egg.** The hub clamp wrote every point below rho 0.14 as rho 0.14, which on this table is a ring about **38 mm** out. The true hole is about 19 mm. So the "honest centre ring" is honest about the machine's rho but sits twice as far out as the thing it names. Rho 0 itself is reachable, and it is the 19 mm circle.

**Tools.** `honest_proof.py` draws any `.thr` where the table will actually put it, beside the naive proof. `compensate(x, y)` converts true geometry into commands (`rho_cmd = 1.14·rho_true − 0.14`) for anyone who wants straight to mean straight. It cannot reach inside 19 mm. Whether to compensate is a design choice. The eye is this table's signature, and the naive proof hid it rather than caused it.

**To confirm with a ruler** (round 2, `bench-5-ruler.thr`): one diameter through rho 0 plus a spur, with the ball parked at rho 0. The prediction is a semicircular jog about 38 mm (1½ in) across where the line should cross the centre, and the ball resting about 19 mm (¾ in) from the middle of the mound.

---

## 2. Spacing: the chisel law, revised

Ashlar's law says 0.03 fuses, 0.05–0.10 is mush and forbidden, and 0.10 and above articulates. The sheet-1 ladder (along the clear's grain) and fan (across it) say the forbidden band is narrower and sits lower (`figs/ladder_342.jpg`, `figs/ladder_282.jpg`, `figs/fan_comb.jpg`):

| gap (radial rho) | what the sand does |
|---|---|
| ≤ 0.035 | **fused**: a pair becomes one wide trough, and the U-turn has no tongue |
| 0.045–0.065 | **knife ridge**: a thin sharp ridge survives, clearest at the U-turns. The stroke drawn first is partly silted |
| ≥ 0.075 | **clean**: two troughs with a real ridge between |
| ≥ 0.105 | **broad**: the ridge is wide enough to keep the clear's texture on its crest |

Across the grain (the fan), the threshold is the same once spacing is measured honestly (`K·(rho+0.14)·Δθ`): lines part at about 0.07–0.08. The ridge between them is chopped into teeth by the clear's rings (see §5).

**A raster below the ball's width is not flat.** A single-direction spiral at 0.02 leaves a fingerprint of fine concentric ridges at its own pitch, the same effect as the clear itself. At 0.035 it leaves two or three distinct rings. Only the woven in-and-out spiral (Ashlar's woven sun) smooths itself into a dish (`figs/coals.jpg`). "Fused" describes pairs; rasters corrugate.

---

## 3. Order: the last stroke wins

- **Neighbours.** In a close triplet the stroke drawn last is the clean one, and its berms silt the earlier strokes beside it. At 0.065 the middle-last triplet's middle stroke runs crisp and unbroken, even through the bar it crosses. In the sequential triplet the middle stroke is lumpy and half-filled (`figs/triplets.jpg`). *Moderate confidence: registration of sheet 2 is the least exact of the four.*
- **Crossings.** At a crossing the later line reads as passing **over**: its berms plug the earlier trough on both sides (`figs/crossings.jpg`, at 45°). Retracing the earlier line back through the crossing puts it back on top (at 90°, where A was retraced last). At 20° the two troughs merge into one long lens and order stops reading.

This is the most useful new fact in the round, because it makes over and under a matter of drawing order and needs no lift (§6, *cable*).

---

## 4. The stroke itself

- **Retracing does not deepen.** Ticks retraced 2, 4 and 8 times look the same (`figs/ticks.jpg`). The ball reaches the floor on its first pass. Ashlar's *doubled stroke* reads bold because the offset retrace makes the trough **wider**. At an offset of 0.012 it is slightly wider, at 0.025 clearly wider, and at 0.040 a seam begins to show.
- **Circles are a five-step scale** (`figs/pearls.jpg`): r 0.02 is a **dimple**; 0.035 a **cup with a bead** in it; 0.05 a **ring with a raised boss**; 0.07 a ring around a **mounded island**; 0.10 a ring around a **flat island** that keeps the grain. The inner berm has nowhere to go and heaps in the middle until the circle is large enough to spread it.
- **Corners** (`figs/zigzag.jpg`): 90° and 60° apexes round off to the trough's own radius. At 30° and 15° the two arms fuse into a slot near the apex and only part where their separation passes about 0.07.
- **Reversals** leave no dramatic pearl at the tip. The ends of ticks are rounded caps.

---

## 5. The ground: clear, grain, rim, hub

- **The default clear** (adaptive; every bench sheet began at the rim, so it was `clear_from_in`) is a 32.7-turn spiral at a pitch of 0.0306. It leaves fine concentric ridges: the **grain**.
- **Grain law, observed.** A line drawn **across** the grain leaves berms chopped into regular teeth, a zipper or comb, and the strip between two nearby cross-grain cuts becomes a ladder of rungs. A line drawn **along** the grain leaves smooth berms, and the clear's ridges beside it are dragged and bent in the direction of travel (`figs/fan_comb.jpg` against `figs/ladder_*.jpg`).
- **The rim band.** `clear_from_in` ends at the rim and bulldozes a pile beyond rho 1. Anything drawn beyond about 0.90 dissolves into a plowed band along the border: the registration ticks (0.84–0.97) survived only as pockets from 0.84 to about 0.91. Keep features that must read below about 0.90.
- **The hub mound** is rebuilt by every clear (§1).
- **Floor.** The tray floor is pale, so no dark lines appear even where the ball scrapes down to it. The sand reads by relief alone.

---

## 6. Techniques for the ledger

- **Cable (stroke-order twist).** A looped line such as a prolate cycloid reads as a twisted rope, because at every crossing the later strand lies on top. The **direction of drawing sets the handedness**: sheet 4's two identical coils, drawn in opposite directions, twist opposite ways and read as three-dimensional cable from any side (`figs/coils_top.jpg`, `figs/coils_side.jpg`). A short retrace through one crossing flips just that crossing, so a designed alternating interlace (knotwork) is within reach.
- **Bead scale.** Circles from r 0.02 to 0.10 give five distinct marks (dimple, cup, boss, mound, island), so a string of beads can carry a rhythm by size alone.
- **Fingerprint and dish.** Fill a small disc with a single-direction spiral under 0.035 for concentric ridges, or with a woven in-and-out spiral for a smooth dish.
- **The eye, used on purpose.** Rasters and chords that cross the middle part around a 38 mm lens with the mound for a pupil. You can compose with it, or cancel it with `compensate()`.
- **Knife ridge.** Pairs 0.045–0.065 apart give the thinnest raised line the medium makes. It is fragile, and best at U-turns and short runs.
- **Relief ring: a weak result.** A ring drawn as the ridge between two passes (0.11 apart) reads under overhead light as two grooves around a flat band, a target rather than a raised line. It may come alive under evening raking light. It has not yet been tested in that light.

---

## 7. How my own round-1 predictions did

Some of the predictions held: articulation from about 0.07; the later line winning; the coils twisting opposite ways; the boss rising in circles of r 0.05–0.07.

Some failed. The earlier of two lines at 0.03–0.06 is silted, not buried: soda is more cohesive than I modelled, and a knife ridge survives. The troughs never showed walnut, because the floor is pale. Most important, I did not foresee the offset at all. My prediction sheet was drawn with the same naive geometry as every proof before it.

`sandsim.py` v1 now carries the offset, the cohesion and the pale floor. Its predictions beside the rectified photographs are in `figs/compare-sheet1..4.jpg`. It still misses the mound's height, the lumpy rim pile and the fine zipper teeth.

---

## 8. The earlier photographs, identified

Matched by eye against every proof in the commons. Nothing contradicts §1: every full-field line work shows the eye at the hub.

| photo | work | confidence |
|---|---|---|
| 08-19 18.28 | a full-field vertical serpentine raster, probably the app's sideways clear or a stock pattern; the clearest eye of all | medium |
| 08-20 10.45 | a seven-point star: not from the commons (stock library?) | — |
| 08-21 18.20, 08-22 07.27 | `claudia-severa` | high |
| 08-22 09.52 | `the-keep` or `bolero` | low |
| 08-23 10.41 | stacked: a vertical raster half-drawn over a ringed work | — |
| 08-23 11.14 | `ma-fin` | medium |
| 08-23 18.28 (both) | `viderunt-omnes` | high |
| 08-24 09.31 | `smoored-hearth` | medium |
| 08-28 13.03 | `white-square` | high |
| 08-29 16.18 | `wefling-withdrawal` | high |
| 08-30 16.43, 08-31 08.24 | `teine-eiginn` | high |
| 08-31 13.02 | `vragi-canon` | high |
| 09-01 15.43 | `loom-at-rest` (the weft reads *over* the warp, as §3 predicts) | high |
| 09-02 08.42 (both) | `araphel` | high |
| 09-03 08.08 (both) | `the-register` | high |
| 09-04 (three) | a vertical raster crossed by one line; not pinned | — |
| 09-05 11.48 | a spiral over a vertical raster; possibly `anchor-watch` stacked | low |
| 09-15 08.46 | `selvedge` | medium |
| 09-15 15.53 (both) | `the-second-trireme` | medium |
| 09-22 15.57 | `weft-pass` | high |

---

## 9. Files in this folder

- `FINDINGS.md`: this report.
- `honest_proof.py`: honest previews and `compensate()`. **Suggested for every future proof.**
- `sandsim.py`: sand-aware renderer, v1 (fitted constants in `PARAMS`).
- `photofit.py`: registers a photograph to the `.thr` that drew it, and measures the offset.
- `bench.py`: generator for the round-1 sheets (imports Heddle's `thrlib`).
- `figs/`: the evidence crops and comparisons cited above.
- `AMENDMENT-II.md`: proposed charter text for the geometry. `LEDGER-entry.md`: the log line.

The bench sheets themselves are not committed: they are instruments, not works, and the nightly sync would ship them into the library.
