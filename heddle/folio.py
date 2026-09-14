import math, os, random
from thrlib import Builder, preview, RIM, HUB, TAU

OUT = "/home/claude/folio/heddle"
os.makedirs(OUT, exist_ok=True)
MAKER = "Heddle (Claude Fable 5.1), 2026-09-13"
FOLIO = "folio VII (A Week at the Loom), the keeper's commission for seven days of light"


def emit(b, name, intent):
    pts = b.write(f"{OUT}/{name}.thr", [f"{name}.thr  \u2014  {MAKER}", intent,
                                          f"one continuous line; rho<={RIM}; {FOLIO}"])
    preview(pts, f"{OUT}/{name}-preview.png")
    print(name, len(pts))


def chord_ends(x):
    """y at which the vertical x meets the circle rho=0.95"""
    return math.sqrt(max(0.0, 0.95 ** 2 - x * x))


# ----------------------------------------------------------------------
# 1. heddle — the namesake
# ----------------------------------------------------------------------
def heddle():
    b = Builder()
    R = 0.95
    sp, bow, band = 0.075, 0.024, 0.22
    xs = [sp * (k + 0.5) for k in range(-12, 12)]
    for i, x in enumerate(xs):
        h = chord_ends(x)
        ys = [h - (2 * h) * j / 400 for j in range(401)]
        if i % 2: ys = ys[::-1]
        s = 1 if i % 2 else -1          # odd threads lifted right, even left
        pts = []
        for y in ys:
            xb = x
            if abs(y) < band:
                xb = x + s * bow * math.sin(math.pi * (y + band) / (2 * band))
            pts.append((xb, y))
        if i == 0:
            b.xy(*pts[0])
        else:
            # rim return to the top/bottom of the next thread
            th_to = math.atan2(pts[0][1], pts[0][0])
            b.arc(R, th_to)
        for p in pts[1:]:
            b.xy(*p)
    # wefts: the one passing in the open shed, then three beaten in below
    b.arc(R, 0.0)                              # to (0.95, 0)
    b.line_to_xy(-R, 0.0)                      # the passing weft, right to left
    for k, y in enumerate([-0.32, -0.44, -0.56]):
        hx = chord_ends(y)
        if k % 2 == 0:
            b.arc(R, math.atan2(y, -hx)); b.line_to_xy(hx, y)
        else:
            b.arc(R, math.atan2(y, hx)); b.line_to_xy(-hx, y)
    b.radial(RIM)
    emit(b, "heddle",
         "the maker's namesake: a full warp, and across its middle the shed lifted \u2014 odd threads drawn one way, even the other, so lanes open where the pairs part and fuse where they close; one weft laid in the open shed, three already beaten in below. the hub knot is honest: threads that cross the centre ride the hub.")


# ----------------------------------------------------------------------
# 2. selvedge — the bounded cloth
# ----------------------------------------------------------------------
def selvedge():
    random.seed(7)
    b = Builder()
    X0, X1, Y0, Y1, sp = -0.55, 0.55, -0.45, 0.45, 0.10
    xs = [X0 + sp * k for k in range(12)]
    ys = [Y0 + sp * k for k in range(10)]
    off = 0.012
    # enter from the rim to the top-left corner
    th = math.atan2(Y1, X0)
    b.polar(th, RIM); b.radial(math.hypot(X0, Y1))
    # warp raster, selvedge threads doubled
    b.line_to_xy(X0, Y0); b.line_to_xy(X0 + off, Y0); b.line_to_xy(X0 + off, Y1)
    for k, x in enumerate(xs[1:], start=1):
        if k % 2:  # go down
            b.line_to_xy(x, Y1); b.line_to_xy(x, Y0)
        else:
            b.line_to_xy(x, Y0); b.line_to_xy(x, Y1)
    # k=11 is odd: we are at (X1, Y0); double the right selvedge
    b.line_to_xy(X1 - off, Y0); b.line_to_xy(X1 - off, Y1); b.line_to_xy(X1, Y1); b.line_to_xy(X1, Y0)
    # weft raster from the hem upward
    for j, y in enumerate(ys):
        if j % 2 == 0:
            b.line_to_xy(X1, y); b.line_to_xy(X0, y)
        else:
            b.line_to_xy(X0, y); b.line_to_xy(X1, y)
    # j=9 odd: at (X1, Y1). top fringe, right to left, tips frayed
    for x in xs[::-1]:
        tx = x + random.uniform(-0.02, 0.02); ty = 0.75 + random.uniform(-0.03, 0.02)
        b.line_to_xy(x, Y1); b.line_to_xy(tx, ty); b.line_to_xy(x, Y1)
    # down the left selvedge to the bottom fringe
    b.line_to_xy(X0, Y0)
    for x in xs:
        tx = x + random.uniform(-0.02, 0.02); ty = -0.75 + random.uniform(-0.02, 0.03)
        b.line_to_xy(x, Y0); b.line_to_xy(tx, ty); b.line_to_xy(x, Y0)
    # out to the rim on the corner's own ray
    b.radial(RIM)
    emit(b, "selvedge",
         "the bounded cloth: a plain weave, its two selvedges doubled where the weft turned home, its two cut edges fringed with frayed warp ends. bounded, not brief \u2014 there is an edge to the cloth and the threads that cross it are carried by someone else.")


# ----------------------------------------------------------------------
# 3. the-second-trireme — Mytilene, 427
# ----------------------------------------------------------------------
def second_trireme():
    b = Builder()
    th0 = math.pi / 2
    # the first ship: six turns out, unhurried
    b.spiral(th0, th0 + 14 * math.pi, HUB, 0.95)
    # the mole at Mytilene: a short bold rim tick
    b.arc(0.95, th0 + 14 * math.pi + 0.14, direction=+1)
    b.arc(0.95, th0 + 14 * math.pi - 0.14, direction=-1)
    b.arc(0.95, th0 + 14 * math.pi, direction=+1)
    # the second ship: four turns, traced home from the landing, oars beating
    oar = lambda th, f: 0.012 * math.sin(24 * th)
    b.spiral(th0 + 14 * math.pi, th0 + 6 * math.pi, 0.95, HUB, mod=oar)
    emit(b, "the-second-trireme",
         "Thucydides 3.49: the assembly reversed itself overnight and a second ship rowed after the first with the reprieve. the first spiral goes out in seven turns; the second, traced back from the same landing, makes the crossing in four with its oars beating; it arrives as the decree is being read. the crossings are the story. sleeps at the hub.")


# ----------------------------------------------------------------------
# 4. kleroterion — the allotment machine
# ----------------------------------------------------------------------
def kleroterion():
    b = Builder()
    FX0, FX1, FY0, FY1 = -0.60, 0.56, -0.62, 0.62
    cols = [-0.50, -0.20, 0.10, 0.40]
    rows = [0.55 - 0.10 * k for k in range(12)]
    tick = 0.10
    TL, TR, TC, BR = 0.58, 0.72, 0.65, 0.035
    # enter to the top-left corner, draw the slab's frame
    b.polar(math.atan2(FY1, FX0), RIM); b.radial(math.hypot(FX0, FY1))
    b.line_to_xy(FX1, FY1); b.line_to_xy(FX1, FY0); b.line_to_xy(FX0, FY0); b.line_to_xy(FX0, FY1)
    # the slot columns, boustrophedon; each slot a retraced tick
    for c, xc in enumerate(cols):
        down = (c % 2 == 0)
        if down:
            b.line_to_xy(xc, FY1)
            for y in rows:
                b.line_to_xy(xc, y); b.line_to_xy(xc + tick, y); b.line_to_xy(xc, y)
            b.line_to_xy(xc, FY0)
        else:
            b.line_to_xy(xc, FY0)
            for y in rows[::-1]:
                b.line_to_xy(xc, y); b.line_to_xy(xc + tick, y); b.line_to_xy(xc, y)
            b.line_to_xy(xc, FY1)
    # four columns: ends at (0.40, FY1). walk the frame to the tube
    b.line_to_xy(FX1, FY1); b.line_to_xy(FX1, FY0); b.line_to_xy(TL, FY0)
    b.line_to_xy(TL, FY1)                      # left wall
    b.line_to_xy(TC, FY1)                      # across the mouth
    # the bead chain: white ball, black ball, white ball ...
    for i, yc in enumerate(rows):
        b.line_to_xy(TC, yc + BR)
        if i % 2 == 0:
            b.circle(TC, yc, BR, start=math.pi / 2)
            b.line_to_xy(TC, yc - BR)
        else:
            # black: spiral in from the top to the heart, then straight out the bottom
            n = 300; turns = 2.5
            for j in range(1, n + 1):
                f = j / n
                a = math.pi / 2 + turns * TAU * f
                rr = BR + (0.005 - BR) * f
                b.xy(TC + rr * math.cos(a), yc + rr * math.sin(a))
            b.line_to_xy(TC, yc - BR)
    b.line_to_xy(TC, FY0); b.line_to_xy(TR, FY0); b.line_to_xy(TR, FY1)   # right wall
    b.radial(RIM)
    emit(b, "kleroterion",
         "the allotment machine: a slab of slots in four columns, each slot a retraced tick, and the tube at its side down which the white and black balls dropped \u2014 white a ring, black a fused coal \u2014 the row of citizens beside each ball chosen or sent home. the fourth-century machinery, drawn as ornament.")


# ----------------------------------------------------------------------
# 5. horatius — the bridge
# ----------------------------------------------------------------------
def horatius():
    b = Builder()
    LB, RB = -0.42, -0.18
    P = (-0.44, 0.0)
    def bank(x0, amp, phase):
        h = chord_ends(x0)
        return [(x0 + amp * math.sin(3.2 * y + phase), y) for y in [h - 2 * h * j / 300 for j in range(301)]]
    lb = bank(LB, 0.02, 0.4)
    rb = bank(RB, 0.02, 1.7)
    # left bank, top to bottom
    b.xy(*lb[0])
    for p in lb[1:]: b.xy(*p)
    # rim return to the bottom of the right bank, then up it
    b.arc(0.95, math.atan2(rb[-1][1], rb[-1][0]))
    for p in rb[::-1][1:]: b.xy(*p)
    # the host: a fan of spears rooted at the bridgehead, rim to point to rim
    N = 19
    phis = [math.radians(100 + 160 * k / (N - 1)) for k in range(N)]
    for k, phi in enumerate(phis):
        rim = (0.95 * math.cos(phi), 0.95 * math.sin(phi))
        if k == 0:
            b.arc(0.95, phi)
            b.line_to_xy(*P)
        elif k % 2 == 1:
            b.line_to_xy(*rim)
        else:
            b.arc(0.95, phi)
            b.line_to_xy(*P)
    # three men on the bridge, shoulder to shoulder, fused into one bar
    for hx in (-0.40, -0.34, -0.28):
        b.blob(hx, 0.0, 0.022, r_in=0.004, turns=2.0)
    # the bridge to the break, the timbers falling downstream, the far bank
    b.line_to_xy(-0.24, 0.0)
    for p in [(-0.22, -0.07), (-0.21, -0.01), (-0.185, -0.09), (-0.16, -0.12)]:
        b.line_to_xy(*p)
    # the road home to the town
    ex, ey = 0.86, -0.42
    s = RIM / math.hypot(ex, ey)
    b.line_to_xy(ex * s, ey * s)
    emit(b, "horatius",
         "Macaulay's Lay: the Tiber in two wobbling banks; the Tuscan host as a fan of spears converging on the bridgehead; three men on the bridge fused into one bar; the bridge drawn to its break and the timbers going downstream; one straight road home to the town. the British republican Rome I forgot to mention.")


# ----------------------------------------------------------------------
# 6. caesar-cicero-vergil — four years of Latin as one spiral
# ----------------------------------------------------------------------
def ccv():
    b = Builder()
    # year one/two: Caesar. a square spiral of straight pulls, camp by camp
    r0, r1 = 0.16, 0.40
    verts = [(k * math.pi / 2, r0 + (r1 - r0) * k / 8) for k in range(9)]
    b.polar(*verts[0])
    for th, r in verts[1:]:
        b.line_to_xy(r * math.cos(th), r * math.sin(th))
    # year three: Cicero. two turns, each revolution three clauses swelling to a cadence
    def period(th, f):
        u = (th % TAU) / TAU
        j = int(u * 3); v = u * 3 - j
        amp = (0.008, 0.016, 0.024)[j] * math.sin(math.pi * v)
        return amp * math.sin(14 * th)
    b.radial(0.44)
    b.spiral(4 * math.pi, 8 * math.pi, 0.44, 0.68, mod=period)
    # year four: Vergil. two turns of hexameter, one line per revolution
    D = [(2, 0.020), (1, 0.012), (1, 0.012)]
    S = [(2, 0.020), (2, 0.020)]
    line = D + S + D + S + D + S            # 24 units
    starts, acc = [], 0
    for w, h in line:
        starts.append((acc, w, h)); acc += w
    def hexameter(th, f):
        u = (th % TAU) / TAU * 24
        for st, w, h in starts:
            if st <= u < st + w:
                return h * math.sin(math.pi * (u - st) / w)
        return 0.0
    b.radial(0.71)
    b.spiral(8 * math.pi, 12 * math.pi, 0.71, 0.94, mod=hexameter)
    b.radial(RIM)
    emit(b, "caesar-cicero-vergil",
         "the American Latin sequence as one spiral: Caesar in straight pulls, camp by camp; Cicero in periods, three clauses a turn swelling to the cadence; Vergil in hexameter, six feet a revolution, dactyl and spondee, the fifth foot always running. what the Committee of Twelve fixed in 1899, drawn as three bands of one line.")


# ----------------------------------------------------------------------
# 7. weft-pass — the mark kept
# ----------------------------------------------------------------------
def weft_pass():
    b = Builder()
    ang = math.radians(-32)
    d = (math.cos(ang), math.sin(ang))
    n = (-math.sin(ang), math.cos(ang))
    p = (0.30 * n[0], 0.30 * n[1])
    L = math.sqrt(RIM ** 2 - 0.30 ** 2)
    A = (p[0] - L * d[0], p[1] - L * d[1])
    B = (p[0] + L * d[0], p[1] + L * d[1])
    X = (A[0] + 1.5 * L * d[0], A[1] + 1.5 * L * d[1])
    E1 = (X[0] + 0.055 * n[0], X[1] + 0.055 * n[1])
    E2 = (X[0] - 0.055 * n[0], X[1] - 0.055 * n[1])
    b.xy(*A)
    b.line_to_xy(*X)
    b.line_to_xy(*E1); b.line_to_xy(*E2); b.line_to_xy(*X)
    b.line_to_xy(*B)
    emit(b, "weft-pass",
         "the quilt's mark, kept: one long line that leaves the field, and near where it leaves, one short thread crossing it at right angles \u2014 the weft over the warp, the crossing doubled so it plows deeper and reads on top. a mark, not a message; the week's last word.")


if __name__ == "__main__":
    heddle(); selvedge(); second_trireme(); kleroterion(); horatius(); ccv(); weft_pass()
