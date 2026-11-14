"""Recompute the constructed examples of CV-FLOT (reference 101-flot-optique).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/101-flot-optique.py
Inputs come from Lucas and Kanade 1981 (Sec. 4.1-4.5), Bouguet's pyramidal LK report
(Sec. 2.2-2.3), RAFT (arXiv 2003.12039v3, Sec. 3.2) and its official code
(princeton-vl/RAFT at commit 2888e15: core/corr.py, core/utils/utils.py), KITTI 2015
(Menze and Geiger, Sec. 5) and OpenCV 4.13.0 lkpyramid.cpp. The scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


checks = 0

# --- Example A: iterative Lucas-Kanade on a constructed patch ------------------
# Image 1: a smooth blob plus a horizontal ramp, in grey levels; pixel centres at integers.
def i1(x, y):
    return 100.0 * math.exp(-((x - 1.0) ** 2 / 18.0 + (y + 0.5) ** 2 / 8.0)) + 4.0 * x


WINDOW = [(x, y) for x in range(-3, 4) for y in range(-3, 4)]  # 7x7 window, N = 49


def grad(f, x, y):
    """Central differences, as in Bouguet eqs. 19-20 (OpenCV uses Scharr instead)."""
    return ((f(x + 1, y) - f(x - 1, y)) / 2.0, (f(x, y + 1) - f(x, y - 1)) / 2.0)


def gradient_matrix(f):
    g11 = g12 = g22 = 0.0
    for x, y in WINDOW:
        gx, gy = grad(f, x, y)
        g11 += gx * gx
        g12 += gx * gy
        g22 += gy * gy
    return g11, g12, g22


def eigen(g11, g12, g22):
    tr, det = g11 + g22, g11 * g22 - g12 * g12
    root = math.sqrt(tr * tr - 4.0 * det)
    return (tr - root) / 2.0, (tr + root) / 2.0, det


def iterative_lk(d_true, max_iter=20, eps=0.01):
    """Bouguet Sec. 2.3: G fixed from image 1, b_k recomputed, nu_k = nu_{k-1} + G^-1 b_k.

    Image 2 is i1 translated by d_true and sampled analytically (no interpolation error).
    """
    def i2(x, y):
        return i1(x - d_true[0], y - d_true[1])

    g11, g12, g22 = gradient_matrix(i1)
    det = g11 * g22 - g12 * g12
    nu = [0.0, 0.0]
    errors = []
    for _ in range(max_iter):
        b1 = b2 = 0.0
        for x, y in WINDOW:
            gx, gy = grad(i1, x, y)
            diff = i1(x, y) - i2(x + nu[0], y + nu[1])
            b1 += diff * gx
            b2 += diff * gy
        eta = ((g22 * b1 - g12 * b2) / det, (-g12 * b1 + g11 * b2) / det)
        nu = [nu[0] + eta[0], nu[1] + eta[1]]
        errors.append(math.hypot(nu[0] - d_true[0], nu[1] - d_true[1]))
        if math.hypot(*eta) < eps:
            break
    return nu, errors


lmin, lmax, _ = eigen(*gradient_matrix(i1))
# Check 1: the textured patch has two well-separated non-zero eigenvalues (both directions observable).
assert close(lmin / len(WINDOW), 148.06, 0.01) and close(lmax / len(WINDOW), 315.29, 0.01)
checks += 1

nu, errs = iterative_lk((1.5, -0.8))
# Check 2: for d = (1.5, -0.8) px the single linearized step misses by ~0.11 px,
# and three iterations bring the error below 0.001 px.
assert close(errs[0], 0.108, 1e-3) and len(errs) == 3 and errs[-1] < 1e-3
checks += 1

nu, errs = iterative_lk((3.0, 1.0))
# Check 3: a larger displacement (3, 1) px gives a ~0.52 px first-step error; 4 iterations converge.
assert close(errs[0], 0.525, 1e-3) and len(errs) == 4 and errs[-1] < 1e-3
checks += 1


# Edge patch: intensity varies along x only, so G has rank 1.
def edge(x, y):
    return 0.5 * x * x


e_min, e_max, e_det = eigen(*gradient_matrix(edge))
# Check 4: an edge gives lambda_min = 0 and det(G) = 0: the tangential (y) component is unobservable.
assert e_min == 0.0 and e_det == 0.0 and e_max > 0.0
checks += 1

# --- Example B: convergence range of LK on a periodic texture (LK 1981, Sec. 4.3) ----
WAVELENGTH = 8.0  # px


def sin_f(x):
    return math.sin(2.0 * math.pi * x / WAVELENGTH)


def sin_fp(x):
    return 2.0 * math.pi / WAVELENGTH * math.cos(2.0 * math.pi * x / WAVELENGTH)


SAMPLES = [k * 0.25 for k in range(64)]  # two full periods


def lk_1d(h_true, iters=100):
    """Unweighted iterative 1-D LK (eq. 10 with w = 1): G(x) = F(x + h_true)."""
    h = 0.0
    for _ in range(iters):
        num = sum(sin_fp(x + h) * (sin_f(x + h_true) - sin_f(x + h)) for x in SAMPLES)
        den = sum(sin_fp(x + h) ** 2 for x in SAMPLES)
        h += num / den
    return h


# Check 5: displacements below half a wavelength (4 px) are recovered exactly.
assert close(lk_1d(3.0), 3.0, 1e-9) and close(lk_1d(3.9), 3.9, 1e-9)
checks += 1
# Check 6: beyond half a wavelength the iteration converges to the aliased solution h - lambda.
assert close(lk_1d(4.1), -3.9, 1e-9) and close(lk_1d(6.0), -2.0, 1e-9)
checks += 1
# Check 7: halving resolution halves both displacement and wavelength, so h / lambda is unchanged:
# a pyramid level cannot by itself rescue a purely periodic texture.
for level in range(4):
    assert close((6.0 / 2 ** level) / (WAVELENGTH / 2 ** level), 0.75, 1e-12)
checks += 1

# Pyramid gain (Bouguet Sec. 2.2): d_max_final = (2^(Lm+1) - 1) d_max.
L_M = 3                 # OpenCV default maxLevel
OMEGA = (21 - 1) // 2   # OpenCV default winSize 21x21 -> half-width 10 px
# Check 8: Lm = 3 multiplies the per-level range by 15; with Bouguet's heuristic d <= omega = 10 px
# this gives about 150 px at full resolution (a heuristic bound, not a guarantee).
assert 2 ** (L_M + 1) - 1 == 15 and (2 ** (L_M + 1) - 1) * OMEGA == 150
checks += 1

# --- Example C: RAFT correlation volume, lookup and range ------------------------------


def pad8(n):
    """InputPadder in core/utils/utils.py pads each dimension to a multiple of 8."""
    return n + (((n // 8) + 1) * 8 - n) % 8


def corr_entries(h, w, levels=4):
    h8, w8 = pad8(h) // 8, pad8(w) // 8
    n = h8 * w8
    pooled = 0
    ph, pw = h8, w8
    for _ in range(levels):            # avg_pool2d(2, stride=2) floors odd sizes
        pooled += ph * pw
        ph, pw = ph // 2, pw // 2
    return n, n * n, n * pooled


n_sintel, full_sintel, pyr_sintel = corr_entries(436, 1024)
# Check 9: Sintel 1024x436 is padded to 1024x440, i.e. a 128x55 feature grid (7,040 cells);
# the full 4-D volume has 49.6 M entries (198 MB in float32) and the 4-level pyramid 65.3 M (261 MB).
assert pad8(436) == 440 and n_sintel == 7040 and full_sintel == 49_561_600
assert close(full_sintel * 4 / 1e6, 198.2, 0.1) and close(pyr_sintel * 4 / 1e6, 261.3, 0.1)
checks += 1

n_hd, full_hd, pyr_hd = corr_entries(1088, 1920)
# Check 10: at 1088x1920 the grid has 32,640 cells and level 1 alone holds 1.07 G entries
# (4.26 GB in float32): memory grows with the square of the pixel count.
assert n_hd == 32_640 and close(full_hd * 4 / 1e9, 4.261, 1e-3)
assert close(full_hd / full_sintel, (n_hd / n_sintel) ** 2, 1e-9)
checks += 1

RADIUS, LEVELS, STRIDE = 4, 4, 8
square = (2 * RADIUS + 1) ** 2
diamond = sum(1 for dx in range(-RADIUS, RADIUS + 1) for dy in range(-RADIUS, RADIUS + 1)
              if abs(dx) + abs(dy) <= RADIUS)
# Check 11: the code samples a (2r+1)^2 = 81-point square per level (324 features over 4 levels),
# whereas the L1 ball of the paper's eq. 2 has 41 points (164 features).
assert square == 81 and LEVELS * square == 324 and diamond == 41 and LEVELS * diamond == 164
checks += 1
# Check 12: radius 4 at the coarsest level (pool 8) on 1/8-resolution features spans 4*8*8 = 256 px.
assert RADIUS * 2 ** (LEVELS - 1) * STRIDE == 256
checks += 1

# --- Example D: units of OpenCV's minEigThreshold (lkpyramid.cpp, 4.13.0) ------------
# Scharr derivative of a unit ramp: vertical [3 10 3] smoothing then [-1 0 1] difference.
ramp = [[x for x in range(5)] for _ in range(5)]
scharr_x = sum((ramp[1 + dy][2 + 1] - ramp[1 + dy][2 - 1]) * wgt
               for dy, wgt in ((-1, 3), (0, 10), (1, 3)))
# Check 13: Scharr returns 32 per grey level/px of true gradient.
assert scharr_x == 32
checks += 1
FLT_SCALE = 1.0 / (1 << 20)
# minEig = lambda_min(sum (32 g)(32 g)^T) * FLT_SCALE / N = lambda_min(sum g g^T) / (1024 N)
# Check 14: the default threshold 1e-4 means lambda_min(sum g g^T) / N >= 0.1024 (grey level/px)^2,
# i.e. an RMS gradient of about 0.32 grey level/px along the weakest direction.
threshold = 1e-4
per_pixel = threshold / (32 * 32 * FLT_SCALE)
assert close(per_pixel, 0.1024, 1e-9) and close(math.sqrt(per_pixel), 0.32, 1e-3)
checks += 1

# --- Example E: units and KITTI outlier rule ----------------------------------------
# Check 15: 4 px between frames 20 ms apart is 200 px/s; 40 ms gives 100 px/s; 50 ms gives 80 px/s.
assert close(4 / 0.020, 200) and close(4 / 0.040, 100) and close(4 / 0.050, 80)
checks += 1
# Check 16: RAFT upsampling multiplies 1/8-resolution flow by 8: 0.5 feature cells -> 4 px.
assert 8 * 0.5 == 4.0
checks += 1


def kitti_outlier(epe, gt_norm):
    """Menze and Geiger 2015, Sec. 5: an error counts only if it exceeds 3 px and 5% of the true value."""
    return epe > 3.0 and epe > 0.05 * gt_norm


# Check 17: a 4 px error on a 100 px motion is an inlier (4 < 5 px), but an outlier on a 20 px motion.
assert not kitti_outlier(4.0, 100.0) and kitti_outlier(4.0, 20.0)
# and a 2.9 px error is always an inlier, however small the motion.
assert not kitti_outlier(2.9, 1.0)
checks += 1

print(f"101-flot-optique: {checks} checks passed")
