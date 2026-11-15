"""Recompute the constructed example of CV-HANDEYE-006 (reference 57-calibration-hand-eye).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-15-accepted-proposals/checks/57-calibration-hand-eye.py

What is recomputed: how an error in the rotation of X enters the translation step of a
separable hand-eye solver through R_X t_B, its amplification by 1 / (2 sin(theta / 2)) for an
inter-station rotation theta, the constructed numbers of the card (0.2 deg, 0.3 m, 20 deg and
60 deg), a two-motion least-squares case, and the length-unit scaling of the translation rows
of a joint linear (Andreff) system.

Conventions fixed by the sources:
- AX = XB with A = G_j^-1 G_i (gripper motions) and B = C_j C_i^-1 (camera motions); rotation
  and translation parts R_A R_X = R_X R_B and (R_A - I) t_X = R_X t_B - t_A (Horaud and Dornaika
  1995, arXiv 2311.12655, Section 3, eqs. 15-16).
- Separable translation step with the estimated rotation held fixed:
  (Rgij - I) * Tcg = Rcg * Tcij - Tgij (OpenCV 4.13.0 modules/calib3d/src/calibration_handeye.cpp
  L353-L376, Tsai; same structure for Park L425-L447 and Horaud L520-L538).
- Joint linear system of Andreff: rows I9 - kron(Rgij, Rcij) on vec(R), and
  kron(I3, tcij^T) vec(R) + (I3 - Rgij) t = tgij (calibration_handeye.cpp L599-L617).
Poses, angles and errors are constructed; no robot, image or OpenCV call is involved.
"""

import math

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def norm(v):
    return math.sqrt(sum(x * x for x in v))


def unit(v):
    n = norm(v)
    return [x / n for x in v]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rot(axis, ang):
    x, y, z = unit(axis)
    c, s, C = math.cos(ang), math.sin(ang), 1 - math.cos(ang)
    return [[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C]]


def mm3(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def mv(a, v):
    return [sum(a[i][k] * v[k] for k in range(3)) for i in range(3)]


def tr(a):
    return [[a[j][i] for j in range(3)] for i in range(3)]


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def solve3(m, b):
    """Solve a 3x3 linear system by Cramer's rule."""
    def det(q):
        return (q[0][0] * (q[1][1] * q[2][2] - q[1][2] * q[2][1])
                - q[0][1] * (q[1][0] * q[2][2] - q[1][2] * q[2][0])
                + q[0][2] * (q[1][0] * q[2][1] - q[1][1] * q[2][0]))
    d = det(m)
    out = []
    for c in range(3):
        q = [row[:] for row in m]
        for r in range(3):
            q[r][c] = b[r]
        out.append(det(q) / d)
    return out


def least_squares(rows, rhs):
    """Normal equations for a tall system with 3 unknowns."""
    ata = [[sum(r[i] * r[j] for r in rows) for j in range(3)] for i in range(3)]
    atb = [sum(r[i] * y for r, y in zip(rows, rhs)) for i in range(3)]
    return solve3(ata, atb)


def make_motion(R_X, t_X, axis, theta, w):
    """Gripper motion A about `axis` by theta whose camera motion satisfies R_X t_B = w."""
    R_A = rot(axis, theta)
    RAmI = [[R_A[i][j] - (1.0 if i == j else 0.0) for j in range(3)] for i in range(3)]
    t_A = sub(w, mv(RAmI, t_X))                       # from R_A t_X + t_A = R_X t_B + t_X
    R_B = mm3(tr(R_X), mm3(R_A, R_X))                 # R_A R_X = R_X R_B
    t_B = mv(tr(R_X), w)
    return R_A, t_A, R_B, t_B, RAmI


def separable_t(motions, R_hat, extra_rows=(), extra_rhs=()):
    """Translation step of a separable solver with the estimated rotation held fixed."""
    rows, rhs = [], []
    for R_A, t_A, R_B, t_B, RAmI in motions:
        b = sub(mv(R_hat, t_B), t_A)
        for i in range(3):
            rows.append(RAmI[i])
            rhs.append(b[i])
    rows += list(extra_rows)
    rhs += list(extra_rhs)
    return least_squares(rows, rhs)


# Constructed hand-eye transformation X = (R_X, t_X), in metres.
R_X = rot([1.0, 2.0, 3.0], math.radians(40.0))
t_X = [0.05, -0.02, 0.12]
delta = math.radians(0.2)                            # error of the estimated rotation of X
tB_norm = 0.3                                        # camera translation between stations (m)

# Check 1: the right-hand-side perturbation is at most delta * |t_B| = 1.047 mm, and the nonzero
# singular values of R_A - I are 2 sin(theta / 2): 0.347 at 20 deg (x 2.88), 1.000 at 60 deg.
pert = delta * tB_norm
assert close(pert * 1000, 1.0472, 1e-4)
for theta, s_expected, gain in ((20.0, 0.3473, 2.879), (60.0, 1.0, 1.0)):
    s = 2 * math.sin(math.radians(theta) / 2)
    assert close(s, s_expected, 1e-4) and close(1 / s, gain, 1e-3)
# OpenCV's Tsai filter keeps |2 sin(theta/2)| in [0.3, 1.7] (calibration_handeye.cpp L307-L318):
# about 17.3 deg to 116.4 deg, so 20 deg and 60 deg pairs are both retained.
lo_deg, hi_deg = (math.degrees(2 * math.asin(v / 2)) for v in (0.3, 1.7))
assert close(lo_deg, 17.25, 0.01) and close(hi_deg, 116.42, 0.01) and lo_deg < 20.0 < 60.0 < hi_deg
checks += 1

# Check 2: single motion of 20 deg about n_A, camera translation 0.3 m (R_X t_B perpendicular to
# n_A), rotation error of 0.2 deg about n_A. The separable translation step returns t_X off by
# 1.047 / 0.347 = 3.01 mm in the plane perpendicular to n_A (the component along n_A is fixed to
# its true value, since one motion leaves it free).
n_A = unit([1.0, -1.0, 2.0])
w = [0.3 * x for x in unit(cross(n_A, [0.0, 0.0, 1.0]))]
errors = {}
for theta in (20.0, 60.0):
    motion = make_motion(R_X, t_X, n_A, math.radians(theta), w)
    R_A, t_A, R_B, t_B, RAmI = motion
    assert close(norm(t_B), 0.3, 1e-12) and close(dot(mv(R_X, t_B), n_A), 0.0, 1e-12)
    # Exact rotation: the separable step recovers t_X exactly.
    t_ok = separable_t([motion], R_X, [n_A], [dot(n_A, t_X)])
    assert all(close(a, b, 1e-12) for a, b in zip(t_ok, t_X))
    R_hat = mm3(rot(n_A, delta), R_X)
    t_bad = separable_t([motion], R_hat, [n_A], [dot(n_A, t_X)])
    errors[theta] = norm(sub(t_bad, t_X))
assert close(errors[20.0] * 1000, 1.0472 / 0.3473, 2e-3)       # 3.01 mm
assert close(errors[20.0] * 1000, 3.015, 2e-3)
checks += 1

# Check 3: the same perturbation through a 60 deg motion gives 1.05 mm: about 2.9 times less.
assert close(errors[60.0] * 1000, 1.047, 1e-3)
assert close(errors[20.0] / errors[60.0], 2.879, 1e-3); checks += 1

# Check 4: two motions about non-parallel axes, each with a 0.3 m camera translation, and a
# 0.2 deg error about a third axis. The stacked least-squares translation is again off by
# millimetres, and more for 20 deg motions than for 60 deg motions.
axes = [unit([1.0, 0.0, 0.2]), unit([0.1, 1.0, 0.0])]
u = unit([0.3, -0.5, 1.0])
R_hat = mm3(rot(u, delta), R_X)
stack_err = {}
for theta in (20.0, 60.0):
    motions = []
    for ax in axes:
        w_k = [0.3 * x for x in unit(cross(ax, [0.4, 0.4, 1.0]))]
        motions.append(make_motion(R_X, t_X, ax, math.radians(theta), w_k))
    t_ok = separable_t(motions, R_X)
    assert all(close(a, b, 1e-10) for a, b in zip(t_ok, t_X))
    stack_err[theta] = norm(sub(separable_t(motions, R_hat), t_X))
# Here: 1.74 mm with 20 deg motions against 0.55 mm with 60 deg motions.
assert close(stack_err[20.0] * 1000, 1.74, 5e-3) and close(stack_err[60.0] * 1000, 0.555, 5e-4)
checks += 1

# Check 5: in Andreff's joint linear system, the rotation rows are dimensionless and the
# translation rows (with their right-hand side) carry the length unit: changing metres to
# millimetres multiplies only the translation rows by 1000, so the relative weighting of the two
# groups of equations depends on the unit chosen.
def andreff_rows(R_A, t_A, R_B, t_B):
    kron = [[R_A[i // 3][j // 3] * R_B[i % 3][j % 3] for j in range(9)] for i in range(9)]
    rot_rows = [[(1.0 if i == j else 0.0) - kron[i][j] for j in range(9)] + [0.0] * 3 for i in range(9)]
    tr_rows = []
    for i in range(3):
        row = [0.0] * 9
        for k in range(3):
            row[3 * i + k] = t_B[k]
        row += [(1.0 if i == j else 0.0) - R_A[i][j] for j in range(3)]
        tr_rows.append(row + [t_A[i]])
    return rot_rows, tr_rows


R_A, t_A, R_B, t_B, _ = make_motion(R_X, t_X, n_A, math.radians(20.0), w)
rot_m, tr_m = andreff_rows(R_A, t_A, R_B, t_B)
rot_mm, tr_mm = andreff_rows(R_A, [1000 * x for x in t_A], R_B, [1000 * x for x in t_B])
assert rot_m == rot_mm
vecR0 = [R_X[i][j] for i in range(3) for j in range(3)]
assert all(close(sum(a * b for a, b in zip(r[:9], vecR0)), 0.0, 1e-12) for r in rot_m)  # row-major vec
# Translation rows in mm: the vec(R) block and the right-hand side scale by 1000; the (I - R_A)
# block multiplies t, which is itself 1000 times larger, so every term of the row scales by 1000.
vecR = [R_X[i][j] for i in range(3) for j in range(3)]
for rm, rmm in zip(tr_m, tr_mm):
    lhs_m = sum(a * b for a, b in zip(rm[:9], vecR)) + sum(a * b for a, b in zip(rm[9:12], t_X))
    lhs_mm = sum(a * b for a, b in zip(rmm[:9], vecR)) + sum(a * b for a, b in zip(rmm[9:12], [1000 * x for x in t_X]))
    assert close(lhs_m, rm[12], 1e-12) and close(lhs_mm, rmm[12], 1e-9)
    assert close(lhs_mm, 1000 * lhs_m, 1e-9)
checks += 1

print(f"57-calibration-hand-eye (CV-HANDEYE-006): {checks} checks passed")
