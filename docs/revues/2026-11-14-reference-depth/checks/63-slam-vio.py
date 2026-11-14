"""Recompute the constructed examples of CV-VIO (reference 63-slam-vio).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/63-slam-vio.py
Inputs: the discrete-noise relation of Forster et al. (arXiv 1512.02363, Sec. V:
Cov(eta_d) = Cov(eta) / dt), the yaw-only gauge of Zhang and Scaramuzza (IROS 2018,
Sec. III-A, Table I) and elementary kinematics. Sensor values and scenarios are
constructed, not taken from a datasheet.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


G = 9.81

# --- Example A: white noise versus a constant accelerometer bias ----------------
sigma_c = 2e-3        # accelerometer noise density, m/s^2/sqrt(Hz) (constructed)
rate = 200.0          # IMU rate, Hz
sigma_d = sigma_c / math.sqrt(1 / rate)
# Check 1: a density of 2e-3 m/s^2/sqrt(Hz) sampled at 200 Hz gives ~0.028 m/s^2 per sample.
assert close(sigma_d, 0.02828, 1e-5)
T = 10.0
sigma_v = sigma_c * math.sqrt(T)
sigma_p = sigma_c * T ** 1.5 / math.sqrt(3)
# Check 2: after 10 s, white noise alone gives ~6.3 mm/s velocity and ~3.7 cm position standard deviation
# (double integration of white noise: Var(p) = sigma_c^2 T^3 / 3).
assert close(sigma_v, 0.006325, 1e-6) and close(sigma_p, 0.03651, 1e-5)
b_a = 0.02            # residual accelerometer bias, m/s^2 (constructed)
dv_bias, dp_bias = b_a * T, 0.5 * b_a * T ** 2
# Check 3: an uncorrected 0.02 m/s^2 bias gives 0.2 m/s and 1.0 m after 10 s, ~27x the noise-only position spread.
assert close(dv_bias, 0.2, 1e-12) and close(dp_bias, 1.0, 1e-12) and close(dp_bias / sigma_p, 27.39, 1e-2)

# --- Example B: gyroscope bias, tilt and gravity leakage -------------------------
b_g = math.radians(0.1)   # 0.1 deg/s, constructed
tilt_10s = b_g * T
# Check 4: 0.1 deg/s integrates to a 1 degree attitude error after 10 s.
assert close(math.degrees(tilt_10s), 1.0, 1e-9)
# A tilt theta(t) = b_g t makes the estimator subtract gravity in a wrong direction:
# horizontal acceleration error ~ g * b_g * t, position error ~ g * b_g * t^3 / 6.
p_leak = G * b_g * T ** 3 / 6
# Check 5: after 10 s the gravity leak alone displaces the position by ~2.85 m (cubic in time).
assert close(p_leak, 2.853, 1e-3)
# Check 6: doubling the time multiplies the tilt-induced error by 8 but the accelerometer-bias error by 4,
# which separates the two signatures in a drift-versus-time plot.
assert close((G * b_g * (2 * T) ** 3 / 6) / p_leak, 8.0, 1e-12)
assert close((0.5 * b_a * (2 * T) ** 2) / dp_bias, 4.0, 1e-12)
def rot_z(a, v):
    return (math.cos(a) * v[0] - math.sin(a) * v[1], math.sin(a) * v[0] + math.cos(a) * v[1], v[2])


def rot_x(a, v):
    return (v[0], math.cos(a) * v[1] - math.sin(a) * v[2], math.sin(a) * v[1] + math.cos(a) * v[2])


g_vec = (0.0, 0.0, G)
one_deg = math.radians(1.0)
g_yaw, g_tilt = rot_z(one_deg, g_vec), rot_x(one_deg, g_vec)
# Check 7: a 1 degree yaw error rotates about gravity and leaves it unchanged (no leak), whereas a
# 1 degree tilt puts ~0.171 m/s^2 of gravity into the horizontal plane.
assert max(abs(a - b) for a, b in zip(g_yaw, g_vec)) < 1e-12
assert close(math.hypot(g_tilt[0], g_tilt[1]), 0.1712, 1e-4)

# --- Example C: metric scale from accelerations ----------------------------------
def scale_ratio(acc, bias):
    """First-order scale fitted from s * a_visual = a_measured with a bias along the motion."""
    return (acc + bias) / acc


# Check 8: with 0.02 m/s^2 residual bias, gentle 0.2 m/s^2 accelerations leave a 10% scale error,
# 2 m/s^2 accelerations a 1% error.
assert close(scale_ratio(0.2, b_a) - 1, 0.10, 1e-12) and close(scale_ratio(2.0, b_a) - 1, 0.01, 1e-12)

# --- Example D: an alignment that also fits scale hides a scale error ------------
xs = [float(i) for i in range(101)]       # ground truth along a straight 100 m path, 1 m spacing
est = [1.05 * x for x in xs]              # estimate with a 5% scale error
# 4-DOF (yaw + translation) alignment of collinear points along x: the best yaw is 0 and the best
# translation matches the centroids, so the residual is the scaled spread around the centroid.
cx_gt, cx_est = sum(xs) / len(xs), sum(est) / len(est)
res_4dof = [(e - cx_est) - (x - cx_gt) for x, e in zip(xs, est)]
ate_4dof = math.sqrt(sum(r * r for r in res_4dof) / len(res_4dof))
# Check 9: the 4-DOF aligned ATE is ~1.46 m (0.05 x sqrt(850)).
assert close(ate_4dof, 0.05 * math.sqrt(850), 1e-9) and close(ate_4dof, 1.4577, 1e-4)
s_fit = sum((e - cx_est) * (x - cx_gt) for x, e in zip(xs, est)) / sum((e - cx_est) ** 2 for e in est)
res_sim3 = [s_fit * (e - cx_est) - (x - cx_gt) for x, e in zip(xs, est)]
# Check 10: a Sim(3) alignment fits s = 1/1.05 and drives the ATE to zero, hiding the metric error.
assert close(s_fit, 1 / 1.05, 1e-12) and max(abs(r) for r in res_sim3) < 1e-9

# --- Example E: latency and angular rate -----------------------------------------
omega_deg, latency = 100.0, 0.020
err_deg = omega_deg * latency
offset_mm = 1000.0 * math.radians(err_deg)          # at 1 m from the head
# Check 11: 20 ms at 100 deg/s is a 2 degree pose error, ~35 mm at 1 m.
assert close(err_deg, 2.0, 1e-12) and close(offset_mm, 34.91, 1e-2)
# Check 12: the same 20 ms as an unmodelled camera-IMU time offset gives the same 2 degree
# disagreement between visual and inertial rotation; at 10 deg/s it is only 0.2 degree.
assert close(10.0 * latency, 0.2, 1e-12)

print("63-slam-vio: 12 checks passed "
      f"(bias 1.0 m vs noise {sigma_p * 100:.1f} cm at 10 s, gravity leak {p_leak:.2f} m, "
      f"4-DOF ATE {ate_4dof:.2f} m vs Sim(3) 0, 2 deg = {offset_mm:.0f} mm at 1 m)")
