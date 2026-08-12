# Wiring Crib Sheet — Ombonad Build, OUR Parts, OUR Names

Companion to the build sheet. The assembly PDF's electronics chapter describes the
Arduino + CNC-shield era; our build is DLC32 + Pi. This document is the translation
layer plus the full no-solder wiring procedure in the names of the parts on the bench.

---

## 1 · TRANSLATION TABLE (PDF says → we have)

| PDF / BOM term | Our actual part | Notes |
|---|---|---|
| "Arduino Uno + CNC Shield" | **MKS DLC32 board** | Whole electronics chapter diverges here |
| "EN-GND jumper on CNC shield" | *(none needed)* | DLC32 driver sockets don't use that jumper |
| "X and Y slots on CNC Shield" | **DLC32 X and Y driver sockets** | Same logical axes; see §4 orientation |
| "motor drivers" / "DRV8825 from kit" | **BTT TMC2209 V1.3 ×2** | Kit's A4988s = spares drawer, never installed |
| "12V (5A) adapter" | **ALITOVE 12V/5A**, 5.5×2.5 plug | |
| "1-to-3 splitter" | **CENSHI 1F→3M splitter, 5.5×2.5** | |
| "female DC plug / connect to shield" | **MEIRIYFA female pigtail (bare leads)** | Bucks only (board needs no pigtail — see below) |
| "12V→5V buck for the Pi" | **Buck #2** (micro-USB output cable) | Plugs straight into Pi power port |
| *(no PDF equivalent — LED was 12V COB)* | **Buck #1** (same module) → 5V LED rail | Micro plug gets snipped; leads → WAGO |
| "COB LED strip (12V)" | **BTF WS2812B 5mm 2020, 5V, 2m** | Addressable; data wire is NEW vs PDF |
| "LED dimmer (potentiometer)" | *(deleted)* | Brightness in DW software |
| "on/off switch + soldering (step 3)" | *(deleted — no-solder path)* | DC plug = the switch; skip PDF step 3 entirely |
| "Raspberry Pi Zero" | **CanaKit Pi Zero 2 W** (case, heatsink) | |
| "OTG adapter" | **micro-USB M → USB-A F adapter** | Pi's INNER micro port (data), not outer (power) |
| "glue the magnet" | **Gorilla 5-min epoxy** | ~2mm protrusion is normal |
| "baking soda ~300g" | pantry | |
| solder + heat shrink | **WAGO 221s + WGGE stripper + Scotch 700** | Every joint is lever or screw |

Naming convention from here on (DESIGNATED AT GATE 1, 7/29): **Buck #2 = Pi power, permanent resident (flight-certified on Pi boot). Buck #1 = LED rail, gets the micro-plug snip at Gate 5 (also flight-certified pre-surgery).** Both proven by booting the Pi. Tape labels updated accordingly.

---

## 2 · POWER TREE (one wall plug, whole machine)

```
ALITOVE 12V/5A ──► 90° extension (through GLADOM leg)
                └──► side-ring DC input (press-fit in printed ring; no switch, no solder)
                      └──► SPLITTER (1F → 3M, all 5.5×2.5)
                            ├─[out 1]► male plug DIRECT into DLC32 barrel jack "POWER 12-24V" (below fuse, beside USB). CORRECTED 8/1: prior "screw terminal" was confabulated; black SPINDLE terminal = OUTPUT, never power in.
                            ├─[out 2]► pigtail F → WAGO ×2 → Buck #2 leads → micro-USB → Pi POWER port
                            └─[out 3]► pigtail F → WAGO ×2 → Buck #1 leads → (snip micro plug)
                                        → strip 5V feed: RED→WAGO→strip +5V, BLACK→WAGO→strip GND
```

Polarity discipline: **red = +12V, black = GND** everywhere on the input side; verify
every pigtail's lead colors with the meter before landing them (cheap pigtails
occasionally swap colors — 20 seconds of continuity checking per pigtail: meter on
continuity, probe center pin ↔ red lead. Center pin is ALWAYS +.)

## 3 · DATA & CONTROL TREE

```
Pi (inner micro-USB, data) → OTG adapter → DLC32 kit's USB cable → DLC32 USB port
Pi GPIO18 (physical pin 12) → jumper wire → LED strip DIN
Pi any GND pin (e.g. physical pin 14) → jumper wire → LED strip GND   ← REQUIRED:
   data needs common ground even though strip power comes from Buck #1
```

Strip has an arrow on it: data flows IN at the arrow's tail. Connect DIN at the end
where the arrow points AWAY along the strip.

## 4 · DLC32-SPECIFIC NOTES (what the PDF can't tell you)

- **Driver install:** DLC32 sockets are labeled X / Y1 / Y2 / Z. Our two TMC2209s go
  in **X and Y1**. Orientation: match the EN pin marking on the BTT stick to the EN
  marking on the DLC32 silkscreen — double-check before power; a reversed stepstick
  dies instantly. (Heatsinks on the driver chips, from the BTT bag.)
- **Motor mapping:** Outer motor → X, Inner motor → Y1 (mirrors PDF's shield logic).
  If Gate 3 shows swapped/mirrored motion, swapping the two motor plugs is the whole
  fix — harmless, diagnostic, expected on first builds.
- **Vref:** same procedure as PDF (pot + meter, motors UNPLUGGED, board powered),
  target **~0.8V** on each BTT stick. Pin: do not raise toward the motors' 1.5A
  nameplate.
- **Firmware — RESOLVED (extracted from repo 7/29):** the DLC32 ships with Makerbase firmware and must be flashed to **FluidNC**; the config is in the repo at **`firmware/dune_weaver/config.yaml`** (first line: `board: MKS-DLC32 V2.1` — written for our exact board; per-model folders exist, ours is `dune_weaver`).
  **Procedure (Gate 3 prep, ~15 min):**
  1. Download the config: browse github.com/tuanchris/dune-weaver → `firmware/dune_weaver/config.yaml` → Raw → save. (No SSH needed.)
  2. DLC32 → USB → the Mac/desktop, **Chrome or Edge** (Web-Serial browsers).
  3. Go to **installer.fluidnc.com** → connect → select the serial port → install current FluidNC release. (This overwrites the Makerbase firmware; the TS35 screen goes dark forever — expected, it's a spare anyway.)
  4. Upload `config.yaml` to the board: via the installer's file/config tool if offered, else via FluidNC's own WebUI (board briefly hosts a "FluidNC" WiFi AP / serves a page) — file upload, confirm `$Config/Filename=config.yaml`, restart board.
  5. Thereafter the DW app on the Pi reads/tunes settings over the same USB link through its Setup UI — no more computer needed.
  *Honesty flag: steps 3–4's exact click-path may drift with installer versions; if any screen surprises, stop and bring Ashlar the screenshot — this is a together-at-the-screen step by design.*
- **Kit spares (never installed):** A4988 drivers, TS35 touchscreen, endstops (we
  crash-home; no endstops in this design).

## 5 · WIRING ORDER OF OPERATIONS (Gates 1–3, step by step)

**Gate 1 — power only, nothing precious attached:**
1. ALITOVE → splitter directly (no ring yet, bench only).
2. Meter on out-1 pigtail bare leads: expect **12.0V ±0.3**, red = +.
3. [DONE 7/29] Connect a buck to out-2 via WAGOs; certify by Pi boot (probe inside plug
   or at USB breakout): expect **5.0–5.2V**.
4. [DONE 7/29] Same for the other buck. Nothing warm after 5 minutes = pass.

**Gate 2 — Vref (board powered, motors unplugged):**
5. TMC2209s into X and Y1, EN-aligned, heatsinks on.
6. Splitter out-1 male plug into DLC32 POWER barrel jack; wiggle test (snug + steady = good; sloppy = 2.5→2.1 adapter-tip scenario, pause). Power up.
7. Meter black probe on board GND, red on each stick's pot/Vref point → adjust to
   ~0.8V. Photo of meter per stick → Ashlar countersigns.

**Gate 3 — first motion:**
8. Flash DLC32 to FluidNC + DW config (per §4 open item). Power down first.
9. Motors into X and Y1 headers. Pi (already flashed & on WiFi) → OTG → USB → DLC32.
10. Power both (Buck #1 feeding Pi, out-1 feeding board — one wall plug, whole tree).
11. DW web UI → connect → upload a pattern → bare shafts dance. Pass.

**LED lands at Gate 5, not before:** strip into top-ring channel, feed from Buck #2,
data from GPIO18, diffuser tape over, brightness cap set in DW settings FIRST, then
lights.

## 6 · WAGO PRACTICE (60-second course)

Strip 11mm of insulation (WGGE has an 11mm-ish notch; the WAGO's side shows a strip
gauge). Lift lever fully, insert wire to the stop, close lever, tug-test. Stranded
wire: twist lightly first. One conductor per port, ever. The clear housing lets you
SEE the copper seated — look every time. That is the entire skill.

---

*Open items rolled up: DLC32→FluidNC flash procedure + config (Ashlar, from repo,
before Gate 3) · pigtail polarity verify per unit (Gate 1) · axis mapping confirm
(Gate 3, swap-plugs fix) · level shifter only if LED flicker (Gate 5).*
