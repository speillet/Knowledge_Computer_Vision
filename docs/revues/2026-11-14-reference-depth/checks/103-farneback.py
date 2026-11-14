"""Recompute the constructed examples of CV-FARNEBACK (reference 103-farneback).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/103-farneback.py
Inputs come from Farnebäck 2003 (SCIA, Sec. 3 eqs. 2-14 and 21-23, Sec. 4 parameters)
and OpenCV 4.13.0 modules/video/src/optflowgf.cpp (pyramid loop, determinant term 1e-3).
The signals and scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


checks = 0

# --- Example A: exact translation of a 2-D quadratic (eqs. 2-8) -------------------
A = [[2.0, 0.0], [0.0, 1.0]]
b1 = [3.0, -1.0]
c1 = 5.0
d = [2.0, -1.0]


def matvec(m, v):
    return [m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1]]


def f1(x):
    return sum(x[i] * matvec(A, x)[i] for i in range(2)) + b1[0] * x[0] + b1[1] * x[1] + c1


Ad = matvec(A, d)
b2 = [b1[i] - 2 * Ad[i] for i in range(2)]
c2 = sum(d[i] * Ad[i] for i in range(2)) - (b1[0] * d[0] + b1[1] * d[1]) + c1


def f2(x):
    return sum(x[i] * matvec(A, x)[i] for i in range(2)) + b2[0] * x[0] + b2[1] * x[1] + c2


# Check 1: f2(x) = f1(x - d) at several points, i.e. eqs. 4-6 hold (A2 = A1, b2 = b1 - 2 A d, c2).
for x in ([0, 0], [1.5, -2], [-3, 4]):
    assert close(f2(x), f1([x[0] - d[0], x[1] - d[1]]), 1e-9)
checks += 1
# Check 2: the card example, b1 - b2 = (8, -2) and 2 A d = b1 - b2 give d = (2, -1) px (eq. 7).
diff = [b1[i] - b2[i] for i in range(2)]
assert diff == [8.0, -2.0] and [diff[0] / (2 * A[0][0]), diff[1] / (2 * A[1][1])] == d
checks += 1

# --- Polynomial expansion by weighted least squares (Sec. 2) ------------------------
N, SIGMA = 5, 1.5           # 11-tap Gaussian applicability, as in Sec. 4 (11x11, sigma 1.5)
G = [math.exp(-t * t / (2 * SIGMA * SIGMA)) for t in range(-N, N + 1)]
TAPS = list(range(-N, N + 1))


def solve3(m, v):
    m = [row[:] + [v[i]] for i, row in enumerate(m)]
    for i in range(3):
        p = max(range(i, 3), key=lambda r: abs(m[r][i]))
        m[i], m[p] = m[p], m[i]
        for r in range(3):
            if r != i:
                f = m[r][i] / m[i][i]
                for c in range(i, 4):
                    m[r][c] -= f * m[i][c]
    return [m[i][3] / m[i][i] for i in range(3)]


def expand(f, x0):
    """Fit c + b t + a t^2 to f(x0 + t), t in [-N, N], with Gaussian applicability."""
    basis = [[1.0, t, t * t] for t in TAPS]
    m = [[sum(G[k] * basis[k][i] * basis[k][j] for k in range(len(TAPS))) for j in range(3)]
         for i in range(3)]
    v = [sum(G[k] * basis[k][i] * f(x0 + TAPS[k]) for k in range(len(TAPS))) for i in range(3)]
    c, b, a = solve3(m, v)
    return a, b, c


quad = lambda x: 2 * x * x + 3 * x + 7
a_q, b_q, c_q = expand(quad, 0)
a_s, b_s, _ = expand(lambda x: quad(x - 1.5), 0)
# Check 3: the expansion is exact on a quadratic, and a 1.5 px shift gives b2 = b1 - 2 a d = -3.
assert close(a_q, 2, 1e-9) and close(b_q, 3, 1e-9) and close(c_q, 7, 1e-9)
assert close(a_s, 2, 1e-9) and close(b_s, -3, 1e-9)
checks += 1

# --- Example B: offset and gain between the frames (1-D form of eqs. 9-11) -----------


def d_hat_1d(a1, b1_, a2, b2_):
    """A = (a1 + a2) / 2, delta_b = -(b2 - b1) / 2, A d = delta_b."""
    return (-(b2_ - b1_) / 2) / ((a1 + a2) / 2)


a, d1 = 1.0, 1.0
for b_first, expected in ((4.0, 0.727), (0.0, 1.091)):
    # Offset only: f2 = f1(x - d) + 30 changes c, not a or b.
    assert close(d_hat_1d(a, b_first, a, b_first - 2 * a * d1), d1, 1e-12)
    # Gain 1.2: f2 = 1.2 f1(x - d) scales a and b of the second frame.
    gain = 1.2
    est = d_hat_1d(a, b_first, gain * a, gain * (b_first - 2 * a * d1))
    # Check 4: an additive offset leaves the estimate exact; a 20 % gain change biases it,
    # by -0.27 px when the window centre is 2 px from the extremum (b1 = 4) and +0.09 px at it.
    assert close(est, expected, 1e-3)
checks += 1

# --- Example C: displacement range and a priori displacement (Sec. 3.4-3.5) ----------
LAMBDA = 16.0


def signal(x):
    return 50 * math.sin(2 * math.pi * x / LAMBDA) + 20 * math.sin(2 * math.pi * x / (LAMBDA * 0.37) + 1.0)


WIN = range(-7, 8)   # 15-pixel aggregation window with uniform weights (eq. 13 in 1-D)


def estimate(d_true, prior=0.0):
    shifted = lambda x: signal(x - d_true)
    num = den = 0.0
    p = round(prior)                       # a priori displacement rounded to an integer (Sec. 3.4)
    for x in WIN:
        a1_, b1_, _ = expand(signal, x)
        a2_, b2_, _ = expand(shifted, x + p)
        a_mean = (a1_ + a2_) / 2           # eq. 21
        db = -(b2_ - b1_) / 2 + a_mean * p  # eq. 22
        num += a_mean * db
        den += a_mean * a_mean
    return num / den


def iterate(d_true, n=6):
    seq = [estimate(d_true)]
    for _ in range(n - 1):
        seq.append(estimate(d_true, prior=seq[-1]))
    return seq


# Check 5: one step is accurate for small shifts and degrades as the shift grows relative to the
# 11-tap applicability: 0.5 -> 0.500, 1.5 -> 1.650, 2.6 -> 2.965, 4.4 -> 1.821 px.
assert close(estimate(0.5), 0.4999, 1e-4) and close(estimate(1.5), 1.650, 1e-3)
assert close(estimate(2.6), 2.965, 1e-3) and close(estimate(4.4), 1.821, 1e-3)
checks += 1
# Check 6: iterating with the rounded a priori field recovers 1.5, 2.602, 4.398 and 8.0 px.
for d_true, final in ((1.5, 1.5), (2.6, 2.602), (4.4, 4.398), (8.0, 8.0)):
    assert close(iterate(d_true)[-1], final, 1e-3)
checks += 1
# Check 7: a 10 px shift, beyond half the 16 px dominant wavelength, converges to a wrong -6.80 px.
assert close(iterate(10.0, 9)[-1], -6.799, 1e-3)
checks += 1

# --- Example D: OpenCV 4.13 pyramid and determinant term (optflowgf.cpp) -------------


def opencv_levels(width, height, levels, pyr_scale, min_size=32):
    k, scale = 0, 1.0
    while k < levels:
        scale *= pyr_scale
        if width * scale < min_size or height * scale < min_size:
            break
        k += 1
    return k


# Check 8: 640x480 with levels=5 and pyr_scale=0.5 keeps 3 coarser levels (40x30 is below 32 px).
assert opencv_levels(640, 480, 5, 0.5) == 3
checks += 1
# Check 9: each level blurs the full-resolution image with sigma = (1/scale - 1) / 2 before resizing,
# i.e. 0.5, 1.5 and 3.5 px for scales 1/2, 1/4 and 1/8; flow is multiplied by 1/pyr_scale = 2 upwards.
assert [(1 / 0.5 ** k - 1) * 0.5 for k in (1, 2, 3)] == [0.5, 1.5, 3.5] and 1 / 0.5 == 2
checks += 1


def shrink(lam, eps=1e-3):
    """Isotropic A = lam I and consistent data: flow = d * lam^4 / (lam^4 + eps)."""
    return lam ** 4 / (lam ** 4 + eps)


# Check 10: the 1e-3 added to the determinant shrinks vectors where curvature is weak:
# lambda = 0.1, 0.2, 0.5 grey level/px^2 keep 9 %, 62 % and 98 % of the true displacement.
assert close(shrink(0.1), 0.0909, 1e-4) and close(shrink(0.2), 0.6154, 1e-4) and close(shrink(0.5), 0.9843, 1e-4)
checks += 1

# --- Card arithmetic -------------------------------------------------------------------
# Check 11: flow[y,x] = (4, -2) over 40 ms is (100, -50) px/s and points to (x + 4, y - 2).
assert close(4 / 0.040, 100) and close(-2 / 0.040, -50)
checks += 1
# Check 12: three halvings turn 32 px into 4 px and a 6 px object into 0.75 px.
assert 32 / 2 ** 3 == 4 and 6 / 2 ** 3 == 0.75
checks += 1
# Check 13: F(x) = 1, B(y) = -y; at x = 0 the round trip evaluated at x + F(x) = 1 gives 0,
# whereas evaluating B at the same index 0 gives a residual of 1.
F = lambda x: 1.0
B = lambda y: -y
assert F(0) + B(0 + F(0)) == 0 and F(0) + B(0) == 1
checks += 1

print(f"103-farneback: {checks} checks passed")
