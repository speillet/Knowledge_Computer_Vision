"""Recompute the constructed examples of CV-SVD (reference 11-moindres-carres-svd).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/11-moindres-carres-svd.py
Inputs come from the Ceres 2.2.0 covariance documentation (min_reciprocal_condition_number
example), Ceres 2.2.0 Solver::Options (initial_trust_region_radius = 1e4), Triggs et al. 2000
(Sec. 4.3, footnote 6) and Hartley 1997 (Sec. 4). The scenarios are constructed.
"""

import math
from fractions import Fraction

EPS = 2.0 ** -52  # IEEE double machine epsilon
checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def sym2_eig(a, b, c):
    """Eigenvalues (descending) and unit eigenvectors of [[a, b], [b, c]]."""
    tr, det = a + c, a * c - b * b
    disc = math.sqrt(max(tr * tr / 4 - det, 0.0))
    l1 = tr / 2 + disc
    l2 = det / l1 if l1 else 0.0  # product form avoids cancellation
    vecs = []
    for lam in (l1, l2):
        if abs(b) > 0:
            v = (b, lam - a)
        else:
            v = (1.0, 0.0) if lam == a else (0.0, 1.0)
        n = math.hypot(*v)
        vecs.append((v[0] / n, v[1] / n))
    return (l1, l2), vecs


def gram(cols):
    c1, c2 = cols
    return sum(x * x for x in c1), sum(x * y for x, y in zip(c1, c2)), sum(y * y for y in c2)


# --- Example A: focal length and depth from a planar target ------------------
# Pinhole, principal point known, 1-D image coordinate u = f X / Z (px), with
# f = 1000 px, target centre at Z0 = 2 m and five target points at s = -0.2..0.2 m.
F_PX, Z0, NOISE_PX = 1000.0, 2.0, 0.5
S = [-0.2, -0.1, 0.0, 0.1, 0.2]


def jacobian_columns(tilt_deg):
    t = math.radians(tilt_deg)
    xs = [s * math.cos(t) for s in S]
    zs = [Z0 + s * math.sin(t) for s in S]
    col_f = [x / z for x, z in zip(xs, zs)]                 # du/df, px per px
    col_z = [-F_PX * x / z ** 2 for x, z in zip(xs, zs)]    # du/dZ, px per m
    return col_f, col_z


# Check 1: fronto-parallel target, the two Jacobian columns are exactly proportional
# (du/dZ = -(f/Z) du/df), so J^T J is singular in exact arithmetic: only f/Z is observable.
cf = [Fraction(s, 10) / 2 for s in (-2, -1, 0, 1, 2)]
cz = [-1000 * x / 2 for x in cf]
a, b, c = gram((cf, cz))
assert a * c - b * b == 0
checks += 1

# Check 2: the null direction is (delta f, delta Z) proportional to (f, Z):
# scaling f and Z by the same factor leaves every u unchanged.
assert all(x * 1000 + y * 2 == 0 for x, y in zip(cf, cz))
checks += 1


def scaled_ratio(tilt):
    col_f, col_z = jacobian_columns(tilt)
    n1 = math.sqrt(sum(x * x for x in col_f))
    n2 = math.sqrt(sum(x * x for x in col_z))
    (l1, l2), _ = sym2_eig(*gram(([x / n1 for x in col_f], [x / n2 for x in col_z])))
    return math.sqrt(max(l2, 0.0)) / math.sqrt(l1)


ratio_30 = scaled_ratio(30)
# Check 3: tilting the target by 30 deg separates f and Z, but after scaling the columns to
# unit norm sigma_min/sigma_max is only about 0.023 (condition number about 44).
assert close(ratio_30, 0.02287, 1e-4) and close(1 / ratio_30, 43.7, 0.1)
checks += 1

col_f, col_z = jacobian_columns(30)
a, b, c = gram((col_f, col_z))
det = a * c - b * b
std_f = NOISE_PX * math.sqrt(c / det)
std_z = NOISE_PX * math.sqrt(a / det)
corr = -b / math.sqrt(a * c)
# Check 4: with 0.5 px noise on 5 points, sigma^2 (J^T J)^{-1} gives std(f) ~ 80 px,
# std(Z) ~ 0.16 m and a correlation of ~0.999 between f and Z.
assert close(std_f, 79.6, 0.1) and close(std_z, 0.158, 1e-3) and corr > 0.998
checks += 1

# --- Example B: forming J^T J squares the condition number (Ceres example) ----
J = [[1.0, 1.0], [1.0, 1.0000001]]
JF = [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(10000001, 10000000)]]
a, b, c = gram(([JF[0][0], JF[1][0]], [JF[0][1], JF[1][1]]))
d = a * c - b * b
exact_00 = float(c / d)
# Check 5: in exact arithmetic (J^T J)^{-1}_{00} = 2.0000002e14.
assert close(exact_00, 2.0000002e14, 1e3)
checks += 1

a, b, c = gram(([J[0][0], J[1][0]], [J[0][1], J[1][1]]))
float_00 = c / (a * c - b * b)
# Check 6: forming J^T J in double and inverting it gives 2.0471e14, the value printed in the
# Ceres documentation: a 2.4% error caused by rounding the entries of J^T J.
assert close(float_00, 2.0471e14, 0.0001e14) and close(float_00 / exact_00 - 1, 0.0235, 5e-4)
checks += 1

dj = J[0][0] * J[1][1] - J[0][1] * J[1][0]
jinv = [[J[1][1] / dj, -J[0][1] / dj], [-J[1][0] / dj, J[0][0] / dj]]
via_j_00 = jinv[0][0] ** 2 + jinv[0][1] ** 2
# Check 7: inverting J itself (condition number ~4e7 instead of ~1.6e15) keeps the
# (J^T J)^{-1} entry within 2e-9 relative of the exact value.
assert abs(via_j_00 / exact_00 - 1) < 2e-9
checks += 1

# Singular values of the 2x2 J from sigma1*sigma2 = |det J| and sigma1^2 + sigma2^2 = ||J||_F^2,
# which avoids forming J^T J (whose float eigenvalues would be wrong, as check 6 shows).
fro2 = sum(x * x for row in J for x in row)
s1sq = (fro2 + math.sqrt(fro2 ** 2 - 4 * dj ** 2)) / 2
kappa_j = math.sqrt(s1sq / (dj ** 2 / s1sq))
# Check 8: kappa(J) ~ 4e7, so kappa(J^T J) = kappa(J)^2 ~ 1.6e15 and kappa^2 * eps ~ 0.36:
# the Triggs footnote-6 bound O(kappa^2 eps) allows errors of tens of percent.
assert 3.9e7 < kappa_j < 4.1e7 and 0.3 < kappa_j ** 2 * EPS < 0.4
checks += 1

# Check 9: error-budget reading for kappa(A) = 1e6: about 6 decimal digits at risk with QR
# (kappa eps ~ 2e-10) and about 12 with the normal equations (kappa^2 eps ~ 2e-4).
assert close(math.log10(1e6), 6) and close(math.log10(1e6 ** 2), 12)
assert 1e-10 < 1e6 * EPS < 1e-9 and 1e-4 < 1e12 * EPS < 1e-3
checks += 1

# --- Example C: Levenberg-Marquardt damping as a spectral filter --------------
LAMBDA0 = 1 / 1e4  # Ceres: initial regularization = 1 / initial_trust_region_radius


def lm_filter(sigma, lam):
    """Factor sigma^2 / (sigma^2 + lam) applied to the Gauss-Newton step along v_i (D = I)."""
    return sigma ** 2 / (sigma ** 2 + lam)


# Check 10: with lambda = 1e-4, a direction with sigma = 1 keeps 99.99% of its Gauss-Newton
# step, a direction with sigma = 1e-3 keeps only 1/101 ~ 0.99%.
assert close(lm_filter(1.0, LAMBDA0), 0.9999, 1e-6)
assert close(lm_filter(1e-3, LAMBDA0), 1 / 101, 1e-9)
checks += 1

# --- Existing executed example (2026-10-23), recomputed with the stdlib -------
A = [[1.0, 1.0], [1.0, 1.001], [1.0, 0.999]]
cols = ([r[0] for r in A], [r[1] for r in A])
(e1, e2), (v1, v2) = sym2_eig(*gram(cols))
s1, s2 = math.sqrt(e1), math.sqrt(e2)
# Check 11: sigma_2 ~ 1.0e-3 and kappa_2(A) ~ 2.4e3, as stated in the note.
assert close(s2, 1.0e-3, 1e-7) and close(s1 / s2, 2449.5, 0.1)
checks += 1
u2 = [(r[0] * v2[0] + r[1] * v2[1]) / s2 for r in A]
db = [1e-3 * x for x in u2]
# delta x = V Sigma^{-1} U^T delta b = (1e-3 / sigma_2) v_2 since delta b is along u_2.
dx_norm = 1e-3 / s2
# Check 12: a perturbation of norm 1e-3 along u_2 moves x by ~1.0 along v_2 ~ (1, -1)/sqrt(2)
# and adds no residual, because u_2 lies in the column space of A.
assert close(dx_norm, 1.0, 1e-6) and close(abs(v2[0]), 1 / math.sqrt(2), 1e-3)
assert v2[0] * v2[1] < 0
assert close(math.sqrt(sum(x * x for x in db)), 1e-3, 1e-12)
checks += 1

# --- Whitening example of CV-SVD-003 -----------------------------------------
r_px, s_px, r_mm, s_mm = 0.8, 0.5, 3.0, 2.0
# Check 13: raw sums depend on the unit (0.64 in metres, 9.64 in millimetres), the whitened
# sum does not (4.81 in both cases).
assert close(r_px ** 2 + (r_mm / 1000) ** 2, 0.640009, 1e-9)
assert close(r_px ** 2 + r_mm ** 2, 9.64)
assert close((r_px / s_px) ** 2 + ((r_mm / 1000) / (s_mm / 1000)) ** 2, 4.81)
checks += 1

# --- Hartley 1997 Sec. 4: magnitudes in one row of the 8-point system ----------
u, v = 100.0, 100.0  # typical point of a 200 x 200 image, both images
row = [u * u, u * v, u, v * u, v * v, v, u, v, 1.0]
# Check 14: the diagonal of A^T A contributed by such a row spans 1e8 down to 1.
assert max(x * x for x in row) == 1e8 and min(x * x for x in row) == 1.0
checks += 1

print(f"{checks} checks passed for CV-SVD (11-moindres-carres-svd)")
