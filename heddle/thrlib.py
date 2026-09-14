import math, random
from PIL import Image, ImageDraw

RIM = 0.97      # quiet border
HUB = 0.14      # centre dead zone: the ball rides the hub rim below this
STEP = 0.005    # charter sampling, ~0.8mm of arc
TAU = 2 * math.pi


class Builder:
    """One continuous theta-rho line. theta accumulates (unwrapped); rho is
    clamped to [HUB, RIM]. Segments may be given in xy (unit disc) or polar."""

    def __init__(self):
        self.pts = []  # (theta, rho)

    # -- primitives -----------------------------------------------------
    def _push(self, th, r):
        r = max(HUB, min(RIM, r))
        if self.pts:
            th0 = self.pts[-1][0]
            k = round((th0 - th) / TAU)
            th += TAU * k
        self.pts.append((th, r))

    def polar(self, th, r):
        """append one polar point (theta taken mod 2pi, nearest branch)."""
        self._push(th, r)

    def xy(self, x, y):
        self._push(math.atan2(y, x), math.hypot(x, y))

    def line_xy(self, x0, y0, x1, y1, step=STEP):
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(math.ceil(d / step)))
        for i in range(1, n + 1):
            t = i / n
            self.xy(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)

    def poly_xy(self, pts, step=STEP):
        if not self.pts:
            self.xy(*pts[0]); pts = pts[1:]
        else:
            # if we are not at the first point, pull straight to it
            self.line_to_xy(*pts[0])
            pts = pts[1:]
        for (x, y) in pts:
            x0, y0 = self.last_xy()
            self.line_xy(x0, y0, x, y, step)

    def line_to_xy(self, x, y, step=STEP):
        x0, y0 = self.last_xy()
        self.line_xy(x0, y0, x, y, step)

    def last_xy(self):
        th, r = self.pts[-1]
        return r * math.cos(th), r * math.sin(th)

    def last(self):
        return self.pts[-1]

    def arc(self, r, th_to, direction=None, step=STEP):
        """constant-radius arc from current angle to angle th_to (absolute, any
        branch). direction: +1 ccw, -1 cw, None = shorter way."""
        th0 = self.pts[-1][0]
        d = (th_to - th0) % TAU
        if direction is None:
            if d > math.pi: d -= TAU
        elif direction > 0:
            d = d if d > 1e-9 else d + TAU
        else:
            d = d - TAU if d > 1e-9 else d
        n = max(1, int(math.ceil(abs(d) * r / step)))
        for i in range(1, n + 1):
            self.pts.append((th0 + d * i / n, max(HUB, min(RIM, r))))

    def radial(self, r_to, step=STEP):
        th, r0 = self.pts[-1]
        n = max(1, int(math.ceil(abs(r_to - r0) / step)))
        for i in range(1, n + 1):
            self.pts.append((th, max(HUB, min(RIM, r0 + (r_to - r0) * i / n))))

    def spiral(self, th0, th1, r0, r1, mod=None, dth=0.004):
        """archimedean from (th0,r0) to (th1,r1); mod(theta, frac) adds rho."""
        n = max(2, int(math.ceil(abs(th1 - th0) / dth)))
        for i in range(0, n + 1):
            f = i / n
            th = th0 + (th1 - th0) * f
            r = r0 + (r1 - r0) * f
            if mod: r += mod(th, f)
            self.pts.append((th, max(HUB, min(RIM, r))))

    def blob(self, cx, cy, r_out, r_in=0.004, turns=2.0, spacing=None):
        """interleaved fused disc at (cx,cy): in-spiral then half-phase out-spiral.
        enters at the left edge (angle pi) and leaves at the right edge (angle 0)."""
        if spacing: turns = (r_out - r_in) / spacing
        self.line_to_xy(cx + r_out * math.cos(math.pi), cy + r_out * math.sin(math.pi))
        n = int(turns * 120)
        for i in range(1, n + 1):
            f = i / n
            a = math.pi + turns * TAU * f
            rr = r_out + (r_in - r_out) * f
            self.xy(cx + rr * math.cos(a), cy + rr * math.sin(a))
        a0 = math.pi + turns * TAU + math.pi
        for i in range(1, n + 1):
            f = i / n
            a = a0 + turns * TAU * f
            rr = r_in + (r_out - r_in) * f
            self.xy(cx + rr * math.cos(a), cy + rr * math.sin(a))
        # a0 + turns*TAU ≡ pi + pi = 0 mod 2pi: exits at the right edge

    def circle(self, cx, cy, r, start=math.pi / 2, ccw=True):
        """one full circle beginning and ending at angle `start`."""
        self.line_to_xy(cx + r * math.cos(start), cy + r * math.sin(start))
        n = max(12, int(math.ceil(TAU * r / STEP)))
        s = 1 if ccw else -1
        for i in range(1, n + 1):
            a = start + s * TAU * i / n
            self.xy(cx + r * math.cos(a), cy + r * math.sin(a))

    # -- finish ---------------------------------------------------------
    def finish(self, step=STEP):
        """subdivide any polar step longer than `step` (hub-riding arcs, long
        pulls) so the file is uniformly sampled; return the list."""
        out = [self.pts[0]]
        for (t0, r0), (t1, r1) in zip(self.pts, self.pts[1:]):
            arc = math.hypot(r1 - r0, ((r0 + r1) / 2) * (t1 - t0))
            n = max(1, int(math.ceil(arc / step)))
            for i in range(1, n + 1):
                f = i / n
                out.append((t0 + (t1 - t0) * f, r0 + (r1 - r0) * f))
        self.pts = out
        return out

    def write(self, path, header_lines):
        pts = self.finish()
        with open(path, "w") as fh:
            for h in header_lines:
                fh.write("# " + h + "\n")
            for th, r in pts:
                fh.write(f"{th:.6f} {r:.5f}\n")
        return pts


def preview(pts, path, size=720, bg=(43, 36, 30), fg=(232, 219, 190)):
    im = Image.new("RGB", (size, size), bg)
    dr = ImageDraw.Draw(im)
    C = size / 2
    S = size / 2 * 0.94
    dr.ellipse([C - S, C - S, C + S, C + S], outline=(110, 98, 84), width=1)
    poly = [(C - r * S * math.cos(t), C - r * S * math.sin(t)) for t, r in pts]
    dr.line(poly, fill=fg, width=1)
    im.save(path)
