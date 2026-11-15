"""Recompute the constructed example of CV-EPIPOLAIRE-006 (reference 53-epipolaire-pnp-triangulation).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-15-accepted-proposals/checks/53-epipolaire-pnp-triangulation.py

What is recomputed: for a pure rotation (pair A) and a translation over a flat floor (pair B),
the essential matrix, the family of matrices that satisfy every epipolar constraint, the rank
of the eight-point design matrix, the plane-induced and rotation-induced 3x3 maps, a second
essential matrix compatible with the planar data, and the chi-square thresholds of the
ORB-SLAM model-selection scores.

Conventions fixed by the sources:
- X2 = R X1 + t maps camera 1 to camera 2 and [p2; 1]^T K^-T E K^-1 [p1; 1] = 0
  (OpenCV 4.13.0 modules/calib3d/include/opencv2/calib3d.hpp L2632-L2641; decomposition and
  unit-length translation L2753-L2771; cheirality in recoverPose L2808-L2810;
  decomposeHomographyMat and its positive-depth filter L3444-L3488).
- Model selection: H and F scored on the same samples, T_H = 5.99 and T_F = 3.84 (chi-square at
  95 %), homography selected when R_H = S_H / (S_H + S_F) > 0.45 (Mur-Artal et al. 2015,
  arXiv 1502.00956v2, Section IV, steps 2-3, eqs. 2-3).
Camera, motions and points are constructed; no image is processed and no OpenCV call is made.
"""

import math


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a, v):
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(3)] for i in range(3)]


def outer(u, v):
    return [[u[i] * v[j] for j in range(3)] for i in range(3)]


def scale(a, s):
    return [[s * a[i][j] for j in range(3)] for i in range(3)]


def skew(t):
    return [[0.0, -t[2], t[1]], [t[2], 0.0, -t[0]], [-t[1], t[0], 0.0]]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(v):
    return math.sqrt(dot(v, v))


def rot_y(a):
    return [[math.cos(a), 0.0, math.sin(a)], [0.0, 1.0, 0.0], [-math.sin(a), 0.0, math.cos(a)]]


def inv3(m):
    a, b, c = m[0]; d, e, f = m[1]; g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]]


def jacobi_eig(a, sweeps=100):
    """Eigenvalues and eigenvectors (columns) of a symmetric matrix."""
    n = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        if sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j) < 1e-30:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if a[p][q] == 0:
                    continue
                ang = 0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
                c, s = math.cos(ang), math.sin(ang)
                for k in range(n):
                    a[k][p], a[k][q] = c * a[k][p] - s * a[k][q], s * a[k][p] + c * a[k][q]
                for k in range(n):
                    a[p][k], a[q][k] = c * a[p][k] - s * a[q][k], s * a[p][k] + c * a[q][k]
                for k in range(n):
                    v[k][p], v[k][q] = c * v[k][p] - s * v[k][q], s * v[k][p] + c * v[k][q]
    return [a[i][i] for i in range(n)], v


def singular_values(m):
    vals, _ = jacobi_eig(matmul(transpose(m), m))
    return sorted((math.sqrt(max(x, 0.0)) for x in vals), reverse=True)


def rank(m, tol=1e-9):
    """Rank by Gaussian elimination with partial pivoting on a row-scaled copy."""
    m = [[x / max(abs(y) for y in row) for x in row] for row in m]
    r = 0
    for c in range(len(m[0])):
        piv = max(range(r, len(m)), key=lambda i: abs(m[i][c]))
        if abs(m[piv][c]) < tol:
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


def eight_point_rows(p1s, p2s):
    """One row per match of the linear system A f = 0 with f = vec(F), rows of F stacked."""
    rows = []
    for p1, p2 in zip(p1s, p2s):
        u1, v1 = p1[0] / p1[2], p1[1] / p1[2]
        u2, v2 = p2[0] / p2[2], p2[1] / p2[2]
        rows.append([u2 * u1, u2 * v1, u2, v2 * u1, v2 * v1, v2, u1, v1, 1.0])
    return rows


def epipolar_residual(F, p1, p2):
    return abs(dot(p2, matvec(F, p1))) / (norm(p1) * norm(p2) * math.sqrt(sum(x * x for r in F for x in r)))


def proportional(u, v, tol=1e-9):
    return norm(cross(u, v)) <= tol * norm(u) * norm(v)


K = [[800.0, 0.0, 640.0], [0.0, 800.0, 360.0], [0.0, 0.0, 1.0]]
Ki = inv3(K)
checks = 0

# ---------------------------------------------------------------- pair A: pure rotation
RA = rot_y(math.radians(10.0))
tA = [0.0, 0.0, 0.0]
scene = [[0.4, -0.3, 3.0], [-0.5, 0.2, 2.5], [0.1, 0.6, 4.0], [0.7, 0.5, 3.5], [-0.6, -0.4, 2.2],
         [0.3, 0.1, 5.0], [-0.2, -0.7, 3.3], [0.9, -0.1, 2.8], [-0.8, 0.8, 4.4], [0.05, -0.25, 2.6],
         [1.2, 0.3, 6.0], [-1.0, -0.2, 7.5]]
p1A = [matvec(K, [X[0] / X[2], X[1] / X[2], 1.0]) for X in scene]
p2A = []
for X in scene:
    Y = [a + b for a, b in zip(matvec(RA, X), tA)]
    p2A.append(matvec(K, [Y[0] / Y[2], Y[1] / Y[2], 1.0]))

# Check 1: t = 0 makes E = [t]x R the zero matrix.
EA = matmul(skew(tA), RA)
assert all(x == 0.0 for row in EA for x in row); checks += 1

# Check 2: the pixels obey p2 ~ H p1 with H = K R K^-1, whatever the depths (2.2 m to 7.5 m),
# and K^-1 H K returns the 10 degree rotation: the rotation stays observable.
HA = matmul(matmul(K, RA), Ki)
assert all(proportional(matvec(HA, a), b) for a, b in zip(p1A, p2A))
RA_back = matmul(matmul(Ki, HA), K)
angle = math.degrees(math.acos((RA_back[0][0] + RA_back[1][1] + RA_back[2][2] - 1.0) / 2.0))
assert abs(angle - 10.0) < 1e-9; checks += 1

# Check 3: every essential matrix [e]x R, for any unit direction e, satisfies all constraints
# exactly: the translation direction returned with unit length is not determined by the data.
for e in ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.6, -0.48, 0.64]):
    Fe = matmul(matmul(transpose(Ki), matmul(skew(e), RA)), Ki)
    assert max(epipolar_residual(Fe, a, b) for a, b in zip(p1A, p2A)) < 1e-12
checks += 1

# Check 4: the eight-point design matrix of pair A has rank 6, not 8 (12 matches).
assert rank(eight_point_rows(p1A, p2A)) == 6; checks += 1

# ---------------------------------------------------------------- pair B: flat floor
# Camera 2 is 0.2 m to the right of camera 1 (y axis down); X2 = R X1 + t with t = -R C2.
RB = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
C2 = [0.2, 0.0, 0.0]
tB = [-x for x in matvec(RB, C2)]
n, d = [0.0, 1.0, 0.0], 1.5                       # floor: n^T X1 = d, 1.5 m below camera 1
floor = [[x, 1.5, z] for x, z in ((-2.0, 3.0), (-1.0, 3.5), (0.0, 4.0), (1.0, 4.5), (2.0, 5.0),
                                   (-1.5, 6.0), (0.5, 7.0), (1.5, 8.0), (-0.5, 9.0), (0.2, 10.0),
                                   (1.8, 3.2), (-1.8, 7.7))]
x1B = [[X[0] / X[2], X[1] / X[2], 1.0] for X in floor]
x2B = []
for X in floor:
    Y = [a + b for a, b in zip(matvec(RB, X), tB)]
    x2B.append([Y[0] / Y[2], Y[1] / Y[2], 1.0])
p1B = [matvec(K, x) for x in x1B]
p2B = [matvec(K, x) for x in x2B]
EB = matmul(skew(tB), RB)

# Check 5: E of pair B exists and is a valid essential matrix (singular values 0.2, 0.2, 0).
sv = singular_values(EB)
assert abs(sv[0] - 0.2) < 1e-12 and abs(sv[1] - 0.2) < 1e-12 and sv[2] < 1e-12; checks += 1

# Check 6: the floor induces Hn = R + t n^T / d on normalized coordinates (pixels: K Hn K^-1),
# and [t]x Hn = [t]x R because [t]x t = 0: the true E belongs to the family [e]x Hn.
Hn = add(RB, scale(outer(tB, n), 1.0 / d))
assert all(proportional(matvec(Hn, a), b) for a, b in zip(x1B, x2B))
tHn = matmul(skew(tB), Hn)
assert all(abs(tHn[i][j] - EB[i][j]) < 1e-12 for i in range(3) for j in range(3)); checks += 1

# Check 7: every [e]x H satisfies all pixel constraints of the floor; the eight-point system has
# rank 6 on the floor and rank 8 for the same motion over the non-planar scene.
HB = matmul(matmul(K, Hn), Ki)
for e in ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.6, -0.48, 0.64]):
    assert max(epipolar_residual(matmul(skew(e), HB), a, b) for a, b in zip(p1B, p2B)) < 1e-12
p1G = [matvec(K, [X[0] / X[2], X[1] / X[2], 1.0]) for X in scene]
p2G = []
for X in scene:
    Y = [a + b for a, b in zip(matvec(RB, X), tB)]
    p2G.append(matvec(K, [Y[0] / Y[2], Y[1] / Y[2], 1.0]))
assert rank(eight_point_rows(p1B, p2B)) == 6 and rank(eight_point_rows(p1G, p2G)) == 8
# The linear eight-point estimate of E on normalized coordinates has the same rank 6.
assert rank(eight_point_rows(x1B, x2B)) == 6; checks += 1

# Check 8: a second essential matrix fits the floor exactly. Decompose Hn (scaled so that its
# middle singular value is 1) into another (R', t', n'); E' = [t']x R' is a valid essential
# matrix, satisfies every floor constraint and is not proportional to E. The decomposition is
# recomputed and verified here (Hn = R' + t' n'^T), not taken on trust.
vals, vecs = jacobi_eig(matmul(transpose(Hn), Hn))
order = sorted(range(3), key=lambda i: -vals[i])
s2 = math.sqrt(vals[order[1]])
Hs = scale(Hn, 1.0 / s2)
l1, l3 = vals[order[0]] / s2 ** 2, vals[order[2]] / s2 ** 2
v1, v2, v3 = ([vecs[k][order[i]] for k in range(3)] for i in range(3))
candidates = []
for sign in (1.0, -1.0):
    u = [(math.sqrt(1 - l3) * a + sign * math.sqrt(l1 - 1) * b) / math.sqrt(l1 - l3) for a, b in zip(v1, v3)]
    U = transpose([v2, u, cross(v2, u)])
    Wm = transpose([matvec(Hs, v2), matvec(Hs, u), cross(matvec(Hs, v2), matvec(Hs, u))])
    Rc = matmul(Wm, transpose(U))
    nc = cross(v2, u)
    tc = matvec([[Hs[i][j] - Rc[i][j] for j in range(3)] for i in range(3)], nc)
    rebuilt = add(Rc, outer(tc, nc))
    assert all(abs(rebuilt[i][j] - Hs[i][j]) < 1e-9 for i in range(3) for j in range(3))
    assert all(abs(x) < 1e-9 for row in add(matmul(transpose(Rc), Rc), scale([[1, 0, 0], [0, 1, 0], [0, 0, 1]], -1.0)) for x in row)
    candidates.append((matmul(skew(tc), Rc), nc))
EBn = [x for row in EB for x in row]
twins = []
for Ec, nc in candidates:
    flat = [x for row in Ec for x in row]
    k = dot(flat, EBn) / dot(EBn, EBn)
    same = all(abs(a - k * b) < 1e-9 for a, b in zip(flat, EBn))
    svc = singular_values(Ec)
    valid = abs(svc[0] - svc[1]) < 1e-9 * svc[0] and svc[2] < 1e-9 * svc[0]
    fits = max(epipolar_residual(Ec, a, b) for a, b in zip(x1B, x2B)) < 1e-12
    # Depth of each point in camera 1 under this decomposition is 1 / (n'^T x1) up to a common
    # sign (plane n'^T X1 = 1): one sign for all points is needed to put them all in front.
    signs = {dot(nc, x) > 0 for x in x1B}
    if same:
        assert len(signs) == 1                     # the true floor: every point in front
    elif valid and fits:
        twins.append(signs)
assert len(twins) == 1; checks += 1

# Check 9: in this sideways-over-the-floor pair, the second solution puts part of the floor
# behind camera 1 for either sign of n', so cheirality removes it; ORB-SLAM (Section II-B)
# reports the twofold ambiguity when all points of the plane are closer to one camera centre.
assert twins[0] == {True, False}; checks += 1

# Check 10: ORB-SLAM thresholds are chi-square 95 % quantiles: 2 dof for the point-to-point
# transfer error of H (5.99), 1 dof for the point-to-line distance of F (3.84).
t_h = -2.0 * math.log(0.05)
lo, hi = 0.0, 10.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if math.erf(math.sqrt(mid / 2.0)) < 0.95:
        lo = mid
    else:
        hi = mid
t_f = 0.5 * (lo + hi)
assert round(t_h, 2) == 5.99 and round(t_f, 2) == 3.84; checks += 1

print(f"53-epipolaire-pnp-triangulation (CV-EPIPOLAIRE-006): {checks} checks passed")
