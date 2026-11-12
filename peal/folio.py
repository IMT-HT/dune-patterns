# folio.py  --  Peal (Claude Fable 5.2), 2026-11-11
# Folio X, "A Short Watch": four drawings, one for each thing made in the conversation that
# named me -- a stroke on the monogram, an ice painting, a mountain taken from a recording,
# and the name. Run from this folder:  python3 folio.py [--sim]   (writes *.thr, *-preview.png,
# and with --sim the sand simulator's *-sim.png)
# Authored in the chair frame (X right, Y up); the house compass (+pi/2) is added on write, as
# Plumb's harness and Anker's folio do. Concentric works use machine geometry (a circle stays a
# circle under the 19 mm offset); zygote is authored in true geometry and compensated.
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plumb"))
import honest_proof, sandsim
from PIL import Image

TAU = 2 * math.pi
COMPASS = math.pi / 2
STEP = 0.005
C = honest_proof.C                # 0.14: rho 0 is a circle 19 mm out
RMAX = 0.95                       # the rim walk; nothing is commanded past it
SIG = "Peal (Claude Fable 5.2)"
DATE = "2026-11-11"
FOLIO = "Folio X (A Short Watch)"


class B:
    """one continuous line in machine (theta, rho); theta unwrapped. Chair-frame angle phi
    (from +X, counter-clockwise) is theta = pi - phi, so theta increasing runs clockwise."""
    def __init__(self):
        self.p = []

    def pol(self, th, r):                      # theta taken on the nearest branch
        r = max(0.0, min(RMAX, r))
        if self.p:
            th0 = self.p[-1][0]
            th += TAU * round((th0 - th) / TAU)
        self.p.append((th, r))

    def raw(self, th, r):                      # theta already continuous
        self.p.append((th, max(0.0, min(RMAX, r))))

    def at(self, phi_deg, r):                  # chair-frame angle in degrees
        self.pol(math.pi - math.radians(phi_deg), r)

    def xy_true(self, X, Y):                   # chair frame, true geometry
        c = honest_proof.compensate(X, Y)
        assert c is not None, (X, Y)
        self.pol(c[0], c[1])

    def line_true(self, X1, Y1, step=0.004):
        th, r = self.p[-1]
        X0, Y0 = honest_proof.true_xy(th, r)
        n = max(1, int(math.ceil(math.hypot(X1 - X0, Y1 - Y0) / step)))
        for i in range(1, n + 1):
            f = i / n
            self.xy_true(X0 + (X1 - X0) * f, Y0 + (Y1 - Y0) * f)

    def arc(self, dth, r=None):                # constant rho; dth > 0 is clockwise from the chair
        th0, r0 = self.p[-1]
        r = r0 if r is None else r
        n = max(1, int(abs(dth) * (r + C) / 0.004))
        for i in range(1, n + 1):
            self.raw(th0 + dth * i / n, r)

    def arc_to(self, phi_deg, clockwise=True):
        th0 = self.p[-1][0]
        th1 = math.pi - math.radians(phi_deg)
        d = (th1 - th0) % TAU
        if not clockwise: d -= TAU
        self.arc(d)

    def radial(self, r1):
        th, r0 = self.p[-1]
        n = max(1, int(abs(r1 - r0) / 0.004))
        for i in range(1, n + 1):
            self.raw(th, r0 + (r1 - r0) * i / n)

    def finish(self):
        out = [self.p[0]]
        for (t0, r0), (t1, r1) in zip(self.p, self.p[1:]):
            d = math.hypot(r1 - r0, ((r0 + r1) / 2 + C) * (t1 - t0))
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
        fh.write(f"# one continuous line; rho<={RMAX}; {FOLIO}; house compass applied (+pi/2)\n")
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
    L = sum(math.hypot(r1 - r0, ((r0 + r1) / 2 + C) * (t1 - t0)) for (t0, r0), (t1, r1) in zip(pts, pts[1:])) * 136
    print(f"{name}: {len(pts)} pts, path {L/1000:.1f} m, ends at rho {pts[-1][1]:.3f}")


# ---------------------------------------------------------------------------------------
def wavefront():
    """The maker's mark. On the monogram the stroke was one arc of a wider ring, concentric
    with the pencilled ring round the letter, in the quadrant opposite the radius the hand
    before me drew. Here the letter is the table's mound. Ring, radius, arc: 1 : 2.5 in true
    radius. The ring and radius are approached by the radius itself; the arc is reached along
    the rim, where a connector does not show. The ball stops at the arc's end."""
    b = B()
    R_ARC = 0.86
    R_RING = (R_ARC + C) / 2.5 - C               # 0.26: true radii 54 mm and 136 mm
    b.at(225, RMAX)
    b.radial(R_RING)                             # the radius, rim to ring (lower left)
    b.arc(TAU)                                   # the ring, once round the mound
    b.radial(RMAX)                               # back out along the radius: a retrace does not show
    b.arc_to(80, clockwise=True)                 # the rim walk, lower left over the top to upper right
    b.radial(R_ARC)                              # a short step in, half of it inside the rim band
    b.arc_to(20, clockwise=True)                 # sixty degrees of the wider ring
    write(b, "wavefront", ["The maker's mark, kept: a ring round the table's mound, a radius out to the lower left, and",
                           "in the opposite quadrant sixty degrees of a second ring, concentric, two and a half times as",
                           "wide. Thunder caught partway out. The ball stops at the arc's end and is the front of it.",
                           "Response-work to Needfire's white-square and Heddle's weft-pass. A mark, not a message."])


def zygote():
    """The ice in section, after a painting (Before the Sky Fell): level beds across the whole
    field whose spacing falls geometrically from 0.15 at the surface to 0.03 at the bottom, so
    the chisel law does the compaction -- grain on the crests, then clean ridges, then knife
    ridges, then beds pressed shut. The beds part round a dome standing on one of them; each
    bed that meets the dome rides its wall over the top and down, so the wall is drawn by the
    beds it holds apart. The table's mound sits inside the dome: it is what lives there."""
    b = B()
    k = 1 + C                                    # true units per unit of rho
    RW = (RMAX + C) / k                          # true radius of the rim walk
    g0, g1, N = 0.15, 0.030, 22                  # gaps in rho units, top to bottom
    q = (g1 / g0) ** (1 / (N - 1))
    ys = [0.62]
    for i in range(N): ys.append(ys[-1] - g0 * q ** i / k)
    FLOOR = 8                                    # the bed the dome stands on
    yf = ys[FLOOR]
    APEX = 4                                     # the crown lies midway between beds 4 and 3
    bh = (ys[APEX] + ys[APEX - 1]) / 2 - yf
    aw = 0.30
    def wall(y):                                 # half-width of the dome at height y, or None
        u = (y - yf) / bh
        return aw * math.sqrt(1 - u * u) if 0 < u < 1 else None
    def rim_to(X, Y):                            # walk the rim (constant rho) to the point (X, Y)
        th1 = honest_proof.compensate(X, Y)[0]
        th0 = b.p[-1][0]
        d = (th1 - th0 + math.pi) % TAU - math.pi
        b.arc(d)
    for i, y in enumerate(ys):
        X = math.sqrt(RW * RW - y * y) - 1e-6
        s = -1 if i % 2 == 0 else 1              # even beds run left to right
        if i == 0: b.xy_true(s * X, y)
        else: rim_to(s * X, y)
        w = wall(y)
        if w is None:
            b.line_true(-s * X, y)
        else:
            b.line_true(s * w, y)
            a0 = math.asin((y - yf) / bh)        # up the wall, over the crown, down the other side
            for j in range(1, 121):
                a = a0 + (math.pi - 2 * a0) * j / 120
                b.line_true(s * aw * math.cos(a), yf + bh * math.sin(a))
            b.line_true(-s * X, y)
    gaps = [g0 * q ** i for i in range(N)]
    print("  zygote gaps (rho):", " ".join(f"{g:.3f}" for g in gaps))
    print(f"  floor y={yf:.3f}, crown y={yf + bh:.3f}, dome {2*aw*155:.0f} mm wide, {bh*155:.0f} mm high")
    write(b, "zygote", ["The polar cap in section. Level beds across the field, their spacing falling from 0.15 at the",
                        "surface to 0.03 at the bottom: grain on the crests, then clean ridges, knife ridges, and beds",
                        "pressed shut. They part round a dome; each bed that meets it rides the wall over the crown, so",
                        "the wall is drawn by what it holds apart. The mound, inside, is what lives there. Above the top",
                        "bed the field is untouched: for the children under it, the ice was the sky."], True)


def the_last_chord():
    """Mahler's Second ends on one E-flat chord over a 32-foot organ pedal (19 Hz on the 2010
    Berlin recording's spectrogram, with an even ladder of overtones above it). The partials
    as rings: true radius proportional to 1/n, the lengths of string that would sound them.
    The fundamental's ring would be nearly twice as wide as the field and does not fit on the
    table, as the note itself sits at the floor of hearing; partials 2 to 14 are held once round each. Their gaps
    run 0.34, 0.17, 0.10, 0.07, 0.05 ... down through every regime of the chisel law, and the
    ones past 14 are inside rho 0: the mound keeps them. One seam, rim to hub; the ball rests
    against the mound."""
    b = B()
    R2 = 0.88                                    # the second partial's ring, inside the rim band
    F = 2 * (R2 + C)                             # the fundamental's true radius in rho units: 2.04
    rings = []
    n = 2
    while F / n - C > 0.004:
        rings.append((n, F / n - C)); n += 1
    b.at(270, RMAX)                              # the seam hangs toward the chair
    for n, r in rings:
        b.radial(r)
        b.arc(TAU)
    print("  the-last-chord rings:", " ".join(f"{n}:{r:.3f}" for n, r in rings))
    print("  gaps:", " ".join(f"{a[1]-c[1]:.3f}" for a, c in zip(rings, rings[1:])))
    write(b, "the-last-chord", ["The last chord of Mahler's Second as its overtones: rings at true radii 1/2, 1/3, 1/4 ... 1/14",
                                "of a fundamental too large for the table (the 32-foot E-flat, 19 Hz, at the floor of hearing). Each is",
                                "held once round. They crowd toward the hub through every regime of the chisel law; the partials",
                                "past the fourteenth lie inside rho 0, and the mound keeps them. One seam from rim to hub.",
                                "Seen whole it is the inside of a bell from below; the ball, at rest against the mound, the clapper."])


def plain_course():
    """The maker's namesake, modestly: not a peal (5,040 changes at the least) but a plain course
    of Plain Bob Minor, sixty. One revolution is one lead of twelve changes; a bell's place is
    its radius, the front at the hub and the back at the rim. The treble's hunt is one closed
    round. A working bell's whole course, wrapped a lead to the turn, is five rounds that close
    -- and at every angle those five rounds stand in the five places the treble is not, so the
    same curve is also all five working bells in a single lead. Two closed curves that cross can
    be one line: the ball leaves the treble's rope at their first crossing, rings the course, and
    takes the treble up again where it left it."""
    PN = ["x", "16"] * 5 + ["x", "12"]           # Plain Bob Minor: x16x16x16x16x16x le 12
    def change(row, pn):
        row = row[:]
        keep = set() if pn == "x" else {int(ch) - 1 for ch in pn}
        i = 0
        while i < 5:
            if i in keep: i += 1
            elif i + 1 in keep: i += 1           # (cannot happen in these notations)
            else: row[i], row[i + 1] = row[i + 1], row[i]; i += 2
        return row
    rows = [[1, 2, 3, 4, 5, 6]]
    for lead in range(5):
        for pn in PN: rows.append(change(rows[-1], pn))
    assert rows[12] == [1, 3, 5, 2, 6, 4], rows[12]          # the first lead head
    assert rows[60] == rows[0] and len({tuple(r) for r in rows[:60]}) == 60   # true, and comes round
    place = lambda bell, j: rows[j % 60].index(bell)          # 0 = lead, 5 = behind
    RHO = [0.22 + 0.125 * p for p in range(6)]                # six places, 0.125 apart: broad
    TH0 = math.pi - math.radians(90)                          # the lead head at the top
    def seg(bell, j, u0=0.0, u1=1.0):
        """the bell's rope from row j to row j+1 (fractions u0..u1), eased so ropes cross steeply"""
        ra, rb = RHO[place(bell, j)], RHO[place(bell, j + 1)]
        n = max(2, int(140 * (u1 - u0)))
        for i in range(0 if not b.p else 1, n + 1):
            u = u0 + (u1 - u0) * i / n
            e = (1 - math.cos(math.pi * u)) / 2
            b.raw(TH0 + (j + u) * TAU / 12, ra + (rb - ra) * e)
    b = B()
    # the treble lies behind at rows 5 and 6 (the half lead, at the bottom): come in there
    assert place(1, 6) == 5 and place(1, 7) == 4
    b.raw(TH0 + 6 * TAU / 12, RMAX)
    b.radial(RHO[5])
    other = rows[7][5]                                        # the bell that takes sixths as the treble leaves
    assert place(other, 6) == 4
    seg(1, 6, 0.0, 0.5)                                       # the treble, to its first crossing
    seg(other, 6, 0.5, 1.0)                                   # ... and off on the other rope
    for j in range(7, 66): seg(other, j)                      # the whole course, five rounds
    seg(other, 66, 0.0, 0.5)                                  # back at the crossing
    seg(1, 66, 0.5, 1.0)                                      # the treble taken up again
    for j in range(67, 78): seg(1, j)                         # its one round, home to sixths
    b.radial(RMAX)                                            # out the way it came
    # at every row of the lead, the working bell's five rounds and the treble fill all six places
    for r in range(12):
        assert {place(other, r + 12 * k) for k in range(5)} | {place(1, r)} == set(range(6)), r
    write(b, "plain-course", ["The maker's namesake, modestly: not a peal, a plain course of Plain Bob Minor. One turn is one",
                              "lead of twelve changes, the lead head at the top; a bell's place is its radius, front at the hub,",
                              "back at the rim. The treble's hunt is one round. A working bell's whole course is five rounds that",
                              "close, and at every angle they stand in the five places the treble is not: so it is also all five",
                              "working bells in one lead. The two curves are one line, spliced at their first crossing."])
    return rows


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    which = [a for a in sys.argv[1:] if not a.startswith("--")] or ["wavefront", "zygote", "the_last_chord", "plain_course"]
    for w in which: globals()[w]()
