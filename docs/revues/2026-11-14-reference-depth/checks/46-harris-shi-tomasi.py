"""Recompute the constructed examples of CV-CORNERS (reference 46-harris-shi-tomasi).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/46-harris-shi-tomasi.py
Formulas: Harris and Stephens 1988 (R = Det - k Tr^2, contrast factor p^2 on the
eigenvalues), Shi and Tomasi TR 93-1399 (eq. 4.1, min eigenvalue). OpenCV scaling:
opencv 4.13.0 modules/imgproc/src/corner.cpp L247-L252 (derivative scale
1 / (2^(ksize-1) * blockSize), times 1/255 for 8-bit input) and L313-L314
(unnormalized box filter). The images and scenarios are constructed.
"""

import math


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


def eig2(a, b, c):
    """Eigenvalues (largest, smallest) of the symmetric matrix [[a, c], [c, b]]."""
    mean = (a + b) / 2
    rad = math.sqrt(((a - b) / 2) ** 2 + c * c)
    return mean + rad, mean - rad


def harris(a, b, c, k=0.04):
    return a * b - c * c - k * (a + b) ** 2


# --- Card CV-CORNERS-001 numbers ------------------------------------------------
# Check 1: diag(100, 1) gives R_H = 100 - 0.04 * 101^2 = -308.04 and R_S = 1.
assert close(harris(100, 1, 0), -308.04) and close(eig2(100, 1, 0)[1], 1)
# Check 2: diag(20, 20) gives R_H = 400 - 0.04 * 40^2 = 336 and R_S = 20.
assert close(harris(20, 20, 0), 336) and close(eig2(20, 20, 0)[1], 20)

# --- Example A: the Harris sign depends only on the eigenvalue ratio -----------
def ratio_threshold(k):
    """Smallest r = l2/l1 in (0, 1] with r - k (1 + r)^2 = 0 (R_H changes sign)."""
    # k r^2 + (2k - 1) r + k = 0, smaller root
    disc = (2 * k - 1) ** 2 - 4 * k * k
    return ((1 - 2 * k) - math.sqrt(disc)) / (2 * k)


r04, r06 = ratio_threshold(0.04), ratio_threshold(0.06)
# Check 3: with k = 0.04 the response is positive only if l2/l1 > 0.0436.
assert close(r04, 0.04356, 1e-5)
# Check 4: with k = 0.06 (Schmid et al. 2000, Sec. 2.2) the boundary moves to 0.0685.
assert close(r06, 0.06850, 1e-5)
# Check 5: at the boundary R_H = 0, and the sign is unchanged when both eigenvalues
# are scaled (contrast), because R_H is homogeneous of degree 2 in (l1, l2).
for scale in (1e-3, 1.0, 1e4):
    assert abs(harris(scale, scale * r04, 0)) <= 1e-9 * scale * scale
    assert harris(scale, scale * 0.05, 0) > 0 > harris(scale, scale * 0.03, 0)
# Check 6: an isotropic corner l1 = l2 = l gives (1 - 4k) l^2, positive only if k < 1/4.
assert close(harris(10, 10, 0, k=0.04), (1 - 4 * 0.04) * 100)
assert harris(10, 10, 0, k=0.25) == 0 and harris(10, 10, 0, k=0.3) < 0

# --- Example B: worst-direction precision of a translation estimate ----------
# Linearized least squares with i.i.d. intensity noise sigma: cov(d) = sigma^2 M^-1,
# so the worst-direction standard deviation is sigma / sqrt(l_min).
sigma = 1.0
# Check 7: diag(100, 1): 0.1 px along the strong direction, 1.0 px along the weak one.
assert close(sigma / math.sqrt(100), 0.1) and close(sigma / math.sqrt(1), 1.0)
# Check 8: diag(20, 20): 0.2236 px in every direction, better than 1.0 px in the worst case.
assert close(sigma / math.sqrt(20), 0.22361, 1e-5)

# --- Example C: OpenCV-normalized tensor on ideal 8-bit patterns ----------------
def sobel_x(img, x, y):
    return sum(w * (img(x + 1, y + dy) - img(x - 1, y + dy)) for dy, w in ((-1, 1), (0, 2), (1, 1)))


def sobel_y(img, x, y):
    return sum(w * (img(x + dx, y + 1) - img(x + dx, y - 1)) for dx, w in ((-1, 1), (0, 2), (1, 1)))


def opencv_tensor(img, x0, y0, block=3, ksize=3, depth8=True):
    """Tensor entries (A, B, C) as cornerEigenValsVecs builds them, away from borders."""
    scale = float((1 << (ksize - 1)) * block)
    if depth8:
        scale *= 255.0
    scale = 1.0 / scale
    a = b = c = 0.0
    r = block // 2
    for y in range(y0 - r, y0 + r + 1):
        for x in range(x0 - r, x0 + r + 1):
            gx, gy = sobel_x(img, x, y) * scale, sobel_y(img, x, y) * scale
            a, b, c = a + gx * gx, b + gy * gy, c + gx * gy
    return a, b, c


def step(h):
    return lambda x, y: h if x >= 0 else 0


def l_corner(h):
    return lambda x, y: h if (x >= 0 and y >= 0) else 0


a, b, c = opencv_tensor(step(255), 0, 0)
# Check 9: a 255-level vertical step gives A = 2/3, B = C = 0: l_max = 2/3, l_min = 0,
# Harris = -0.04 * (2/3)^2 = -0.0178 (8-bit input, ksize = 3, blockSize = 3).
assert close(a, 2 / 3) and b == 0 and c == 0 and close(harris(a, b, c), -0.017778, 1e-6)

a, b, c = opencv_tensor(l_corner(255), 0, 0)
l1, l2 = eig2(a, b, c)
# Check 10: an ideal 255-level right-angle corner gives, at pixel (0, 0),
# A = B = 13/36, C = 1/9, hence l_max = 17/36, l_min = 1/4 and Harris = 0.0972.
assert close(a, 13 / 36) and close(b, 13 / 36) and close(c, 1 / 9)
assert close(l1, 17 / 36) and close(l2, 0.25) and close(harris(a, b, c), 0.097191, 1e-6)
# Check 11: pixel (0, 0) holds the largest l_min of its 5x5 neighborhood, so the
# integer detection lies 0.71 px from the geometric corner at (-0.5, -0.5).
scores = {(x, y): eig2(*opencv_tensor(l_corner(255), x, y))[1]
          for x in range(-2, 3) for y in range(-2, 3)}
assert max(scores, key=scores.get) == (0, 0)
assert close(math.hypot(0.5, 0.5), 0.70711, 1e-5)
# Check 12: the same corner passed as float32 in [0, 255] (no 1/255 factor) gives
# 255^2 = 65025 times the minimum eigenvalue and 255^4 times the Harris response.
af, bf, cf = opencv_tensor(l_corner(255), 0, 0, depth8=False)
assert close(eig2(af, bf, cf)[1] / l2, 255 ** 2, 1e-3)
assert close(harris(af, bf, cf) / harris(a, b, c), 255 ** 4, 1.0)

# --- Example D: one relative threshold, two scores, mixed contrast -----------
q = 0.01
contrast_ratio = 40 / 255  # scene corners at 40 levels, target corners at 255 levels
# Check 13: min-eigenvalue score ratio (40/255)^2 = 0.0246 > 0.01: scene corners kept.
assert close(contrast_ratio ** 2, 0.024606, 1e-6) and contrast_ratio ** 2 > q
# Check 14: Harris ratio (40/255)^4 = 0.000605 < 0.01: the same corners are rejected.
assert close(contrast_ratio ** 4, 0.00060545, 1e-8) and contrast_ratio ** 4 < q
# Check 15: smallest contrast kept against a 255-level corner: 25.5 levels for the
# minimum eigenvalue (q^(1/2)) and 80.6 levels for Harris (q^(1/4)).
assert close(255 * q ** 0.5, 25.5) and close(255 * q ** 0.25, 80.64, 1e-2)
# Check 16: on simulated patterns, the scaled corners confirm the power laws.
low = opencv_tensor(l_corner(40), 0, 0)
assert close(eig2(*low)[1] / l2, contrast_ratio ** 2, 1e-9)
assert close(harris(*low) / harris(a, b, c), contrast_ratio ** 4, 1e-9)

# --- Sizing rule: spacing that makes a point budget unreachable ---------------
# With minimum spacing d, a hexagonal packing gives each point an area sqrt(3)/2 d^2,
# so at most about 2 H W / (sqrt(3) d^2) points fit in an H x W image.
H, W, N = 480, 640, 500
d_max = math.sqrt(2 * H * W / (math.sqrt(3) * N))
# Check 17: a budget of 500 points in 640x480 is unreachable once minDistance exceeds ~26.6 px.
assert close(d_max, 26.63, 1e-2)
# Check 18: minDistance = 10 px leaves room for about 3,547 points, far above the budget.
assert close(2 * H * W / (math.sqrt(3) * 10 ** 2), 3547.2, 0.1)

print("46-harris-shi-tomasi: 18 checks passed")
