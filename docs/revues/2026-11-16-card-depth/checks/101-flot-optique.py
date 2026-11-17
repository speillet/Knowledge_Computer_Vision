"""Recompute the constructed numbers added to CV-FLOT-001 and CV-FLOT-004 and the
coordinates of cv-flot-aperture.svg (reference 101-flot-optique, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/101-flot-optique.py
Constraint line and its distance |E_t|/|grad E|: Horn and Schunck 1981, Sec. 4, Fig. 1.
Forward-backward tolerance |w + w_hat|^2 < 0.01 (|w|^2 + |w_hat|^2) + 0.5: Sundaram,
Brox and Keutzer 2010, Sec. 4, eq. 5. OpenCV rule: samples/python/lk_track.py L56-L59
at tag 4.13.0 (max over axes of |p0 - p0r| < 1).
"""
import math

checks = 0
EPS = 1e-12


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# --- CV-FLOT-001: normal flow at an edge ------------------------------------------
gx, gy, it = 6.0, 8.0, -20.0
norm = math.hypot(gx, gy)
dn = (-it * gx / norm**2, -it * gy / norm**2)
assert close(dn[0], 1.2) and close(dn[1], 1.6)
assert close(math.hypot(*dn), 2.0) and close(abs(it) / norm, 2.0)   # HS Fig. 1 distance
checks += 1

d = (2.0, 1.0)
assert close(gx * d[0] + gy * d[1] + it, 0.0)                # true flow on the line
tang = (d[0] - dn[0], d[1] - dn[1])
assert close(tang[0], 0.8) and close(tang[1], -0.6)
assert close(math.hypot(*tang), 1.0)
assert close(tang[0] * gx + tang[1] * gy, 0.0)                # along the edge
# every point dn + s * tangent satisfies the same equation
for s in (-3.0, -1.0, 0.5, 2.0):
    p = (dn[0] + 0.8 * s, dn[1] - 0.6 * s)
    assert close(gx * p[0] + gy * p[1] + it, 0.0)
checks += 1


# --- CV-FLOT-001: corner, normal equations and eigenvalues -------------------------
def normal_eq(rows):
    a = sum(r[0] * r[0] for r in rows)
    b = sum(r[0] * r[1] for r in rows)
    c = sum(r[1] * r[1] for r in rows)
    rhs = (sum(-r[2] * r[0] for r in rows), sum(-r[2] * r[1] for r in rows))
    return a, b, c, rhs


def eig2(a, b, c):
    tr, det = a + c, a * c - b * b
    disc = math.sqrt(tr * tr / 4 - det)
    return tr / 2 + disc, tr / 2 - disc


corner = [(6.0, 8.0, -20.0), (0.0, 10.0, -10.0)]
a, b, c, rhs = normal_eq(corner)
assert (a, b, c) == (36.0, 48.0, 164.0) and rhs == (120.0, 260.0)
det = a * c - b * b
sol = ((c * rhs[0] - b * rhs[1]) / det, (-b * rhs[0] + a * rhs[1]) / det)
assert close(sol[0], 2.0) and close(sol[1], 1.0)
assert close(0 * 2 + 10 * 1 - 10, 0.0)                        # second line v = 1
lmax, lmin = eig2(a, b, c)
assert close(lmax, 180.0) and close(lmin, 20.0)
checks += 1

edge = [(6.0, 8.0, -20.0), (6.0, 8.0, -20.0)]
a2, b2, c2, _ = normal_eq(edge)
lmax2, lmin2 = eig2(a2, b2, c2)
assert close(lmax2, 200.0) and close(lmin2, 0.0, 1e-6)
assert close(a + c, a2 + c2)                                  # equal traces, 200
checks += 1


# --- CV-FLOT-004: occlusion band in 1-D ---------------------------------------------
W, x0, x1, motion = 120, 40, 60, 6        # object occupies [40, 60) in I1, moves +6
def obj1(x): return x0 <= x < x1
def obj2(x): return x0 + motion <= x < x1 + motion
fwd = [motion if obj1(x) else 0 for x in range(W)]          # on the I1 grid
bwd = [-motion if obj2(x) else 0 for x in range(W)]         # on the I2 grid
fwd_bad = [x for x in range(W) if fwd[x] + bwd[x + fwd[x]] != 0]
bwd_bad = [y for y in range(W) if bwd[y] + fwd[y + bwd[y]] != 0]
assert fwd_bad == list(range(60, 66))      # background ahead, covered in I2
assert bwd_bad == list(range(40, 46))      # background behind, uncovered in I2
assert len(fwd_bad) == len(bwd_bad) == motion
checks += 1


# --- CV-FLOT-004: Sundaram tolerance against the 1 px per-axis rule -----------------
def sundaram_ok(w, wh):
    lhs = (w[0] + wh[0]) ** 2 + (w[1] + wh[1]) ** 2
    rhs = 0.01 * (w[0] ** 2 + w[1] ** 2 + wh[0] ** 2 + wh[1] ** 2) + 0.5
    return lhs < rhs, lhs, rhs


def lk_track_ok(w, wh):
    return max(abs(w[0] + wh[0]), abs(w[1] + wh[1])) < 1


ok, lhs, rhs = sundaram_ok((0, 0), (-6, 0))
assert not ok and close(lhs, 36) and close(rhs, 0.86)
ok, lhs, rhs = sundaram_ok((6, 0), (-6, 0))
assert ok and close(lhs, 0) and close(rhs, 1.22)
ok, lhs, rhs = sundaram_ok((20, 0), (-18.8, 0.4))
assert ok and close(lhs, 1.6) and abs(rhs - 8.04) < 0.005
assert not lk_track_ok((20, 0), (-18.8, 0.4))                 # 1.2 px on x
assert math.sqrt(0.5) < 0.71                                  # tolerance at zero motion
checks += 1


# --- Figure coordinates (cv-flot-aperture.svg) ---------------------------------------
OX, OY, K = 110.0, 400.0, 80.0                                # velocity space, v down
def px(u, v): return (OX + K * u, OY + K * v)
assert px(*dn) == (206.0, 528.0) and px(*d) == (270.0, 480.0)
assert px(-0.3, (20 + 1.8) / 8) == (86.0, 618.0)              # line end at u = -0.3
end = px((20 + 2.4) / 6, -0.3)
assert close(end[0], 408.6667, 1e-3) and close(end[1], 376.0)
assert px(0, 1)[1] == 480.0
# right-angle mark at dn, size 10 along -g and +t
g, t = (0.6, 0.8), (0.8, -0.6)
p1 = (206 - 10 * g[0], 528 - 10 * g[1]); p3 = (206 + 10 * t[0], 528 + 10 * t[1])
assert (round(p1[0], 6), round(p1[1], 6)) == (200, 520) and (round(p3[0], 6), round(p3[1], 6)) == (214, 522)
# windows: centre (140, 170) and (400, 170), 30 px per px/frame
S = 30.0
assert (140 + S * dn[0], 170 + S * dn[1]) == (176.0, 218.0)
assert (140 + S * d[0], 170 + S * d[1]) == (200.0, 200.0)
assert (400 + S * d[0], 170 + S * d[1]) == (460.0, 200.0)
# dashed edge at t+1 passes through (200, 200) along t: endpoints (80, 290) and (250, 162.5)
for (x, y) in ((80, 290), (250, 162.5)):
    assert close((x - 200) * g[0] + (y - 200) * g[1], 0.0)
assert close((540 - 460) * g[0] + (140 - 200) * g[1], 0.0)    # corner's moved oblique edge
checks += 1

print(f"101-flot-optique (CV-FLOT-001, CV-FLOT-004, figure): {checks} checks passed")
