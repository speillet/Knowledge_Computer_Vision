"""Recompute the constructed examples of CV-SE3 (reference 12-rotations-se3).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/12-rotations-se3.py
Formulas come from Sola et al., "A micro Lie theory" (arXiv 1812.01537v9): eq. 132-139 (SO(3)),
eq. 170-175 (SE(3)), and Ceres 2.2.0 internal/ceres/manifold.cc (QuaternionPlusImpl).
The scenarios are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def vclose(u, v, tol=1e-9):
    return all(close(a, b, tol) for a, b in zip(u, v))


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def matvec(a, v):
    return [sum(a[i][k] * v[k] for k in range(3)) for i in range(3)]


def transpose(a):
    return [[a[j][i] for j in range(3)] for i in range(3)]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def skew(v):
    return [[0.0, -v[2], v[1]], [v[2], 0.0, -v[0]], [-v[1], v[0], 0.0]]


def add(a, b, s=1.0):
    return [[a[i][j] + s * b[i][j] for j in range(3)] for i in range(3)]


I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def exp_so3(theta_vec):
    """Rodrigues formula, Sola eq. 134."""
    th = math.sqrt(sum(x * x for x in theta_vec))
    if th == 0:
        return [row[:] for row in I3]
    u = [x / th for x in theta_vec]
    k = skew(u)
    return add(add(I3, k, math.sin(th)), matmul(k, k), 1 - math.cos(th))


def rz(a):
    return exp_so3([0.0, 0.0, a])


def ry(a):
    return exp_so3([0.0, a, 0.0])


def rx(a):
    return exp_so3([a, 0.0, 0.0])


def angle_trace(r):
    """Geodesic angle from the trace (Sola eq. 135), argument clamped to [-1, 1]."""
    c = (r[0][0] + r[1][1] + r[2][2] - 1) / 2
    return math.acos(max(-1.0, min(1.0, c)))


def angle_robust(r):
    """atan2 form: sin(theta) from the skew part, cos(theta) from the trace."""
    s = 0.5 * math.sqrt((r[2][1] - r[1][2]) ** 2 + (r[0][2] - r[2][0]) ** 2 + (r[1][0] - r[0][1]) ** 2)
    c = (r[0][0] + r[1][1] + r[2][2] - 1) / 2
    return math.atan2(s, c)


def quat_to_r(q):
    """Hamilton quaternion (w, x, y, z) to rotation matrix, Sola eq. 138."""
    w, x, y, z = q
    return [
        [w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z],
    ]


def qmul(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (aw * bw - ax * bx - ay * by - az * bz,
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw)


# --- Composition and inversion (Sola eq. 170-171) ----------------------------
R_wc1, t_wc1 = rz(math.pi / 2), [0.0, 0.0, 0.0]
R_wc2, t_wc2 = I3, [1.0, 0.0, 0.0]
R_c1w = transpose(R_wc1)
t_c1w = [-x for x in matvec(R_c1w, t_wc1)]
R_c1c2 = matmul(R_c1w, R_wc2)
t_c1c2 = [a + b for a, b in zip(matvec(R_c1w, t_wc2), t_c1w)]
# Check 1: camera 2's origin is at (0, -1, 0) m in camera 1 when camera 1 is yawed by 90 deg.
assert vclose(t_c1c2, [0.0, -1.0, 0.0], 1e-12)
checks += 1
back = [a + b for a, b in zip(matvec(R_wc1, t_c1c2), t_wc1)]
# Check 2: mapping it back with T_wc1 recovers the world position (1, 0, 0) m.
assert vclose(back, [1.0, 0.0, 0.0], 1e-12)
checks += 1

# --- Lever arm through the SE(3) adjoint (Sola eq. 175) ----------------------
# Body (IMU) frame b, camera c rigidly mounted with R_bc = I and t_bc = (0.5, 0, 0) m.
# A right (body-frame) perturbation xi_b = (rho, theta) of T_wb moves the camera pose by
# xi_c = Ad_{T_cb} xi_b, with T_cb = T_bc^{-1} = (I, -t_bc).
t_bc = [0.5, 0.0, 0.0]
theta_b = [0.0, 0.0, 0.01]  # 0.01 rad about the body z axis
rho_c = cross([-x for x in t_bc], theta_b)  # [t]_x R theta with t = -t_bc, R = I
# Check 3: a 0.01 rad body yaw moves a camera 0.5 m away by 5 mm along its y axis.
assert vclose(rho_c, [0.0, 0.005, 0.0], 1e-15)
checks += 1
# Check 4: the exact motion of the camera origin, R_z(0.01) t_bc - t_bc, agrees to first order;
# the remaining second-order term is 0.5 * 0.01^2 * 0.5 m = 25 micrometres along -x.
exact = [a - b for a, b in zip(matvec(rz(0.01), t_bc), t_bc)]
assert close(exact[1], rho_c[1], 1e-7) and close(exact[0], -2.5e-5, 1e-8)
checks += 1

# --- SE(3) Exp versus chained translation (Sola eq. 172-174, Sec. IV) --------
theta = [0.0, 0.0, math.pi / 2]
rho = [1.0, 0.0, 0.0]
th = math.pi / 2
k = skew(theta)
V = add(add(I3, k, (1 - math.cos(th)) / th ** 2), matmul(k, k), (th - math.sin(th)) / th ** 3)
t_se3 = matvec(V, rho)
# Check 5: Exp of the twist (rho = 1 m along x, quarter turn about z) translates by (2/pi, 2/pi, 0) m,
# the chord of a quarter circle of arc length 1 m (|t| = 0.9003 m), not by rho = (1, 0, 0) m.
assert vclose(t_se3, [2 / math.pi, 2 / math.pi, 0.0], 1e-12)
assert close(math.sqrt(sum(x * x for x in t_se3)), 0.9003, 1e-4)
checks += 1

# --- Geodesic angle versus Euler differences (existing 2026-10-23 example) ---
def zyx(yaw, pitch, roll):
    return matmul(matmul(rz(math.radians(yaw)), ry(math.radians(pitch))), rx(math.radians(roll)))


ra, rb = zyx(30, 89.9, 0), zyx(0, 89.9, -30)
geo = math.degrees(angle_robust(matmul(transpose(ra), rb)))
# Check 6: ZYX (30, 89.9, 0) and (0, 89.9, -30) deg differ by 30 deg on two Euler angles but by
# only ~0.052 deg of geodesic angle (near gimbal lock yaw and roll compensate).
assert close(geo, 0.0524, 1e-3)
checks += 1

# --- Quaternion double cover and the half-angle in 4-D (Sola eq. 110-112) ----
q = (math.cos(0.3), 0.0, math.sin(0.3), 0.0)
mq = tuple(-x for x in q)
# Check 7: q and -q give the same rotation matrix but are at Euclidean distance 2 as 4-vectors.
assert all(vclose(r1, r2, 1e-15) for r1, r2 in zip(quat_to_r(q), quat_to_r(mq)))
assert close(math.sqrt(sum((a - b) ** 2 for a, b in zip(q, mq))), 2.0)
checks += 1
q1 = (math.cos(0.1), math.sin(0.1), 0.0, 0.0)          # 0.2 rad about x
q2 = (math.cos(0.25), 0.0, 0.0, math.sin(0.25))         # 0.5 rad about z
dot = sum(a * b for a, b in zip(q1, q2))
theta_q = 2 * math.acos(abs(dot))
theta_r = angle_robust(matmul(transpose(quat_to_r(q1)), quat_to_r(q2)))
# Check 8: 2 arccos|<q1, q2>| equals the geodesic angle of R1^T R2, also after flipping q2's sign.
assert close(theta_q, theta_r, 1e-12)
assert close(2 * math.acos(abs(sum(a * -b for a, b in zip(q1, q2)))), theta_r, 1e-12)
checks += 1

# Check 9: Hamilton active q = (sqrt2/2, 0, 0, sqrt2/2) maps e_x to e_y (quarter turn about z).
s2 = math.sqrt(2) / 2
assert vclose(matvec(quat_to_r((s2, 0.0, 0.0, s2)), [1.0, 0.0, 0.0]), [0.0, 1.0, 0.0], 1e-15)
checks += 1

# --- Precision of the trace formula near zero ---------------------------------
tiny = 1e-8
r_tiny = rz(tiny)
# Check 10: for a 1e-8 rad rotation the arccos-of-trace formula returns 0 (cos rounds to 1),
# while the atan2 form recovers 1e-8 rad to machine precision.
assert angle_trace(r_tiny) == 0.0
assert close(angle_robust(r_tiny), tiny, 1e-22)
checks += 1
small = 1e-6
# Check 11: at 1e-6 rad the trace formula is already off by more than 1e-5 relative.
assert abs(angle_trace(rz(small)) / small - 1) > 1e-5
assert abs(angle_robust(rz(small)) / small - 1) < 1e-12
checks += 1

# --- Ceres 2.2.0 QuaternionManifold: left product and half-angle tangent ------
delta = [0.0, 0.0, 0.005]
nd = math.sqrt(sum(x * x for x in delta))
q_delta = (math.cos(nd), *(math.sin(nd) / nd * x for x in delta))
x0 = (1.0, 0.0, 0.0, 0.0)
xp = qmul(q_delta, x0)
rot_angle = 2 * math.atan2(math.sqrt(sum(c * c for c in xp[1:])), abs(xp[0]))
# Check 12: a Ceres quaternion tangent step of norm 0.005 rotates by 0.01 rad (twice the norm).
assert close(rot_angle, 0.01, 1e-15)
checks += 1
xr = (math.cos(0.4), 0.0, math.sin(0.4), 0.0)  # non-identity base orientation
left = quat_to_r(qmul(q_delta, xr))
right = quat_to_r(qmul(xr, q_delta))
# Check 13: with a non-identity base, the left product used by Ceres differs from a right
# (body-frame) product with the same numbers.
assert max(abs(left[i][j] - right[i][j]) for i in range(3) for j in range(3)) > 1e-3
checks += 1

# --- OpenCV to OpenGL camera axes ---------------------------------------------
M = [[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]]
det_m = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
         - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
         + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
# Check 14: diag(1, -1, -1) is a proper rotation (det +1, a half-turn about x) and sends an OpenCV
# point 2 m in front, (0, 0, 2), to OpenGL (0, 0, -2), i.e. in front along -z.
assert det_m == 1.0 and vclose(matmul(M, M)[0], [1.0, 0.0, 0.0])
assert vclose(matvec(M, [0.0, 0.0, 2.0]), [0.0, 0.0, -2.0])
assert all(vclose(r1, r2, 1e-15) for r1, r2 in zip(M, rx(math.pi)))
checks += 1

print(f"{checks} checks passed for CV-SE3 (12-rotations-se3)")
