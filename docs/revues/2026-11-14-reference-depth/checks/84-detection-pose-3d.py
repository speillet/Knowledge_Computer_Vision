"""Recompute the constructed examples of CV-POSE3D (reference 84-detection-pose-3d).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/84-detection-pose-3d.py
Definitions come from the nuScenes detection README (devkit commit b40adc4: center-distance
matching, ASE = 1 - IoU after aligning centers and orientation, AOE in radians, size order
width, length, height), the COCO keypoint evaluation page (OKS, kappa_i = 2 sigma_i),
BOP 2020 (arXiv 2009.07378v2, Sec. 2.2-2.4: MSSD, thresholds 5-50% of the diameter),
PoseCNN (arXiv 1711.00199v3, Sec. V-B: ADD, 10% of the diameter) and Martinez et al.
(arXiv 1705.03098v2, Sec. 4: protocols #1 and #2). All scenarios are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


# --- Example A: a size-order mistake under nuScenes-style errors -----------------
def footprint(cx, cy, length, width, yaw):
    """Four BEV corners of a box: length along the heading, width across it."""
    c, s = math.cos(yaw), math.sin(yaw)
    pts = []
    for dx, dy in ((length / 2, width / 2), (-length / 2, width / 2),
                   (-length / 2, -width / 2), (length / 2, -width / 2)):
        pts.append((cx + c * dx - s * dy, cy + s * dx + c * dy))
    return pts


def aligned_iou_3d(d1, d2):
    """IoU of two boxes with the same center and orientation; d = (l, w, h)."""
    inter = 1.0
    for a, b in zip(d1, d2):
        inter *= min(a, b)
    v1 = d1[0] * d1[1] * d1[2]
    v2 = d2[0] * d2[1] * d2[2]
    return inter / (v1 + v2 - inter)


gt = (4.0, 2.0, 1.5)                      # length, width, height in m
swapped = (2.0, 4.0, 1.5)                 # same numbers written in nuScenes order (w, l, h) but read as (l, w, h)
ase = 1 - aligned_iou_3d(gt, swapped)
# Check 1: centers coincide, so the prediction matches at every distance threshold (ATE = 0),
# but the aligned 3D IoU is 6 / 18 = 1/3 and ASE = 2/3.
assert close(aligned_iou_3d(gt, swapped), 1 / 3) and close(ase, 2 / 3)
checks += 1
a = footprint(10, 5, 4, 2, math.radians(30))
b = footprint(10, 5, 2, 4, math.radians(30 + 90))
# Check 2: a swapped size compensated by a 90-degree yaw offset covers exactly the same footprint
# (same corner set), yet ASE stays 2/3 and AOE is pi/2 = 1.571 rad.
assert all(any(close(p[0], q[0], 1e-9) and close(p[1], q[1], 1e-9) for q in b) for p in a)
assert close(math.pi / 2, 1.5708, 1e-4)
checks += 1
# Check 3: NDS-style TP score of the size term, max(1 - ASE, 0) = 1/3.
assert close(max(1 - ase, 0.0), 1 / 3)
checks += 1

# --- Example B: OKS per keypoint --------------------------------------------------
SIGMA = {"eye": 0.025, "wrist": 0.062, "hip": 0.107}   # COCO person sigmas; kappa = 2 sigma


def ks(d, s, sigma):
    kappa = 2 * sigma
    return math.exp(-d * d / (2 * s * s * kappa * kappa))


s100 = 100.0                                            # sqrt of a 10,000 px^2 segment area
# Check 4: a 10 px error gives similarity 0.135 on an eye, 0.722 on a wrist and 0.897 on a hip.
assert close(ks(10, s100, SIGMA["eye"]), math.exp(-2), 1e-12)
assert close(ks(10, s100, SIGMA["wrist"]), 0.7224, 1e-4)
assert close(ks(10, s100, SIGMA["hip"]), 0.8966, 1e-4)
checks += 1
# Check 5: for a person with a 2,500 px^2 segment (s = 50 px) the same 10 px give 0.0003 on an eye
# and 0.646 on a hip: OKS is relative to object scale and keypoint type.
assert close(ks(10, 50, SIGMA["eye"]), math.exp(-8), 1e-12) and close(ks(10, 50, SIGMA["hip"]), 0.6462, 1e-4)
checks += 1

# --- Example C: a cylinder rotated about its axis: ADD versus MSSD -----------------
r, height = 20.0, 100.0                  # mm
diameter = math.hypot(2 * r, height)     # largest vertex distance of the closed cylinder
n = 360
side = [(r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n), z)
        for k in range(n) for z in (0.0, height)]


def rot_z(p, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (c * p[0] - s * p[1], s * p[0] + c * p[1], p[2])


def dist(p, q):
    return math.dist(p, q)


err = math.radians(45)
add = sum(dist(rot_z(p, err), p) for p in side) / len(side)
# Check 6: rim vertices move by the chord 2 r sin(22.5 deg) = 15.31 mm; the diameter is 107.7 mm,
# so ADD = 15.31 mm exceeds the 10% threshold (10.77 mm) and the pose is rejected.
assert close(add, 2 * r * math.sin(err / 2), 1e-9) and close(add, 15.307, 1e-3)
assert close(diameter, 107.70, 1e-2) and add > 0.1 * diameter
checks += 1
sym = [math.radians(k) for k in range(360)]      # continuous symmetry discretized at 1 degree
mssd_sym = min(max(dist(rot_z(p, err), rot_z(p, s)) for p in side) for s in sym)
mssd_textured = max(dist(rot_z(p, err), p) for p in side)
# Check 7: with the axial symmetry in S_M, MSSD = 0; if a texture mark removes it (S_M = {I}),
# MSSD = 15.31 mm.
assert close(mssd_sym, 0.0, 1e-9) and close(mssd_textured, 15.307, 1e-3)
checks += 1
thresholds = [f / 100 * diameter for f in range(5, 55, 5)]
recall_share = sum(mssd_textured < t for t in thresholds) / len(thresholds)
# Check 8: against thresholds of 5%..50% of the diameter, the textured case is correct at 8 of 10
# thresholds (from 15%, i.e. 16.2 mm), contributing 0.8 to AR_MSSD for this instance.
assert recall_share == 0.8
checks += 1

# --- Example D: 3D joint error under different alignments --------------------------
gt_j = [(0.0, 0.0, 0.0), (0.0, 500.0, 0.0), (300.0, 0.0, 0.0), (0.0, 0.0, 400.0)]   # mm, root first
pred = [tuple(1.1 * c for c in p) for p in gt_j]                                     # 10% scale error
mpjpe_root = sum(dist(p, q) for p, q in zip(pred, gt_j)) / len(gt_j)
# Check 9: after root alignment (protocol #1 style) the mean error is (0 + 50 + 30 + 40) / 4 = 30 mm.
assert close(mpjpe_root, 30.0)
checks += 1
centroid = tuple(sum(p[i] for p in gt_j) / 4 for i in range(3))
rigid = sum(0.1 * dist(p, centroid) for p in gt_j) / 4
# Check 10: the best rigid alignment of a uniformly scaled copy is a translation of centroids with
# identity rotation, leaving 0.1 |p - c| per joint, 29.5 mm on average; a similarity alignment
# (with scale) leaves 0 mm, so the scale error disappears from the metric.
assert close(rigid, 29.54, 1e-2)
checks += 1

print(f"84-detection-pose-3d: {checks} checks passed")
