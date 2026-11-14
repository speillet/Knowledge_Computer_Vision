"""Recompute the constructed examples of CV-FISHEYE (reference 56-calibration-fisheye).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/56-calibration-fisheye.py
Inputs: OpenCV 4.13.0 fisheye model (calib3d.hpp L509-L536: theta = atan(r),
theta_d = theta (1 + k1 theta^2 + ... + k4 theta^8)); fisheye.cpp
estimateNewCameraMatrixForUndistortRectify (L655-L724: f = balance fmin + (1 - balance) fmax
from the four undistorted edge midpoints) and undistortPoints (Newton iteration, theta_d
clipped to pi/2). Focal lengths, image sizes and coefficients are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def theta_d(theta, k):
    return theta * (1 + k[0] * theta**2 + k[1] * theta**4 + k[2] * theta**6 + k[3] * theta**8)


# --- Example A: zero coefficients are still an angular (equidistant) model -----
th = math.radians(60)
# Check 1: at 60 deg and f = 300 px the fisheye radius is 314.16 px, the pinhole radius 519.62 px.
assert close(300 * th, 314.159, 1e-3) and close(300 * math.tan(th), 519.615, 1e-3)
checks += 1
# Check 2: near the axis the relative gap (tan(theta) - theta) / theta is about theta^2 / 3.
small = 0.1
assert close((math.tan(small) - small) / small, small**2 / 3, 2e-5)
checks += 1

# Check 3: projection families of Kannala and Brandt eqs. 1-5 at f = 300 px (radius in px):
# 60 deg -> perspective 519.6, stereographic 346.4, equidistance 314.2, equisolid 300.0, orthogonal 259.8;
# 90 deg -> perspective infinite, stereographic 600.0, equidistance 471.2, equisolid 424.3, orthogonal 300.0.
fam = {
    "stereographic": lambda x: 2 * 300 * math.tan(x / 2),
    "equidistance": lambda x: 300 * x,
    "equisolid": lambda x: 2 * 300 * math.sin(x / 2),
    "orthogonal": lambda x: 300 * math.sin(x),
}
r60 = {k: f(math.radians(60)) for k, f in fam.items()}
r90 = {k: f(math.radians(90)) for k, f in fam.items()}
assert close(r60["stereographic"], 346.41, 0.01) and close(r60["equidistance"], 314.16, 0.01)
assert close(r60["equisolid"], 300.0, 1e-9) and close(r60["orthogonal"], 259.81, 0.01)
assert close(r90["stereographic"], 600.0, 1e-9) and close(r90["equidistance"], 471.24, 0.01)
assert close(r90["equisolid"], 424.26, 0.01) and close(r90["orthogonal"], 300.0, 1e-9)
assert math.cos(math.radians(90)) < 1e-15  # tan(90 deg) is unbounded: the pinhole radius diverges
checks += 1

# --- Example B: sensitivity of high-order coefficients ------------------------
F = 500.0
# Check 4: changing k4 by 0.01 moves a point by f * 0.01 * theta^9:
# 2.6e-6 px at 0.2 rad, 0.05 px at 0.6 rad and 25.8 px at 1.2 rad.
shift = [F * 0.01 * t**9 for t in (0.2, 0.6, 1.2)]
assert close(shift[0], 2.56e-6, 1e-9) and close(shift[1], 0.0504, 1e-4) and close(shift[2], 25.80, 0.01)
checks += 1

# --- Example C: what OpenCV's balance does for a constructed equidistant lens --
W, H = 1280, 960
th_x, th_y = (W / 2) / F, (H / 2) / F           # angles of the right and bottom edge midpoints (k = 0)
f1 = (W / 2) / math.tan(th_x)                   # fisheye.cpp: f1 = w/2 / (cn_x - minx), cn = 0
f3 = (H / 2) / math.tan(th_y)
fmin, fmax = min(f1, f3), max(f1, f3)
# Check 5: edge midpoints at 1.28 rad (73.3 deg) and 0.96 rad (55 deg) give fmin = 191.5 px, fmax = 336.1 px.
assert close(math.degrees(th_x), 73.34, 0.01) and close(fmin, 191.54, 0.01) and close(fmax, 336.05, 0.01)
checks += 1
# Check 6: balance = 0.5 interpolates linearly: f = 263.8 px.
assert close(0.5 * fmin + 0.5 * fmax, 263.79, 0.01)
checks += 1
# Check 7: at the image centre the raw image samples 1/500 rad per px; the rectified output samples
# 1/fmin = 5.22 mrad/px (balance 1, 2.61x coarser) or 1/fmax = 2.98 mrad/px (balance 0, 1.49x coarser).
assert close(1000 / fmin, 5.221, 1e-3) and close(F / fmin, 2.610, 1e-3) and close(F / fmax, 1.488, 1e-3)
checks += 1
# Check 8: at the horizontal edge (balance 1) the pinhole output stretches radially by
# fmin / cos^2(theta) = 2,330 px/rad against 500 px/rad in the raw image: 4.7 output px per raw px.
stretch = fmin / math.cos(th_x) ** 2
assert close(stretch, 2330.0, 0.5) and close(stretch / F, 4.66, 0.01)
checks += 1
# Check 9: the image corner (half-diagonal 800 px) sees 1.6 rad = 91.7 deg, beyond 90 deg:
# no pinhole rectification represents it, and undistortPoints clips theta_d to pi/2.
half_diag = math.hypot(W / 2, H / 2)
assert close(half_diag, 800.0) and half_diag / F > math.pi / 2 and close(math.degrees(half_diag / F), 91.67, 0.01)
checks += 1

# --- Example D: monotonicity of the fitted polynomial --------------------------
k_bad = (-0.1, 0.0, 0.0, 0.0)
th_peak = math.sqrt(1 / 0.3)
# Check 10: with k1 = -0.1 alone, d theta_d / d theta = 1 - 0.3 theta^2 vanishes at 1.826 rad (104.6 deg);
# beyond it two angles share one radius and inversion is ambiguous.
assert close(th_peak, 1.8257, 1e-4) and close(math.degrees(th_peak), 104.6, 0.05)
assert theta_d(th_peak - 0.2, k_bad) < theta_d(th_peak, k_bad) > theta_d(th_peak + 0.2, k_bad)
checks += 1

# --- Example E: Newton inversion as in fisheye::undistortPoints ---------------
k = (0.02, -0.005, 0.001, -0.0001)
target = theta_d(1.0, k)
t = target
for it in range(10):  # OpenCV default criteria: 10 iterations, eps 1e-8
    fix = (theta_d(t, k) - target) / (1 + 3 * k[0] * t**2 + 5 * k[1] * t**4 + 7 * k[2] * t**6 + 9 * k[3] * t**8)
    t -= fix
    if abs(fix) < 1e-8:
        break
# Check 11: starting from theta = theta_d, Newton recovers theta = 1 rad within 1e-10 in under 10 iterations.
assert abs(t - 1.0) < 1e-10 and it < 9
checks += 1

# --- Cost: memory of float rectification maps -------------------------------
# Check 12: two CV_32FC1 maps for a 1280 x 960 output take 1280*960*8 bytes = 9.83 MB.
assert close(1280 * 960 * 8 / 1e6, 9.8304)
checks += 1

# --- Example F: an average weights regions by observation count ---------------
rms = math.sqrt((90 * 0.2**2 + 10 * 2.0**2) / 100)
# Check 13: 90 points at 0.2 px and 10 at 2 px give an RMS of 0.66 px.
assert close(rms, 0.6603, 1e-4)
checks += 1

print(f"56-calibration-fisheye: {checks} checks passed")
