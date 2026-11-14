"""Recompute the constructed examples of CV-BEV (reference 64-nuages-bev-occupation).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/64-nuages-bev-occupation.py
Inputs: PointPillars (arXiv 1812.05784, Sec. 2.1 and 3.1/3.2 settings), Lift-Splat-Shoot
(arXiv 2008.05711, Sec. 4.1 settings), BEVFormer (arXiv 2203.17270v2, eq. 3 and Sec. 4.2
settings), OctoMap (Hornung et al. 2013, eqs. 2-4 and Sec. 5.1; octomap v1.10.0 defaults).
Motion values and the LiDAR angular resolution are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: grid sizes and sparsity ------------------------------------------
# PointPillars car setting: x in (0, 70.4), y in (-40, 40), z in (-3, 1) m, xy resolution 0.16 m.
nx, ny = round(70.4 / 0.16), round(80.0 / 0.16)
cells = nx * ny
# Check 1: the car canvas is 440 x 500 = 220,000 pillars.
assert (nx, ny, cells) == (440, 500, 220_000)
# Check 2: 6k-9k non-empty pillars (paper, HDL-64E) means 95.9%-97.3% empty pillars.
sparsity_lo, sparsity_hi = 1 - 9000 / cells, 1 - 6000 / cells
assert close(sparsity_lo, 0.9591, 1e-4) and close(sparsity_hi, 0.9727, 1e-4)
# Check 3: the dense tensor holds at most P x N = 12,000 x 100 points (D = 9 features each).
assert 12_000 * 100 * 9 == 10_800_000
# Check 4: a voxel grid with 0.1 m height cells over the same 4 m of z would have 40x more cells.
nz = round(4.0 / 0.1)
assert nz == 40 and cells * nz == 8_800_000
# Check 5: halving the cell size multiplies BEV cells by 4 and voxel cells by 8.
assert round(70.4 / 0.08) * round(80 / 0.08) == 4 * cells
assert round(70.4 / 0.08) * round(80 / 0.08) * round(4.0 / 0.05) == 8 * cells * nz

# --- Example B: index-to-metre conventions of camera BEV grids -------------------
H = W = 200
s_bevformer = 0.512
# BEVFormer eq. 3: x' = (x - W/2) * s, with the ego car at the origin.
x_first, x_last = (0 - W / 2) * s_bevformer, (W - 1 - W / 2) * s_bevformer
# Check 6: index 0 maps to -51.2 m and index 199 to 50.688 m, so eq. 3 is a cell-corner convention;
# a renderer that labels cell centres is offset by half a cell (0.256 m).
assert close(x_first, -51.2, 1e-9) and close(x_last, 50.688, 1e-9) and close(s_bevformer / 2, 0.256, 1e-12)
# Check 7: BEVFormer covers 200 x 0.512 = 102.4 m; LSS covers 200 x 0.5 = 100 m with the same 200 x 200 shape.
assert close(W * s_bevformer, 102.4, 1e-9) and close(200 * 0.5, 100.0, 1e-12)
# Check 8: LSS depth bins from 4.0 m to 45.0 m every 1.0 m give 41 bins per pixel if 45 m is excluded
# (half-open range) and 42 if it is included; the paper's sentence does not settle it.
bins_half_open = len([4.0 + k for k in range(100) if 4.0 + k < 45.0])
bins_closed = len([4.0 + k for k in range(100) if 4.0 + k <= 45.0])
assert (bins_half_open, bins_closed) == (41, 42)
# Check 9: BEVFormer's 4 anchor heights spread uniformly over [-5, 3] m are 8/3 m apart.
heights = [-5 + k * 8 / 3 for k in range(4)]
assert close(heights[-1], 3.0, 1e-12) and close(heights[1] - heights[0], 2.6667, 1e-4)

# --- Example C: OctoMap log-odds with clamping -------------------------------------
def logit(p):
    return math.log(p / (1 - p))


def prob(l):
    return 1 / (1 + math.exp(-l))


l_hit, l_miss, l_min, l_max = logit(0.7), logit(0.4), logit(0.1192), logit(0.971)
# Check 10: the paper's log-odds 0.85, -0.4, -2 and 3.5 match probabilities 0.7, 0.4, 0.12 and 0.97.
assert close(l_hit, 0.847, 1e-3) and close(l_miss, -0.405, 1e-3)
assert close(l_min, -2.0, 2e-3) and close(l_max, 3.5, 2e-2)


def update(l, z, clamp=True):
    l = l + (l_hit if z else l_miss)
    return max(min(l, l_max), l_min) if clamp else l


def hits_to_occupied(l, clamp=True):
    n = 0
    while prob(l) <= 0.5:
        l = update(l, True, clamp)
        n += 1
    return n


l_clamped = l_unclamped = 0.0
for _ in range(20):                       # a cell seen free 20 times (constructed)
    l_clamped = update(l_clamped, False)
    l_unclamped = update(l_unclamped, False, clamp=False)
# Check 11: with clamping the cell stops at l_min and 3 hits make it occupied again;
# without clamping it needs 10 hits after 20 free observations.
assert close(l_clamped, l_min, 1e-12) and hits_to_occupied(l_clamped) == 3
assert hits_to_occupied(l_unclamped, clamp=False) == 10
# Check 12: one hit on an unknown cell (L = 0) gives p = 0.7 > 0.5: a single return marks it occupied.
assert close(prob(update(0.0, True)), 0.7, 1e-9)

# --- Example D: time offset during ego rotation ---------------------------------
omega, dt = math.radians(30.0), 0.050      # 30 deg/s yaw rate and 50 ms offset (constructed)
yaw_err = omega * dt
lateral = {r: r * math.tan(yaw_err) for r in (5.0, 20.0)}
# Check 13: 1.5 degrees of yaw error moves a point at 20 m by ~0.52 m (3.3 cells of 0.16 m) but only 0.13 m at 5 m.
assert close(math.degrees(yaw_err), 1.5, 1e-9)
assert close(lateral[20.0], 0.5237, 1e-4) and close(lateral[20.0] / 0.16, 3.27, 1e-2) and close(lateral[5.0], 0.1309, 1e-4)
# Check 14: a 10 m/s translation with the same offset shifts every point by 0.5 m regardless of range.
assert close(10.0 * dt, 0.5, 1e-12)

# --- Example E: LiDAR sampling against range -------------------------------------
az, el = math.radians(0.2), math.radians(0.4)   # constructed angular resolutions
spacing = {r: (r * az, r * el) for r in (10.0, 50.0)}
# Check 15: at 50 m consecutive returns are ~0.17 m apart horizontally and ~0.35 m vertically,
# so a 0.16 m cell receives at most about one return per scan line; at 10 m, ~0.035 m.
assert close(spacing[50.0][0], 0.1745, 1e-4) and close(spacing[50.0][1], 0.3491, 1e-4)
assert close(spacing[10.0][0], 0.0349, 1e-4)
# Check 16: the density of returns per square metre on a surface facing the sensor falls as 1/r^2 (25x from 10 m to 50 m).
dens = {r: 1 / (spacing[r][0] * spacing[r][1]) for r in (10.0, 50.0)}
assert close(dens[10.0] / dens[50.0], 25.0, 1e-9)

print("64-nuages-bev-occupation: 16 checks passed "
      f"(PointPillars canvas {nx}x{ny}, sparsity {sparsity_lo:.3f}-{sparsity_hi:.3f}, "
      f"BEVFormer half cell {s_bevformer / 2} m, OctoMap hits after clamping 3 vs 10, "
      f"yaw offset {lateral[20.0]:.2f} m at 20 m)")
