"""Recompute the constructed examples of CV-CAPTEURS (reference 22-capteurs-horodatage).

Stdlib only. Run with:
    python3 docs/revues/2026-11-14-reference-depth/checks/22-capteurs-horodatage.py
Inputs: line delay 24.12 us for an iPhone 4S at 1920x1080 (Oth et al., CVPR 2013, Table 3);
NTP offset and delay formulas (RFC 5905, Sec. 8); FMCW relations (TI SPYY005A, eqs. 4, 9, 11,
12, 14). Speeds, angular rates, ranges, drift and chirp settings are constructed values.
"""

import math

C = 299_792_458.0  # speed of light, m/s
checks = 0


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: rolling-shutter skew ------------------------------------------
LINE_DELAY = 24.12e-6   # s per row (Oth et al., Table 3)
ROWS = 1080
readout = (ROWS - 1) * LINE_DELAY
# Check 1: the readout spans 1079 x 24.12 us = 26.0 ms.
assert close(readout, 0.02603, 1e-5)
checks += 1
# Check 2: at 1000 px/s the bottom row is displaced by about 26 px; 1 ms exposure blurs 1 px.
assert close(1000 * readout, 26.03, 1e-2) and close(1000 * 1e-3, 1.0)
checks += 1
# Check 3: a flash window t_exp - (H-1) d exists only for exposures longer than 26.0 ms.
for t_exp, opens in ((0.020, False), (0.026, False), (0.027, True)):
    assert (t_exp - readout > 0) == opens
checks += 1
# Check 4: card CV-CAPTEURS-001 appendix, 20 ms span and 0.1 ms exposure at 1000 px/s:
# 20 px of skew against 0.1 px of blur.
assert close(1000 * 0.020, 20.0) and close(1000 * 0.1e-3, 0.1)
checks += 1

# --- Example B: timing budget of a turning vehicle ----------------------------
DT = 0.050
# Check 5: translation 2 m/s x 50 ms = 0.10 m (card CV-CAPTEURS-002).
assert close(2.0 * DT, 0.10)
checks += 1
yaw = math.radians(30)
# Check 6: yaw 30 deg/s on a point 20 m away gives omega * r * dt = 0.52 m, about 5x the translation term.
assert close(yaw * 20 * DT, 0.5236, 1e-4) and close(yaw * 20 * DT / (2.0 * DT), 5.236, 1e-3)
checks += 1
# Check 7: 20 ppm over 10 min accumulates 12 ms, i.e. 24 mm at 2 m/s.
drift = 20e-6 * 600
assert close(drift, 0.012, 1e-12) and close(drift * 2.0, 0.024, 1e-12)
checks += 1


def ntp(t1, t2, t3, t4):
    """RFC 5905 Sec. 8: offset theta and round-trip delay delta."""
    return 0.5 * ((t2 - t1) + (t3 - t4)), (t4 - t1) - (t3 - t2)


# Check 8: with true offset 5 ms, outbound 3 ms and return 1 ms, NTP returns 6 ms:
# a 1 ms bias (half the asymmetry), within the delta/2 = 2 ms bound.
true_offset, out, back = 0.005, 0.003, 0.001
t1 = 10.0
t2 = t1 + out + true_offset
t3 = t2 + 0.0002
t4 = t3 - true_offset + back
theta, delta = ntp(t1, t2, t3, t4)
assert close(theta - true_offset, (out - back) / 2, 1e-12) and close(theta - true_offset, 0.001, 1e-12)
assert close(delta, out + back, 1e-12) and abs(theta - true_offset) <= delta / 2
checks += 1
# Check 9: symmetric paths give an exact offset.
t2s = t1 + 0.002 + true_offset
t3s = t2s + 0.0002
t4s = t3s - true_offset + 0.002
assert close(ntp(t1, t2s, t3s, t4s)[0], true_offset, 1e-12)
checks += 1
# Check 10: trigger stamp versus mid-exposure, auto-exposure 1-7 ms gives offsets 0.5-3.5 ms.
assert close(0.001 / 2, 0.0005) and close(0.007 / 2, 0.0035)
checks += 1
# Check 11: LiDAR at 10 sweeps/s: 100 ms sweep; 10 m/s -> 1.0 m; 30 deg/s -> 3 deg -> 1.05 m arc at 20 m.
sweep = 1 / 10
assert close(10 * sweep, 1.0) and close(30 * sweep, 3.0) and close(20 * math.radians(30 * sweep), 1.047, 1e-3)
checks += 1


# Check 12: pinhole image error f_x (v_X Z - X v_Z) dt / Z^2 = 10 px for X = 0, Z = 10 m,
# f_x = 1000 px, v_X = 2 m/s, dt = 50 ms (card CV-CAPTEURS-002 appendix); checked against
# a finite difference of the projection.
def project(x, z, fx=1000.0, cx=0.0):
    return fx * x / z + cx


du_formula = 1000 * (2.0 * 10 - 0 * 0) * DT / 10 ** 2
du_exact = project(0 + 2.0 * DT, 10.0) - project(0.0, 10.0)
assert close(du_formula, 10.0) and close(du_exact, 10.0)
checks += 1

# --- Example C: radar velocity limits ------------------------------------------
lam = C / 77e9
TC, N = 40e-6, 128
v_max = lam / (4 * TC)
v_res = lam / (2 * N * TC)
# Check 13: lambda = 3.89 mm, v_max = 24.3 m/s, v_res = 0.38 m/s.
assert close(lam, 0.003893, 1e-6) and close(v_max, 24.33, 1e-2) and close(v_res, 0.380, 1e-3)
checks += 1
# Check 14: a 30 m/s closing speed exceeds v_max and wraps into (-v_max, v_max].
wrapped = (30.0 + v_max) % (2 * v_max) - v_max
assert 30.0 > v_max and close(wrapped, 30.0 - 2 * v_max, 1e-9) and abs(wrapped) < v_max
checks += 1
# Check 15: range resolution c/(2B) is 3.75 cm for B = 4 GHz; 1 ns of round trip is 0.15 m.
assert close(C / (2 * 4e9), 0.0375, 1e-4) and close(C * 1e-9 / 2, 0.15, 1e-3)
checks += 1
# Check 16: Doppler null space: adding a velocity orthogonal to r_hat leaves v_r unchanged.
r_hat = (1 / math.sqrt(2), 1 / math.sqrt(2), 0.0)
v_rel = (3.0, -1.0, 0.5)
orth = (2.0, -2.0, 7.0)  # dot(r_hat, orth) = 0
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
assert close(dot(r_hat, orth), 0.0, 1e-12)
assert close(dot(r_hat, v_rel), dot(r_hat, tuple(a + b for a, b in zip(v_rel, orth))), 1e-12)
checks += 1

print(f"22-capteurs-horodatage: {checks} checks passed")
