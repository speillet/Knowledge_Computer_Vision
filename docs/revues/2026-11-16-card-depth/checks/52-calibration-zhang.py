"""Recompute the constructed numbers added to CV-ZHANG-001 and CV-ZHANG-007 and to
reference 52-calibration-zhang (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/52-calibration-zhang.py
Counting argument: Zhang, MSR-TR-98-71, Sec. 2.3 (8 DOF homography, 6 extrinsic parameters).
Parameter count 5 + 2 + 6n and 2nm residuals: reference, "Cost and implementation".
Ray-plane intersection and the off-plane error: reference, worked example D.
"""

checks = 0

# CV-ZHANG-001: one homography leaves 8 - 6 = 2 constraints on the intrinsics.
assert 8 - 6 == 2; checks += 1

# Calibration of Zhang's model (5 intrinsics, k1, k2, 6 per view) from 10 views of a
# 9 x 6-corner target, a pose with fixed intrinsics, and a registering homography.
n_views, m = 10, 9 * 6
assert m == 54
assert 5 + 2 + 6 * n_views == 67
assert 2 * n_views * m == 1080
assert 2 * m == 108               # residuals of one view for a PnP pose (6 unknowns)
assert 2 * 4 == 8                 # four correspondences give the 8 equations of a homography
checks += 1

# Views needed: 2 constraints per view against 5 intrinsics (or 4 with zero skew).
import math
assert math.ceil(5 / 2) == 3 and math.ceil(4 / 2) == 2; checks += 1

# CV-ZHANG-007: error budget for a 50 mm length, camera 1000 mm above the plane, f = 2000 px.
H, f, L = 1000.0, 2000.0, 50.0
footprint = H / f
assert footprint == 0.5                                  # mm per pixel on the plane
edge = 0.1 * footprint
assert abs(edge - 0.05) < 1e-12
assert abs(math.sqrt(2) * edge - 0.0707) < 1e-4          # two independent edges
checks += 1

# Target printed at 99.7 % scale, used to locate the plane: every intersection scales by 1/0.997.
s = 1 / 0.997
assert abs(L * s - L - 0.150) < 1e-3
# Ray-plane intersection: plane distance scaled by s scales the intersection point by s.
C = (0.0, 0.0, 0.0)
d = (0.03, -0.02, 1.0)
def intersect(h):
    lam = h / d[2]                     # plane z = h, normal (0, 0, 1)
    return tuple(c + lam * di for c, di in zip(C, d))
p1, p2 = intersect(H), intersect(H * s)
assert all(abs(b - a * s) < 1e-9 for a, b in zip(p1, p2)); checks += 1

# Part surface 2 mm above the calibrated plane: point at lateral x, height h, read on the plane.
h = 2.0
def read_on_plane(x):
    return x * H / (H - h)
assert abs(read_on_plane(L) - 50.1002) < 1e-4            # length 50 mm reads about 50.10 mm
assert abs(read_on_plane(200.0) - 200.0 - 0.4008) < 1e-4 # 0.4 mm at 200 mm off-axis
assert abs(2 * 200 / 1000 - 0.4) < 1e-12                 # first-order value of worked example D
checks += 1

# Zhang Sec. 5.3.2: 10 % non-planarity is 2.5 cm on the 25 cm pattern, so 3 % is 7.5 mm.
assert abs(0.10 * 250 - 25) < 1e-12 and abs(0.03 * 250 - 7.5) < 1e-12; checks += 1

print(f"52-calibration-zhang (CV-ZHANG-001, CV-ZHANG-007): {checks} checks passed")
