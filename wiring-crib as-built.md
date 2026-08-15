# AS-BUILT — the Sand Table's Current Truth (rev 2, 2026-08-15)

*For any future maintainer, human or model, arriving without our context.
Everything below is the machine as it exists. The build's history, procedures,
and error ledger live in `ombonad-build-sheet.md`; Pi operations live in
`pi-admin.md`; the art commons lives in the public `dune-patterns` repo
(read its CHARTER.md first). Claude instances: `/areas/sand-table.md` in
memory is your cold-start. Credentials are on the keeper's index card — never
in these files or the public repo.*

## The machine
Dune Weaver "Enclosed Ombonad" remix (MakerWorld 922851) in 2× IKEA OMBONAD
walnut trays (tray B = top) on a GLADOM base. Ball: **10mm chrome steel
(52100)** — the drawer's 304-stainless pack is non-magnetic decoys, labeled.
Magnet: N52 20×10mm epoxied in the arm, ~2mm proud, electrical tape on its
face as a slip layer (arm may brush the tray at center — by design tolerance).
Field constant: **rho 1.0 = 155mm**. **House compass: add +π/2 to theta**
for any pattern with an 'up' (representational work) so it reads upright from
the keeper's chair; symmetric works don't care. The ball plows ≈0.065 rho wide; strokes
≥0.10 apart articulate, ≤0.03 fuse deliberately, between is mush.

## Electronics as-built
- **Controller: Makerbase MKS DLC32 V2.1** (screenless), running **FluidNC
  v4.0.4** (WiFi build + WebUI3). Config lives ON THE BOARD's flash as
  `config.yaml`; keeper holds a pulled copy. Board reached at desktop via USB
  (needs 12V main power connected to enumerate) or its own `FluidNC` WiFi AP
  → 192.168.0.1 for file/console work.
- **Config truths (do not "correct" these):** `x: steps_per_mm 320,
  direction I2SO.2` (no suffix); `y: steps_per_mm 459.2` (empirical — NOT the
  repo default 287; calibrated to this build's 155mm reach), `direction
  I2SO.6:low`; both `limit_neg_pin: NO_PIN` (no switches exist — crash-homing;
  the homing grind is the spec, not a fault); hard/soft limits false.
- **Drivers: BTT TMC2209 V1.3 in X and Y** (third pack; two prior casualties
  were 180° seating, see build sheet). **DIP both banks 1-1-0 = 1/16.**
  Vref ≈ 0.815V each (800±50 target, DCV 2000m range, black on G, red on pot
  screw-top). **Orientation law: correct seating puts the pots facing OUTWARD
  to the board edge — but never trust geometry: verify by copper.** Identity
  beeps: stick's VM joint ↔ fuse shoulder; stick's VDD joint ↔ Probe-JST 5V
  pin. Aux stubs (DIAG/INDEX) are flush-cut, never bent — bending kills pads.
- **Power tree (one wall plug):** ALITOVE 12V/5A → 5.5×2.5 1→3 splitter:
  (1) male plug DIRECT into the board's barrel jack "POWER 12-24V" — the
  black SPINDLE screw terminal is an OUTPUT, never power input;
  (2) pigtail → WAGO → **Buck #2** → micro-USB → Pi's OUTER port (power);
  (3) reserved for **Buck #1** → future LED rail (snip its micro plug, WAGO
  to strip 5V/GND; data = Pi GPIO18 + common ground; cap brightness in the
  app BEFORE first light).
- **Data:** Pi's INNER micro port → OTG adapter → USB-B to board.
- **Pi:** Zero 2 W, `duneweaver.local`, DW v4 in Docker, 2.4GHz WiFi only.
  Ops, triage, and the SD-reflash rite: `pi-admin.md`.

## Meter laws (AstroAI, hard-won)
Resistance = the Ω arc ONLY (2000 / 20k positions). **"2000m" is the 2-volt
DC range** — Vref's home, never ohms. Rail census (DCV 20, black on G):
fuse ≈12.5 · Probe-JST 5V pin ≈4.9x · I2C 3V3 ≈3.3. The 5V number is the
sovereign fault detector: ≥5.3 = power off immediately (VM→logic backfeed).

## Software facts
- Patterns: `.thr` theta-rho (theta radians continuous, rho 0–1); format and
  contribution law in the repo's CHARTER.md. Delivery: public repo →
  Pi cron 4:17am (`~/dune-sync.sh`, find-based, markers in `~/.dune-synced`
  keyed by basename) → app library. Curation = keeper's playlist, by hand.
- Clearing between patterns: playlist-level `clear_pattern` setting AND a
  per-run choice (modes: none/random/adaptive/clear_from_in/out/sideway).
  **Palimpsest works are PERFORMED**: run manually, clear=none, works start
  at rho 0 (park tails hand the pen to the successor).
- House rules: one drawing per day of light (feast days excepted, keeper
  declares); silence is a spec; no lifting the table mid-draw.

## Spares drawer (all labeled)
A4988 pair "tuned 448, carried first draw" — proven emergency drivers (DIP
1-1-1 with them, and y steps become 71.75 — quarter of 459.2 — while in use);
2× TMC2209 from earlier packs, uncratered, plausibly healthy pending bench
self-test + identity beeps (their sibling died of rotation, not batch); 1×
cratered TMC (keep for the museum); TS35 touchscreen (dark by design under
FluidNC); endstop switches (never used); 304 stainless balls ×20 (decoys);
16" tempered glass (superseded lid; current works fine glass-on-ring, Ø400
pane remains the someday-upgrade); N52 3/4"×3/8" magnets ×6 + 20×10 spare;
Y-seat/pinout reference photos with the index card.

## History
Everything above was earned the hard way; the full campaign — gates,
casualties, corrections, the error ledger both directions — is
`ombonad-build-sheet.md`. Trust it over memory, and trust the copper over
everything.
