"""Recompute the constructed examples of CV-SFM (reference 152-sfm-incrementale-globale).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-16-photogrammetry/checks/152-sfm-incrementale-globale.py

Every number below is a constructed example or arithmetic on a cited value. The
COLMAP conventions reproduced here were read in the 4.2.1 sources, not executed:
- visibility pyramid score: src/colmap/scene/visibility_pyramid.cc L39-L72 (level l, 0-based,
  has (2^(l+1))^2 cells; a newly occupied cell adds the number of cells of its level);
  6 levels: src/colmap/sfm/observation_manager.h L52-L53;
- global refinement trigger: src/colmap/controllers/incremental_pipeline.cc L543-L555 with
  ratio 1.1 and frequency 500 frames (incremental_pipeline.h L122-L124);
- AUC: benchmark/reconstruction/evaluation/utils.py L1561-L1590 (sorted errors, recall
  curve starting at (0, 0), trapezoid up to the threshold, divided by the threshold, x100).
No COLMAP, GLOMAP or Eigen code is executed.
"""

import bisect
import itertools
import math
from fractions import Fraction as F

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# ---------------------------------------------------------------------------------------
# Worked example A: what an uncontrolled reconstruction determines (similarity gauge).
# ---------------------------------------------------------------------------------------
def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def matvec(A, v):
    return [sum(A[i][k] * v[k] for k in range(3)) for i in range(3)]


def transpose(A):
    return [[A[j][i] for j in range(3)] for i in range(3)]


def project(R, t, X):
    """Ideal normalized projection of world point X for x_c = R X + t (cam_from_world)."""
    xc = [a + b for a, b in zip(matvec(R, X), t)]
    return (xc[0] / xc[2], xc[1] / xc[2])


Rz90 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
Rx90 = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
# Two cameras looking along +z; camera 2 has its centre at C2 = (3, 0, 0) (t2 = -R2 C2).
cams = [(I3, [F(0), F(0), F(0)]), (I3, [F(-3), F(0), F(0)])]
points = [[F(1), F(2), F(10)], [F(-2), F(1), F(12)], [F(4), F(-1), F(9)], [F(0), F(0), F(15)]]
s, Q, u = F(5, 2), matmul(Rz90, Rx90), [F(7), F(-3), F(2)]  # world similarity X' = sQX + u


def apply_similarity(cams, points, s, Q, u):
    new_points = [[s * a + b for a, b in zip(matvec(Q, X), u)] for X in points]
    new_cams = []
    for R, t in cams:
        # x_c = R X + t = R Q^T (X' - u) / s + t, scaled by s: same rays, pose (R Q^T, s t - R Q^T u)
        RQt = matmul(R, transpose(Q))
        new_cams.append((RQt, [s * a - b for a, b in zip(t, matvec(RQt, u))]))
    return new_cams, new_points


cams2, points2 = apply_similarity(cams, points, s, Q, u)
# Check 1: every projection is unchanged exactly (Fractions), distances scale by s = 5/2,
# distance ratios are unchanged.
for (R, t), (R2, t2) in zip(cams, cams2):
    for X, X2 in zip(points, points2):
        assert project(R, t, X) == project(R2, t2, X2)
d = lambda a, b: sum((x - y) ** 2 for x, y in zip(a, b))
assert d(points2[0], points2[1]) == s * s * d(points[0], points[1])
assert d(points2[0], points2[1]) * d(points[2], points[3]) == d(points[0], points[1]) * d(points2[2], points2[3])
checks += 1

# Check 2: holding camera 1's pose fixed leaves only the scalings about its centre C1:
# with Q = I and u = -(s - 1) C1, camera 1 is unchanged and C2' = C1 + s (C2 - C1).
# Fixing a coordinate of C2 with a non-zero baseline component forces s = 1; fixing a
# coordinate where the baseline component is 0 leaves s free. Gauge count 6 + 1 = 7.
C1, C2 = [F(0), F(0), F(0)], [F(3), F(0), F(4)]
for s_try in (F(2), F(1, 3)):
    u_try = [-(s_try - 1) * c for c in C1]
    C2_new = [s_try * c + v for c, v in zip(C2, u_try)]
    assert C2_new == [a + s_try * (b - a) for a, b in zip(C1, C2)]
    assert C2_new[0] != C2[0] and C2_new[2] != C2[2]   # x and z components move with s
    assert C2_new[1] == C2[1]                          # y component (baseline 0) does not
assert 6 + 1 == 7
checks += 1

# ---------------------------------------------------------------------------------------
# Worked example B: initial-pair gates and triangulation angles.
# ---------------------------------------------------------------------------------------
# Check 3: |t_z| < 0.95 for a unit translation means the baseline is more than 18.19 deg
# away from the optical axis.
assert close(math.degrees(math.acos(0.95)), 18.194872, 1e-6)
checks += 1


def tri_angle_deg(ca, cb, X):
    """Schonberger and Frahm eq. 3: angle between the rays from the two centres to X."""
    va = [a - x for a, x in zip(ca, X)]
    vb = [b - x for b, x in zip(cb, X)]
    na, nb = math.sqrt(sum(v * v for v in va)), math.sqrt(sum(v * v for v in vb))
    return math.degrees(math.acos(sum(a * b for a, b in zip(va, vb)) / (na * nb)))


# Check 4: symmetric configuration, alpha = 2 atan(b / 2d). Baseline/depth ratio needed for
# 16 deg is 0.2811 (5.62 m at 20 m); for 1.5 deg it is 0.0262 (0.52 m at 20 m). A 1 m baseline
# gives 2.86 deg at 20 m and 1.15 deg at 50 m.
assert close(tri_angle_deg([-0.5, 0, 0], [0.5, 0, 0], [0, 0, 20]), 2 * math.degrees(math.atan(0.5 / 20)))
assert round(2 * math.tan(math.radians(8)), 4) == 0.2811
assert round(20 * 2 * math.tan(math.radians(8)), 2) == 5.62
assert round(2 * math.tan(math.radians(0.75)), 4) == 0.0262
assert round(20 * 2 * math.tan(math.radians(0.75)), 2) == 0.52
assert round(tri_angle_deg([-0.5, 0, 0], [0.5, 0, 0], [0, 0, 20]), 2) == 2.86
assert round(tri_angle_deg([-0.5, 0, 0], [0.5, 0, 0], [0, 0, 50]), 2) == 1.15
# With a 1 m baseline the 1.5 deg gate is reached at d = 1 / (2 tan 0.75 deg) = 38.2 m.
assert round(1 / (2 * math.tan(math.radians(0.75))), 1) == 38.2
checks += 1

# ---------------------------------------------------------------------------------------
# Worked example C: next-best-view visibility pyramid (COLMAP 4.2.1 convention).
# ---------------------------------------------------------------------------------------
def pyramid_score(pts, W, H, L):
    full = [set() for _ in range(L)]
    score = 0
    maxdim = 1 << L
    for x, y in pts:
        cx = min(max(int(maxdim * x / W), 0), maxdim - 1)
        cy = min(max(int(maxdim * y / H), 0), maxdim - 1)
        for level in range(L - 1, -1, -1):
            if (cx, cy) not in full[level]:
                full[level].add((cx, cy))
                score += (1 << (level + 1)) ** 2
            cx >>= 1
            cy >>= 1
    return score


def grid(nx, ny, x0, x1, y0, y1):
    return [(x0 + (i + 0.5) * (x1 - x0) / nx, y0 + (j + 0.5) * (y1 - y0) / ny)
            for i in range(nx) for j in range(ny)]


W = H = 1024
# Check 5: three levels (weights 4, 16, 64): 16 spread points score 1296; 16 points in one
# quadrant score 1092; 64 points in the same quadrant still score 1092 (cells saturated).
assert pyramid_score(grid(4, 4, 0, W, 0, H), W, H, 3) == 16 + 256 + 1024 == 1296
assert pyramid_score(grid(4, 4, 0, W / 2, 0, H / 2), W, H, 3) == 4 + 64 + 1024 == 1092
assert pyramid_score(grid(8, 8, 0, W / 2, 0, H / 2), W, H, 3) == 1092
checks += 1

# Check 6: COLMAP's six levels: maximum score 17,895,696; 256 spread points 1,380,624 against
# 1,328,196 for 256 points in one quadrant (3.9 % apart); 576 points in that quadrant score
# 2,638,916 and beat the 256 spread points. The count dominates while points are few.
assert sum((1 << (l + 1)) ** 4 for l in range(6)) == 17895696
a6 = pyramid_score(grid(16, 16, 0, W, 0, H), W, H, 6)
b6 = pyramid_score(grid(16, 16, 0, W / 2, 0, H / 2), W, H, 6)
c6 = pyramid_score(grid(24, 24, 0, W / 2, 0, H / 2), W, H, 6)
assert (a6, b6, c6) == (1380624, 1328196, 2638916)
assert round(100 * (a6 - b6) / b6, 1) == 3.9 and c6 > a6
checks += 1

# ---------------------------------------------------------------------------------------
# Worked example D: what relative directions determine (translation averaging).
# ---------------------------------------------------------------------------------------
def direction(a, b):
    v = [y - x for x, y in zip(a, b)]
    n = math.sqrt(sum(c * c for c in v))
    return tuple(round(c / n, 12) for c in v)


# Check 7: three collinear cameras at x = 0, 10, 30 m. Any re-spacing along the line with
# the same order (here x3 = 50 m) gives the same three directions: the 10:20 spacing ratio
# is unobservable from camera-camera directions alone.
c1, c2, c3, c3b = (0, 0), (10, 0), (30, 0), (50, 0)
assert all(direction(p, q) == direction(p2, q2) for (p, q), (p2, q2) in
           zip([(c1, c2), (c1, c3), (c2, c3)], [(c1, c2), (c1, c3b), (c2, c3b)]))
checks += 1

# Check 8: a point P = (20, 10) m seen by the three cameras. With C1 = (0, 0) and C2 = (10, 0)
# fixed by the gauge, rays C1->P along (2, 1) and C2->P along (1, 1) intersect at P = (20, 10);
# the ray from C3 towards P along (-1, 1), meeting the line y = 0, gives C3 = (30, 0) exactly.
# Solve 2 t = 10 + v and t = v (Fractions).
t_ = F(10)
P = (2 * t_, 1 * t_)
assert P == (10 + t_, 0 + t_) == (20, 10)
w_ = P[1] / 1                       # C3 = P - w (-1, 1) with C3_y = 0
C3 = (P[0] + w_, P[1] - w_)
assert C3 == (30, 0)
checks += 1

# Check 9: nearly collinear triangle. C3 = (30, 1): direction angles 1.909 deg (from C1) and
# 2.862 deg (from C2), apex angle 0.953 deg. A 0.5 deg error on the C2 -> C3 direction moves
# the intersection to |C1C3| = 23.13 m or 52.11 m instead of 30.02 m.
a1, a2 = math.atan2(1, 30), math.atan2(1, 20)
dist = lambda a1, a2: 10 * math.sin(a2) / math.sin(a2 - a1)   # law of sines, |C1C2| = 10 m
assert (round(math.degrees(a1), 3), round(math.degrees(a2), 3)) == (1.909, 2.862)
assert round(math.degrees(a2 - a1), 3) == 0.953
assert close(dist(a1, a2), math.hypot(30, 1)) and round(dist(a1, a2), 2) == 30.02
assert round(dist(a1, a2 + math.radians(0.5)), 2) == 23.13
assert round(dist(a1, a2 - math.radians(0.5)), 2) == 52.11
checks += 1

# Check 10: rotation cycle (single axis, angles add): 30 + 40 - 70 = 0 deg; one wrong edge
# measured as 50 deg instead of 40 deg leaves a 10 deg cycle error.
assert 30 + 40 - 70 == 0 and 30 + 50 - 70 == 10
checks += 1

# Check 11: bounded errors. GLOMAP's global-positioning residual equals sin(theta) below 90 deg
# and 1 beyond; 1DSfM's chordal distance between unit vectors is 2 sin(theta / 2).
for deg, expected in ((2, 0.0349), (30, 0.5)):
    assert round(math.sin(math.radians(deg)), 4) == expected
for deg in (10, 60, 120):
    th = math.radians(deg)
    uvec, vvec = (1.0, 0.0), (math.cos(th), math.sin(th))
    assert close(math.dist(uvec, vvec), 2 * math.sin(th / 2))
    assert close(1 - (uvec[0] * vvec[0] + uvec[1] * vvec[1]), 2 * math.sin(th / 2) ** 2)
checks += 1

# ---------------------------------------------------------------------------------------
# Worked example E: duplicate structure.
# ---------------------------------------------------------------------------------------
# Check 12: Heinly et al. eq. 1 edge cost e = 1 - |Oi n Oj| / |Oi u Oj|. Two cameras on the
# same facade instance with surroundings: 300 and 260 points, 240 shared -> 1/4. Two cameras
# on different instances sharing only the 150 facade points out of 300 each -> 2/3.
edge = lambda oi, oj, inter: 1 - F(inter, oi + oj - inter)
assert edge(300, 260, 240) == F(1, 4) and edge(300, 300, 150) == F(2, 3)
checks += 1

# Check 13: a camera at 50 m from the tower axis registered to the facade 90 deg away is
# displaced by the chord 2 R sin(45 deg) = 70.71 m.
assert round(2 * 50 * math.sin(math.radians(45)), 2) == 70.71
checks += 1

# ---------------------------------------------------------------------------------------
# Worked example F: evaluation against a reference.
# ---------------------------------------------------------------------------------------
ref = [complex(0, 0), complex(40, 0), complex(40, 30), complex(0, 30), complex(20, 15)]  # metres
a0, b0 = 0.1j, complex(5, -2)        # model = 0.1 x (90 deg rotation) of metres + offset
offset = {1: 15j}                    # camera 2 misplaced 15 m north, others perfect
est = [a0 * (r + offset.get(i, 0)) + b0 for i, r in enumerate(ref)]


def fit_similarity(src, tgt):
    """Least-squares 2D similarity tgt ~ a src + b, a complex (rotation and scale)."""
    n = len(src)
    ms, mt = sum(src) / n, sum(tgt) / n
    a = sum((y - mt) * (x - ms).conjugate() for x, y in zip(src, tgt)) / sum(abs(x - ms) ** 2 for x in src)
    return a, mt - a * ms


# Check 14: before alignment the coordinate differences (5.39 to 47.20) mix model units and
# metres and mean nothing. Without the misplaced camera the alignment is exact (scale 10,
# rotation -90 deg, residuals 0).
raw = [abs(x - r) for x, r in zip(est, ref)]
assert (round(min(raw), 2), round(max(raw), 2)) == (5.39, 47.2)
clean = [a0 * r + b0 for r in ref]
a, b = fit_similarity(clean, ref)
assert close(abs(a), 10) and close(math.degrees(math.atan2(a.imag, a.real)), -90)
assert max(abs(a * x + b - r) for x, r in zip(clean, ref)) < 1e-9
checks += 1

# Check 15: least-squares alignment with the misplaced camera spreads its error: residuals
# 2.90, 9.25, 5.81, 1.21, 3.09 m (RMS 5.27 m), scale 10.29 (+2.9 %), rotation 7.51 deg off.
# Fitting on the four correct cameras (what a robust alignment keeps) gives 0 on them and
# 15.00 m on camera 2. Normal equations hold; Umeyama's scale tr(DS)/sigma_x^2 equals |a|.
a, b = fit_similarity(est, ref)
res = [abs(a * x + b - r) for x, r in zip(est, ref)]
assert [round(v, 2) for v in res] == [2.90, 9.25, 5.81, 1.21, 3.09]
assert round(math.sqrt(sum(v * v for v in res) / 5), 2) == 5.27
assert round(abs(a), 2) == 10.29 and round(-90 - math.degrees(math.atan2(a.imag, a.real)), 2) == 7.51
assert abs(sum(a * x + b - r for x, r in zip(est, ref))) < 1e-9
ms = sum(est) / 5
assert abs(sum((a * x + b - r) * (x - ms).conjugate() for x, r in zip(est, ref))) < 1e-9
# Umeyama eqs. 34-42 in 2D: Sigma_xy = (1/n) sum (y - mu_y)(x - mu_x)^T, c = tr(DS) / sigma_x^2.
mt = sum(ref) / 5
Sxy = [[0.0, 0.0], [0.0, 0.0]]
for x, y in zip(est, ref):
    xv, yv = (x - ms), (y - mt)
    xs, ys = (xv.real, xv.imag), (yv.real, yv.imag)
    for i in range(2):
        for j in range(2):
            Sxy[i][j] += ys[i] * xs[j] / 5
p, q, r_, s_ = Sxy[0][0], Sxy[0][1], Sxy[1][0], Sxy[1][1]
assert p * s_ - q * r_ > 0                              # det > 0, so S = I
trDS = math.hypot(p + s_, r_ - q)                       # sum of singular values of a 2x2 matrix
sigma_x2 = sum(abs(x - ms) ** 2 for x in est) / 5
assert close(trDS / sigma_x2, abs(a))
inl = [0, 2, 3, 4]
a2, b2 = fit_similarity([est[i] for i in inl], [ref[i] for i in inl])
res2 = [abs(a2 * x + b2 - r) for x, r in zip(est, ref)]
assert max(res2[i] for i in inl) < 1e-9 and round(res2[1], 2) == 15.0 and close(abs(a2), 10)
checks += 1

# Check 16: gauge-free relative errors. Orientations are correct, so each pair's error is the
# angle between estimated and true baseline directions: 20.56 deg (1-2), 16.31 deg (2-4),
# 36.87 deg (2-5), 0 deg elsewhere, including pair 2-3 (camera 2 moved along that baseline).
pert = [r + offset.get(i, 0) for i, r in enumerate(ref)]
errs = {}
for i, j in itertools.combinations(range(5), 2):
    z = (pert[j] - pert[i]) * (ref[j] - ref[i]).conjugate()
    errs[(i + 1, j + 1)] = abs(math.degrees(math.atan2(z.imag, z.real)))
assert round(errs[(1, 2)], 2) == 20.56 and round(errs[(2, 4)], 2) == 16.31
assert round(errs[(2, 5)], 2) == 36.87 and errs[(2, 3)] < 1e-9
assert sum(v < 1e-9 for v in errs.values()) == 7
checks += 1


def auc(errors, t):
    """COLMAP 4.2.1 benchmark compute_auc with min_error = 0."""
    e = [0.0] + sorted(errors)
    n = len(errors)
    rec = [0.0] + [(k + 1) / n for k in range(n)]
    last = bisect.bisect_right(e, t)
    rr = rec[:last] + [rec[last - 1]]
    ee = e[:last] + [t]
    return 100 * sum((ee[k + 1] - ee[k]) * (rr[k + 1] + rr[k]) / 2 for k in range(len(ee) - 1)) / t


# Check 17: AUC of these ten pair errors: 70.0 at 5 and 10 deg, 75.92 at 20 deg; recall 0.7,
# 0.7, 0.8. Counting ordered pairs, as the COLMAP benchmark does (each error twice), leaves
# 70.0 at 5 and 10 deg but gives 73.88 at 20 deg: the trapezoid interpolates between sorted
# samples, so duplicates change the area. A small list [0.5, 1, 2, 4, 180] gives AUC 20.0,
# 43.33 and 58.0 at 1, 3 and 5 deg.
vals = list(errs.values())
assert [round(auc(vals, t), 2) for t in (5, 10, 20)] == [70.0, 70.0, 75.92]
assert [round(auc(vals + vals, t), 2) for t in (5, 10, 20)] == [70.0, 70.0, 73.88]
assert [round(auc([0.5, 1, 2, 4, 180], t), 2) for t in (1, 3, 5)] == [20.0, 43.33, 58.0]
checks += 1

# ---------------------------------------------------------------------------------------
# Worked example G: cost and scaling.
# ---------------------------------------------------------------------------------------
# Check 18: exhaustive matching tests N (N - 1) / 2 pairs: 499,500 for 1,000 images and
# 49,995,000 for 10,000; with 100 retrieved neighbours per image at most 1,000,000 pairs.
assert 1000 * 999 // 2 == 499500 and 10000 * 9999 // 2 == 49995000 and 10000 * 100 == 1000000
checks += 1


def global_refinements(n_frames, ratio=1.1, freq=500, start=2):
    """Frame criteria of CheckRunGlobalRefinement only; point criteria can add more."""
    prev, count = start, 0
    for k in range(start + 1, n_frames + 1):
        if k >= ratio * prev or k >= freq + prev:
            count, prev = count + 1, k
    return count


# Check 19: registering frames one at a time from a 2-frame seed triggers 28, 52 and 79 global
# refinements for 100, 1,000 and 10,000 frames, against 98, 998 and 9,998 local refinements.
assert [global_refinements(n) for n in (100, 1000, 10000)] == [28, 52, 79]
checks += 1

# Check 20: ratios of cited runtimes (GLOMAP Tables 1, 4, 5): IMC 2023 4051.0 / 497.3 = 8.1;
# LaMAR 354660.4 / 12405.3 = 28.6; ETH3D SLAM 1115.4 / 133.5 = 8.4. 1DSfM Trafalgar 8.1 h / 3.4 h = 2.4.
assert [round(x, 1) for x in (4051.0 / 497.3, 354660.4 / 12405.3, 1115.4 / 133.5, 8.1 / 3.4)] == [8.1, 28.6, 8.4, 2.4]
checks += 1

print(f"152-sfm-incrementale-globale (CV-SFM): {checks} checks passed")
