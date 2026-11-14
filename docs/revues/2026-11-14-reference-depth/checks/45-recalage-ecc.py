"""Recompute the constructed examples of CV-ECC (reference 45-recalage-ecc).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/45-recalage-ecc.py
The ECC update follows OpenCV 4.13.0 modules/video/src/ecc.cpp (L571-L605): Hessian G^T G,
lambda = (|i|^2 - i^T P i) / (t^T i - t^T P i) with P = G (G^T G)^-1 G^T, and
dp = (G^T G)^-1 G^T (lambda t - i). The Gaussian sigma rule comes from OpenCV 4.13.0
imgproc.hpp (getGaussianKernel). Signals, shifts and gains are constructed; the 1-D
simulations stand in for images and are not image experiments.
"""

import math
import random


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def zero_mean(v):
    m = sum(v) / len(v)
    return [x - m for x in v]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def ecc(t, i):
    t, i = zero_mean(t), zero_mean(i)
    return dot(t, i) / math.sqrt(dot(t, t) * dot(i, i))


checks = 0

# --- Example A: photometric invariance and normalized SSD -------------------
t = [10.0, 20.0, 30.0, 50.0, 35.0, 12.0]
# Check 1: a positive gain and an offset leave rho at 1; a negative gain flips it to -1.
assert close(ecc(t, [1.5 * x + 10 for x in t]), 1.0)
assert close(ecc(t, [-1.0 * x + 200 for x in t]), -1.0); checks += 1
i = [12.0, 18.0, 33.0, 44.0, 39.0, 9.0]
tz, iz = zero_mean(t), zero_mean(i)
tn = [x / math.sqrt(dot(tz, tz)) for x in tz]
inn = [x / math.sqrt(dot(iz, iz)) for x in iz]
# Check 2: the SSD between zero-mean unit-norm vectors equals 2 - 2 rho.
assert close(sum((a - b) ** 2 for a, b in zip(tn, inn)), 2 - 2 * ecc(t, i)); checks += 1


# --- Closed-form step maximizes the linearized correlation (n = 2) ----------
def solve2(h, g):
    det = h[0][0] * h[1][1] - h[0][1] * h[1][0]
    return [(h[1][1] * g[0] - h[0][1] * g[1]) / det, (-h[1][0] * g[0] + h[0][0] * g[1]) / det]


def ecc_step(G, t, i):
    """G: list of N rows with n=2 columns; t and i zero-mean. Returns (lambda, dp)."""
    cols = [[r[k] for r in G] for k in range(2)]
    H = [[dot(cols[a], cols[b]) for b in range(2)] for a in range(2)]
    gi = [dot(c, i) for c in cols]
    gt = [dot(c, t) for c in cols]
    hgi = solve2(H, gi)
    lam_n = dot(i, i) - dot(gi, hgi)
    lam_d = dot(t, i) - dot(gt, hgi)
    lam = lam_n / lam_d
    err = [lam * a - b for a, b in zip(t, i)]
    return lam, lam_d, solve2(H, [dot(c, err) for c in cols])


rng = random.Random(7)
N = 12
G = [[rng.uniform(-1, 1), rng.uniform(-1, 1)] for _ in range(N)]
t0 = zero_mean([rng.uniform(0, 1) for _ in range(N)])
i0 = zero_mean([a + rng.uniform(-0.3, 0.3) for a in t0])
lam, lam_d, dp = ecc_step(G, t0, i0)


def lin_corr(d):
    v = [a + r[0] * d[0] + r[1] * d[1] for a, r in zip(i0, G)]
    return dot(t0, v) / math.sqrt(dot(t0, t0) * dot(v, v))


best = lin_corr(dp)
# Check 3: with a positive denominator, the closed-form step is a local maximum of the
# linearized correlation t^T (i + G dp) / (|t| |i + G dp|): every nearby step scores lower.
assert lam_d > 0
for k in range(200):
    d = [dp[0] + rng.uniform(-0.05, 0.05), dp[1] + rng.uniform(-0.05, 0.05)]
    assert lin_corr(d) <= best + 1e-12
checks += 1

# --- Example B: a gain at the true alignment, ECC versus Lucas-Kanade ---------
W = 40
bump = [100 * math.exp(-(x - 34) ** 2 / (2 * 9)) for x in range(W)]   # sigma 3 px, near the right edge
img = [1.5 * b + 10 for b in bump]                                     # gain 1.5, offset 10, aligned
xs = range(1, W - 1)
gx = [0.5 * (img[x + 1] - img[x - 1]) for x in xs]                    # Jacobian of a 1-D translation
lk_step = dot(gx, [bump[x] - img[x] for x in xs]) / dot(gx, gx)
tz = zero_mean([bump[x] for x in xs])
iz = zero_mean([img[x] for x in xs])
H1 = dot(gx, gx)
lam1 = (dot(iz, iz) - dot(gx, iz) ** 2 / H1) / (dot(tz, iz) - dot(gx, tz) * dot(gx, iz) / H1)
ecc_dp = dot(gx, [lam1 * a - b for a, b in zip(tz, iz)]) / H1
# Check 4: ECC finds lambda = 1.5 and a zero step; SSD-based Lucas-Kanade moves by -0.157 px
# because the bump is truncated by the window and the gain is not modelled.
assert close(lam1, 1.5, 1e-9) and abs(ecc_dp) < 1e-9
assert close(lk_step, -0.157, 1e-3); checks += 1


# --- Example C: capture range of a 1-D ECC translation versus blur ------------
def interp(f, x):
    k = math.floor(x)
    a = x - k
    if k < 0 or k + 1 >= len(f):
        return None
    return (1 - a) * f[k] + a * f[k + 1]


def ecc_translate(T, I, p=0.0, iters=200):
    """Forward additive ECC for x -> x + p on 1-D signals; returns (p, status)."""
    for _ in range(iters):
        iw, gr, tv = [], [], []
        for x in range(len(T)):
            v, v1, v0 = interp(I, x + p), interp(I, x + p + 1), interp(I, x + p - 1)
            if v is None or v1 is None or v0 is None:
                continue                      # outside the input image: masked out
            iw.append(v); gr.append(0.5 * (v1 - v0)); tv.append(T[x])
        i_, t_ = zero_mean(iw), zero_mean(tv)
        h = dot(gr, gr)
        if h < 1e-12:
            return None, "no gradient"
        gi, gt = dot(gr, i_), dot(gr, t_)
        lam_den = dot(t_, i_) - gt * gi / h
        if lam_den <= 0:
            return None, "lambda denominator <= 0"
        lam_ = (dot(i_, i_) - gi * gi / h) / lam_den
        step = dot(gr, [lam_ * a - b for a, b in zip(t_, i_)]) / h
        p += step
        if abs(step) < 1e-4:
            return p, "converged"
    return p, "max iterations"


def bump_signal(sigma, shift=0.0, n=120, centre=60):
    return [100 * math.exp(-(x - centre - shift) ** 2 / (2 * sigma ** 2)) for x in range(n)]


def recovers(sigma, d):
    T = bump_signal(sigma)
    I = [1.5 * v + 10 for v in bump_signal(sigma, d)]
    p, status = ecc_translate(T, I)
    return p is not None and abs(p - d) < 0.05, status


# Check 5: with a bump of sigma = 3 px, shifts up to 7.75 px are recovered; at 8 px the
# lambda denominator becomes non-positive (OpenCV would throw StsNoConv).
assert recovers(3, 7.75)[0] and recovers(3, 8.0) == (False, "lambda denominator <= 0"); checks += 1
# Check 6: doubling the blur scale to sigma = 6 px extends the range to 12.75 px (fails at 13 px).
assert recovers(6, 12.75)[0] and not recovers(6, 13.0)[0]; checks += 1

# Check 7: OpenCV's default gaussFiltSize = 5 uses sigma = 0.3 ((5 - 1) / 2 - 1) + 0.8 = 1.1 px;
# a 15-px kernel gives 2.6 px.
sig = lambda k: 0.3 * ((k - 1) * 0.5 - 1) + 0.8
assert close(sig(5), 1.1) and close(sig(15), 2.6); checks += 1


# --- Example D: carrying a warp between pyramid levels ------------------------
def matmul(a, b):
    return [[sum(a[r][k] * b[k][c] for k in range(3)) for c in range(3)] for r in range(3)]


def apply(h, p):
    v = [h[r][0] * p[0] + h[r][1] * p[1] + h[r][2] for r in range(3)]
    return (v[0] / v[2], v[1] / v[2])


S = [[2.0, 0, 0], [0, 2.0, 0], [0, 0, 1.0]]
S_inv = [[0.5, 0, 0], [0, 0.5, 0], [0, 0, 1.0]]
Hc = [[1.01, 0.02, 3.0], [-0.01, 0.99, -1.5], [2e-4, -1e-4, 1.0]]
Hf = matmul(matmul(S, Hc), S_inv)
# Check 8: for x_coarse = x_fine / 2, H_fine = S H_coarse S^-1 doubles the translation, keeps the
# linear part and halves the projective row; it maps fine points consistently with H_coarse.
assert close(Hf[0][2], 6.0) and close(Hf[1][2], -3.0) and close(Hf[0][0], 1.01)
assert close(Hf[2][0], 1e-4) and close(Hf[2][1], -5e-5)
pf = (300.0, 180.0)
pc = apply(Hc, (pf[0] / 2, pf[1] / 2))
assert all(close(a, 2 * b, 1e-9) for a, b in zip(apply(Hf, pf), pc)); checks += 1

# --- Example E: lever arm of affine parameters in raw pixel coordinates -------
width = 640
mean_x2 = sum(x * x for x in range(width)) / width
# Check 9: with x = 0..639, the a11 Jacobian column x * Ix has a mean-square lever arm of
# 136,213.5 px^2 against 1 for tx, i.e. a ratio of about 369 in RMS magnitude.
assert close(mean_x2, 136213.5) and close(math.sqrt(mean_x2), 369.07, 1e-2); checks += 1

print(f"45-recalage-ecc: {checks} checks passed")
