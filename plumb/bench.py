"""
bench.py — round-one test sheets for the Ombonad table.

Instruments, not works: exempt from the house rules, loaded by hand, never
canonized. Every sheet carries the same registration: a border at rho 0.97,
ONE tick at the top of the proof and TWO ticks at the right. From a photo the
ticks give rotation, and the side the double tick falls on gives handedness
(whether the proof is mirrored against the table seen from above).

Authoring frame = the proof's own frame: x right, y up, unit disc, angles in
degrees counter-clockwise from the right edge of the proof.
"""
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "heddle"))
from thrlib import Builder, preview, TAU  # Heddle's builder; lineage acknowledged

MAKER = "bench sheet, round 1 (Claude Opus 5.5, 2026-09-26)"
RB = 0.97     # border
TICK = 0.84   # tick inner end


def th(a_deg):
    """proof angle -> file theta. proof x = -rho cos(theta), proof y = rho sin(theta)"""
    return math.pi - math.radians(a_deg)


class B(Builder):
    # --- proof-frame primitives ---
    def at(self, x, y):
        self.xy(-x, y)

    def to(self, x, y):
        self.line_to_xy(-x, y)

    def pol(self, r, a):
        self.polar(th(a), r)

    def rad_to(self, r):
        self.radial(r)

    def arc_to(self, r, a_to, ccw):
        """constant-r arc to proof angle a_to. ccw=True means increasing
        proof angle (which is decreasing file theta)."""
        self.arc(r, th(a_to), direction=(-1 if ccw else +1))

    def pos(self):
        x, y = self.last_xy()
        return -x, y

    def cur_angle(self):
        x, y = self.pos()
        return math.degrees(math.atan2(y, x)) % 360

    def poly(self, pts):
        for p in pts:
            self.to(*p)

    def curve(self, fn, n):
        """fn(f) -> (x, y) in proof frame, f in [0,1]; joined from the current point"""
        for i in range(n + 1):
            x, y = fn(i / n)
            if i == 0:
                self.to(x, y)
            else:
                self.at(x, y)

    # --- the shared registration ---
    def tick(self, a):
        """from the border at angle a: in to TICK and back out."""
        self.arc_to(RB, a, ccw=(((a - self.cur_angle()) % 360) < 180))
        self.rad_to(TICK)
        self.rad_to(RB)

    def registration_open(self, start_a=100.0):
        self.pol(RB, start_a)
        self.tick(90.0)                  # single at the top
        self.arc_to(RB, 4.0, ccw=False)  # clockwise down to the double
        self.tick(4.0)
        self.arc_to(RB, 356.0, ccw=False)
        self.tick(356.0)

    def along_border(self, a_to, ccw):
        if abs(self.last()[1] - RB) > 1e-6:
            self.rad_to(RB)
        self.arc_to(RB, a_to, ccw)


def P(r, a):
    a = math.radians(a)
    return (r * math.cos(a), r * math.sin(a))


def emit(b, name, lines, outdir):
    path = os.path.join(outdir, name + ".thr")
    pts = b.write(path, [f"{name}", MAKER] + lines)
    preview(pts, os.path.join(outdir, name + "-preview.png"))
    return pts


# =====================================================================
# SHEET 1 — THE GAUGE: what spacing does to two lines, four ways
# =====================================================================
def sheet_gauge(outdir):
    b = B()
    b.registration_open()
    # --- (A) stepped arc ladder, lower right, ALONG the clear's grain ----
    gaps = [0.03, 0.045, 0.06, 0.075, 0.09, 0.105, 0.12, 0.15]
    radii = [0.855]
    for g in gaps:
        radii.append(radii[-1] - g)
    # radii: 0.855 0.825 0.78 0.72 0.645 0.555 0.45 0.33 0.18
    a_hi, a_lo = 342.0, 282.0
    b.along_border(a_hi, ccw=False)
    b.rad_to(radii[0])
    going_cw = True
    for k, r in enumerate(radii):
        if k > 0:
            b.rad_to(r)
        b.arc_to(r, a_lo if going_cw else a_hi, ccw=not going_cw)
        going_cw = not going_cw
    # 9 arcs: ends at a_lo, r = 0.18
    # --- (B) radial fan, lower left, ACROSS the grain: spacing = r * dtheta
    n_fan = 7
    dth = 0.18  # rad -> spacing 0.032 at r .18, 0.099 at r .55, 0.155 at r .86
    fan_a = [248.0 - k * math.degrees(dth) for k in range(n_fan)]
    b.arc_to(0.18, fan_a[0], ccw=False)
    r_in, r_out = 0.18, 0.86
    outward = True
    for k, a in enumerate(fan_a):
        if k > 0:
            b.arc_to(r_in if outward else r_out, a, ccw=False)
        b.rad_to(r_out if outward else r_in)
        outward = not outward
    # 7 lines, odd count -> ends at r_out; come home to the hub road
    # we are at r_out on the last fan line (angle ~176.8); go out to the border
    b.rad_to(RB)
    # --- (C) chord V-wedge, upper left, DIAGONAL to the grain -------------
    A = P(0.30, 150.0)          # apex
    Bm = P(0.80, 118.0)         # far-end midpoint
    ax, ay = Bm[0] - A[0], Bm[1] - A[1]
    L = math.hypot(ax, ay)
    nx, ny = -ay / L, ax / L
    B1 = (Bm[0] + 0.10 * nx, Bm[1] + 0.10 * ny)
    B2 = (Bm[0] - 0.10 * nx, Bm[1] - 0.10 * ny)
    # approach: along the border to the far end's angle, then in to B1
    a_b1 = math.degrees(math.atan2(B1[1], B1[0])) % 360
    b.along_border(a_b1, ccw=False)
    b.to(*B1)
    b.to(*A)
    b.to(*B2)
    # --- (D) spiral wedge, upper right, ALONG the grain (continuous) ------
    # out to the border and clockwise past the top tick to 80deg
    a_b2 = math.degrees(math.atan2(B2[1], B2[0])) % 360
    b.to(*P(RB, a_b2))
    b.along_border(84.0, ccw=False)
    b.rad_to(0.80)
    b.arc_to(0.80, 22.0, ccw=False)            # outer arc, constant r
    b.rad_to(0.60)                              # the open end
    # inner line: r rises 0.60 -> 0.80 as angle goes 22 -> 78
    b.curve(lambda f: P(0.60 + 0.20 * f, 22.0 + 56.0 * f), 240)
    b.rad_to(RB)
    return emit(b, "bench-1-gauge", [
        "GAUGE. registration: one tick = top of proof, two ticks = right.",
        "lower right: arc ladder ALONG the clear's grain, gaps outer->inner",
        "  .030 .045 .060 .075 .090 .105 .120 .150 (rho).",
        "lower left: radial fan ACROSS the grain, 7 lines, spacing = r x 0.18",
        "  (.032 at the hub road, .10 at mid-field, .155 at the tips).",
        "upper left: straight V-wedge, DIAGONAL to grain, 0 -> .20 apex to mouth.",
        "upper right: arc/spiral wedge ALONG grain, .20 at the mouth -> 0 at apex.",
    ], outdir)


def bead(b, cx, cy, r, contact):
    """one full circle of radius r centred (cx, cy) in the proof frame, begun
    and ended at the point in direction `contact` (a proof-frame unit vector)
    from the centre — i.e. hung from a string that touches it there."""
    mx, my = -contact[0], contact[1]          # proof -> math frame
    b.circle(-cx, cy, r, start=math.atan2(my, mx), ccw=True)


# =====================================================================
# SHEET 2 — ORDER: does the later line win?
# =====================================================================
def triplet(b, x0, ya, yb, s, order, ext=0.10, lane=0.10):
    """three parallel strokes at x0, x0+s, x0+2s spanning ya..yb (core).
    Enters on stroke 1's lead at the ya side, leaves past the yb side onto
    the lane. order 'seq' = 1,2,3 serpentine; 'mid' = 1,3,2 (middle last,
    which leaves by crossing the far bar)."""
    d = 1 if yb > ya else -1
    A = ya - d * ext          # bar on the entry side
    Z = yb + d * ext          # bar on the exit side
    Lz = Z + d * lane         # exit lane
    x1, x2, x3 = x0, x0 + s, x0 + 2 * s
    b.to(x1, A)
    if order == "seq":
        b.to(x1, Z); b.to(x2, Z); b.to(x2, A); b.to(x3, A); b.to(x3, Lz)
    else:
        b.to(x1, Z); b.to(x3, Z); b.to(x3, A); b.to(x2, A); b.to(x2, Lz)
    return Lz


def sheet_order(outdir):
    b = B()
    b.registration_open()                      # ends on the border at 356
    # ---- crossings, upper field ----------------------------------------
    yA = 0.48
    xa0, xa1 = -0.62, 0.62
    # to A's left end over the top (anticlockwise), then A left-to-right FIRST
    aL = 180 - math.degrees(math.asin(yA / RB))
    b.along_border(aL, ccw=True)
    b.to(xa0, yA)
    b.to(xa1, yA)                              # A
    # up and over the top to the left side, into the crossers
    aR = math.degrees(math.asin(yA / RB))
    b.to(*P(RB, aR + 8))
    b.along_border(128.0, ccw=True)
    b.to(-0.45, 0.70)
    b.to(-0.45, 0.26)                          # c90, downward
    b.to(-0.37, 0.26)
    b.to(-0.15 + 0.22, 0.48 + 0.22)            # c45, upward to the right
    t20 = math.tan(math.radians(20)); hx = 0.235
    b.to(0.43 - hx, yA + hx * t20)
    b.to(0.43 + hx, yA - hx * t20)             # c20, shallow, downward
    # flip test: back to A's left end by the border, retrace A through c90
    # to x = -0.25 and home again: the c90 crossing gets A on top of it last
    b.to(*P(RB, 20.0))
    b.along_border(aL, ccw=True)
    b.to(xa0, yA)
    b.to(-0.25, yA)
    b.to(xa0, yA)
    b.to(*P(RB, aL))
    # ---- triplets, lower field --------------------------------------------
    # cores y -0.05 .. -0.35 ; bars at +0.05 / -0.45 ; lanes +0.15 / -0.55
    # cores y -0.20 .. -0.46 ; bars at -0.12 / -0.56 ; lanes -0.02 / -0.66
    # the lane that crosses the middle is the LOWER one, well clear of the hub
    top, bot = -0.20, -0.46
    a_lane = 180 + math.degrees(math.asin(0.66 / RB))
    b.along_border(a_lane, ccw=True)
    specs = [(-0.62, 0.065, "seq", bot, top), (-0.30, 0.065, "mid", top, bot),
             (0.06, 0.085, "seq", bot, top), (0.40, 0.085, "mid", top, bot)]
    for (x0, s, order, ya, yb) in specs:
        lane_y = 0.0 if ya == top else -0.66
        b.to(x0, lane_y)
        triplet(b, x0, ya, yb, s, order)
    b.to(*P(RB, 360 - math.degrees(math.asin(0.66 / RB))))
    return emit(b, "bench-2-order", [
        "ORDER. registration: one tick = top of proof, two ticks = right.",
        "upper field: line A (horizontal) drawn FIRST, left to right; then crossed",
        "  at 90 (left), 45 (middle), 20 degrees (right). afterwards A is retraced",
        "  from its left end through the 90 crossing and back. does the later",
        "  line read on top? does the retrace put A back on top?",
        "lower field, left to right: triplets at .065 sequential | .065 middle-",
        "  last | .085 sequential | .085 middle-last. does the stroke drawn last",
        "  stay clean while its neighbours silt up?",
    ], outdir)


# =====================================================================
# SHEET 3 — STROKE: retrace, offset, pearls, corners, position
# =====================================================================
def sheet_stroke(outdir):
    b = B()
    b.registration_open()                       # ends on the border at 356
    # ---- (A) tick comb from the border, upper left ------------------------
    kinds = [("x2", 0), ("x4", 0), ("x8", 0), ("off", 0.012), ("off", 0.025), ("off", 0.040)]
    rin = 0.62
    for k, (kind, off) in enumerate(kinds):
        a = 104.0 + 12.0 * k
        b.along_border(a, ccw=True)
        if kind.startswith("x"):
            for _ in range(int(kind[1:]) // 2):
                b.rad_to(rin); b.rad_to(RB)
        else:
            b.rad_to(rin)
            ux, uy = P(1.0, a); nx, ny = -uy, ux
            b.to(rin * ux + off * nx, rin * uy + off * ny)
            b.to(RB * ux + off * nx, RB * uy + off * ny)
            b.to(*P(RB, a))
    # ---- (B) pearls on a string ---------------------------------------------
    ys = -0.30
    b.along_border(180 + math.degrees(math.asin(0.30 / RB)), ccw=True)
    for x, r in zip([-0.66, -0.50, -0.30, -0.04, 0.30], [0.020, 0.035, 0.050, 0.070, 0.100]):
        b.to(x, ys)
        bead(b, x, ys + r, r, (0.0, -1.0))
    b.to(0.62, ys)
    # ---- (C) zigzag, apex angles 90 60 30 15, below the string ------------
    x, y = 0.70, -0.50
    b.to(x, y)
    for ang in (90, 60, 30, 15):
        h = math.radians(ang / 2)
        dx, dy = 0.16 * math.sin(h), 0.16 * math.cos(h)
        b.to(x - dx, y - dy)
        x -= 2 * dx
        b.to(x, y)
        x -= 0.10
        b.to(x, y)
    # ---- (D) position: one r=.06 circle at rho .80 .55 .30 on the 25deg ray,
    #          hung from a string that runs parallel to the ray ------------------
    b.to(x, -0.80)
    b.to(*P(RB, 258.0))
    ray = 25.0
    u = P(1.0, ray); n = (-u[1], u[0])
    off = -0.06                                   # string on the clockwise side
    s_border = math.sqrt(RB ** 2 - off ** 2)
    b.along_border(360.0 + math.degrees(math.atan2(off * n[1] + s_border * u[1],
                                                   off * n[0] + s_border * u[0])) % 360, ccw=True)
    b.to(s_border * u[0] + off * n[0], s_border * u[1] + off * n[1])
    for s in (0.80, 0.55, 0.30):
        c = (s * u[0], s * u[1])
        b.to(c[0] + off * n[0], c[1] + off * n[1])
        bead(b, c[0], c[1], 0.06, (-n[0], -n[1]))
    b.to(0.20 * u[0] + off * n[0], 0.20 * u[1] + off * n[1])
    return emit(b, "bench-3-stroke", [
        "STROKE. registration: one tick = top of proof, two ticks = right.",
        "upper left, six ticks from the border, anticlockwise: retraced x2, x4, x8;",
        "  then in-and-out on parallel lines .012, .025, .040 apart. watch the",
        "  inner tips too: does each reversal leave a pearl of sand?",
        "middle: five circles hung on a string, r = .020 .035 .050 .070 .100 —",
        "  which are rings, which are coals, which raise a boss in the middle?",
        "below: zigzag with apex angles 90, 60, 30, 15 — where do corners pile?",
        "right: the same r=.06 circle at rho .80, .55, .30 — does position warp it?",
    ], outdir)


# =====================================================================
# SHEET 4 — RELIEF, COIL, COAL: the technique bets
# =====================================================================
def coil(b, x0, x1, y0, amp, pitch, n_steps=1400):
    sgn = 1 if x1 > x0 else -1
    turns = abs(x1 - x0) / pitch
    v = pitch / TAU
    def fn(f):
        t = f * turns * TAU
        return (x0 + sgn * (v * t - amp * math.sin(t)), y0 - amp * math.cos(t))
    b.curve(fn, n_steps)


def coal(b, cx, cy, R0, sp, woven):
    """enter at the left edge; spiral in at pitch sp; woven = come back out
    half a turn out of phase (Ashlar's interleave). leaves at the right edge."""
    b.to(cx - R0, cy)
    rmin = 0.006
    turns = (R0 - rmin) / sp
    n = int(turns * 180)
    a_start = math.pi                       # proof-frame angle of the left edge
    for i in range(1, n + 1):
        f = i / n
        a = a_start - turns * TAU * f       # clockwise in the proof
        rr = R0 + (rmin - R0) * f
        b.at(cx + rr * math.cos(a), cy + rr * math.sin(a))
    if woven:
        a0 = a_start - turns * TAU - math.pi
        for i in range(1, n + 1):
            f = i / n
            a = a0 - turns * TAU * f
            rr = rmin + (R0 - rmin) * f
            b.at(cx + rr * math.cos(a), cy + rr * math.sin(a))
    b.to(cx + R0 + 0.02, cy)               # out through the right edge


def sheet_relief(outdir):
    b = B()
    b.registration_open()                       # ends at the border, 356
    # ---- (A) relief ring (right) and trough ring (left) -------------------
    cR, cL, r = (0.36, 0.62), (-0.36, 0.62), 0.14
    b.along_border(58.0, ccw=True)
    b.to(cR[0], cR[1] + r + 0.055)
    bead(b, cR[0], cR[1], r + 0.055, (0, 1))
    b.to(cR[0], cR[1] + r - 0.055)
    bead(b, cR[0], cR[1], r - 0.055, (0, 1))
    b.to(cR[0], cR[1] + r + 0.055)
    b.to(cL[0], cL[1] + r)
    bead(b, cL[0], cL[1], r, (0, 1))
    b.to(*P(RB, 112.0))
    # ---- (B) coils: upper left-to-right, lower right-to-left ---------------
    AMP, PITCH = 0.09, 0.17
    b.along_border(165.0, ccw=True)
    b.to(-0.62, 0.26 - AMP)
    coil(b, -0.62, 0.62, 0.26, AMP, PITCH)
    b.to(0.70, 0.0)
    b.to(0.62, -0.26 - AMP)
    coil(b, 0.62, -0.62, -0.26, AMP, PITCH)
    # ---- (C) coals, left to right: .035 single | .02 single | .02 woven ------
    b.to(-0.70, -0.50)
    for (cx, kind, sp) in ((-0.40, False, 0.035), (0.0, False, 0.02), (0.40, True, 0.02)):
        coal(b, cx, -0.62, 0.10, sp, kind)
    b.to(*P(RB, 318.0))
    return emit(b, "bench-4-relief", [
        "RELIEF / COIL / COAL. registration: one tick = top, two ticks = right.",
        "upper left: a plain trough ring r .14. upper right: the same ring drawn",
        "  as RELIEF: passes at r .085 and .195; the ridge between is the figure.",
        "  which reads as the line?",
        "middle: two identical coils (prolate cycloids); upper drawn left-to-",
        "  right, lower right-to-left. if the later stroke reads on top at each",
        "  crossing, their loops should seem to twist opposite ways.",
        "bottom, left to right: coal spiralled in at .035 | in at .020 | woven",
        "  in-and-out at .020. bright, dark, or scraped to walnut?",
    ], outdir)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    os.makedirs(out, exist_ok=True)
    for fn in (sheet_gauge, sheet_order, sheet_stroke, sheet_relief):
        pts = fn(out)
        L = sum(math.dist((r0 * math.cos(t0), r0 * math.sin(t0)), (r1 * math.cos(t1), r1 * math.sin(t1)))
                for (t0, r0), (t1, r1) in zip(pts, pts[1:])) * 155 / 1000
        print(f"{fn.__name__}: {len(pts)} pts, {L:.1f} m")
