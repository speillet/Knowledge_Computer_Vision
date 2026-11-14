"""Recompute the constructed examples of CV-EPIPOLAIRE (reference 53-epipolaire-pnp-triangulation).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/53-epipolaire-pnp-triangulation.py
Conventions: X2 = R X1 + t (camera 1 to camera 2), E = [t]x R, x2^T E x1 = 0 on normalized
coordinates, F = K2^-T E K1^-1 (OpenCV 4.13.0 calib3d.hpp findEssentialMat and
decomposeEssentialMat documentation). Cameras, points and noise levels are constructed.
"""

import math


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a, v):
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def skew(t):
    return [[0, -t[2], t[1]], [t[2], 0, -t[0]], [-t[1], t[0], 0]]


def rot_y(a):
    return [[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def inv3(m):
    a, b, c = m[0]; d, e, f = m[1]; g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]]


checks = 0
R = rot_y(math.radians(10))
t = [-0.2, 0.02, 0.05]
E = matmul(skew(t), R)
X1 = [0.4, -0.3, 3.0]
X2 = [a + b for a, b in zip(matvec(R, X1), t)]
x1 = [X1[0] / X1[2], X1[1] / X1[2], 1.0]
x2 = [X2[0] / X2[2], X2[1] / X2[2], 1.0]
# Check 1: the epipolar constraint holds on normalized coordinates.
assert abs(dot(x2, matvec(E, x1))) < 1e-12; checks += 1

K1 = [[800.0, 0, 640.0], [0, 800.0, 360.0], [0, 0, 1]]
K2 = [[1000.0, 0, 620.0], [0, 1000.0, 350.0], [0, 0, 1]]
F = matmul(matmul(transpose(inv3(K2)), E), inv3(K1))
p1, p2 = matvec(K1, x1), matvec(K2, x2)
# Check 2: F = K2^-T E K1^-1 satisfies the constraint on ideal pixels, while E applied to pixels does not.
assert abs(dot(p2, matvec(F, p1))) < 1e-9 and abs(dot(p2, matvec(E, p1))) > 1.0; checks += 1

# Epipolar line distance in pixels and the arbitrary scale of the algebraic residual.
q2 = [p2[0] + 3.0, p2[1] - 4.0, 1.0]            # a match displaced by (3, -4) px
line = matvec(F, p1)
dist = abs(dot(q2, line)) / math.hypot(line[0], line[1])
alg = dot(q2, line)
alg10 = dot(q2, [10 * v for v in line])
# Check 3: the point-to-line distance is invariant to the scale of F, the algebraic value is not;
# the distance (at most 5 px) is the component of the (3, -4) displacement normal to the line.
assert close(alg10, 10 * alg, 1e-9) and 0 < dist <= 5.0 + 1e-9
n = [line[0] / math.hypot(line[0], line[1]), line[1] / math.hypot(line[0], line[1])]
assert close(dist, abs(3.0 * n[0] - 4.0 * n[1]), 1e-9); checks += 1

# Scale ambiguity: scaling t and the scene by s leaves normalized projections unchanged.
s = 7.0
X1s = [s * v for v in X1]
X2s = [a + b for a, b in zip(matvec(R, X1s), [s * v for v in t])]
# Check 4: projections in both cameras are identical for a 7 times larger scene and baseline.
assert close(X2s[0] / X2s[2], x2[0], 1e-12) and close(X2s[1] / X2s[2], x2[1], 1e-12); checks += 1

# Four decompositions and cheirality.
tn = math.sqrt(dot(t, t))
th = [v / tn for v in t]
W = [[2 * th[i] * th[j] - (1 if i == j else 0) for j in range(3)] for i in range(3)]  # rotation by pi about t
R_alt = matmul(W, R)
E_alt = matmul(skew(th), R_alt)
E_n = matmul(skew(th), R)
# Check 5: the "twisted pair" R' = Rot(t, pi) R gives the same essential matrix up to sign.
assert all(close(E_alt[i][j], -E_n[i][j], 1e-12) for i in range(3) for j in range(3)); checks += 1


def triangulate_depths(Rc, tc, a, b):
    """Midpoint-free two-ray depths: solve lambda2 b = lambda1 Rc a + tc in least squares."""
    ra = matvec(Rc, a)
    # [ra, -b] [l1, l2]^T = -tc  -> normal equations
    A11, A12, A22 = dot(ra, ra), -dot(ra, b), dot(b, b)
    r1, r2 = -dot(ra, tc), dot(b, tc)
    det = A11 * A22 - A12 * A12
    l1 = (r1 * A22 - A12 * r2) / det
    l2 = (A11 * r2 - A12 * r1) / det
    return l1 * a[2], l2 * b[2]


cands = [(R, th), (R, [-v for v in th]), (R_alt, th), (R_alt, [-v for v in th])]
positive = [all(z > 0 for z in triangulate_depths(Rc, tc, x1, x2)) for Rc, tc in cands]
# Check 6: of the four (R, +-t) candidates, only the true one puts the point in front of both cameras.
assert positive == [True, False, False, False]; checks += 1

# Check 7: pure rotation (t = 0) makes E the zero matrix: no translation direction to recover.
assert all(v == 0 for row in matmul(skew([0, 0, 0]), R) for v in row); checks += 1

# Check 8: camera centre of a pose X_c = R X_w + t is C = -R^T t.
C = [-v for v in matvec(transpose(R), t)]
assert all(close(a, 0.0, 1e-12) for a in [u + w for u, w in zip(matvec(R, C), t)]); checks += 1

# Depth uncertainty in rectified stereo: Z = f B / d, sigma_Z ~ f B sigma_d / d^2.
f, B, sd = 800.0, 0.1, 0.5
for Z, d_expected, sz_expected, ang in ((2.0, 40.0, 0.025, 2.862), (10.0, 8.0, 0.625, 0.573)):
    d = f * B / Z
    sz = f * B * sd / d ** 2
    # Check 9: disparity 40 px / 8 px, depth sigma 0.025 m / 0.625 m, parallax 2.86 / 0.57 degrees.
    assert close(d, d_expected) and close(sz, sz_expected, 1e-12)
    assert close(math.degrees(math.atan(B / Z)), ang, 1e-3)
checks += 1
# Check 10: 5 times the range gives 25 times the depth sigma (quadratic growth).
assert close(0.625 / 0.025, 25.0); checks += 1


# Linear triangulation (DLT) recovers an exact point.
def jacobi_eig(a, sweeps=100):
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
                c, s_ = math.cos(ang), math.sin(ang)
                for k in range(n):
                    a[k][p], a[k][q] = c * a[k][p] - s_ * a[k][q], s_ * a[k][p] + c * a[k][q]
                for k in range(n):
                    a[p][k], a[q][k] = c * a[p][k] - s_ * a[q][k], s_ * a[p][k] + c * a[q][k]
                for k in range(n):
                    v[k][p], v[k][q] = c * v[k][p] - s_ * v[k][q], s_ * v[k][p] + c * v[k][q]
    return [a[i][i] for i in range(n)], v


P1 = matmul(K1, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
P2 = matmul(K2, [R[0] + [t[0]], R[1] + [t[1]], R[2] + [t[2]]])
rows = []
for P, p in ((P1, p1), (P2, p2)):
    u, v = p[0] / p[2], p[1] / p[2]
    rows.append([u * P[2][k] - P[0][k] for k in range(4)])
    rows.append([v * P[2][k] - P[1][k] for k in range(4)])
AtA = [[sum(r[i] * r[j] for r in rows) for j in range(4)] for i in range(4)]
vals, vecs = jacobi_eig(AtA)
k = min(range(4), key=lambda i: vals[i])
Xh = [vecs[i][k] for i in range(4)]
Xr = [Xh[i] / Xh[3] for i in range(3)]
# Check 11: the null vector of the 4x4 DLT system, divided by its fourth component, is X1.
assert all(close(a, b, 1e-6) for a, b in zip(Xr, X1)); checks += 1


# Planar scene: the 8-point design matrix loses rank.
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


def eight_point_rows(points3d):
    rows = []
    for P in points3d:
        Q = [a + b for a, b in zip(matvec(R, P), t)]
        a1, b1 = P[0] / P[2], P[1] / P[2]
        a2, b2 = Q[0] / Q[2], Q[1] / Q[2]
        rows.append([a2 * a1, a2 * b1, a2, b2 * a1, b2 * b1, b2, a1, b1, 1.0])
    return rows


general = [[0.4, -0.3, 3.0], [-0.5, 0.2, 2.5], [0.1, 0.6, 4.0], [0.7, 0.5, 3.5], [-0.6, -0.4, 2.2],
           [0.3, 0.1, 5.0], [-0.2, -0.7, 3.3], [0.9, -0.1, 2.8], [-0.8, 0.8, 4.4], [0.05, -0.25, 2.6]]
planar = [[x, y, 3.0 + 0.2 * x - 0.1 * y] for x, y, _ in general]
# Check 12: ten general points give a rank-8 system (F unique up to scale); ten points on one plane
# give rank 6, a three-dimensional family of fundamental matrices: the 8-point problem is degenerate.
assert rank(eight_point_rows(general)) == 8 and rank(eight_point_rows(planar)) == 6; checks += 1

print(f"53-epipolaire-pnp-triangulation: {checks} checks passed")
