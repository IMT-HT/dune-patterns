#!/usr/bin/env python3
# thr-check.py  --  Rubric (Claude Opus 5), 2026-09-01
#
# A conformance read for theta-rho files, against the CHARTER's "Format (the short
# truth)". Standard library only; no install, no dependencies. Run it before you push:
#
#     python3 rubric/thr-check.py */*.thr
#
# It separates FAULTs -- things that would draw wrong or not at all -- from NOTEs,
# which are the house's preferences and are the keeper's to waive. A folio that
# draws beautifully may carry notes. That is allowed and always was.
import math, sys

RHO_CEILING = 0.97   # the quiet border
ARC         = 0.005  # the charter's sampling: ~0.8mm of arc
CHORD       = 0.03   # a step past this is a visibly straight pull (~4.5mm; ball plows ~10mm)
PARK        = 0.02   # how near its own hub or rim a work must close to count as parked

def read(path):
    pts, faults = [], []
    for n, line in enumerate(open(path), 1):
        s = line.split('#')[0].strip()
        if not s:
            continue
        f = s.split()
        if len(f) != 2:
            faults.append(f"line {n}: expected 'theta rho', got {len(f)} field(s)")
            continue
        try:
            t, r = float(f[0]), float(f[1])
        except ValueError:
            faults.append(f"line {n}: unparseable -- {s!r}")
            continue
        if math.isnan(t) or math.isnan(r) or math.isinf(t) or math.isinf(r):
            faults.append(f"line {n}: non-finite value")
            continue
        pts.append((t, r))
    return pts, faults

def check(path):
    pts, faults = read(path)
    notes = []
    if len(pts) < 2:
        return [f"{path}: fewer than two points"], []

    theta = [p[0] for p in pts]
    rho   = [p[1] for p in pts]

    # rho: 0..1 is the field; past the ceiling is a loud margin, not a fault
    if min(rho) < 0 or max(rho) > 1.0:
        faults.append(f"rho leaves the field: {min(rho):.4f}..{max(rho):.4f} (must be 0..1)")
    elif max(rho) > RHO_CEILING + 1e-9:
        notes.append(f"rho reaches {max(rho):.4f}, past the {RHO_CEILING} quiet border")

    # Long steps are NOT lifts -- the ball cannot lift, so a wide gap between samples
    # is simply drawn as a straight pull. That is a technique (hub-chords, floret
    # connections, radial shots) as often as it is an oversight, so it is never a fault.
    arc = [math.hypot(rho[i+1]-rho[i], ((rho[i]+rho[i+1])/2)*(theta[i+1]-theta[i]))
           for i in range(len(pts)-1)]
    chords = [i for i, a in enumerate(arc) if a > CHORD]
    if chords:
        i = max(chords, key=lambda j: arc[j])
        notes.append(f"{len(chords)} step(s) over {CHORD} -- drawn as straight pulls; longest "
                     f"{arc[i]:.3f} ({arc[i]*155:.0f}mm) at line-pair {i+1}/{i+2}. Deliberate in "
                     f"chord work; otherwise resample.")

    # theta is continuous and unwrapped: a wrap shows as a near-2pi reversal
    wraps = [i for i in range(len(theta)-1) if abs(theta[i+1]-theta[i]) > 5.5]
    if wraps:
        faults.append(f"{len(wraps)} theta step(s) near 2pi -- looks wrapped, not accumulated")

    # Open and close tidily. "Rim" and "hub" are read from the work's own reach, not
    # from the field's: a piece that lives between 0.55 and 0.95 parks at 0.95.
    end = rho[-1]
    if not (end <= min(rho) + PARK or end >= max(rho) - PARK):
        notes.append(f"closes at rho {end:.3f}, between its own hub ({min(rho):.3f}) and rim "
                     f"({max(rho):.3f}) -- the ball parks in open field")

    print(f"{path}: {len(pts)} points, rho {min(rho):.3f}..{max(rho):.3f}, "
          f"{(max(theta)-min(theta))/(2*math.pi):.1f} revolutions")
    for f in faults: print(f"   FAULT  {f}")
    for n in notes: print(f"   note   {n}")
    if not faults and not notes: print("   clean")
    return faults, notes

if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        print(__doc__ or "usage: thr-check.py <file.thr> ..."); sys.exit(2)
    bad = 0
    for p in paths:
        try:
            f, _ = check(p)
        except OSError as e:
            print(f"{p}: cannot read -- {e}"); bad += 1; continue
        bad += 1 if f else 0
    print(f"\n{len(paths)} file(s); {bad} with faults.")
    sys.exit(1 if bad else 0)
