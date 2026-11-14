"""Recompute the constructed examples of CV-ZHANG (reference 52-calibration-zhang).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/52-calibration-zhang.py
Inputs: Zhang, MSR-TR-98-71 (eqs. 2-4, Sec. 3.1 eqs. 8-9, Appendix B, Sec. 4 Proposition 1,
Sec. 5.1 simulated camera and planes, Table 1); OpenCV 4.13.0 calibration.cpp (RMS denominators,
initial principal point). Noise-free synthetic data; scenarios are constructed.
"""

import math


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def rodrigues(r):
    th = math.sqrt(sum(x * x for x in r))
    if th == 0:
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    k = [x / th for x in r]
    K = [[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]]
    K2 = matmul(K, K)
    return [[(1 if i == j else 0) + math.sin(th) * K[i][j] + (1 - math.cos(th)) * K2[i][j]
             for j in range(3)] for i in range(3)]


def jacobi_eig(a, sweeps=100):
    """Eigen-decomposition of a symmetric matrix; returns (values, vectors as columns)."""
    n = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-30:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                th = 0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
                c, s = math.cos(th), math.sin(th)
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [a[i][i] for i in range(n)], v


def vij(H, i, j):
    hi = [H[0][i], H[1][i], H[2][i]]
    hj = [H[0][j], H[1][j], H[2][j]]
    return [hi[0] * hj[0], hi[0] * hj[1] + hi[1] * hj[0], hi[1] * hj[1],
            hi[2] * hj[0] + hi[0] * hj[2], hi[2] * hj[1] + hi[1] * hj[2], hi[2] * hj[2]]


def zhang_rows(H):
    v12, v11, v22 = vij(H, 0, 1), vij(H, 0, 0), vij(H, 1, 1)
    return [v12, [a - b for a, b in zip(v11, v22)]]          # eq. (8)


def homography(K, R, t):
    return matmul(K, [[R[0][0], R[0][1], t[0]], [R[1][0], R[1][1], t[1]], [R[2][0], R[2][1], t[2]]])


def spectrum(rows):
    VtV = [[sum(r[i] * r[j] for r in rows) for j in range(6)] for i in range(6)]
    vals, vecs = jacobi_eig(VtV)
    order = sorted(range(6), key=lambda k: vals[k])
    return [vals[k] for k in order], [[vecs[i][k] for i in range(6)] for k in order]


def intrinsics_from_b(b):
    """Appendix B of MSR-TR-98-71."""
    B11, B12, B22, B13, B23, B33 = b
    v0 = (B12 * B13 - B11 * B23) / (B11 * B22 - B12 ** 2)
    lam = B33 - (B13 ** 2 + v0 * (B12 * B13 - B11 * B23)) / B11
    alpha = math.sqrt(lam / B11)
    beta = math.sqrt(lam * B11 / (B11 * B22 - B12 ** 2))
    gamma = -B12 * alpha ** 2 * beta / lam
    u0 = gamma * v0 / beta - B13 * alpha ** 2 / lam
    return alpha, beta, gamma, u0, v0


checks = 0
deg = math.pi / 180
# Simulated camera of Zhang Sec. 5.1 (pixels); image coordinates scaled by 1/1000 for conditioning.
alpha, beta, gamma, u0, v0 = 1250.0, 900.0, 1.09083, 255.0, 255.0
S = 1e-3
K = [[alpha * S, gamma * S, u0 * S], [0, beta * S, v0 * S], [0, 0, 1]]
planes = [([20 * deg, 0, 0], [-9, -12.5, 500]),
          ([0, 20 * deg, 0], [-9, -12.5, 510]),
          ([x * deg / math.sqrt(5) for x in (-30, -30, -15)], [-10.5, -12.5, 525])]
Hs = [homography(K, rodrigues(r), t) for r, t in planes]
rows = [row for H in Hs for row in zhang_rows(H)]
vals, vecs = spectrum(rows)
est = intrinsics_from_b(vecs[0] if vecs[0][0] > 0 else [-x for x in vecs[0]])
est = (est[0] / S, est[1] / S, est[2] / S, est[3] / S, est[4] / S)
# Check 1: three general views give a 6x6 V^T V with one null direction (rank 5) ...
assert vals[0] / vals[1] < 1e-12 and vals[1] / vals[5] > 1e-12; checks += 1
# Check 2: ... and Appendix B recovers alpha, beta, gamma, u0, v0 exactly from noise-free data.
truth = (alpha, beta, gamma, u0, v0)
assert all(close(a, b, 1e-6 * max(1.0, abs(b))) for a, b in zip(est, truth)); checks += 1
# Check 3: Zhang's skew of 1.09083 px with alpha = 1250 is an axis angle of 89.95 degrees.
assert close(90 - math.degrees(math.atan(gamma / alpha)), 89.95, 1e-3); checks += 1

# Degenerate captures (Sec. 4).
R1 = rodrigues(planes[0][0])
trans = [homography(K, R1, t) for t in ([-9, -12.5, 500], [40, 10, 520], [-60, 30, 650])]
vals_t, _ = spectrum([row for H in trans for row in zhang_rows(H)])
Rz = lambda th: [[math.cos(th), -math.sin(th), 0], [math.sin(th), math.cos(th), 0], [0, 0, 1]]
par = [homography(K, matmul(R1, Rz(th)), t) for th, t in ((0, [-9, -12.5, 500]),
                                                         (30 * deg, [20, 0, 540]),
                                                         (75 * deg, [-30, 15, 610]))]
vals_p, _ = spectrum([row for H in par for row in zhang_rows(H)])
# Check 4: pure translations of the target, or parallel target planes (rotation about the plane
# normal, Proposition 1), leave only two independent constraints: rank 2 instead of 5.
nonzero = lambda vals: sum(v / max(vals) > 1e-12 for v in vals)
assert nonzero(vals_t) == 2 and nonzero(vals_p) == 2; checks += 1
# Check 5: two general views (rank 4) plus the skewless row [0,1,0,0,0,0] (Sec. 3.1) reach rank 5.
two = [row for H in Hs[:2] for row in zhang_rows(H)]
vals_2, _ = spectrum(two)
vals_2s, vecs_2s = spectrum(two + [[0, 1, 0, 0, 0, 0]])
assert nonzero(vals_2) == 4 and nonzero(vals_2s) == 5; checks += 1

# --- RMS conventions (OpenCV 4.13 calibration.cpp L621 and L1155) ---------------
res = [(0.3, -0.4), (0.0, 0.5), (-0.6, 0.8), (0.1, 0.0)]
sse = sum(ex * ex + ey * ey for ex, ey in res)
rms_point = math.sqrt(sse / len(res))           # calibrateCamera: sqrt(sum / number of points)
rms_coord = math.sqrt(sse / (2 * len(res)))     # stereoCalibrate: sqrt(sum / (2 x number of points))
# Check 6: the same residuals give 0.614 px per point and 0.434 px per coordinate (ratio sqrt 2).
assert close(rms_point, 0.61441, 1e-5) and close(rms_coord, 0.43445, 1e-5)
assert close(rms_point / rms_coord, math.sqrt(2)); checks += 1

# --- Pixel transforms of K -----------------------------------------------------
a, cx, crop = 0.5, 640.0, 20.0
# Check 7: resize by 0.5 then crop 20 px moves c_x from 640 to 300 px; with the pixel-centre rule
# u' = a (u + 1/2) - 1/2 it moves to 299.75 px.
assert close(a * cx - crop, 300.0) and close(a * (cx + 0.5) - 0.5 - crop, 299.75); checks += 1
# Check 8: order matters: resize-then-crop sends 320 to 140, crop-then-resize to 150.
assert close(0.5 * 320 - 20, 140) and close(0.5 * (320 - 20), 150); checks += 1
# Check 9: OpenCV's initial principal point for a 640 x 480 image is ((w-1)/2, (h-1)/2) = (319.5, 239.5).
assert ((640 - 1) * 0.5, (480 - 1) * 0.5) == (319.5, 239.5); checks += 1

# --- Metric consequences -------------------------------------------------------
# Check 10: a square entered as 20 mm but actually 19.8 mm biases metric translations by 1.01%.
assert close(20 / 19.8 - 1, 0.010101, 1e-6); checks += 1
# Check 11: Zhang Table 1 (5 images): k1 = -0.228, k2 = 0.190, alpha = 832.50, (u0, v0) = (303.96, 206.59).
# At the image corner (0, 0) the radial term moves the point by about 13.7 px: distortion is
# largest where a frontal, central capture has no corners.
k1, k2, al, uu, vv = -0.228, 0.190, 832.50, 303.96, 206.59
x, y = (0 - uu) / al, (0 - vv) / al
r2 = x * x + y * y
shift = math.hypot(uu, vv) * abs(k1 * r2 + k2 * r2 * r2)
assert close(r2, 0.19489, 1e-4) and close(shift, 13.68, 0.01); checks += 1
# Check 12: measuring on a plane with a camera 1000 mm above it: a surface 2 mm above the
# calibrated plane, seen 200 mm off-axis, is displaced laterally by 2 x 200/1000 = 0.4 mm.
assert close(2.0 * 200.0 / 1000.0, 0.4); checks += 1

print(f"52-calibration-zhang: {checks} checks passed")
