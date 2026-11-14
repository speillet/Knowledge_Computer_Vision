"""Recompute the constructed examples of CV-SIFT (reference 41-sift).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/41-sift.py
Inputs: Lowe 2004 (IJCV) Sec. 3 (k = 2^(1/s), s + 3 images, sigma = 1.6, input blur 0.5,
image doubling), Sec. 4 (|D| < 0.03, r = 10), Sec. 6.1 (4x4x8, 0.2), Sec. 7.1 (ratio 0.8);
Rey-Otero and Delbracio 2014 (IPOL) Sec. 3.3 (C_DoG scaling with n_spo);
opencv 4.13.0 sift.dispatch.cpp L176-L262 and L503-L580, sift.simd.hpp L292-L395 and
L710-L1001, resize.cpp L4101 (INTER_LINEAR mapping). Scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: scale-space sampling -------------------------------------------
s, sigma0 = 3, 1.6
k = 2 ** (1 / s)
# Check 1: three intervals per octave give k = 2^(1/3) = 1.2599, and s + 3 = 6 Gaussian
# images and s + 2 = 5 DoG images per octave.
assert close(k, 1.259921, 1e-6) and s + 3 == 6 and s + 2 == 5
total = [sigma0 * k ** i for i in range(s + 3)]
incr = [sigma0] + [math.sqrt((sigma0 * k ** i) ** 2 - (sigma0 * k ** (i - 1)) ** 2) for i in range(1, s + 3)]
# Check 2: total blur per layer 1.6, 2.02, 2.54, 3.2, 4.03, 5.08; layer 3 doubles sigma.
assert [round(v, 2) for v in total] == [1.6, 2.02, 2.54, 3.2, 4.03, 5.08] and close(total[3], 2 * sigma0)
# Check 3: incremental blurs applied by OpenCV's loop: 1.226, 1.545, 1.947, 2.453, 3.090.
assert [round(v, 3) for v in incr[1:]] == [1.226, 1.545, 1.947, 2.453, 3.09]
# Check 4: with an assumed input blur of 0.5 doubled to 1.0, the first blur is
# sqrt(1.6^2 - 1^2) = 1.249; without doubling it is sqrt(1.6^2 - 0.5^2) = 1.520.
assert close(math.sqrt(1.6 ** 2 - 1.0 ** 2), 1.249, 1e-3) and close(math.sqrt(1.6 ** 2 - 0.25), 1.520, 1e-3)
# Check 5: a 640x480 image is doubled to 1280x960 and gets round(log2(960) - 2) + 1 = 9 octaves.
assert round(math.log2(960) - 2) + 1 == 9

# --- Example B: edge rejection ---------------------------------------------------
r = 10
bound = (r + 1) ** 2 / r


def edgeness(alpha, beta):
    return (alpha + beta) ** 2 / (alpha * beta)


# Check 6: the bound (r + 1)^2 / r is 12.1 for r = 10.
assert close(bound, 12.1)
# Check 7: curvature ratio 12 gives 14.08 (rejected); ratio 8 gives 10.125 (kept);
# ratio exactly 10 sits on the bound, which OpenCV rejects (>=).
assert edgeness(12, 1) > bound and close(edgeness(12, 1), 14.083, 1e-3)
assert edgeness(8, 1) < bound and close(edgeness(8, 1), 10.125)
assert close(edgeness(10, 1), bound)
# Check 8: the test depends only on the ratio, not on contrast.
assert close(edgeness(120, 10), edgeness(12, 1))

# --- Example C: one contrast threshold, three conventions ----------------------
lowe = 0.03
opencv_default = 0.04 / s
# Check 9: OpenCV's default 0.04 divided by nOctaveLayers = 3 keeps |D| >= 0.0133,
# 2.25 times more permissive than Lowe's 0.03; 0.09 reproduces Lowe (header note).
assert close(opencv_default, 0.013333, 1e-6) and close(lowe / opencv_default, 2.25) and close(0.09 / s, lowe)


def ipol_scale(n):
    return (2 ** (1 / n) - 1) / (2 ** (1 / 3) - 1)


# Check 10: IPOL scales its threshold by (2^(1/n) - 1)/(2^(1/3) - 1); OpenCV's 3/n is close
# because 2^(1/n) - 1 ~ ln 2 / n: 0.728 vs 0.75 for n = 4, 0.471 vs 0.5 for n = 6.
assert close(ipol_scale(4), 0.728, 1e-3) and close(ipol_scale(6), 0.471, 1e-3)
assert close(ipol_scale(3), 1.0) and abs(ipol_scale(4) - 3 / 4) < 0.03 and abs(ipol_scale(6) - 3 / 6) < 0.03

# --- Example D: ratio test and OpenCV descriptor scale ----------------------------
# Check 11: card CV-SIFT-004: 20/21 = 0.952 rejected, 35/80 = 0.4375 kept at 0.8.
assert close(20 / 21, 0.95238, 1e-5) and 20 / 21 >= 0.8 and 35 / 80 == 0.4375
# Check 12: comparing squared distances with 0.8 accepts distance ratios up to 0.894;
# the equivalent squared threshold for tau = 0.8 is 0.64.
assert close(math.sqrt(0.8), 0.8944, 1e-4) and close(0.8 ** 2, 0.64)
# Check 13: OpenCV stores 512 x the unit descriptor: two non-negative unit vectors are at most
# sqrt(2) apart, i.e. 724 in OpenCV units; a unit-space distance of 0.4 reads as ~205.
assert close(512 * math.sqrt(2), 724.08, 1e-2) and close(512 * 0.4, 204.8)

# --- Example E: location bias of the default (non-precise) upscale ---------------
def linear_src(u, scale=0.5):
    """Source coordinate sampled by INTER_LINEAR for destination index u (resize.cpp L4101)."""
    return (u + 0.5) * scale - 0.5


p = 37.0                         # feature centre in input pixels
u_peak = 2 * p + 0.5             # destination index whose source coordinate is p
# Check 14: destination index 2p + 0.5 samples source p, so the peak is detected there ...
assert close(linear_src(u_peak), p)
# Check 15: ... and multiplying by 0.5 reports p + 0.25: a +0.25 px bias on x and on y
# (0.354 px diagonally); the precise path samples src = u / 2 and reports p exactly.
assert close(0.5 * u_peak - p, 0.25) and close(math.hypot(0.25, 0.25), 0.3536, 1e-4)
assert close(0.5 * (2 * p) - p, 0.0)

# --- Example F: local anisotropy of a tilted plane -------------------------------
# Check 16: under a tilt theta (orthographic approximation) one axis shrinks by cos(theta):
# anisotropy 1.56 at 50 deg, 2.00 at 60 deg, 2.92 at 70 deg.
for deg, ratio in ((50, 1.556), (60, 2.0), (70, 2.924)):
    assert close(1 / math.cos(math.radians(deg)), ratio, 1e-3)

# --- Example G: descriptor support and costs --------------------------------------
d_hist, n_ori, scl_fctr = 4, 8, 3.0
# Check 17: 4 x 4 x 8 = 128; each cell is 3 sigma wide, the grid 12 sigma wide, the
# Gaussian weight sigma is 2 cells = 6 sigma (half the width, as in Lowe Sec. 6.1).
assert d_hist * d_hist * n_ori == 128 and d_hist * scl_fctr == 12 and (d_hist / 2) * scl_fctr == 6
# Check 18: OpenCV's sampling radius round(3 sigma * sqrt(2) * (4 + 1) / 2) is 21 px for sigma = 2.
assert round(3 * 2 * math.sqrt(2) * (d_hist + 1) * 0.5) == 21
# Check 19: the Gaussian pyramid of a 640x480 image (doubled, 6 images per octave, 9 octaves)
# holds about 32 HW samples, i.e. ~9.8 million.
W2, H2 = 1280, 960
samples = sum(6 * (W2 >> o) * (H2 >> o) for o in range(9))
assert close(samples / (640 * 480), 32.0, 0.1) and 9.8e6 < samples < 9.9e6
# Check 20: exhaustive matching of 2,000 x 2,000 descriptors of dimension 128 costs
# 512 million multiply-adds.
assert 2000 * 2000 * 128 == 512_000_000

print("41-sift: 20 checks passed")
