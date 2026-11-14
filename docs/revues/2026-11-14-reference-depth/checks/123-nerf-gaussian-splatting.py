"""Recompute the constructed examples of CV-RENDU3D (reference 123-nerf-gaussian-splatting).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/123-nerf-gaussian-splatting.py
Formulas: NeRF quadrature (Mildenhall et al. 2020, eq. 3); 3DGS covariance Sigma = R S S^T R^T
(Kerbl et al. 2023, eq. 6) with position, scale, quaternion, opacity and 4 SH bands per colour (Sec. 4-5).
Rays, densities and scene sizes are constructed.
"""

import math


def render_weights(sigmas, deltas):
    """NeRF eq. 3: w_i = T_i (1 - exp(-sigma_i delta_i)), T_i = exp(-sum_{j<i} sigma_j delta_j)."""
    weights, optical = [], 0.0
    for s, d in zip(sigmas, deltas):
        weights.append(math.exp(-optical) * (1 - math.exp(-s * d)))
        optical += s * d
    return weights


# --- Example A: two layers on one ray and the "expected depth" ---------------------------
t = [2.0, 4.0]                    # sample depths in scene units
deltas = [0.1, 0.1]
sigmas = [7.0, 50.0]              # optical thicknesses 0.7 (semi-transparent) and 5 (opaque)
w = render_weights(sigmas, deltas)
depth = sum(wi * ti for wi, ti in zip(w, t)) / sum(w)
# Check 1: weights 0.503 and 0.493 sum to 0.996; the weighted depth is about 2.99, between the
# two layers, where no density exists: an expected depth is not a surface.
assert abs(w[0] - 0.5034) < 1e-4 and abs(w[1] - 0.4933) < 1e-4 and abs(sum(w) - 0.9967) < 1e-4
assert abs(depth - 2.99) < 0.01

# --- Example B: scale gauge -------------------------------------------------------------
a = 2.5                                        # scale scene and cameras by a
w_scaled = render_weights([s / a for s in sigmas], [d * a for d in deltas])
# Check 2: scaling distances by a and densities by 1/a leaves every weight, hence every pixel, unchanged.
assert all(abs(p - q) < 1e-12 for p, q in zip(w, w_scaled))
# Check 3: the expected depth scales by a; the images cannot tell 2.99 units from 7.48 units.
depth_scaled = sum(wi * ti * a for wi, ti in zip(w_scaled, t)) / sum(w_scaled)
assert abs(depth_scaled - a * depth) < 1e-12

# --- Example C: 3D Gaussian covariance ----------------------------------------------------
s = (3.0, 1.0, 0.1)                            # scales of a flat, elongated Gaussian
theta = math.radians(30)                       # rotation about the z axis
R = [[math.cos(theta), -math.sin(theta), 0.0], [math.sin(theta), math.cos(theta), 0.0], [0.0, 0.0, 1.0]]
S = [[s[0], 0, 0], [0, s[1], 0], [0, 0, s[2]]]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def transpose(A):
    return [list(r) for r in zip(*A)]


RS = matmul(R, S)
Sigma = matmul(RS, transpose(RS))
trace = sum(Sigma[i][i] for i in range(3))
# Check 4: Sigma = R S S^T R^T has trace s1^2 + s2^2 + s3^2 = 10.01 and is symmetric.
assert abs(trace - 10.01) < 1e-9 and all(abs(Sigma[i][j] - Sigma[j][i]) < 1e-12 for i in range(3) for j in range(3))
# Check 5: the variance along the rotated first axis is s1^2 = 9 (Rayleigh quotient with the axis).
u = [R[0][0], R[1][0], R[2][0]]
var_u = sum(u[i] * Sigma[i][j] * u[j] for i in range(3) for j in range(3))
assert abs(var_u - 9.0) < 1e-9

# --- Example D: memory of a Gaussian scene --------------------------------------------------
floats = 3 + 3 + 4 + 1 + 3 * 16               # position, scale, quaternion, opacity, 4 SH bands x RGB
# Check 6: 59 float32 values = 236 bytes per Gaussian; one million Gaussians need about 236 MB.
assert floats == 59 and floats * 4 == 236 and floats * 4 * 1_000_000 / 1e6 == 236

print("123-nerf-gaussian-splatting: 6 checks passed (render weights, expected depth, scale gauge, covariance, memory)")
