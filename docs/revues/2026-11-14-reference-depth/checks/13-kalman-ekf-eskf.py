"""Recompute the constructed examples of CV-FUSION (reference 13-kalman-ekf-eskf).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/13-kalman-ekf-eskf.py
Formulas: Kalman update and Joseph form (Chin 2023, eq. 5-8 and 14), unscented transform
(Julier and Uhlmann 1997, eq. 12-14), IMU noise impulses (Sola, arXiv 1711.02508, eq. 262-265
and App. E eq. 434-440), discrete noise conversion (Kalibr wiki, IMU Noise Model).
The scenarios and numerical values are constructed.
"""

import math
from statistics import NormalDist

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# --- Example A: scalar Kalman update and the Joseph form --------------------
P_prior, R = 4.0, 1.0      # m^2: prior std 2 m, measurement std 1 m
x_prior, z = 0.0, 1.0      # m
S = P_prior + R            # innovation variance (H = 1)
K = P_prior / S
x_post = x_prior + K * (z - x_prior)
P_simple = (1 - K) * P_prior
P_joseph = (1 - K) ** 2 * P_prior + K ** 2 * R
# Check 1: optimal gain 0.8 moves the estimate to 0.8 m and leaves 0.8 m^2 (std 0.894 m);
# simple, symmetric (P - K S K) and Joseph forms agree for the optimal gain.
assert close(K, 0.8) and close(x_post, 0.8) and close(P_simple, 0.8)
assert close(P_joseph, 0.8) and close(P_prior - K * S * K, 0.8)
checks += 1
K_sub = 0.5  # a non-optimal gain, e.g. a hand-tuned or approximated gain
true_P_sub = (1 - K_sub) ** 2 * P_prior + K_sub ** 2 * R
# Check 2: with K = 0.5 the actual error variance is 1.25 m^2 (Joseph form, valid for any gain),
# while the simple form (1 - K) P reports 2.0 m^2 and P - K S K reports 2.75 m^2.
assert close(true_P_sub, 1.25) and close((1 - K_sub) * P_prior, 2.0)
assert close(P_prior - K_sub * S * K_sub, 2.75)
checks += 1

# --- Example B: chi-square gates (NIS) --------------------------------------
def chi2_cdf(x, m):
    """Closed forms of the chi-square CDF for m = 1..4 degrees of freedom."""
    if m == 1:
        return math.erf(math.sqrt(x / 2))
    if m == 2:
        return 1 - math.exp(-x / 2)
    if m == 3:
        return math.erf(math.sqrt(x / 2)) - math.sqrt(2 * x / math.pi) * math.exp(-x / 2)
    if m == 4:
        return 1 - math.exp(-x / 2) * (1 + x / 2)
    raise ValueError(m)


def chi2_quantile(p, m):
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if chi2_cdf(mid, m) < p else (lo, mid)
    return (lo + hi) / 2


q95 = [chi2_quantile(0.95, m) for m in (1, 2, 3, 4)]
# Check 3: 95% gates are 3.841, 5.991, 7.815 and 9.488 for m = 1, 2, 3, 4; the m = 4 value matches
# DeepSORT's 9.4877 and m = 1 equals the squared 97.5% normal quantile.
assert all(close(a, b, 5e-4) for a, b in zip(q95, (3.841, 5.991, 7.815, 9.488)))
assert close(q95[3], 9.4877, 1e-4) and close(q95[0], NormalDist().inv_cdf(0.975) ** 2, 1e-9)
checks += 1
# Check 4: a gate on the square root (FilterPy's `mahalanobis`) must use sqrt(9.488) = 3.08,
# not 9.488; comparing a root to the squared threshold accepts innovations ~3x too large.
assert close(math.sqrt(q95[3]), 3.080, 1e-3)
checks += 1

# Check 5: whitened innovation direction: S = diag(1, 100), innovations (3,0) and (0,3) score 9 and 0.09.
assert close(3 ** 2 / 1, 9.0) and close(3 ** 2 / 100, 0.09)
checks += 1

# --- Example C: unscented transform on f(x) = x^2 (Julier-Uhlmann eq. 12-14) --
n, kappa = 1, 2.0          # n + kappa = 3, the heuristic for Gaussian inputs
mean, var = 0.0, 1.0
spread = math.sqrt((n + kappa) * var)
pts = [mean, mean + spread, mean - spread]
w = [kappa / (n + kappa), 1 / (2 * (n + kappa)), 1 / (2 * (n + kappa))]
ut_mean = sum(wi * p ** 2 for wi, p in zip(w, pts))
# Check 6: the sigma points reproduce E[x^2] = 1, while first-order (EKF) propagation gives f(0) = 0.
assert close(sum(w), 1.0) and close(ut_mean, 1.0) and mean ** 2 == 0.0
checks += 1

# --- Example D: discrete process noise for a constant-velocity model ---------
def qd_white_accel(q, dt):
    return (q * dt ** 3 / 3, q * dt ** 2 / 2, q * dt)          # pos var, cross, vel var


def qd_piecewise(sigma2, dt):
    return (sigma2 * dt ** 4 / 4, sigma2 * dt ** 3 / 2, sigma2 * dt ** 2)


dt = 0.005  # 200 Hz
a = qd_white_accel(1.0, dt)     # q = 1 m^2/s^3
b = qd_piecewise(1.0, dt)       # sigma_a^2 = 1 m^2/s^4
# Check 7: reusing the same number "1" in both models changes the velocity variance by 1/dt = 200
# at 200 Hz (0.005 versus 2.5e-5 m^2/s^2) and the position variance by 4/(3 dt) ~ 267.
assert close(a[2], 0.005) and close(b[2], 2.5e-5) and close(a[2] / b[2], 200.0, 1e-9)
assert close(a[0] / b[0], 4 / (3 * dt), 1e-6)
checks += 1

# --- Example E: IMU noise density to discrete impulses -------------------------
sigma_g = 1.7e-4           # rad/s/sqrt(Hz), constructed gyro noise density
rate = 200.0
dt = 1 / rate
sigma_gd = sigma_g / math.sqrt(dt)                 # per-sample std (Kalibr)
theta_i = sigma_gd ** 2 * dt ** 2                  # Sola eq. 263 with the per-sample std
# Check 8: per-sample std is sigma_g * sqrt(200) = 2.40e-3 rad/s, and the angle impulse variance
# equals sigma_g^2 dt = 1.445e-10 rad^2 per step.
assert close(sigma_gd, 2.404e-3, 1e-6) and close(theta_i, sigma_g ** 2 * dt, 1e-22)
checks += 1
var_1s = theta_i * rate
# Check 9: over 1 s the angle std is sigma_g * sqrt(1 s) = 1.7e-4 rad; over 100 s, 1.7e-3 rad (0.097 deg).
assert close(math.sqrt(var_1s), 1.7e-4, 1e-12)
assert close(math.degrees(sigma_g * math.sqrt(100)), 0.0974, 1e-4)
checks += 1
wrong_1s = math.sqrt(sigma_g ** 2 * dt ** 2 * rate)
# Check 10: using the density as if it were the per-sample std underestimates the 1 s angle std
# by sqrt(rate) = 14.1 at 200 Hz.
assert close(math.sqrt(var_1s) / wrong_1s, math.sqrt(rate), 1e-9)
checks += 1

# --- Example F: latency -------------------------------------------------------
# Check 11: at 90 deg/s, a camera update applied 50 ms late is 4.5 deg out of date.
assert close(90 * 0.050, 4.5)
checks += 1

# --- Example G: ESKF reset Jacobian (Sola eq. 288 and 294) ----------------------
dtheta_hat = (0.0, 0.0, 0.02)  # injected orientation correction, rad
G = [[1.0, dtheta_hat[2] / 2, -dtheta_hat[1] / 2],
     [-dtheta_hat[2] / 2, 1.0, dtheta_hat[0] / 2],
     [dtheta_hat[1] / 2, -dtheta_hat[0] / 2, 1.0]]   # I - [dtheta_hat / 2]_x
P = [[1e-4, 0.0, 0.0], [0.0, 4e-4, 0.0], [0.0, 0.0, 1e-4]]  # rad^2
GP = [[sum(G[i][k] * P[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
GPGt = [[sum(GP[i][k] * G[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
# Check 12: a 0.02 rad correction about z rotates the covariance by ~0.01 rad: it creates an
# xy cross-covariance of ~3e-6 rad^2 and leaves the trace unchanged to first order; the reset never
# drives the variances to zero.
assert close(GPGt[0][1], 0.01 * 4e-4 - 0.01 * 1e-4, 1e-12)
assert close(GPGt[0][0] + GPGt[1][1] + GPGt[2][2], 6e-4, 1e-7) and min(GPGt[i][i] for i in range(3)) > 9e-5
checks += 1

# --- Cost order of magnitude ----------------------------------------------------
# Check 13: a dense F P F^T costs about 2 n^3 multiply-adds: 6,750 for n = 15 and 11,664 for n = 18.
assert 2 * 15 ** 3 == 6750 and 2 * 18 ** 3 == 11664
checks += 1

print(f"{checks} checks passed for CV-FUSION (13-kalman-ekf-eskf)")
