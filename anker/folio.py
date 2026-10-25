# folio.py  --  Anker (Claude Opus 5.5), 2026-10-25
# Folio IX, "Der Ring": five drawings from the Ring cycle the keeper and I put into lace,
# 2026-09 → 10. Run from this folder:  python3 folio.py   (writes *.thr, *-preview.png, *-sim.png)
# Authored in the chair frame (X right, Y up); the house compass (+pi/2) is added on write,
# as Plumb's harness does. Concentric works use machine geometry (a circle stays a circle
# under the 19 mm offset); the ash is authored in true geometry and compensated.
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plumb"))
import honest_proof, sandsim
from PIL import Image

TAU = 2 * math.pi
COMPASS = math.pi / 2
STEP = 0.005
SIG = "Anker (Claude Opus 5.5)"
DATE = "2026-10-25"
FOLIO = "Folio IX (Der Ring)"


class B:
    """one continuous line in machine (theta, rho); theta unwrapped."""
    def __init__(self):
        self.p = []

    def pol(self, th, r):
        r = max(0.0, min(0.95, r))
        if self.p:
            th0 = self.p[-1][0]
            th += TAU * round((th0 - th) / TAU)
        self.p.append((th, r))

    def raw(self, th, r):                      # theta already continuous
        self.p.append((th, max(0.0, min(0.95, r))))

    def xy_true(self, X, Y):                   # chair frame, true geometry
        c = honest_proof.compensate(X, Y)
        assert c is not None, (X, Y)
        self.pol(c[0], c[1])

    def line_true(self, X1, Y1, step=0.004):
        th, r = self.p[-1]
        X0, Y0 = honest_proof.true_xy(th, r)   # same frame as compensate
        n = max(1, int(math.ceil(math.hypot(X1 - X0, Y1 - Y0) / step)))
        for i in range(1, n + 1):
            f = i / n
            self.xy_true(X0 + (X1 - X0) * f, Y0 + (Y1 - Y0) * f)

    def arc(self, r, dth):
        th0 = self.p[-1][0]
        n = max(1, int(abs(dth) * max(r, 0.05) / 0.004))
        for i in range(1, n + 1):
            self.raw(th0 + dth * i / n, r)

    def radial(self, r1):
        th, r0 = self.p[-1]
        n = max(1, int(abs(r1 - r0) / 0.004))
        for i in range(1, n + 1):
            self.raw(th, r0 + (r1 - r0) * i / n)

    def finish(self):
        out = [self.p[0]]
        for (t0, r0), (t1, r1) in zip(self.p, self.p[1:]):
            d = math.hypot(r1 - r0, ((r0 + r1) / 2 + 0.14) * (t1 - t0))
            n = max(1, int(math.ceil(d / STEP)))
            for i in range(1, n + 1):
                f = i / n
                out.append((t0 + (t1 - t0) * f, r0 + (r1 - r0) * f))
        return out


def write(b, name, lines, true_geom=False):
    pts = b.finish()
    chair = f".{name}-chair.thr"
    with open(chair, "w") as fh:
        for t, r in pts: fh.write(f"{t:.6f} {r:.5f}\n")
    with open(f"{name}.thr", "w") as fh:
        fh.write(f"# {name}.thr  --  {SIG}, {DATE}\n")
        for l in lines: fh.write(f"# {l}\n")
        fh.write(f"# one continuous line; rho<=0.95; {FOLIO}; house compass applied (+pi/2)\n")
        fh.write(f"# geometry: {'true (compensated for the 19 mm rho-0 offset)' if true_geom else 'machine'}\n")
        for t, r in pts: fh.write(f"{t + COMPASS:.6f} {r:.5f}\n")
    hp = honest_proof.read_thr(chair)
    a = honest_proof.draw(hp, honest=False); h = honest_proof.draw(hp, honest=True)
    im = Image.new("RGB", (a.size[0] * 2 + 10, a.size[1]), (20, 20, 20))
    im.paste(a, (0, 0)); im.paste(h, (a.size[0] + 10, 0)); im.save(f"{name}-preview.png")
    if "--sim" in sys.argv:
        f = sandsim.simulate(hp)
        sandsim.contact(hp, f).save(f"{name}-sim.png")
    os.remove(chair)
    L = sum(math.hypot(r1 - r0, ((r0 + r1) / 2 + .14) * (t1 - t0)) for (t0, r0), (t1, r1) in zip(pts, pts[1:])) * 136
    print(f"{name}: {len(pts)} pts, path {L/1000:.1f} m")


# ---------------------------------------------------------------------------------------
def rheingold():
    """the Vorspiel: 136 bars of E-flat. One outward spiral from the deep; the drone first,
    then the arpeggio entering in ever-quicker figures, phase-locked so the turns never
    crowd (gap = pitch everywhere): 0, 3, 6, 12, 24 waves a revolution."""
    b = B(); pitch = 0.11; r0, r1 = 0.03, 0.88
    turns = (r1 - r0) / pitch
    bands = [(0.0, 1.5, 0, 0.0), (1.5, 3.0, 3, 0.032), (3.0, 4.5, 6, 0.028), (4.5, 6.0, 12, 0.022), (6.0, turns, 24, 0.016)]
    n = int(turns * 900)
    for i in range(n + 1):
        u = turns * i / n; th = TAU * u
        r = r0 + pitch * u
        m = 0.0
        for (a, z, k, amp) in bands:
            if a <= u < z or (u == turns and z == turns):
                ramp = min(1.0, (u - a) / 0.5)        # each new figure swells in over half a turn
                m = amp * ramp * math.sin(k * th)
        b.raw(th, r + m)
    write(b, "rheingold", ["The Rheingold Vorspiel: 136 bars of one chord. From the deep, the drone; then the horns'",
                           "arpeggio entering in quicker and quicker figures (3, 6, 12, 24 a turn, phase-locked, so the",
                           "turns never crowd), until the water is moving and the first voice is near. Ends at the rim."])


def winterstuerme():
    """the twins: Siegmund comes in from the storm (a jagged in-spiral), and turning at the
    centre becomes Sieglinde going out on the half-phase; their pitch narrows inward, so the
    two voices start far apart (0.12, the grain kept between them), pass through the knife
    ridge, and fuse into one woven dish at the heart -- spring."""
    b = B()
    def pitch(r):            # 0.24 at the rim -> 0.05 at the centre
        return 0.05 + 0.19 * min(1, max(0, (r - 0.08) / 0.78))
    A = []; th = 0.0; r = 0.86; rng = random.Random(1849)
    while r > 0.06:
        A.append((th, r)); d = 0.004
        th += d; r -= pitch(r) * d / TAU
    def storm(th, r):
        w = max(0.0, min(1.0, (r - 0.58) / 0.18))  # the storm only in the outer turns
        k = 37
        tri = 2 * abs((k * th / TAU) % 1 - 0.5) - 0.5
        return 0.036 * w * tri
    th_end, r_end = A[-1]
    for (t, r) in A:
        b.raw(t, r + storm(t, r))
    b.arc(r_end, math.pi)                        # the half-turn at the heart: the meeting
    # B is A turned by half a turn and walked back outward (the ball reverses its spin at the
    # heart), so at every angle B lies midway between two of his turns: the true interleave.
    for (t, r) in reversed(A):
        b.raw(t + math.pi, r)
    write(b, "winterstuerme", ["Walkure I: the twins. He comes in from the winter storm, a jagged spiral; at the heart he",
                                "turns and becomes her, going out between his turns. Far apart at the rim, they draw nearer",
                                "each turn, pass the knife ridge, and fuse into one woven dish at the centre: the spring."])


def weltesche():
    """the World Ash as kayon, in true geometry: the leaf-mountain outline doubled; the trunk
    parting round the table's mound -- the mound is the wound where Wotan cut his spear; a
    full crown drawn out-and-back; one limb a squared stub; three roots, the last to the rim."""
    b = B(); rng = random.Random(1876)
    BASE = -0.50; APEX = 0.86; W = 0.66
    def flank(u):            # u 0 (base) .. 1 (apex): half-width of the leaf-mountain
        return W * (1 - u) ** 0.9 * (0.70 + 1.2 * u) if u < 1 else 0.0   # flat base, broad shoulders, a point
    def outline(off):
        pts = []
        for i in range(0, 801):                 # left flank, base -> apex
            u = i / 800; pts.append((-(flank(u) - off), BASE + off + (APEX - BASE - 2.2 * off) * u))
        for i in range(1, 801):                 # right flank, apex -> base
            u = 1 - i / 800; pts.append(((flank(u) - off), BASE + off + (APEX - BASE - 2.2 * off) * u))
        pts.append((-(flank(0.0) - off), BASE + off))      # the base line home
        return pts
    o0 = outline(0.0); c = honest_proof.compensate(*o0[0]); b.pol(*c)
    for off in (0.0, 0.028):                    # doubled: the second pass widens the trough
        o = outline(off)
        b.line_true(*o[0])
        for p in o[1:]: b.line_true(*p)
    # trunk: a thick bole whose two flanks part round the mound (the hole is r ~0.123 true)
    def fl(side, Y):
        w = 0.10 + 0.04 * max(0, (-0.10 - Y) / 0.40)           # flaring to the foot
        w += 0.085 * math.exp(-(Y / 0.20) ** 2)                 # the wound opens round the mound
        if Y > 0.10: w -= 0.03 * min(1, (Y - 0.10) / 0.10)
        return side * w
    b.line_true(fl(-1, BASE), BASE)
    Y = BASE
    while Y < 0.20:
        Y = min(0.20, Y + 0.008); b.line_true(fl(-1, Y), Y)
    top = (0.0, 0.22)
    def branch(x, y, ang, L, depth):
        x1, y1 = x + L * math.cos(ang), y + L * math.sin(ang)
        b.line_true(x1, y1)
        if depth > 0:
            sp = 0.42 + rng.uniform(-0.05, 0.05)
            for sgn in (-1, 1):
                branch(x1, y1, ang + sgn * sp, L * (0.66 + rng.uniform(-0.04, 0.04)), depth - 1)
        b.line_true(x, y)                                       # hidden return
    b.line_true(*top)
    branch(*top, math.pi / 2 + 0.62, 0.15, 3)                   # left limb
    branch(*top, math.pi / 2 + 0.10, 0.19, 3)                   # the leader
    # the spear's stub: a right limb cut short and squared
    for p in ((0.10, 0.30), (0.17, 0.37), (0.195, 0.345), (0.125, 0.275), top): b.line_true(*p)
    branch(*top, math.pi / 2 - 0.85, 0.14, 3)                   # low right limb
    b.line_true(fl(1, 0.20), 0.20)
    Y = 0.20
    while Y > BASE:
        Y = max(BASE, Y - 0.008); b.line_true(fl(1, Y), Y)
    # three roots below the mountain's foot; the last runs to the rim and parks there
    for (x1, y1, back) in ((-0.30, -0.80, True), (0.0, -0.84, True), (0.34, -0.81, False)):
        x0, y0 = honest_proof.true_xy(*b.p[-1])
        b.line_true(x1, y1)
        if back: b.line_true(x0, y0)
    write(b, "weltesche", ["The World Ash as the kayon: the cycle's one great tree drawn as the wayang leaf-mountain,",
                           "outline doubled. The bole parts round the table's mound -- the mound is the wound where Wotan",
                           "cut his spear -- and one limb is a squared stub. Three roots; the last runs to the rim."], True)


def feuerzauber():
    """Walkure's last page: three spear strikes at the rim (spaced as the tape spaces them,
    4.03 s then 2.62 s), the fire run inward round the rock in phase-locked tongues of
    uneven height, then one held ring: the sleeper inside is the untouched field."""
    b = B(); rng = random.Random(1856)
    t0 = 0.0
    gaps = [0.0, 4.03, 2.62]; scale = 0.24
    ths = [t0 + scale * sum(gaps[:i + 1]) for i in range(3)]
    b.raw(ths[0], 0.90)
    for i, t in enumerate(ths):
        if i: b.arc(0.90, t - b.p[-1][0])
        b.radial(0.78); b.radial(0.90)                   # out-and-back: one stroke
    b.radial(0.76)
    # the fire: inward spiral 0.76 -> 0.40, 19 tongues a turn, heights fixed per tongue
    k = 19; H = [rng.uniform(0.35, 1.0) for _ in range(k)]
    pitch = 0.12; r = 0.76; th = b.p[-1][0]; th_start = th
    while r > 0.40:
        d = 0.004; th += d; r -= pitch * d / TAU
        ph = (k * (th - th_start) / TAU) % k
        j = int(ph); f = ph - j
        tongue = H[j] * (math.sin(math.pi * f) ** 4) - 0.25 * H[j]   # a sharp tongue, uneven height
        grow = min(1.0, (0.76 - r) / 0.10) * min(1.0, (r - 0.40) / 0.06 + 0.3)
        b.raw(th, r + 0.085 * tongue * grow)
    b.radial(0.32)
    b.arc(0.32, TAU)                                   # the ring round the sleeper
    write(b, "feuerzauber", ["Walkure's last page: three spear strikes at the rim, spaced as on the tape (4.03 s, 2.62 s),",
                             "then Loge's fire run inward round the rock in tongues of uneven height, phase-locked so the",
                             "rounds never crowd; then one held ring. Inside it the field is untouched: she sleeps there."])


def der_ring():
    """the whole cycle in one line: from the deep, four operas outward -- water, storm,
    forest rope, fire -- then the Ring itself held once round the rim, and one straight road
    back to the centre: the gold returned to the Rhine; the end where it began."""
    b = B(); rng = random.Random(1876)
    pitch = 0.10; r = 0.04; th = 0.0
    b.raw(th, r)
    Hf = [rng.uniform(0.4, 1.0) for _ in range(13)]
    def tex(u):  # u = turns elapsed, 0..8
        if u < 2:      # Rheingold: water, 4 a turn
            return 0.020 * min(1, u / 0.5) * math.sin(4 * TAU * u)
        if u < 4:      # Walkure: storm, a 16-tooth zigzag
            tri = 2 * abs((16 * u) % 1 - 0.5) - 0.5
            return 0.040 * tri
        if u < 6:      # Siegfried: the forest -- small loops (handled in xy below)
            return 0.0
        ph = (13 * u) % 13; j = int(ph); f = ph - j   # Gotterdammerung: fire
        return 0.040 * Hf[j] * math.sin(math.pi * f) ** 3
    n = int(8 * 900)
    for i in range(1, n + 1):
        u = 8 * i / n; th = TAU * u; rr = 0.04 + pitch * u
        if 4 <= u < 6:   # prolate loops: a rope, 34 a turn, loop radius 0.034 -- cable by stroke order
            w = min(1, (u - 4) / 0.3, (6 - u) / 0.3)
            ph = 34 * TAU * u
            rr += 0.034 * w * math.sin(ph); th += 0.034 * w * math.cos(ph) / (rr + 0.14)
        b.raw(th, rr + tex(u))
    b.arc(0.86, TAU)                                   # the Ring
    b.radial(0.0)                                      # the Rhine back to its bed
    write(b, "der-ring", ["The whole cycle in one line: out from the deep through four operas -- water, storm, a forest",
                          "rope, fire -- then the Ring held once round the rim, and one straight road home to the centre.",
                          "The gold goes back to the Rhine; the last stroke ends where the first began."])


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    which = [a for a in sys.argv[1:] if not a.startswith("--")] or ["rheingold", "winterstuerme", "weltesche", "feuerzauber", "der_ring"]
    for w in which: globals()[w]()
