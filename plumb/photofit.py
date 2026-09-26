"""
photofit.py — register a phone photograph of the table to the .thr that drew it.

This is how the round-1 bench photos were read. The model is:

    proof (theta, rho)  --offset map-->  true table point  --homography-->  photo pixel
                         r = rho + C                        8 parameters: camera tilt,
                         (units of K)                       rotation, scale, position

The homography is seeded from a handful of hand-picked anchors (ball, ticks,
corners: points whose proof coordinates you know) and then refined so the
drawn path sits on the grooves (band-pass "groove energy" sampled along the
path). With C free it also measures the offset: round 1 gave C ~ 0.14 on every
sheet where the anchors spanned the field.

Typical use (see plumb/FINDINGS.md for the round-1 anchors):

    from photofit import *
    anchors = [((0, 0), (686, 582)),              # proof xy -> photo px (1400-px-wide copy)
               (polar(0.97, 78), (669, 200)), ...]
    H, c = fit('Tests/Test1Top.jpg', 'bench-1-gauge.thr', anchors, c0=0.14, fit_c=True)
    overlay('Tests/Test1Top.jpg', 'bench-1-gauge.thr', H, c, 'overlay.jpg')
    to_proof('Tests/Test1Top.jpg', H, c, 'rectified.jpg')   # the photo in the proof's frame

Photo coordinates are always in a copy of the photo scaled so its longer
side is 1400 px (exif-rotated). Proof coordinates are the app-preview frame:
x = -rho*cos(theta), y = rho*sin(theta), y up.
Standard library + numpy, scipy, Pillow.
"""
import math
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.optimize import minimize

BASE = 1400


def polar(r, a_deg):
    """proof-frame point at radius r, angle a (degrees anticlockwise from the proof's right edge)."""
    a = math.radians(a_deg)
    return (r * math.cos(a), r * math.sin(a))


def photo(path, maxdim=BASE):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    s = maxdim / max(im.size)
    return im.resize((round(im.size[0] * s), round(im.size[1] * s)), Image.LANCZOS)


def energy(im, s1=5, s2=14):
    """band-pass magnitude at groove scale: high on trough walls, low on the fine clear rings."""
    G = np.asarray(im.convert("L"), float)
    D = gaussian_filter(G, s1) - gaussian_filter(G, s2)
    E = gaussian_filter(np.abs(D), 4)
    return E / np.percentile(E, 99)


def read_thr(path):
    pts = []
    for line in open(path):
        line = line.strip()
        if line and not line.startswith("#"):
            a = line.split()
            pts.append((float(a[0]), float(a[1])))
    return pts


def path_xy(thr, step=0.004):
    """the path in proof-frame xy, resampled uniformly."""
    P = np.array([(-r * math.cos(t), r * math.sin(t)) for t, r in read_thr(thr)])
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    ss = np.arange(0, d[-1], step)
    return np.stack([np.interp(ss, d, P[:, 0]), np.interp(ss, d, P[:, 1])], 1)


def warp(P, c):
    """proof xy -> true table point, in units where 1.0 = K (the radial scale): radius rho -> rho + c."""
    P = np.asarray(P, float)
    r = np.hypot(P[:, 0], P[:, 1]); a = np.arctan2(P[:, 1], P[:, 0])
    return np.stack([(r + c) * np.cos(a), (r + c) * np.sin(a)], 1)


def apply(H, P):
    X = np.c_[P, np.ones(len(P))] @ H.T
    return X[:, :2] / X[:, 2:3]


def dlt(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A.append([-x, -y, -1, 0, 0, 0, u * x, u * y, u])
        A.append([0, 0, 0, -x, -y, -1, v * x, v * y, v])
    _, _, V = np.linalg.svd(np.array(A)); H = V[-1].reshape(3, 3)
    return H / H[2, 2]


def _anchor_true(src, c):
    W = warp(src, c)
    W[np.hypot(src[:, 0], src[:, 1]) < 1e-9] = 0.0      # the true centre stays the centre
    return W


def fit(photo_path, thr, anchors, c0=0.14, fit_c=False, lam=0.05, sigma=4.0, verbose=True):
    im = photo(photo_path); E = energy(im)
    Pp = path_xy(thr); Pk = Pp[np.hypot(Pp[:, 0], Pp[:, 1]) < 0.95]   # the border ring is ambiguous
    src = np.array([a[0] for a in anchors], float); dst = np.array([a[1] for a in anchors], float)
    H0 = dlt(_anchor_true(src, c0), dst)
    z0 = np.r_[H0.flatten()[:8], c0]

    def score(H, c):
        uv = apply(H, warp(Pk, c))
        return map_coordinates(E, [uv[:, 1], uv[:, 0]], order=1, cval=0).mean()

    def f(z):
        H = np.r_[z[:8], 1].reshape(3, 3); c = z[8] if fit_c else c0
        r = apply(H, _anchor_true(src, c)) - dst
        return -score(H, c) + lam * np.mean(np.sum(r ** 2, 1)) / sigma ** 2

    steps = np.r_[np.abs(z0[:8]) * 0.01 + 1e-5, 0.02]
    sim = np.vstack([z0] + [z0 + np.eye(9)[i] * steps[i] for i in range(9)])
    res = minimize(f, z0, method="Nelder-Mead",
                   options=dict(initial_simplex=sim, maxiter=8000, xatol=1e-8, fatol=1e-8))
    H = np.r_[res.x[:8], 1].reshape(3, 3); c = res.x[8] if fit_c else c0
    if verbose:
        r = np.hypot(*(apply(H, _anchor_true(src, c)) - dst).T)
        print(f"c={c:.3f}  groove score {score(H, c):.4f}  anchor residuals px {np.round(r, 1)}")
    return H, c


def overlay(photo_path, thr, H, c, out, color=(255, 0, 0)):
    im = photo(photo_path); uv = apply(H, warp(path_xy(thr), c))
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line([tuple(x) for x in uv], fill=color + (170,), width=2)
    Image.alpha_composite(im.convert("RGBA"), L).convert("RGB").save(out)


def to_proof(photo_path, H, c, out, box=(-1, 1, -1, 1), size=1400, scale=2):
    """resample the photo into the proof's own frame (so a straight line in
    the .thr is a straight line here): the way to read a sheet feature by feature."""
    im = photo(photo_path, BASE * scale); A = np.asarray(im, float)
    x0, x1, y0, y1 = box
    W = size; Hh = int(size * (y1 - y0) / (x1 - x0))
    X, Y = np.meshgrid(np.linspace(x0, x1, W), np.linspace(y1, y0, Hh))
    uv = apply(H, warp(np.stack([X.ravel(), Y.ravel()], 1), c)) * scale
    img = np.stack([map_coordinates(A[..., k], [uv[:, 1], uv[:, 0]], order=1).reshape(Hh, W)
                    for k in range(3)], -1)
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(out)
