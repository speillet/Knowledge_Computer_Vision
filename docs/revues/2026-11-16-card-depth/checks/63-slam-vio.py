"""Recompute the constructed numbers added to CV-VIO-003 and CV-VIO-004 (reference
63-slam-vio, revision 9, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/63-slam-vio.py
Gauge algebra: Zhang and Scaramuzza, IROS 2018, Sec. III-A, eqs. 8, 11 and 12 (the
similarity p' = sRp + t, v' = sRv, R'_i = R R_i and the transformed velocity increment).
Scale and alignment numbers: reference worked examples C and D. Outage budget: reference
worked example F, with ORB-SLAM3's 15-point and 5 s thresholds (Campos et al., Sec. V-D).
All sensor values, motions and the 1 cm tolerance are constructed.
"""

import math

checks = 0
G = 9.81


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def matvec(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def transpose(m):
    return tuple(tuple(m[j][i] for j in range(3)) for i in range(3))


def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return ((1, 0, 0), (0, c, -s), (0, s, c))


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return ((c, 0, s), (0, 1, 0), (-s, 0, c))


def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return ((c, -s, 0), (s, c, 0), (0, 0, 1))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(v, k):
    return tuple(k * x for x in v)


def norm(v):
    return math.sqrt(sum(x * x for x in v))


g = (0.0, 0.0, -G)                       # gravity in a Z-up world frame
dt = 0.5                                 # interval between keyframes i and k, s (constructed)
R_i = matmul(rot_z(0.7), matmul(rot_y(0.2), rot_x(-0.1)))   # body-to-world at i (constructed)
v_i, v_k = (1.0, 0.3, 0.0), (1.8, 0.1, 0.2)                  # world velocities, m/s (constructed)


def delta_v(R_i, v_i, v_k):
    """Preintegrated velocity increment R_i^T (v_k - v_i - g dt) (Forster eq. 33; Zhang eq. 5)."""
    return matvec(transpose(R_i), sub(sub(v_k, v_i), scale(g, dt)))


def transformed(s, R):
    """Increment after p' = sRp + t, v' = sRv, R'_i = R R_i applied to every state (Zhang eq. 8)."""
    return delta_v(matmul(R, R_i), matvec(R, scale(v_i, s)), matvec(R, scale(v_k, s)))


ref = delta_v(R_i, v_i, v_k)
# Check 1: a rotation about gravity with s = 1 leaves the increment unchanged (Zhang eqs. 11-12):
# yaw and translation are gauge directions for any motion.
assert all(close(a, b, 1e-12) for a, b in zip(transformed(1.0, rot_z(math.radians(37))), ref))
checks += 1
# Check 2: a 1 degree tilt changes R^T g by 2 g sin(0.5 deg) = 0.171 m/s^2, so the increment moves by
# 0.171 * dt: roll and pitch are observable.
tilt = transformed(1.0, rot_x(math.radians(1)))
assert close(norm(sub(tilt, ref)) / dt, 2 * G * math.sin(math.radians(0.5)), 1e-12)
assert close(norm(sub(tilt, ref)) / dt, 0.1712, 1e-4)
checks += 1
# Check 3: a 5% scale error changes the increment by (s - 1) R_i^T (v_k - v_i), and by nothing at
# constant velocity.
s = 1.05
diff = sub(transformed(s, ((1, 0, 0), (0, 1, 0), (0, 0, 1))), ref)
expected = scale(matvec(transpose(R_i), sub(v_k, v_i)), s - 1)
assert all(close(a, b, 1e-12) for a, b in zip(diff, expected))
v_const = (1.0, 0.3, 0.0)
assert norm(sub(delta_v(R_i, scale(v_const, s), scale(v_const, s)), delta_v(R_i, v_const, v_const))) < 1e-12
checks += 1

# Check 4 (reference worked example C): residual bias 0.02 m/s^2 along the motion, first-order scale
# fit s * a_visual = a + b: 10% error at 0.2 m/s^2, 1% at 2 m/s^2.
b_a = 0.02
assert close((0.2 + b_a) / 0.2 - 1, 0.10, 1e-12) and close((2.0 + b_a) / 2.0 - 1, 0.01, 1e-12)
checks += 1
# Check 5 (reference worked example D): straight 100 m path, 1 m sampling, 5% scale error.
xs = [float(i) for i in range(101)]
est = [1.05 * x for x in xs]
cg, ce = sum(xs) / len(xs), sum(est) / len(est)
ate_4dof = math.sqrt(sum(((e - ce) - (x - cg)) ** 2 for x, e in zip(xs, est)) / len(xs))
s_fit = sum((e - ce) * (x - cg) for x, e in zip(xs, est)) / sum((e - ce) ** 2 for e in est)
ate_sim3 = math.sqrt(sum((s_fit * (e - ce) - (x - cg)) ** 2 for x, e in zip(xs, est)) / len(xs))
assert close(ate_4dof, 1.4577, 1e-4) and ate_sim3 < 1e-9
checks += 1

# --- Outage budget (CV-VIO-004; reference worked example F) --------------------------------
eps = 0.01                                # overlay tolerance, m (constructed)
b_g = math.radians(0.1)                   # gyroscope bias, rad/s (constructed)
t_acc = math.sqrt(2 * eps / b_a)
t_tilt = (6 * eps / (G * b_g)) ** (1 / 3)
# Check 6: 1 cm is reached after 1.0 s with the accelerometer bias and ~1.5 s with the tilt leak.
assert close(t_acc, 1.0, 1e-12) and close(t_tilt, 1.519, 1e-3)
assert close(0.5 * b_a * t_acc ** 2, eps, 1e-12) and close(G * b_g * t_tilt ** 3 / 6, eps, 1e-12)
checks += 1
T_lost = 5.0                              # ORB-SLAM3 short-term loss window, s (Sec. V-D)
p_acc, p_tilt = 0.5 * b_a * T_lost ** 2, G * b_g * T_lost ** 3 / 6
yaw_deg = math.degrees(b_g * T_lost)
# Check 7: after 5 s, 0.25 m and 0.36 m of position error, but 0.5 deg of orientation, 8.7 mm at 1 m.
assert close(p_acc, 0.25, 1e-12) and close(p_tilt, 0.3567, 1e-4)
assert close(yaw_deg, 0.5, 1e-12) and close(1000 * math.tan(math.radians(yaw_deg)), 8.727, 1e-3)
# The 5 s window is 5 and 3.3 times the two 1 cm budgets: "several times too long".
assert T_lost / t_acc >= 3 and T_lost / t_tilt >= 3
checks += 1

print(f"63-slam-vio (CV-VIO-003, CV-VIO-004): {checks} checks passed")
