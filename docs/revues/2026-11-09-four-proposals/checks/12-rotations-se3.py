"""Recompute the constructed examples of CV-SE3-007 (reference 12-rotations-se3).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-09-four-proposals/checks/12-rotations-se3.py

Conventions and formulas follow Sola, Deray and Atchuthan, "A micro Lie theory for state
estimation in robotics" (arXiv 1812.01537v9):
- T_ab = (R_ab, t_ab) maps b coordinates to a coordinates, p_a = R_ab p_b + t_ab;
  inverse eq. 170, composition eq. 171;
- tangent vectors tau = (rho, theta), translation first (eq. 169); right plus
  X Exp(tau) (eq. 25), left plus Exp(tau) X (eq. 27);
- SE(3) Exp with V(theta) (eq. 172-174), SO(3) Exp by the Rodrigues formula (eq. 134);
- adjoint Ad_M = [[R, [t]x R], [0, R]] (eq. 175), Ad_{X^-1} = Ad_X^-1 (eq. 33),
  X Exp(tau) X^-1 = Exp(Ad_X tau) (Sec. II-F, derivation before eq. 29);
- Jacobians of composition: d(Ma Mb)/dMa = [[Rb^T, -Rb^T [tb]x], [0, Rb^T]] = Ad_{Mb}^-1
  (eq. 65, 177) and d(Ma Mb)/dMb = I (eq. 66, 178);
- action on a point M.p = t + R p with Jacobian [R, -R [p]x] (eq. 181-182);
- covariance transport E Sigma = Ad X Sigma Ad^T (eq. 54) and propagation J Sigma J^T (eq. 55).
Exact rational arithmetic (fractions) is used for the covariance numbers; floats only where
trigonometric functions are needed. The scenario is a constructed project example.
"""

import math
import random
from fractions import Fraction as F

checks = 0


# --- Generic small-matrix helpers (work with Fractions or floats) --------------------------
def zeros(n, m):
    return [[0 for _ in range(m)] for _ in range(n)]


def eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def mat_vec(a, v):
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def tr(a):
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]


def neg(a):
    return [[-x for x in row] for row in a]


def madd(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def blocks(a, b, c, d):
    """Assemble a 6x6 matrix from four 3x3 blocks [[a, b], [c, d]]."""
    return [ra + rb for ra, rb in zip(a, b)] + [rc + rd for rc, rd in zip(c, d)]


def sub(m, r0, c0, n=3):
    return [row[c0:c0 + n] for row in m[r0:r0 + n]]


def skew(v):
    return [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def max_abs_diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


# --- SE(3) operations (Sola eq. 170-175) ---------------------------------------------------
def inv(R, t):
    Rt = tr(R)
    return Rt, [-x for x in mat_vec(Rt, t)]


def compose(Ra, ta, Rb, tb):
    return mat_mul(Ra, Rb), [x + y for x, y in zip(ta, mat_vec(Ra, tb))]


def adjoint(R, t):
    """Ad_M = [[R, [t]x R], [0, R]] for tau = (rho, theta), eq. 175."""
    return blocks(R, mat_mul(skew(t), R), zeros(3, 3), R)


def jac_compose_first(Rb, tb):
    """d(Ma Mb)/dMa, eq. 177."""
    Rbt = tr(Rb)
    return blocks(Rbt, neg(mat_mul(Rbt, skew(tb))), zeros(3, 3), Rbt)


def exp_so3(theta):
    """Rodrigues formula, eq. 134 (float)."""
    th = math.sqrt(sum(x * x for x in theta))
    if th == 0:
        return [[float(i == j) for j in range(3)] for i in range(3)]
    k = skew([x / th for x in theta])
    k2 = mat_mul(k, k)
    return [[float(i == j) + math.sin(th) * k[i][j] + (1 - math.cos(th)) * k2[i][j]
             for j in range(3)] for i in range(3)]


def v_so3(theta):
    """V(theta), eq. 174 (float)."""
    th = math.sqrt(sum(x * x for x in theta))
    k = skew(theta)
    k2 = mat_mul(k, k)
    if th < 1e-4:                                    # Taylor expansions near zero
        a, b = 0.5 - th ** 2 / 24, 1 / 6 - th ** 2 / 120
    else:
        a = (1 - math.cos(th)) / th ** 2
        b = (th - math.sin(th)) / th ** 3
    return [[float(i == j) + a * k[i][j] + b * k2[i][j] for j in range(3)] for i in range(3)]


def exp_se3(tau):
    """SE(3) Exp of tau = (rho, theta), eq. 172; returns (R, t)."""
    rho, theta = tau[:3], tau[3:]
    return exp_so3(theta), mat_vec(v_so3(theta), rho)


def solve3(a, b):
    """Cramer's rule for a 3x3 linear system."""
    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    d = det(a)
    out = []
    for c in range(3):
        m = [row[:] for row in a]
        for r in range(3):
            m[r][c] = b[r]
        out.append(det(m) / d)
    return out


def log_se3(R, t):
    """SE(3) Log, eq. 173, with the SO(3) Log of eq. 135 (angles well inside (0, pi))."""
    s = 0.5 * math.sqrt((R[2][1] - R[1][2]) ** 2 + (R[0][2] - R[2][0]) ** 2 + (R[1][0] - R[0][1]) ** 2)
    c = (R[0][0] + R[1][1] + R[2][2] - 1) / 2
    th = math.atan2(s, c)
    w = [R[2][1] - R[1][2], R[0][2] - R[2][0], R[1][0] - R[0][1]]
    f = 0.5 + th ** 2 / 12 if th < 1e-4 else th / (2 * math.sin(th))
    theta = [f * x for x in w]
    return solve3(v_so3(theta), t) + theta


def to_mat4(R, t):
    return [R[0] + [t[0]], R[1] + [t[1]], R[2] + [t[2]], [0, 0, 0, 1]]


def ffloat(m):
    return [[float(x) for x in row] for row in m]


# --- Card scenario (constructed) ------------------------------------------------------------
# Body pose T_wb (body -> world) with mean rotation R_z(90 deg); right perturbation
# T_wb = mean(T_wb) Exp(tau_b), tau_b = (rho_b, theta_b), Sigma_b = diag(s_rho^2 I3, s_th^2 I3).
# Camera rigidly mounted: R_bc = I, t_bc = (0.5, 0, 0) m, treated as exact.
I3 = eye(3)
RZ90 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]           # exact R_z(90 deg)
L = F(1, 2)
t_bc = [L, 0, 0]
R_bc = I3
var_rho = F(2, 1000) ** 2                            # (2 mm)^2 = 4e-6 m^2
var_th = F(1, 100) ** 2                              # (0.01 rad)^2 = 1e-4 rad^2
Sigma_b = blocks([[var_rho if i == j else 0 for j in range(3)] for i in range(3)], zeros(3, 3),
                 zeros(3, 3), [[var_th if i == j else 0 for j in range(3)] for i in range(3)])

R_cb, t_cb = inv(R_bc, t_bc)
Ad_cb = adjoint(R_cb, t_cb)

# Check 1: Ad_{T_cb} = Ad_{T_bc}^-1 (eq. 33) equals the composition Jacobian of eq. 177, for the
# card's extrinsic and for a rotated one (body-to-optical axes, a translated arm).
R_opt = [[0, 0, 1], [-1, 0, 0], [0, -1, 0]]          # columns: camera x, y, z in body axes
t_opt = [F(1, 2), F(1, 10), F(-1, 5)]
for Rb_, tb_ in ((R_bc, t_bc), (R_opt, t_opt)):
    Ri, ti = inv(Rb_, tb_)
    assert adjoint(Ri, ti) == jac_compose_first(Rb_, tb_)
    assert mat_mul(adjoint(Ri, ti), adjoint(Rb_, tb_)) == eye(6)
assert Ad_cb == blocks(I3, neg(skew(t_bc)), zeros(3, 3), I3)
checks += 1

# Check 2: closed form rho_c = R_bc^T (rho_b + theta_b x t_bc), theta_c = R_bc^T theta_b, and for
# the card rho_c = (rho_x, rho_y + 0.5 theta_z, rho_z - 0.5 theta_y).
rng = random.Random(20261116)
for _ in range(50):
    tau = [F(rng.randint(-1000, 1000), 997) for _ in range(6)]
    Ri, ti = inv(R_opt, t_opt)
    got = mat_vec(adjoint(Ri, ti), tau)
    rho_c = mat_vec(tr(R_opt), [a + b for a, b in zip(tau[:3], cross(tau[3:], t_opt))])
    assert got == rho_c + mat_vec(tr(R_opt), tau[3:])
    got = mat_vec(Ad_cb, tau)
    assert got[:3] == [tau[0], tau[1] + L * tau[5], tau[2] - L * tau[4]] and got[3:] == tau[3:]
checks += 1

# Check 3: Sigma_c = Ad Sigma_b Ad^T, exactly: translation variances 4e-6, 2.9e-5, 2.9e-5 m^2;
# cov(rho_y, theta_z) = +5e-5 m rad, cov(rho_z, theta_y) = -5e-5 m rad; rotation block 1e-4 I.
Sigma_c = mat_mul(mat_mul(Ad_cb, Sigma_b), tr(Ad_cb))
expected = zeros(6, 6)
for i, v in enumerate([F(4, 10**6), F(29, 10**6), F(29, 10**6), var_th, var_th, var_th]):
    expected[i][i] = v
expected[1][5] = expected[5][1] = F(5, 10**5)
expected[2][4] = expected[4][2] = F(-5, 10**5)
assert Sigma_c == expected
checks += 1

# Check 4: standard deviations 2 mm and sqrt(2.9e-5) m = 5.39 mm; the lever-arm part alone is
# L * s_th = 5 mm; the copied Sigma_b is 2.69 times too small in sigma on y and z; adding the
# standard deviations (2 + 5 = 7 mm) instead of the variances is wrong.
sd_mm = [math.sqrt(Sigma_c[i][i]) * 1000 for i in range(3)]
assert [round(x, 2) for x in sd_mm] == [2.0, 5.39, 5.39]
assert L ** 2 * var_th == F(25, 10**6)                 # (5 mm)^2
assert round(sd_mm[1] / 2.0, 2) == 2.69 and round(sd_mm[1] / 2.0, 1) == 2.7 and round(sd_mm[1], 2) != 7.0
checks += 1

# Check 5: correlation of rho_y with theta_z is 5e-5 / (sqrt(2.9e-5) * 0.01) = 0.93; conditioning
# on a perfectly known yaw leaves rho_y variance 2.9e-5 - (5e-5)^2 / 1e-4 = 4e-6 m^2 (2 mm).
corr = float(Sigma_c[1][5]) / math.sqrt(float(Sigma_c[1][1] * Sigma_c[5][5]))
assert round(corr, 2) == 0.93 and round(-float(Sigma_c[2][4]) / math.sqrt(float(Sigma_c[2][2] * Sigma_c[4][4])), 2) == 0.93
assert Sigma_c[1][1] - Sigma_c[1][5] ** 2 / Sigma_c[5][5] == var_rho
checks += 1

# Check 6: the wrong direction, Ad_{T_bc}, gives the same variances here (R_bc = I) but flips the
# signs of both translation-rotation cross-covariances.
Ad_bc = adjoint(R_bc, t_bc)
Sigma_wrong = mat_mul(mat_mul(Ad_bc, Sigma_b), tr(Ad_bc))
assert all(Sigma_wrong[i][i] == Sigma_c[i][i] for i in range(6))
assert Sigma_wrong[1][5] == -Sigma_c[1][5] and Sigma_wrong[2][4] == -Sigma_c[2][4]
checks += 1

# Check 7 (worked example A): a body yaw of +0.01 rad gives rho_c = (0, 5 mm, 0) exactly; the camera
# origin really moves by V(theta_c) rho_c in camera axes = (-25 um, 4.99992 mm, 0): positive y, so
# the cross-covariance cov(rho_y, theta_z) must be positive.
tau_b = [0.0, 0.0, 0.0, 0.0, 0.0, 0.01]
tau_c = mat_vec(ffloat(Ad_cb), tau_b)
assert max(abs(a - b) for a, b in zip(tau_c, [0.0, 0.005, 0.0, 0.0, 0.0, 0.01])) < 1e-18
Rw, tw = compose(*exp_se3(tau_b), ffloat(R_bc), [float(x) for x in t_bc])   # body mean = identity
disp = [a - b for a, b in zip(tw, [0.5, 0.0, 0.0])]
assert max(abs(a - b) for a, b in zip(disp, mat_vec(v_so3(tau_c[3:]), tau_c[:3]))) < 1e-15
assert abs(disp[0] + 2.5e-5) < 1e-9 and disp[1] > 0 and abs(disp[1] - 0.005) < 1e-7
assert round(disp[0] * 1000, 3) == -0.025 and round(disp[1] * 1000, 5) == 4.99992 and disp[2] == 0
checks += 1

# Check 8: the transport is exact, not first order: T_cb Exp(tau_b) T_bc = Exp(Ad_{T_cb} tau_b) for
# large random increments (|theta| up to about 1.4 rad, |rho| up to 0.5 m), also with the rotated
# extrinsic; Log of the camera increment returns Ad tau_b.
for Rb_, tb_ in ((R_bc, t_bc), (R_opt, t_opt)):
    Rbf, tbf = ffloat(Rb_), [float(x) for x in tb_]
    Ri, ti = inv(Rbf, tbf)
    Ad = adjoint(Ri, ti)
    for _ in range(200):
        tau = [rng.uniform(-0.3, 0.3) for _ in range(3)] + [rng.uniform(-0.8, 0.8) for _ in range(3)]
        lhs = compose(*compose(Ri, ti, *exp_se3(tau)), Rbf, tbf)
        rhs = exp_se3(mat_vec(Ad, tau))
        assert max_abs_diff(to_mat4(*lhs), to_mat4(*rhs)) < 1e-12
        assert max(abs(a - b) for a, b in zip(log_se3(*lhs), mat_vec(Ad, tau))) < 1e-9
checks += 1

# Check 9: camera position in world axes. To first order (eq. 182 with p = 0, eq. 55) its
# covariance is R_wc Sigma_c,rhorho R_wc^T; with R_wc = R_wb R_bc = R_z(90 deg) this is
# diag(2.9e-5, 4e-6, 2.9e-5) m^2, i.e. 5.39, 2 and 5.39 mm along world x, y, z. The same matrix
# follows from the body pose acting on the point t_bc, Jacobian [R_wb, -R_wb [t_bc]x] (eq. 182).
R_wb = RZ90
R_wc = mat_mul(R_wb, R_bc)
S_pos = mat_mul(mat_mul(R_wc, sub(Sigma_c, 0, 0)), tr(R_wc))
assert S_pos == [[F(29, 10**6), 0, 0], [0, F(4, 10**6), 0], [0, 0, F(29, 10**6)]]
J_point = [ra + rb for ra, rb in zip(R_wb, neg(mat_mul(R_wb, skew(t_bc))))]
assert mat_mul(mat_mul(J_point, Sigma_b), tr(J_point)) == S_pos
assert [round(math.sqrt(S_pos[i][i]) * 1000, 2) for i in range(3)] == [5.39, 2.0, 5.39]
checks += 1

# Check 10: a left (world-frame) perturbation has the same covariance for body and camera,
# Ad_{T_wc} Sigma_c Ad_{T_wc}^T = Ad_{T_wb} Sigma_b Ad_{T_wb}^T, because Ad_{T_wc} Ad_{T_cb} = Ad_{T_wb}
# (eq. 34). For a camera at t_wc = (100, 0, 0) m its translation block has standard deviations of
# 5.39 mm, 1.000 m and 1.000 m along world x, y, z, although the camera position is known to
# 2-5.39 mm: rho_G moves the point at the world origin, not the camera origin.
t_wc = [100, 0, 0]
t_wb = [a - b for a, b in zip(t_wc, mat_vec(R_wb, t_bc))]
assert compose(R_wb, t_wb, R_bc, t_bc) == (R_wc, t_wc)
Ad_wc = adjoint(R_wc, t_wc)
Sigma_G = mat_mul(mat_mul(Ad_wc, Sigma_c), tr(Ad_wc))
Ad_wb = adjoint(R_wb, t_wb)
assert Sigma_G == mat_mul(mat_mul(Ad_wb, Sigma_b), tr(Ad_wb))
assert [Sigma_G[i][i] for i in range(3)] == [F(29, 10**6), 1 + F(4, 10**6), 1 + F(29, 10**6)]
sd_G = [math.sqrt(Sigma_G[i][i]) for i in range(3)]
assert round(sd_G[0] * 1000, 2) == 5.39 and round(sd_G[1], 3) == 1.0 and round(sd_G[2], 3) == 1.0
checks += 1

# Check 11: finite differences confirm the composition Jacobians at the card's poses: perturbing the
# body gives Ad_{T_cb} (eq. 65, 177); perturbing an uncertain extrinsic gives the identity (eq. 66,
# 178), so an independent extrinsic covariance adds unchanged to first order.
Rwbf, twbf = ffloat(R_wb), [float(x) for x in t_wb]
Rbcf, tbcf = ffloat(R_bc), [float(x) for x in t_bc]
Rwc0, twc0 = compose(Rwbf, twbf, Rbcf, tbcf)
Rinv, tinv = inv(Rwc0, twc0)
h = 1e-6
J_body = zeros(6, 6)
J_ext = zeros(6, 6)
for k in range(6):
    e = [h if i == k else 0.0 for i in range(6)]
    pert_b = compose(*compose(Rwbf, twbf, *exp_se3(e)), Rbcf, tbcf)
    pert_e = compose(Rwbf, twbf, *compose(Rbcf, tbcf, *exp_se3(e)))
    col_b = log_se3(*compose(Rinv, tinv, *pert_b))
    col_e = log_se3(*compose(Rinv, tinv, *pert_e))
    for i in range(6):
        J_body[i][k] = col_b[i] / h
        J_ext[i][k] = col_e[i] / h
assert max_abs_diff(J_body, ffloat(Ad_cb)) < 1e-6
assert max_abs_diff(J_ext, ffloat(eye(6))) < 1e-6
checks += 1

print(f"12-rotations-se3 (CV-SE3-007): {checks} checks passed")
