"""Recompute the constructed examples of CV-ICP (reference 62-recalage-global-icp).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/62-recalage-global-icp.py
Inputs: the RANSAC stopping rule and defaults of Open3D v0.19.0
(Registration.cpp L228-L231, Registration.h L81-L84), the point-to-plane Jacobian
row [s x n, n] of TransformationEstimation.cpp L86-L95 and of Low (2004), the
stability analysis of Gelfand et al. (2003, Sec. 2) and the PFH/FPFH costs of
Rusu et al. (2009, Sec. III). The scenes and numbers are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: RANSAC budget for 3-point samples ------------------------------
def ransac_iterations(inlier_ratio, sample_size=3, confidence=0.999):
    """k = log(1 - p) / log(1 - w^n), the Open3D early-termination estimate."""
    return math.log(1 - confidence) / math.log(1 - inlier_ratio ** sample_size)


k50 = ransac_iterations(0.5)
k10 = ransac_iterations(0.10)
k05 = ransac_iterations(0.05)
k02 = ransac_iterations(0.02)
# Check 1: half of the feature matches correct -> about 52 samples suffice.
assert math.ceil(k50) == 52
# Check 2: 10% correct matches -> about 6,905 samples (w^3 = 1e-3).
assert math.ceil(k10) == 6905
# Check 3: 5% correct matches -> about 55,259 samples.
assert math.ceil(k05) == 55259
# Check 4: 2% correct matches -> about 863,000 samples, beyond the 100,000 default cap.
assert 863_000 < k02 < 864_000 and k02 > 100_000
p_success_cap = 1 - (1 - 0.02 ** 3) ** 100_000
# Check 5: stopping at the 100,000-iteration default leaves only ~55% chance of one all-inlier sample.
assert close(p_success_cap, 0.5507, 1e-3)

# --- Example B: small-angle linearization error --------------------------------
def linearization_error(theta, lever_arm):
    """|R p - (I + [w]x) p| for a rotation about z of a point at distance lever_arm on x."""
    exact = (lever_arm * math.cos(theta), lever_arm * math.sin(theta))
    linear = (lever_arm, lever_arm * theta)
    return math.hypot(exact[0] - linear[0], exact[1] - linear[1])


err5 = linearization_error(math.radians(5), 1.0)
err1 = linearization_error(math.radians(1), 1.0)
# Check 6: a 5 degree step at 1 m lever arm is mis-modelled by ~3.8 mm (~theta^2/2).
assert close(err5, 0.003806, 1e-5) and close(err5, math.radians(5) ** 2 / 2, 2e-5)
# Check 7: a 1 degree step is mis-modelled by ~0.15 mm: the error falls with the square of the angle.
assert close(err1, 0.000152, 1e-6)


# --- Example C: which motions a set of planes constrains -----------------------
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def jacobian_row(s, n):
    """Point-to-plane row, ordering (omega_x, omega_y, omega_z, t_x, t_y, t_z) as in Open3D."""
    return list(cross(s, n)) + list(n)


def normal_matrix(rows):
    m = [[0.0] * 6 for _ in range(6)]
    for r in rows:
        for i in range(6):
            for j in range(6):
                m[i][j] += r[i] * r[j]
    return m


def rank(mat, tol=1e-9):
    a = [row[:] for row in mat]
    r = 0
    for c in range(len(a[0])):
        pivot = max(range(r, len(a)), key=lambda i: abs(a[i][c]), default=None)
        if pivot is None or abs(a[pivot][c]) < tol:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(len(a)):
            if i != r:
                f = a[i][c] / a[r][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


grid = [i / 4 for i in range(1, 5)]                       # 0.25 .. 1.0 m
floor = [((x, y, 0.0), (0.0, 0.0, 1.0)) for x in grid for y in grid]
wall = [((0.0, y, z), (1.0, 0.0, 0.0)) for y in grid for z in grid]
side = [((x, 0.0, z), (0.0, 1.0, 0.0)) for x in grid for z in grid]
rows_floor = [jacobian_row(s, n) for s, n in floor]
rows_two = rows_floor + [jacobian_row(s, n) for s, n in wall]
rows_three = rows_two + [jacobian_row(s, n) for s, n in side]
# Check 8: one plane constrains 3 of 6 motions (t_z, omega_x, omega_y).
assert rank(normal_matrix(rows_floor)) == 3
# Check 9: the unconstrained motions of the floor are t_x, t_y and omega_z (their columns are zero).
assert all(abs(r[k]) < 1e-12 for r in rows_floor for k in (2, 3, 4))
# Check 10: two orthogonal planes constrain 5 motions; translation along their intersection (y) stays free.
assert rank(normal_matrix(rows_two)) == 5 and all(abs(r[4]) < 1e-12 for r in rows_two)
# Check 11: three mutually orthogonal planes constrain all 6 motions.
assert rank(normal_matrix(rows_three)) == 6


def jacobi_eigenvalues(m, sweeps=60):
    a = [row[:] for row in m]
    n = len(a)
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-22:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-30:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


def condition(points_normals, scale=1.0, normalize=False):
    pts = [tuple(scale * v for v in s) for s, _ in points_normals]
    if normalize:  # Gelfand et al. 2003, Sec. 3: centroid to origin, mean distance to 1
        c = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
        pts = [tuple(p[i] - c[i] for i in range(3)) for p in pts]
        mean_d = sum(math.sqrt(sum(v * v for v in p)) for p in pts) / len(pts)
        pts = [tuple(v / mean_d for v in p) for p in pts]
    rows = [jacobian_row(p, n) for p, (_, n) in zip(pts, points_normals)]
    ev = jacobi_eigenvalues(normal_matrix(rows))
    return ev[-1] / ev[0]


corner = floor + wall + side
kappa_m = condition(corner, 1.0)
kappa_mm = condition(corner, 1000.0)
kappa_m_norm = condition(corner, 1.0, normalize=True)
kappa_mm_norm = condition(corner, 1000.0, normalize=True)
# Check 12: the same corner expressed in millimetres has a condition number ~10^5 times larger:
# rotation columns carry a lever arm in length units, translation columns do not.
assert kappa_mm / kappa_m > 1e5
# Check 13: after centring and scaling to unit mean distance the condition number is unit-independent.
assert close(kappa_m_norm, kappa_mm_norm, 1e-6 * kappa_m_norm)

# --- Example D: what fitness and inlier RMSE summarize --------------------------
src_points, overlapping = 10_000, 4_000
# Check 14: with Open3D's definition (correspondences / source points), 40% overlap caps fitness at 0.4
# even for the exact pose.
assert overlapping / src_points == 0.4
errors_mm = [1.0] * 10 + [30.0] * 90
rmse_all = math.sqrt(sum(e * e for e in errors_mm) / len(errors_mm))
rmse_kept = math.sqrt(sum(e * e for e in errors_mm[:10]) / 10)
# Check 15: a 5 mm threshold keeps the 10 close pairs (RMSE 1 mm, fitness 0.1);
# a 50 mm threshold keeps all 100 (RMSE 28.5 mm, fitness 1.0) for the same pose.
assert rmse_kept == 1.0 and close(rmse_all, 28.46, 1e-2)

# --- Example E: unit change of a threshold -----------------------------------
threshold_m = 0.02
# Check 16: 0.02 m is 20 mm; reusing 0.02 in millimetre coordinates shrinks the search radius 1000x
# and the search volume 10^9x.
assert close(threshold_m * 1000, 20.0, 1e-12) and close((20.0 / 0.02) ** 3, 1e9, 1e-3)

# --- Example F: PFH versus FPFH pair evaluations -------------------------------
k = 100
# Check 17: PFH evaluates all pairs of a 100-point neighbourhood (4,950) while SPFH uses the 100
# query-neighbour pairs, hence O(n k^2) versus O(n k).
assert math.comb(k, 2) == 4950 and math.comb(k, 2) / k == 49.5

print("62-recalage-global-icp: 17 checks passed "
      f"(RANSAC k at w=0.1: {math.ceil(k10)}, P(success) at w=0.02 with 1e5 iterations: {p_success_cap:.3f}, "
      f"5 deg linearization error: {err5 * 1000:.2f} mm, cond m/mm: {kappa_m:.3g}/{kappa_mm:.3g})")
