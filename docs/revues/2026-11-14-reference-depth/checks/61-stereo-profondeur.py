"""Recompute the constructed examples of CV-STEREO (reference 61-stereo-profondeur).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/61-stereo-profondeur.py
Inputs: OpenCV 4.13.0 calib3d.hpp (Q matrix of stereoRectify, DISP_SHIFT = 4, StereoSGBM
parameter advice) and stereosgbm.cpp (invalid value (minDisparity - 1) * 16);
Hirschmueller 2008 (11-bit costs, S <= 16 (Cmax + P2)); Menze and Geiger 2015 (outlier if
error > 3 px and > 5 %). Focal lengths, baselines and disparities are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


f, B = 1000.0, 0.2   # px, m

# --- Example A: Z = f B / d and the Q matrix -----------------------------------
# Check 1: 20 px gives 10 m and 10 px gives 20 m.
assert close(f * B / 20, 10.0) and close(f * B / 10, 20.0)
checks += 1


def q_depth(x, y, d, cx1, cx2, cy=360.0, Tx=-B):
    """Apply OpenCV's horizontal-stereo Q to (x, y, d, 1) and return Z = Zh / W."""
    Q = [[1, 0, 0, -cx1], [0, 1, 0, -cy], [0, 0, 0, f], [0, 0, -1 / Tx, (cx1 - cx2) / Tx]]
    v = [x, y, d, 1.0]
    h = [sum(Q[i][k] * v[k] for k in range(4)) for i in range(4)]
    return h[2] / h[3], h[0] / h[3]


# Check 2: with cx1 = cx2 and Tx = -0.2 m, Q reproduces Z = 10 m for d = 20 px.
Z, X = q_depth(640.0, 360.0, 20.0, 640.0, 640.0)
assert close(Z, 10.0, 1e-9)
checks += 1
# Check 3: if the rectified principal points differ by 4 px (no CALIB_ZERO_DISPARITY),
# the true depth is f B / (d - 4) = 12.5 m, not the naive 10 m.
Z2, _ = q_depth(640.0, 360.0, 20.0, 644.0, 640.0)
assert close(Z2, 12.5, 1e-9) and close(f * B / (20 - 4), 12.5)
checks += 1

# --- Example B: fixed-point disparities ----------------------------------------
DISP_SHIFT = 4
raw = 320
# Check 4: a CV_16S value of 320 is 20 px; read as 320 px it gives a depth 16x too small (0.625 m).
assert raw / (1 << DISP_SHIFT) == 20.0 and close(f * B / raw, 0.625)
checks += 1
# Check 5: the invalid value is (minDisparity - 1) * 16: -16 for minDisparity 0, -272 for -16.
assert (0 - 1) * 16 == -16 and (-16 - 1) * 16 == -272
checks += 1

# --- Example C: depth uncertainty ------------------------------------------------
fB, sd = 200.0, 0.5
# Check 6: sigma_Z = fB sigma_d / d^2 = 0.25 m at d = 20 px and 1 m at d = 10 px (four times).
assert close(fB * sd / 20**2, 0.25) and close(fB * sd / 10**2, 1.0)
checks += 1
# Check 7: d = 2 +- 0.5 px maps to 80 m .. 133.3 m around 100 m (asymmetric).
assert close(fB / 2.5, 80.0) and close(fB / 1.5, 133.333, 1e-3)
checks += 1
# Check 8: the 1/16 px quantum of the fixed-point output at d = 4 px (Z = 50 m) is about 0.78 m of depth.
assert close((fB / 4) ** 2 / fB / 16, 0.78125)
checks += 1

# --- Example D: sizing the disparity range ---------------------------------------
dmax = f * B / 1.5
# Check 9: to see down to 1.5 m with f = 1000 px and B = 0.2 m, disparities reach 133.3 px,
# so numDisparities must be at least 144 (next multiple of 16).
assert close(dmax, 133.333, 1e-3) and int(math.ceil(dmax / 16) * 16) == 144
checks += 1

# --- Example E: SGM storage and cost bounds --------------------------------------
W, H, D = 1280, 720, 128
mb = W * H * D * 2 / 1e6
# Check 10: one 16-bit W x H x D array is 235.9 MB; C and S together 471.9 MB (full 2-D storage).
assert close(mb, 235.9296) and close(2 * mb, 471.8592)
checks += 1
# Check 11: with 11-bit costs (Cmax <= 2047) and P2 <= 2048, 16 paths stay below 2^16.
assert 16 * (2047 + 2048) < 2**16
checks += 1
# Check 12: OpenCV's suggested penalties 8 cn bs^2 and 32 cn bs^2 give 200/800 (gray, 5x5)
# and 216/864 (colour, 3x3).
assert (8 * 1 * 25, 32 * 1 * 25) == (200, 800) and (8 * 3 * 9, 32 * 3 * 9) == (216, 864)
checks += 1

# --- Example F: KITTI 2015 outlier rule --------------------------------------------


def kitti_outlier(err, d_true):
    return err > 3 and err > 0.05 * d_true


# Check 13: a 4 px error is not an outlier at d = 100 px (5 % = 5 px) but is one at d = 40 px.
assert not kitti_outlier(4, 100) and kitti_outlier(4, 40)
checks += 1

# --- Depth versus distance --------------------------------------------------------
# Check 14: a point at X = 5 m, Z = 10 m is at 11.18 m Euclidean distance from the camera centre.
assert close(math.hypot(5, 10), 11.1803, 1e-4)
checks += 1

print(f"61-stereo-profondeur: {checks} checks passed")
