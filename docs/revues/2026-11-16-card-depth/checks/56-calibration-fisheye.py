"""Recompute the constructed numbers added to CV-FISHEYE-004 and to reference
56-calibration-fisheye (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/56-calibration-fisheye.py
Fisheye model theta_d = theta (1 + k1 theta^2 + ...), x' = theta_d / r * a: OpenCV 4.13.0
calib3d.hpp L509-L536. Rectification map through (P R)^-1 and undistortPoints through P R:
fisheye.cpp L395-L409, L579-L615. New focal length from the edge midpoints: fisheye.cpp
L655-L724 (reference worked example C: f = 500 px, zero coefficients, 1280 x 960).
"""
import math

checks = 0
f, cx, cy, w, h = 500.0, 640.0, 480.0, 1280, 960

# Worked example C of the reference: f_min and f_max from the edge midpoints, balance = 0.
f_min = (w / 2) / math.tan((w / 2) / f)
f_max = (h / 2) / math.tan((h / 2) / f)
assert round(f_min, 1) == 191.5 and round(f_max, 1) == 336.1
balance = 0.0
f_new = balance * f_min + (1 - balance) * f_max
checks += 1

# One ray 0.6 rad off-axis, horizontal, in the raw camera frame (R = identity).
theta = 0.6
u_raw = cx + f * theta                         # equidistant raw image, zero coefficients
u_rect = cx + f_new * math.tan(theta)          # pinhole output with K_new
assert round(u_raw, 1) == 940.0 and round(u_rect, 1) == 869.9
assert round(math.degrees(theta), 1) == 34.4
checks += 1

# Three readings of the rectified pixel.
x = u_rect - cx
right = math.degrees(math.atan(x / f_new))     # K_new as a pinhole: correct
raw_fisheye = math.degrees(x / f)              # raw K and the fisheye model
twice = math.degrees(x / f_new)                # K_new but the fisheye model applied again
assert abs(right - 34.38) < 0.01
assert round(raw_fisheye, 1) == 26.3 and round(raw_fisheye - right, 1) == -8.0
assert round(twice, 1) == 39.2 and round(twice - right, 1) == 4.8
checks += 1

# undistortPoints(raw, K, D, R, P) lands where the map samples: P R applied to the
# undistorted normalized point equals the output pixel whose inverse map hits the raw point.
def rot_y(deg):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
def mv(M, v):
    return [sum(M[i][k] * v[k] for k in range(3)) for i in range(3)]
def T(M):
    return [[M[j][i] for j in range(3)] for i in range(3)]
R = rot_y(4.0)                                 # a stereo-like rectification rotation
P = [[f_new, 0, cx], [0, f_new, cy], [0, 0, 1]]
ray_raw = [math.tan(0.5), 0.1, 1.0]            # normalized pinhole coordinates of a raw ray
# undistortPoints path: P R (a, b, 1)
pr = mv(P, mv(R, ray_raw)); u_out = (pr[0] / pr[2], pr[1] / pr[2])
# map path: from the output pixel, the raw ray is R^T K_new^-1 u'
q = [(u_out[0] - cx) / f_new, (u_out[1] - cy) / f_new, 1.0]
back = mv(T(R), q)
assert all(abs(back[i] / back[2] - ray_raw[i]) < 1e-12 for i in range(3))
checks += 1

# Pose frame: a point X_rect = R X_raw; a pose estimated in the rectified frame maps back by R^T.
X_raw = [0.2, -0.1, 1.5]
X_rect = mv(R, X_raw)
assert all(abs(a - b) < 1e-12 for a, b in zip(mv(T(R), X_rect), X_raw))
# Ignoring a 4 degree rectification rotation moves a point 1.5 m straight ahead by
# 2 x 1.5 x sin(2 deg) = 0.105 m.
X_ahead = [0.0, 0.0, 1.5]
d = math.dist(mv(R, X_ahead), X_ahead)
assert abs(d - 2 * 1.5 * math.sin(math.radians(2))) < 1e-12 and round(d, 3) == 0.105
checks += 1

# Reference label fixed in this pass: with k1 = -0.1 alone, d theta_d / d theta = 1 - 0.3 theta^2
# vanishes at sqrt(1 / 0.3) = 1.83 rad (example D of the 2026-11-14 check script).
assert round(math.sqrt(1 / 0.3), 2) == 1.83
checks += 1

print(f"56-calibration-fisheye (CV-FISHEYE-004): {checks} checks passed")
