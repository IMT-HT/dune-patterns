from harness import *
b = sandlib.Builder(true_geometry=True)
R = 0.94; FACE = -0.36; H = 0.12
ys = [0.84 - H*k for k in range(15)]          # 0.84 .. -0.84
def rimx(y): return -math.sqrt(R*R - y*y)
# courses, top to bottom: out from the face to the rim with joint ticks (upward), then back
first = True
for k, y in enumerate(ys):
    x0 = rimx(y)
    if first: b.move(FACE, y); first = False
    else: b.line(FACE, y)
    # joints: staggered, 0.20 apart, ticks up to the course above (not for the top course)
    off = 0.10 if k % 2 else 0.0
    joints = []
    x = FACE - 0.14 - off
    while x > x0 + 0.06:
        joints.append(x); x -= 0.20
    for xj in joints:
        b.line(xj, y)
        if k > 0 and math.hypot(xj, y + H) < R - 0.02:
            b.line(xj, y + H); b.line(xj, y)
    b.line(x0, y)          # to the rim
    b.line(FACE, y)        # back along the same course (a retrace does not deepen)
# the face: one true vertical, bottom to top
b.line(FACE, ys[-1] - 0.04)
b.line(FACE, ys[0] + 0.05)
# the plumb: from the coping, a true line past the eye, to the bob; the ball parks in the bob
S = -0.17
b.line(S, 0.905)
b.line(S, -0.50)
b.circle(S, -0.55, 0.05, start=90)
b.line(S, -0.55)
finish(b, 'plumb', ["the namesake: a coursed ashlar wall and a plumb line hung beside its face. Both are drawn TRUE --",
    "compensated for the table's 19 mm offset -- so for once a straight line on this table is straight.",
    "The string passes the mound without bending; the ball comes to rest as the bob. A nod to the first hand."], '2026-09-28')
sim('plumb')
