"""Recompute the constructed examples of CV-FILTRES (reference 31-filtrage-gradients).

Stdlib only. Run with:
    python3 docs/revues/2026-11-14-reference-depth/checks/31-filtrage-gradients.py
Kernels come from OpenCV 4.13.0 imgproc.hpp (Sobel, Scharr, getGaussianKernel sigma rule,
pyrDown) and smooth.dispatch.cpp (kernel size from sigma); the pyramid constraint comes from
Burt and Adelson 1983 (equal contribution). Noise levels, ramps and edges are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def correlate_ramp(kernel, slope=1.0):
    """Response of a 3-column kernel (rows x cols) to I(x, y) = slope * x at the centre."""
    rows, cols = len(kernel), len(kernel[0])
    cc = (cols - 1) // 2
    return sum(kernel[r][c] * slope * (c - cc) for r in range(rows) for c in range(cols))


def noise_gain(kernel):
    return math.sqrt(sum(v * v for row in kernel for v in row))


SOBEL_X = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
SCHARR_X = [[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]]
CENTRAL = [[-1, 0, 1]]

# --- Example A: noise and signal gain of derivative kernels -------------------
# Check 1: ramp responses 2g, 8g and 32g (unnormalized kernels).
assert correlate_ramp(CENTRAL) == 2 and correlate_ramp(SOBEL_X) == 8 and correlate_ramp(SCHARR_X) == 32
checks += 1
# Check 2: noise gains sqrt(2) = 1.41, sqrt(12) = 3.46 and sqrt(236) = 15.36.
assert close(noise_gain(CENTRAL), 1.414) and close(noise_gain(SOBEL_X), 3.464) and close(noise_gain(SCHARR_X), 15.362)
checks += 1
ratios = [correlate_ramp(k) / noise_gain(k) for k in (CENTRAL, SOBEL_X, SCHARR_X)]
# Check 3: ratios 1.41, 2.31 and 2.08; Sobel improves on the central difference by about 1.6.
assert close(ratios[0], 1.414) and close(ratios[1], 2.309) and close(ratios[2], 2.083)
assert close(ratios[1] / ratios[0], 1.633)
checks += 1
# Check 4: a Sobel threshold of 100 corresponds to 400 on Scharr for the same edge.
assert close(100 * correlate_ramp(SCHARR_X) / correlate_ramp(SOBEL_X), 400)
checks += 1
# Check 5: Sobel x is the outer product of [1, 2, 1]^T and [-1, 0, 1].
assert SOBEL_X == [[s * d for d in (-1, 0, 1)] for s in (1, 2, 1)]
assert SCHARR_X == [[s * d for d in (-1, 0, 1)] for s in (3, 10, 3)]
checks += 1

# --- Example B: bilateral weights in the right units ---------------------------


def range_weight(diff, sigma_r):
    return math.exp(-diff ** 2 / (2 * sigma_r ** 2))


# Check 6: uint8, sigma_r = 10: 50 DN edge -> 3.7e-6; 7 DN noise -> 0.78.
assert close(range_weight(50, 10), 3.727e-6, 1e-8) and close(range_weight(7, 10), 0.7827, 1e-4)
checks += 1
# Check 7: after /255 with sigma_r kept at 10, the edge weight becomes 0.9998 (no edge preservation).
assert close(range_weight(50 / 255, 10), 0.99981, 1e-5)
checks += 1
# Check 8: rescaling sigma_r by 1/255 restores the weights exactly; 20 DN at sigma 10 is weight 0.135
# in both unit systems; 20/255 = 0.0784 and 10/255 = 0.0392 (card CV-FILTRES-002).
assert close(range_weight(50 / 255, 10 / 255), range_weight(50, 10), 1e-15)
assert close(range_weight(20, 10), 0.1353, 1e-4) and close(range_weight(20 / 255, 10 / 255), 0.1353, 1e-4)
assert close(20 / 255, 0.0784, 1e-4) and close(10 / 255, 0.0392, 1e-4)
checks += 1
# Check 9: affine change I' = a I + b needs sigma_r' = |a| sigma_r (offset cancels).
a, b = -0.5, 30.0
assert close(range_weight((a * 120 + b) - (a * 90 + b), abs(a) * 10), range_weight(30, 10), 1e-15)
checks += 1

# --- Example C: Gaussian kernel sizes --------------------------------------------
# Check 10: sigma from ksize (imgproc.hpp L1470): 3, 5, 7, 9 -> 0.8, 1.1, 1.4, 1.7.
for k, s in ((3, 0.8), (5, 1.1), (7, 1.4), (9, 1.7)):
    assert close(0.3 * ((k - 1) * 0.5 - 1) + 0.8, s, 1e-12)
checks += 1
# Check 11: ksize from sigma (smooth.dispatch.cpp L289): sigma = 2 -> 13 taps (uint8), 17 (float).
assert (round(2 * 3 * 2 + 1) | 1) == 13 and (round(2 * 4 * 2 + 1) | 1) == 17
checks += 1
# Check 12: separable 13-tap pass costs 26 multiplications per pixel instead of 169.
assert 2 * 13 == 26 and 13 * 13 == 169
checks += 1

# --- Other constructed statements ---------------------------------------------------
# Check 13: noise of a uniform 3x3 average is sigma/3 (5 DN -> 1.67 DN); a one-pixel +30 DN scratch
# becomes +3.3 DN.
assert close(5 * math.sqrt(9 * (1 / 9) ** 2), 1.667) and close(30 / 9, 3.333)
checks += 1
# Check 14: median of eight 10s and one 250 is 10; mean is 36.7 (card CV-FILTRES-001).
vals = [10] * 8 + [250]
assert sorted(vals)[4] == 10 and close(sum(vals) / 9, 36.667)
checks += 1
# Check 15: Gaussian semigroup: from sigma 1 to sigma 2 needs an extra sqrt(3) = 1.73.
assert close(math.sqrt(2 ** 2 - 1 ** 2), 1.732)
checks += 1
# Check 16: Burt-Adelson equal contribution a + 2c = 2b with b = 1/4, c = 1/4 - a/2; OpenCV's
# pyrDown kernel [1, 4, 6, 4, 1]/16 is the member a = 0.375; every kernel sums to 1.
for aa in (0.3, 0.375, 0.4, 0.5):
    bb, cc = 0.25, 0.25 - aa / 2
    assert close(aa + 2 * cc, 2 * bb, 1e-12) and close(aa + 2 * bb + 2 * cc, 1.0, 1e-12)
assert close(6 / 16, 0.375) and close(4 / 16, 0.25) and close(1 / 16, 0.25 - 0.375 / 2)
checks += 1
# Check 17: pyramid total cost is about 4/3 of the base level (geometric series of 1/4).
assert close(sum(0.25 ** k for k in range(30)), 4 / 3, 1e-9)
checks += 1
# Check 18: three halvings: 8 px -> 1 px; a radius-5 window at level 3 covers a radius of 40 px.
assert 8 / 2 ** 3 == 1 and 5 * 2 ** 3 == 40
checks += 1
# Check 19: PSNR contribution of a defect: fraction p = 0.001 with error a = 100 adds p*a^2 = 10 to MSE.
assert close(0.001 * 100 ** 2, 10.0)
checks += 1

print(f"31-filtrage-gradients: {checks} checks passed")
