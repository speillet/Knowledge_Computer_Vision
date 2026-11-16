"""Recompute the constructed examples of CV-AEROTRIANGULATION (154-aerotriangulation-georeferencement).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-16-photogrammetry/checks/154-aerotriangulation-georeferencement.py

Formulas re-implemented (no photogrammetric software is executed):
- ASPRS Positional Accuracy Standards, Edition 2, Version 2 (2024): RMSE per axis (section 7.12.1),
  RMSE_H = sqrt(RMSE_X^2 + RMSE_Y^2), product accuracy sqrt(RMSE_1^2 + RMSE_2^2) with the survey
  component (sections 7.12.3-7.12.4, C.7), mean-error rule of 25 % of the target RMSE (7.2),
  blunder threshold of 3 x target RMSE (7.2), 30-checkpoint minimum (7.14, C.3).
- Least-squares redundancy: residual variance of an observation = r * sigma^2, sum of redundancy
  numbers = n - u (Triggs et al. 2000, section 10.4).
- Small-angle ground displacement of a nadir ray, latency x speed, lever-arm error (project
  derivations); Cramer et al. 2000 and Cramer and Stallmann 2001 values are cross-checked.
- Normal-case stereo pair with a radial-distortion error (project derivation, exact fractions).
All inputs are constructed unless a check says it reproduces a cited value.
"""

import math
from fractions import Fraction as F

checks = 0


def rmse(values):
    return math.sqrt(sum(v * v for v in values) / len(values))


# --- Example A (card 001): independent checkpoints versus control residuals -----------------
# Six checkpoints, product minus survey, in cm (constructed).
dx = [3, -2, 4, -1, 2, -3]
dy = [-2, 3, 1, -4, 2, 1]
dz = [6, 8, -2, 7, 9, 5]
gcp_dz = [0.8, -0.6, 0.5, -0.7]
rmse_x, rmse_y, rmse_v1 = rmse(dx), rmse(dy), rmse(dz)
rmse_h1 = math.sqrt(rmse_x ** 2 + rmse_y ** 2)

# Check 1: per-axis and combined fit to checkpoints.
assert (sum(v * v for v in dx), sum(v * v for v in dy), sum(v * v for v in dz)) == (43, 35, 259)
assert round(rmse_x, 2) == 2.68 and round(rmse_y, 2) == 2.42
assert F(43 + 35, 6) == 13 and round(rmse_h1, 2) == 3.61 and round(rmse_v1, 2) == 6.57
checks += 1

# Check 2: product accuracy with survey error RMSE_H2 = 1 cm, RMSE_V2 = 2 cm (ASPRS 7.12.3-7.12.4).
rmse_h = math.sqrt(rmse_h1 ** 2 + 1.0 ** 2)
rmse_v = math.sqrt(rmse_v1 ** 2 + 2.0 ** 2)
assert round(rmse_h, 2) == 3.74 and round(rmse_v, 2) == 6.87
assert rmse_h <= 5 and rmse_v <= 10            # classes 5-cm RMSE_H and 10-cm RMSE_V pass on RMSE
checks += 1

# Check 3: mean vertical error 5.5 cm exceeds 25 % of the 10 cm target; no blunder (> 30 cm);
# only 6 checkpoints, fewer than the 30 required for a compliant statement.
mean_dz = F(sum(dz), len(dz))
assert mean_dz == F(11, 2) and mean_dz > F(25, 100) * 10
assert max(abs(v) for v in dz) < 3 * 10 and len(dz) < 30
sd_dz = math.sqrt(sum((v - float(mean_dz)) ** 2 for v in dz) / (len(dz) - 1))
assert round(sd_dz, 2) == 3.94
checks += 1

# Check 4: the control residuals are an order of magnitude smaller than the checkpoint errors.
assert round(rmse(gcp_dz), 2) == 0.66 and rmse_v1 / rmse(gcp_dz) > 9
checks += 1

# --- Example B: redundancy of a control coordinate ------------------------------------------
# One coordinate observed by a GCP (sigma_g) and determined photogrammetrically (sigma_p), the
# rest of the block held fixed: v = (z_p - z_g) * sigma_g^2 / (sigma_g^2 + sigma_p^2).
sg2, sp2 = F(1), F(9)                          # sigma_g = 1 cm, sigma_p = 3 cm
r = sg2 / (sg2 + sp2)
var_v = (sg2 + sp2) * (sg2 / (sg2 + sp2)) ** 2
var_check = sg2 + sp2                          # checkpoint discrepancy: product plus survey error
# Check 5: r = 0.1, residual sd 0.316 cm, checkpoint sd 3.162 cm, ratio exactly 1/r = 10.
assert r == F(1, 10) and var_v == r * sg2
assert round(math.sqrt(var_v), 3) == 0.316 and round(math.sqrt(var_check), 3) == 3.162
assert var_check / var_v == 100              # ratio of standard deviations = 10
checks += 1

# Check 6: 7-parameter similarity fitted to four 3D GCPs: redundancy 12 - 7 = 5, so the expected
# RMS of the 12 residual coordinates is sigma * sqrt(5/12) = 0.645 sigma.
assert 4 * 3 - 7 == 5 and round(math.sqrt(5 / 12), 3) == 0.645
checks += 1

# --- Example C (card 002): direct-georeferencing error budget -------------------------------
H, v_air = 2000.0, 70.0                        # m above ground, m/s
d_theta = math.radians(0.003)                  # residual boresight error, roll or pitch
d_t, d_lever, d_gnss = 0.002, 0.03, 0.05       # s, m, m
bore = H * math.tan(d_theta)
lat = v_air * d_t
# Roll and pitch boresight errors each contribute one horizontal component (across and along track).
rss = math.sqrt(2 * bore ** 2 + lat ** 2 + d_lever ** 2 + d_gnss ** 2)
along = math.hypot(bore, lat)
# Check 7: 0.105 m per axis, 0.14 m, 0.03 m, 0.05 m; root-sum-square 0.21 m if independent,
# 0.175 m along track from pitch and timing (corrected by the coordinator: 0.18 m counted one axis).
assert round(bore, 3) == 0.105 and round(lat, 3) == 0.14 and round(rss, 2) == 0.21
assert round(along, 3) == 0.175
checks += 1

# Check 8: halving the flying height halves the boresight term but not the latency term;
# opposite flight directions double the discrepancy in the overlap.
assert round(1000.0 * math.tan(d_theta), 3) == 0.052 and round(2 * lat, 2) == 0.28
assert round(100.0 * math.tan(d_theta), 3) == 0.005        # intuition: same error from 100 m
assert round(2 * bore, 2) == 0.21
checks += 1

# Check 9: heading error 0.006 deg at 1000 m from nadir; drone at 100 m with an assumed 0.5 deg
# attitude error (consumer-grade IMU, constructed).
assert round(1000.0 * math.radians(0.006), 3) == 0.105
assert round(100.0 * math.tan(math.radians(0.5)), 2) == 0.87
checks += 1

# Check 10: cross-checks of cited values. Cramer et al. 2000, 3.4.1: misalignment differences of
# about 1.5e-3 deg give about 5 cm at 2000 m. Cramer and Stallmann 2001, 2.4: 20 um focal error
# gives about 20 cm at 1:10000. Cramer et al. 2000, 2.1: 7e-4 m focal correction times scale
# 13000 gives about 9 m in Z0. 2000 m / 13000 = 0.154 m, a wide-angle principal distance.
assert round(2000.0 * math.radians(1.5e-3), 3) == 0.052
assert F(20, 10 ** 6) * 10000 == F(1, 5)
assert round(7e-4 * 13000, 1) == 9.1 and round(2000 / 13000, 3) == 0.154
checks += 1

# --- Example D (card 003): doming -----------------------------------------------------------
# Normal-case stereo pair, cameras at X = 0 and X = B, depth Z, normalized coordinates
# u = X/Z, v = Y/Z. The applied distortion correction leaves an error du = dk * u * r^2.
# Depth from x-parallax: Z' = B / (u1' - u2') = Z / (1 + dk * q), q = u1^2 + u1 u2 + u2^2 + v^2.


def stereo_depth(Xp, Yp, Z, B, dk):
    u1, u2, v = F(Xp) / Z, F(Xp - B) / Z, F(Yp) / Z
    u1e = u1 + dk * u1 * (u1 * u1 + v * v)
    u2e = u2 + dk * u2 * (u2 * u2 + v * v)
    return F(B) / (u1e - u2e), u1, u2, v


Z0, B0, dk0 = F(100), F(30), F(1, 100)
for (Xp, Yp) in [(15, 0), (0, 0), (15, 30), (0, 30), (-10, 12)]:
    z_sim, u1, u2, v = stereo_depth(Xp, Yp, Z0, B0, dk0)
    q = u1 * u1 + u1 * u2 + u2 * u2 + v * v
    assert z_sim == Z0 / (1 + dk0 * q)          # closed form is exact
# Check 11: height errors (depth decrease) of 2.25, 8.99 and 11.24 cm at the model centre, under
# camera 1 and at the model centre 30 m across track: a curved, not planar, error surface.
dh = {p: float(Z0 - stereo_depth(p[0], p[1], Z0, B0, dk0)[0]) for p in [(15, 0), (0, 0), (15, 30)]}
assert [round(100 * dh[p], 2) for p in [(15, 0), (0, 0), (15, 30)]] == [2.25, 8.99, 11.24]
# The distortion error at normalized radius 0.5 with f = 3600 px is 4.5 px.
assert dk0 * F(1, 8) * 3600 == F(9, 2)
checks += 1

# Check 12: radial checkpoint pattern of card 003 (constructed, cm versus metres from centre).
cp = [(20, 16), (20, 15), (70, 14), (70, 14), (70, 13), (120, 10), (120, 11), (120, 10),
      (120, 9), (170, 4), (170, 5), (170, 4)]
n = len(cp)
xs = [F(rr * rr) for rr, _ in cp]
ys = [F(zz) for _, zz in cp]
mx, my = sum(xs) / n, sum(ys) / n
b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
a = my - b * mx
res = [y - (a + b * x) for x, y in zip(xs, ys)]
r2 = 1 - sum(e * e for e in res) / sum((y - my) ** 2 for y in ys)
assert round(float(a), 1) == 15.6 and round(float(b) * 1e4, 1) == -3.9
assert round(math.sqrt(float(-a / b))) == 200          # the fitted dome vanishes near the GCPs
assert round(float(r2), 2) == 0.98
assert round(float(my), 2) == 10.42 and round(rmse([z for _, z in cp]), 2) == 11.18
checks += 1

# --- Example E (card 004): control and checkpoint budget -------------------------------------
target_v, survey_v = 5.0, 2.5
max_fit = math.sqrt(target_v ** 2 - survey_v ** 2)
# Check 13: GCP and checkpoint accuracy at most half the target; the fit to checkpoints may not
# exceed 4.33 cm; a fit of 4.5 cm fails at 5.15 cm; a 1.5 cm survey would allow 4.77 cm.
assert survey_v <= target_v / 2 and round(max_fit, 2) == 4.33
assert round(math.sqrt(4.5 ** 2 + survey_v ** 2), 2) == 5.15
assert round(math.sqrt(target_v ** 2 - 1.5 ** 2), 2) == 4.77
# Przybilla et al. 2020 report height errors of up to 30 GSD without GCPs: 0.60 m at 2 cm GSD.
assert 30 * 2 == 60
checks += 1

# --- Example F: sampling uncertainty of an RMSE ---------------------------------------------
# n * RMSE^2 / sigma^2 ~ chi2_n for zero-mean Gaussian errors; E[RMSE]/sigma = c(n).


def rmse_sd(n_pts):
    mean = math.sqrt(2 / n_pts) * math.exp(math.lgamma((n_pts + 1) / 2) - math.lgamma(n_pts / 2))
    return mean, math.sqrt(1 - mean * mean)


m30, s30 = rmse_sd(30)
m6, s6 = rmse_sd(6)
# Check 14: relative standard error about 13 % with 30 checkpoints and 28 % with 6.
assert round(s30, 3) == 0.129 and round(1 / math.sqrt(60), 3) == 0.129 and round(s6, 2) == 0.28
assert round(m30, 3) == 0.992
checks += 1

# --- Example G (card 005): published orientation results combined horizontally --------------
# Cramer and Stallmann 2001, Table 1 (OEEPE block Cali10, 1:10000): RMS X, Y in cm.
gps_at_sc = math.hypot(4.2, 5.3)       # version 1b, 4 GCP
dg_fixed = math.hypot(16.6, 18.6)      # version 2a, 0 GCP
iso_sc_1 = math.hypot(5.5, 7.3)        # version 3e, 1 GCP
# Check 15: RMSE_H about 6.8, 24.9 and 9.1 cm.
assert [round(x, 1) for x in (gps_at_sc, dg_fixed, iso_sc_1)] == [6.8, 24.9, 9.1]
checks += 1

print(f"154-aerotriangulation-georeferencement (CV-AEROTRIANGULATION): {checks} checks passed")
