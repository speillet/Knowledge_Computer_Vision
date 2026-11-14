"""Recompute the constructed examples of CV-HOMOGRAPHIE (reference 51-ransac-homographie).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/51-ransac-homographie.py
Inputs: Fischler and Bolles 1981, Sec. II.B (E(k) = w^-n, SD(k), k = log(1-z)/log(1-b));
OpenCV 4.13.0 calib3d ptsetreg.cpp RANSACUpdateNumIters (cvRound of the same ratio, capped)
and fundam.cpp HomographyEstimatorCallback::checkSubset (orientation test). Cameras, planes,
points and homographies are constructed.
"""

import math


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def budget_ceil(w, m, p):
    return math.ceil(math.log(1 - p) / math.log(1 - w ** m))


def budget_opencv(w, m, p, max_iters=2000):
    """ptsetreg.cpp: cvRound(log(1-p) / log(1-(1-ep)^m)) with ep the outlier ratio, capped."""
    num, den = math.log(1 - p), math.log(1 - w ** m)
    return max_iters if -num >= max_iters * (-den) else int(math.floor(num / den + 0.5))


checks = 0

# --- Example A: sampling budget -----------------------------------------------
# Check 1: four-point samples at confidence 0.99 need 72, 9 and 567 draws for w = 0.5, 0.8, 0.3.
assert budget_ceil(0.5, 4, 0.99) == 72 and budget_ceil(0.8, 4, 0.99) == 9
assert budget_ceil(0.3, 4, 0.99) == 567; checks += 1
# Check 2: OpenCV rounds instead of taking the ceiling: 71 at 0.99, and 82 instead of 83 at its default 0.995.
assert budget_opencv(0.5, 4, 0.99) == 71 and budget_opencv(0.5, 4, 0.995) == 82
assert budget_ceil(0.5, 4, 0.995) == 83; checks += 1
# Check 3: with w = 0.1 the ratio exceeds the default cap: maxIters = 2000 is returned.
assert budget_ceil(0.1, 4, 0.995) == 52_981 and budget_opencv(0.1, 4, 0.995) == 2000; checks += 1
# Check 4: Fischler and Bolles Sec. II.B: for w = 0.5 and n = 4, E(k) = 16, SD(k) = 15.5,
# and k = log(0.1)/log(15/16) = 35.7 draws for 90% assurance.
b = 0.5 ** 4
assert close(1 / b, 16) and close(math.sqrt(1 - b) / b, 15.49, 1e-2)
assert close(math.log(0.1) / math.log(15 / 16), 35.68, 1e-2); checks += 1
# Check 5: drawing 4 distinct indices among n = 100 pairs with I = 50 inliers gives
# q = C(50,4)/C(100,4) = 0.0587 < 0.0625, hence 77 draws instead of 72 at 0.99.
q = math.comb(50, 4) / math.comb(100, 4)
assert close(q, 0.058732, 1e-6)
assert math.ceil(math.log(0.01) / math.log(1 - q)) == 77; checks += 1


# --- Example B: plane-induced homography and parallax -------------------------
def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a, v):
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def project(K, X):
    v = matvec(K, X)
    return (v[0] / v[2], v[1] / v[2])


f, cx, cy = 800.0, 640.0, 360.0
K = [[f, 0, cx], [0, f, cy], [0, 0, 1]]
K_inv = [[1 / f, 0, -cx / f], [0, 1 / f, -cy / f], [0, 0, 1]]
R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
t = [-0.1, 0.0, 0.0]                       # camera 2 frame: X' = R X + t (0.1 m lateral baseline)
n, d = [0.0, 0.0, 1.0], 2.0                # plane n^T X = d: fronto-parallel at Z = 2 m
A = [[R[i][j] + t[i] * n[j] / d for j in range(3)] for i in range(3)]
H = matmul(matmul(K, A), K_inv)


def apply_h(h, p):
    v = matvec(h, [p[0], p[1], 1.0])
    return (v[0] / v[2], v[1] / v[2])


X_plane = [0.3, -0.2, 2.0]
X2 = [X_plane[i] + t[i] for i in range(3)]
# Check 6: H = K (R + t n^T / d) K^-1 maps the image of a plane point exactly to its second image.
assert all(close(u, v, 1e-9) for u, v in zip(apply_h(H, project(K, X_plane)), project(K, X2))); checks += 1
X_far = [0.3 * 5, -0.2 * 5, 10.0]          # same first-image ray, depth 10 m
X_far2 = [X_far[i] + t[i] for i in range(3)]
res = apply_h(H, project(K, X_far))[0] - project(K, X_far2)[0]
# Check 7: on the same ray, a point at 10 m is mis-transferred by f B (1/2 - 1/10) = 32 px;
# disparities are 40 px at 2 m and 8 px at 10 m.
assert close(abs(res), 32.0, 1e-9) and close(f * 0.1 / 2, 40) and close(f * 0.1 / 10, 8); checks += 1
H_rot = matmul(matmul(K, R), K_inv)
# Check 8: with t = 0, H = K R K^-1 does not depend on the plane: both depths transfer exactly.
assert all(close(u, v, 1e-9) for u, v in zip(apply_h(H_rot, project(K, X_far)), project(K, X_far))); checks += 1


# --- Example C: DLT rank and degenerate minimal sets --------------------------
def dlt_rows(src, dst):
    rows = []
    for (X, Y), (x, y) in zip(src, dst):
        rows.append([X, Y, 1, 0, 0, 0, -x * X, -x * Y, -x])
        rows.append([0, 0, 0, X, Y, 1, -y * X, -y * Y, -y])
    return rows


def rank(m, tol=1e-9):
    m = [row[:] for row in m]
    r = 0
    for c in range(len(m[0])):
        piv = max(range(r, len(m)), key=lambda i: abs(m[i][c]), default=None)
        if piv is None or abs(m[piv][c]) < tol:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r:
                fct = m[i][c] / m[r][c]
                m[i] = [a - fct * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == len(m):
            break
    return r


Hgen = [[1.1, 0.05, 20.0], [-0.03, 0.95, 10.0], [1e-4, 5e-5, 1.0]]
src_ok = [(0, 0), (1, 0), (1, 1), (0, 1)]
src_col = [(0, 0), (1, 0), (2, 0), (0, 1)]        # three collinear source points
dst_ok = [apply_h(Hgen, p) for p in src_ok]
dst_col = [apply_h(Hgen, p) for p in src_col]
# Check 9: four points in general position give an 8x9 system of rank 8 (one-dimensional null
# space = the projective scale); three collinear points drop the rank to 7.
assert rank(dlt_rows(src_ok, dst_ok)) == 8 and rank(dlt_rows(src_col, dst_col)) == 7; checks += 1


# --- Example D: OpenCV orientation test on a minimal sample -------------------
def det3(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def orientation_consistent(src, dst):
    """fundam.cpp checkSubset: all four triangles keep, or all flip, their orientation."""
    tt = [(0, 1, 2), (1, 2, 3), (0, 2, 3), (0, 1, 3)]
    neg = sum(det3(*[src[i] for i in t]) * det3(*[dst[i] for i in t]) < 0 for t in tt)
    return neg in (0, 4)


src4 = [(0, 0), (100, 0), (100, 100), (0, 100)]
dst4 = [apply_h(Hgen, p) for p in src4]
dst_swapped = [dst4[0], dst4[2], dst4[1], dst4[3]]   # one wrong pairing inside the sample
# Check 10: a sample consistent with a homography keeps all triangle orientations; swapping two
# destination points makes two of the four triangles flip and OpenCV rejects the sample.
assert orientation_consistent(src4, dst4) and not orientation_consistent(src4, dst_swapped); checks += 1

# --- Example E: projective term and extrapolation -----------------------------
h31 = 1e-5                                   # 1/px
shift_near = 100 - 100 / (1 + h31 * 100)
shift_far = 1900 - 1900 / (1 + h31 * 1900)
# Check 11: a projective coefficient of 1e-5 per pixel moves x = 100 px by 0.1 px but
# x = 1900 px by 35.4 px: a fit constrained near the origin says little about the far edge.
assert close(shift_near, 0.0999, 1e-4) and close(shift_far, 35.43, 1e-2); checks += 1

# --- Example F: thresholds under resizing -------------------------------------
# Check 12: a uniform resize by 1/2 turns a 4-px deviation into 2 px, so a kept 3-px gate
# becomes 1.5 times more permissive in original pixels (6 px); an anisotropic resize
# (0.5, 1.0) turns a circular 3-px gate into an ellipse of semi-axes 6 and 3 original px.
assert close(4 * 0.5, 2.0) and close(3 / 0.5, 6.0)
assert (3 / 0.5, 3 / 1.0) == (6.0, 3.0); checks += 1

print(f"51-ransac-homographie: {checks} checks passed")
