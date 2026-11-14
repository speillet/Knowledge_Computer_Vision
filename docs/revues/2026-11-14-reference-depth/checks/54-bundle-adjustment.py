"""Recompute the constructed examples of CV-BA (reference 54-bundle-adjustment).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/54-bundle-adjustment.py
Inputs: Triggs et al. 2000 (gauge group of dimension 3 + 3 + 1 = 7, Sec. 9.1;
first-order iteration counts, Sec. 7), Agarwal et al. 2010 (block sizes c and s,
Sec. 2.2), Ceres 2.2.0 loss_function.h (rho(s) conventions and scaling
a^2 rho(s / a^2)). The problem sizes and residual values are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# --- Example A: counting unknowns against residuals --------------------------
GAUGE = 7  # 3 rotation + 3 translation + 1 scale (Triggs Sec. 9.1)


def min_points(views, pose_dof=6, point_dof=3, residuals_per_obs=2):
    """Smallest M with residuals >= unknowns - gauge, every point seen in every view."""
    m = 1
    while residuals_per_obs * views * m < views * pose_dof + point_dof * m - GAUGE:
        m += 1
    return m


# Check 1: two calibrated views need at least 5 points (4M >= 3M + 5), the five-point count.
assert min_points(2) == 5
checks += 1
# Check 2: three calibrated views need at least 4 points (6M >= 3M + 11).
assert min_points(3) == 4
checks += 1

# --- Example B: sizes of the full and reduced systems ------------------------
p, c = 100, 9          # cameras, BAL camera block size (Agarwal Sec. 5.2: 6 pose + f + 2 radial)
q, s = 50_000, 3       # points, point block size
track = 6              # constructed mean number of cameras observing a point
n = p * c + q * s
# Check 3: the full normal matrix has n = pc + qs = 150,900 unknowns.
assert n == 150_900
checks += 1
dense_full_gb = n * n * 8 / 1e9
dense_s_mb = (p * c) ** 2 * 8 / 1e6
# Check 4: dense double storage would be about 182 GB for H and 6.48 MB for S.
assert close(round(dense_full_gb, 1), 182.2, 1e-9) and close(dense_s_mb, 6.48, 1e-9)
checks += 1
flops_full = n ** 3 / 3
flops_s = (p * c) ** 3 / 3
# Check 5: a dense Cholesky costs ~1.15e15 flops on H and ~2.43e8 on S (ratio ~4.7 million).
assert close(flops_full / 1e15, 1.1454, 1e-3) and close(flops_s / 1e8, 2.43, 1e-9)
assert 4.6e6 < flops_full / flops_s < 4.8e6
checks += 1
observations = q * track
# Check 6: 300,000 observations give 600,000 scalar residuals, one c x s block of E each.
assert observations == 300_000 and 2 * observations == 600_000
checks += 1
pairs_per_point = track * (track - 1) // 2
# Check 7: eliminating a point seen by 6 cameras couples 15 camera pairs; at most 4,950 pairs exist.
assert pairs_per_point == 15 and p * (p - 1) // 2 == 4950
checks += 1

# --- Example C: the 7-parameter similarity leaves every pixel unchanged -------


def rot(axis, angle):
    x, y, z = axis
    nrm = math.sqrt(x * x + y * y + z * z)
    x, y, z = x / nrm, y / nrm, z / nrm
    ca, sa = math.cos(angle), math.sin(angle)
    C = 1 - ca
    return [[ca + x * x * C, x * y * C - z * sa, x * z * C + y * sa],
            [y * x * C + z * sa, ca + y * y * C, y * z * C - x * sa],
            [z * x * C - y * sa, z * y * C + x * sa, ca + z * z * C]]


def matvec(M, v):
    return [sum(M[i][k] * v[k] for k in range(3)) for i in range(3)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def transpose(A):
    return [[A[j][i] for j in range(3)] for i in range(3)]


def project(R, t, X, f=800.0, cx=640.0, cy=360.0):
    xc = [a + b for a, b in zip(matvec(R, X), t)]
    return (f * xc[0] / xc[2] + cx, f * xc[1] / xc[2] + cy)


R = rot((0.2, 1.0, 0.1), 0.3)
t = [0.4, -0.1, 2.0]
points = [[0.5, 0.2, 3.0], [-1.0, 0.4, 5.0], [0.1, -0.7, 4.0]]
Q = rot((1.0, -0.5, 0.3), 0.8)   # gauge rotation (3 dof)
b = [2.0, -3.0, 0.5]            # gauge translation (3 dof)
a = 3.7                         # gauge scale (1 dof)
R2 = matmul(R, transpose(Q))
RQtb = matvec(R2, b)
t2 = [a * ti - ri for ti, ri in zip(t, RQtb)]
for X in points:
    X2 = [a * v + bi for v, bi in zip(matvec(Q, X), b)]
    u1, u2 = project(R, t, X), project(R2, t2, X2)
    # Check 8: X' = aQX + b with R' = RQ^T and t' = a t - RQ^T b reproduces each pixel exactly.
    assert close(u1[0], u2[0], 1e-9) and close(u1[1], u2[1], 1e-9)
checks += 1

# --- Example D: robust weights (Ceres convention, scale a in whitened units) --


def huber_weight(u, a):
    """rho'(s / a^2) for Huber, s = u^2: 1 inside, a / u outside."""
    return 1.0 if u <= a else a / u


def cauchy_weight(u, a):
    """rho'(s / a^2) for Cauchy rho(s) = log(1 + s)."""
    return 1.0 / (1.0 + (u / a) ** 2)


A_SCALE = 2.0
# Check 9: for a = 2, an inlier at 1 sigma keeps weight 1 (Huber) but 0.8 (Cauchy).
assert huber_weight(1.0, A_SCALE) == 1.0 and close(cauchy_weight(1.0, A_SCALE), 0.8)
checks += 1
# Check 10: a 10-sigma residual gets weight 0.2 (Huber) and 1/26 ~ 0.0385 (Cauchy).
assert close(huber_weight(10.0, A_SCALE), 0.2) and close(cauchy_weight(10.0, A_SCALE), 1 / 26)
checks += 1
# Check 11: influence rho' * u is 10 for squared loss, capped at a = 2 for Huber, 0.385 for Cauchy.
assert close(10.0 * huber_weight(10.0, A_SCALE), 2.0)
assert close(10.0 * cauchy_weight(10.0, A_SCALE), 10 / 26) and round(10 / 26, 3) == 0.385
checks += 1

# --- Example E: a high-order radial coefficient is invisible near the centre --
F_PX, DK3 = 1000.0, 0.1


def k3_shift(r):
    """Radial pixel shift f * dk3 * r^7 caused by changing k3 at normalized radius r."""
    return F_PX * DK3 * r ** 7


# Check 12: dk3 = 0.1 moves a point by 0.0013 px at r = 0.2, 0.78 px at r = 0.5, 21 px at r = 0.8.
assert close(k3_shift(0.2), 0.00128, 1e-9)
assert close(k3_shift(0.5), 0.78125, 1e-9)
assert close(k3_shift(0.8), 20.97152, 1e-6)
checks += 1

# --- Intuition: moving a point along one ray is seen only by the other view ----
F2, BASE = 800.0, 0.5   # focal length (px) and baseline (m) of a constructed rectified pair
shift = F2 * BASE * (1 / 5.0 - 1 / 6.0)
# Check 13: a point at 5 m placed at 6 m along the first ray keeps 0 px error in view 1
# but moves by f b (1/5 - 1/6) = 13.3 px in view 2.
assert close(shift, 13.3333, 1e-4)
checks += 1

# --- Triggs Sec. 7: iterations of a linearly convergent method -----------------
iters = [math.log(1e-16) / math.log(1 - g) for g in (0.9, 0.1, 0.01)]
# Check 14: 16, ~350 and ~3,670 iterations (Triggs rounds the last to 3,700) for 16 digits.
assert round(iters[0]) == 16 and round(iters[1]) == 350 and 3600 < iters[2] < 3700
checks += 1

# --- Triggs Sec. 10.5: chi-square threshold for one frozen parameter -----------
# For k = 1, P(chi2_1 <= x) = erf(sqrt(x / 2)).
# Check 15: the 5% threshold for one extra coefficient is 3.84 (CDF 0.95 to 4 decimals).
assert abs(math.erf(math.sqrt(3.84 / 2)) - 0.95) < 1e-4
checks += 1

print(f"54-bundle-adjustment: {checks} checks passed")
