"""Recompute the constructed examples of CV-HANDEYE (reference 57-calibration-hand-eye).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/57-calibration-hand-eye.py
Inputs: OpenCV 4.13.0 calib3d.hpp (eye-in-hand chain, L2210-L2353) and
calibration_handeye.cpp (all pairs i < j, Tsai motion filter |2 sin(theta/2)| in [0.3, 1.7],
L275-L336). Poses, angles and noise levels are constructed.
"""

import math
import random

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def rot(axis, ang):
    x, y, z = axis
    n = math.sqrt(x * x + y * y + z * z)
    x, y, z = x / n, y / n, z / n
    c, s, C = math.cos(ang), math.sin(ang), 1 - math.cos(ang)
    return [[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C]]


def T(R, t):
    return [R[0] + [t[0]], R[1] + [t[1]], R[2] + [t[2]], [0.0, 0.0, 0.0, 1.0]]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def inv(M):
    R = [[M[j][i] for j in range(3)] for i in range(3)]
    t = [-sum(R[i][k] * M[k][3] for k in range(3)) for i in range(3)]
    return T(R, t)


def maxdiff(A, B):
    return max(abs(A[i][j] - B[i][j]) for i in range(4) for j in range(4))


def angle_of(M):
    tr = M[0][0] + M[1][1] + M[2][2]
    return math.acos(max(-1.0, min(1.0, (tr - 1) / 2)))


random.seed(7)
X = T(rot((0.3, 0.2, 1.0), 0.7), [0.05, -0.02, 0.10])   # camera -> gripper (m), constructed
Y = T(rot((1.0, -0.4, 0.2), 1.1), [0.60, 0.20, 0.05])   # target -> base (m), constructed
G = [T(rot((random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)), random.uniform(0.4, 1.2)),
       [random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), random.uniform(0.3, 0.6)]) for _ in range(6)]
C = [mul(mul(inv(X), inv(Gi)), Y) for Gi in G]          # target -> camera, consistent by construction

# --- Example A: the eye-in-hand chain and AX = XB ----------------------------
# Check 1: G_i X C_i equals the fixed target-to-base pose Y for every pose.
assert all(maxdiff(mul(mul(G[i], X), C[i]), Y) < 1e-12 for i in range(6))
checks += 1
# Check 2: with A = G_j^-1 G_i and B = C_j C_i^-1, AX = XB holds for every pair i < j.
for i in range(6):
    for j in range(i + 1, 6):
        A = mul(inv(G[j]), G[i])
        B = mul(C[j], inv(C[i]))
        assert maxdiff(mul(A, X), mul(X, B)) < 1e-12
checks += 1
# Check 3: feeding base->gripper (G^-1) instead of gripper->base breaks closure: Y_i varies by
# decimetres and tens of degrees across poses, whereas the correct chain varies by 0.
Ywrong = [mul(mul(inv(G[i]), X), C[i]) for i in range(6)]
spread_t = max(math.dist([Ywrong[0][k][3] for k in range(3)], [Ywrong[i][k][3] for k in range(3)]) for i in range(6))
spread_r = max(angle_of(mul(inv(Ywrong[0]), Ywrong[i])) for i in range(6))
assert spread_t > 0.1 and math.degrees(spread_r) > 10
checks += 1

# --- Example B: pair counts in OpenCV ----------------------------------------
# Check 4: n poses give n(n-1)/2 motion pairs: 10 -> 45 and 25 -> 300 (the count in the OpenCV comment).
assert 10 * 9 // 2 == 45 and 25 * 24 // 2 == 300
checks += 1

# --- Example C: OpenCV's Tsai motion filter -----------------------------------
lo = math.degrees(2 * math.asin(0.3 / 2))
hi = math.degrees(2 * math.asin(1.7 / 2))
# Check 5: |2 sin(theta/2)| < 0.3 or > 1.7 discards motions below 17.3 deg or above 116.4 deg
# (the source comment rounds the upper bound to 120 deg).
assert close(lo, 17.25, 0.01) and close(hi, 116.42, 0.01)
checks += 1

# --- Example D: translation leverage of a relative rotation -------------------


def sv_RminusI(theta):
    """Nonzero singular values of R - I for a rotation by theta: both equal 2 sin(theta/2)."""
    return 2 * math.sin(theta / 2)


# Check 6: for 5 deg the nonzero singular values of R_A - I are 0.087, for 30 deg 0.518, for 90 deg 1.414:
# translation noise is amplified about 11.5x, 1.9x and 0.7x along the constrained directions.
s5, s30, s90 = sv_RminusI(math.radians(5)), sv_RminusI(math.radians(30)), sv_RminusI(math.radians(90))
assert close(s5, 0.08724, 1e-5) and close(s30, 0.51764, 1e-5) and close(s90, math.sqrt(2), 1e-12)
assert close(1 / s5, 11.46, 0.01) and close(1 / s30, 1.93, 0.01)
checks += 1
# Check 7: numerically, (R_A - I) for a 30 deg rotation about z has a zero singular value along z.
Rz = rot((0, 0, 1), math.radians(30))
M = [[Rz[i][j] - (1 if i == j else 0) for j in range(3)] for i in range(3)]
MtM = [[sum(M[k][i] * M[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
assert close(MtM[2][2], 0.0, 1e-15) and close(MtM[0][0], s30**2, 1e-12)
checks += 1

# --- Example E: rotation error leaking into translation ------------------------
dth = math.radians(0.1)
tB = 0.5  # m, camera translation between the two poses
leak = tB * dth
# Check 8: a 0.1 deg error in R_X with |t_B| = 0.5 m perturbs R_X t_B by 0.87 mm; through a 30 deg motion
# (singular value 0.518) this becomes about 1.69 mm in t_X.
assert close(leak * 1000, 0.8727, 1e-4) and close(leak / s30 * 1000, 1.686, 1e-3)
checks += 1

print(f"57-calibration-hand-eye: {checks} checks passed")
