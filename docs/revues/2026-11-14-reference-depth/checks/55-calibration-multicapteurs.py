"""Recompute the constructed examples of CV-MULTICALIB (reference 55-calibration-multicapteurs).

Stdlib only. Run with:
python3 docs/revues/2026-11-14-reference-depth/checks/55-calibration-multicapteurs.py
Inputs: OpenCV 4.13.0 calib3d.hpp (stereoCalibrate convention X2 = R X1 + T,
calibrateHandEye chain), Rehder, Siegwart and Furgale 2016 as reproduced in Rehder's
ETH thesis ch. 3 (mid-exposure offset slope 0.5, 200 Hz IMU, 20 Hz camera, 1-2 min),
Kalibr wiki (camera 20 Hz, IMU 200 Hz). Focal length, speeds and errors are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


F = 1000.0  # focal length in pixels (constructed)

# --- Example A: pixel error caused by a time offset ---------------------------
dt = 0.020        # s
omega = 1.0       # rad/s
# Check 1: rotation at 1 rad/s with a 20 ms offset misplaces every point by f*omega*dt = 20 px,
# independently of depth (small-angle approximation; exact on-axis value f*tan = 20.003 px).
assert close(F * omega * dt, 20.0) and close(F * math.tan(omega * dt), 20.0027, 1e-4)
checks += 1
v = 10.0          # m/s, lateral
# Check 2: translation at 10 m/s gives v*dt = 0.2 m, i.e. 20 px at 10 m depth and 4 px at 50 m.
assert close(v * dt, 0.2) and close(F * v * dt / 10.0, 20.0) and close(F * v * dt / 50.0, 4.0)
checks += 1
# Check 3: at constant speed a delay mimics a translation offset of v*dt: 0.2 m at 10 m/s,
# 0.1 m at 5 m/s, so two speeds separate a delay from a constant extrinsic translation.
assert close(10.0 * dt, 0.2) and close(5.0 * dt, 0.1)
checks += 1

# --- Example B: propagation of extrinsic errors -------------------------------
dtheta = math.radians(0.1)
# Check 4: a 0.1 deg rotation error moves image points by about f*dtheta = 1.745 px at any depth
# and moves a LiDAR point at 50 m by about 8.7 cm.
assert close(F * dtheta, 1.7453, 1e-4) and close(50.0 * math.tan(dtheta), 0.08727, 1e-5)
checks += 1
dtrans = 0.01     # m
# Check 5: a 1 cm lateral translation error gives f*dt/Z = 5 px at 2 m and 0.2 px at 50 m.
assert close(F * dtrans / 2.0, 5.0) and close(F * dtrans / 50.0, 0.2)
checks += 1
# Check 6: rotation and translation errors give equal pixel errors at Z = dtrans/dtheta ~ 5.7 m.
assert close(dtrans / dtheta, 5.7296, 1e-4)
checks += 1

# --- Example C: timestamping at exposure start --------------------------------
# Check 7: an 8 ms exposure timestamped at its start adds 4 ms to the offset (slope 0.5);
# Rehder reports a fitted slope of 0.498.
assert close(0.5 * 8.0, 4.0) and abs(0.498 - 0.5) < 0.005
checks += 1
# Check 8: +-0.2 ms is 4 % of the 5 ms IMU period at 200 Hz.
assert close(0.2 / (1000.0 / 200.0), 0.04)
checks += 1
# Check 9: 120 s of data gives 24,000 IMU samples at 200 Hz and 2,400 images at 20 Hz.
assert 120 * 200 == 24_000 and 120 * 20 == 2_400
checks += 1

# --- Example D: hand-eye translation unobservable along the rotation axis ------


def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return [[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]


RA = rot_z(math.radians(30))
M = [[RA[i][j] - (1.0 if i == j else 0.0) for j in range(3)] for i in range(3)]
n = [0.0, 0.0, 1.0]
Mn = [sum(M[i][k] * n[k] for k in range(3)) for i in range(3)]
det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
       - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
       + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
minor = M[0][0] * M[1][1] - M[0][1] * M[1][0]
# Check 10: (R_A - I) n = 0 for the rotation axis n, det = 0 and a nonzero 2x2 minor: rank 2,
# so (R_A - I) t_X = R_X t_B - t_A leaves t_X free along n.
assert all(abs(x) < 1e-12 for x in Mn) and abs(det) < 1e-12 and abs(minor) > 0.1
checks += 1

# --- OpenCV stereoCalibrate convention ----------------------------------------
R = rot_z(math.radians(2.0))
T = [-0.12, 0.0, 0.003]  # m, constructed
X1 = [0.4, -0.2, 3.0]
X2 = [sum(R[i][k] * X1[k] for k in range(3)) + T[i] for i in range(3)]
back = [sum(R[k][i] * (X2[k] - T[k]) for k in range(3)) for i in range(3)]
# Check 11: X2 = R X1 + T maps camera-1 coordinates to camera 2; X1 = R^T (X2 - T) inverts it,
# and the camera-2 centre expressed in camera 1 is -R^T T, not T.
assert all(close(a, b, 1e-12) for a, b in zip(back, X1))
c2_in_1 = [-sum(R[k][i] * T[k] for k in range(3)) for i in range(3)]
assert close(c2_in_1[0], 0.12 * math.cos(math.radians(2.0)), 1e-12)
checks += 1

print(f"55-calibration-multicapteurs: {checks} checks passed")
