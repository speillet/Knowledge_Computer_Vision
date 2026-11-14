"""Recompute the constructed examples of CV-FACTEURS (reference 14-graphes-facteurs).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/14-graphes-facteurs.py
Formulas: Gaussian MAP as weighted least squares (Kaess et al. 2012, Sec. 2), DCS scaling
s = min(1, 2 Phi / (Phi + chi2)) (Agarwal et al. 2013, eq. 15), GTSAM 4.2 mEstimator::DCS weight
(LossFunctions.cpp L353-L362). The 1-D graphs below are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# --- Example A: gauge of a relative graph --------------------------------------
# Three 1-D poses linked by unit-weight relative factors x1-x0, x2-x1, x2-x0: the information
# matrix is the graph Laplacian.
L = [[2.0, -1.0, -1.0], [-1.0, 2.0, -1.0], [-1.0, -1.0, 2.0]]


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


# Check 1: relative factors leave a common translation free: L (1,1,1) = 0 and det L = 0.
assert all(close(sum(row), 0.0) for row in L) and close(det3(L), 0.0)
checks += 1
w_prior = 1e-6
Lp = [row[:] for row in L]
Lp[0][0] += w_prior
# Check 2: even a very weak prior (weight 1e-6) on x0 makes the system invertible
# (det = 3e-6, the number of spanning trees times the prior weight): invertibility says nothing
# about how much absolute information the prior really carries.
assert close(det3(Lp), 3 * w_prior, 1e-15)
checks += 1

# --- Example B: closing a loop on a drifting 1-D chain --------------------------
N, sigma_o = 10, 0.01          # 10 odometry steps, 1 cm std each
odo_sum = 10.1                 # odometry says 10.1 m (1% drift); the truth is 10.0 m


def solve_endpoint(loop_meas, w_loop):
    """Least-squares end-to-start distance: the chain behaves like one factor of variance N sigma_o^2."""
    v_chain = N * sigma_o ** 2
    return (odo_sum / v_chain + w_loop * loop_meas) / (1 / v_chain + w_loop)


sigma_l = 0.01
d_true = solve_endpoint(10.0, 1 / sigma_l ** 2)
per_edge = (odo_sum - d_true) / N
# Check 3: a correct loop with the same std as one odometry step spreads the 0.1 m discrepancy in
# proportion to the variances: the loop absorbs 1/11 and each odometry edge 1/11 of it (9.1 mm).
assert close(d_true, 10.0 + 0.1 / 11, 1e-9) and close(per_edge, 0.1 / 11, 1e-9)
checks += 1
d_false = solve_endpoint(5.0, 1 / sigma_l ** 2)
edge_res = (odo_sum - d_false) / N / sigma_o
# Check 4: a false loop measuring 5.0 m with the same weight bends every odometry edge by 0.464 m,
# i.e. a whitened residual of about 46 on each of the 10 edges and on the loop itself.
assert close(edge_res, 5.1 / 11 / 0.01, 1e-9) and 46 < edge_res < 47
checks += 1

# --- Example C: DCS weights (Agarwal et al. eq. 15; GTSAM DCS weight = s^2) ---------
def dcs_s(chi2, phi=1.0):
    return min(1.0, 2 * phi / (phi + chi2))


def gtsam_dcs_weight(distance, c=1.0):
    e2 = distance * distance
    return (2 * c / (c + e2)) ** 2 if e2 > c else 1.0


# Check 5: with Phi = 1, chi2 = 9 gives s = 0.2 and an information factor s^2 = 0.04; chi2 <= 1 keeps s = 1;
# GTSAM's DCS weight on a whitened distance of 3 is the same 0.04.
assert close(dcs_s(9.0), 0.2) and close(dcs_s(9.0) ** 2, 0.04) and dcs_s(1.0) == 1.0
assert close(gtsam_dcs_weight(3.0), 0.04)
checks += 1


def dcs_fixed_point(loop_meas, sig_l, iters=100):
    d = odo_sum  # start from the odometry-only solution
    s = 1.0
    for _ in range(iters):
        s = dcs_s(((d - loop_meas) / sig_l) ** 2)
        d = solve_endpoint(loop_meas, s * s / sig_l ** 2)
    return s, d


s_false, d_f = dcs_fixed_point(5.0, 0.01)
# Check 6: the false loop is switched off (s ~ 8e-6) and the chain keeps its odometry length.
assert s_false < 1e-5 and close(d_f, odo_sum, 1e-6)
checks += 1
s_true, d_t = dcs_fixed_point(10.0, 0.01)
# Check 7: the TRUE loop is also nearly switched off (s ~ 0.02, drift left at 9.96 cm), because its
# 10 cm residual is 10 loop sigmas although it is only ~3.2 sigmas of accumulated odometry (sqrt(10) cm).
assert 0.019 < s_true < 0.021 and close(d_t - 10.0, 0.0996, 1e-3)
assert close(0.1 / (sigma_o * math.sqrt(N)), 3.162, 1e-3)
checks += 1
s_true5, d_t5 = dcs_fixed_point(10.0, 0.05)
# Check 8: with a 5 cm loop std the same true loop keeps s ~ 0.45 and removes only ~8% of the drift.
assert 0.44 < s_true5 < 0.46 and 0.092 < d_t5 - 10.0 < 0.093
checks += 1

# --- Example D: counting the same evidence twice --------------------------------
# Check 9: inserting one factor twice doubles its information, so the reported std shrinks by sqrt(2).
assert close(1 / math.sqrt(2 / sigma_o ** 2), sigma_o / math.sqrt(2))
checks += 1

# --- Example E: chi-square gate for a 6-D relative-pose residual ------------------
def chi2_cdf6(x):
    return 1 - math.exp(-x / 2) * (1 + x / 2 + x * x / 8)


lo, hi = 0.0, 50.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if chi2_cdf6(mid) < 0.95 else (lo, mid)
# Check 10: the 95% quantile of chi-square with 6 degrees of freedom is 12.59; a DCS scale Phi = 1
# already down-weights a correct 6-D loop whose chi2 sits at its mean value 6 (s = 2/7).
assert close((lo + hi) / 2, 12.592, 1e-3) and close(dcs_s(6.0), 2 / 7)
checks += 1

print(f"{checks} checks passed for CV-FACTEURS (14-graphes-facteurs)")
