"""Recompute the constructed examples of CV-ANOMALIES (reference 73-patchcore-padim).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/73-patchcore-padim.py
Inputs come from PatchCore (arXiv 2106.08265v2, Sec. 3.1, 4.1, Table 5, App. A),
PaDiM (arXiv 2011.08785v1, Sec. III-B, IV-B, V-A, Table VIII), MVTec AD
(Bergmann et al., CVPR 2019, Table 1, Sec. 4.3), ResNet (He et al. 2016, Table 1)
and the official PatchCore README (resize 256, crop 224, 1024-d features, 10 %
coreset). Training-set sizes, gradients, noise levels and line rates are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


checks = 0

# --- Example A: resolution trace of the MVTec preprocessing -------------------
ORIG, RESIZE, CROP = 1024, 256, 224        # MVTec side length; resize and centre crop
STRIDE_L1, STRIDE_L2 = 4, 8                 # ResNet conv2_x and conv3_x strides (56x56, 28x28 at 224)
grid_l1, grid_l2 = CROP // STRIDE_L1, CROP // STRIDE_L2
# Check: a 224 px crop gives 56x56 (layer1, PaDiM grid) and 28x28 (layer2, PatchCore grid) cells.
assert (grid_l1, grid_l2) == (56, 56 // 2) == (56, 28); checks += 1
scale = ORIG / RESIZE
cell_orig = STRIDE_L2 * scale
# Check: one layer2 cell spans 8 crop px, i.e. 32 px of the 1024 px original; a 3x3 neighbourhood spans 96 px.
assert (cell_orig, 3 * cell_orig) == (32.0, 96.0); checks += 1
border_crop = (RESIZE - CROP) // 2
border_orig = border_crop * scale
# Check: the centre crop removes 16 px per side at 256 px, i.e. 64 px per side of the original,
# 12.5 % of the original width in total.
assert (border_crop, border_orig) == (16, 64.0) and close(2 * border_orig / ORIG, 0.125, 1e-12); checks += 1
# Check: a 10 px scratch in the original covers 2.5 px after resizing, under a third of one 8 px cell.
assert close(10 / scale, 2.5, 1e-12) and 10 / scale / STRIDE_L2 < 1 / 3; checks += 1

# --- Example B: PatchCore memory bank and search cost -------------------------
N_TRAIN = 200                               # constructed (MVTec categories hold 60-391 training images)
PATCHES = grid_l2 * grid_l2                 # 784 patch features per image (stride s = 1)
D_FEAT, BYTES = 1024, 4                     # official README: 1024-d features; float32
D_PROJ = 128                                # official sampler: random projection to 128 dims
bank = N_TRAIN * PATCHES
# Check: 200 images x 784 patches = 156,800 features.
assert bank == 156_800; checks += 1
mb = lambda n: n * D_FEAT * BYTES / 1e6
# Check: full bank 642.3 MB; 10 % coreset 64.2 MB; 1 % coreset 6.42 MB (float32, no index overhead).
assert close(mb(bank), 642.2528) and close(mb(bank // 10), 64.22528) and close(mb(bank // 100), 6.422528); checks += 1
macs_10 = PATCHES * (bank // 10) * D_FEAT
macs_1 = PATCHES * (bank // 100) * D_FEAT
# Check: exact search for one test image costs 1.26e10 multiply-accumulates at 10 %, 1.26e9 at 1 %.
assert macs_10 == 12_588_154_880 and macs_1 == 1_258_815_488; checks += 1
greedy = (bank // 10) * bank * D_PROJ
# Check: greedy selection of 15,680 centres over 156,800 projected features costs ~3.15e11 MACs (offline).
assert greedy == 314_703_872_000; checks += 1
full_matrix_gb = bank * bank * BYTES / 1e9
# Check: a full float32 N x N distance matrix would need ~98.3 GB, hence the approximate sampler.
assert close(full_matrix_gb, 98.34496, 1e-4); checks += 1

# --- Example C: PaDiM covariance storage, rank and scale ----------------------
POS = grid_l1 * grid_l1                     # 3136 positions on the layer1 grid
def padim_bytes(d):
    return POS * (d + d * d) * BYTES        # mean + full covariance (or its inverse) per position
# Check: d = 100 needs 126.7 MB and d = 550 needs 3.80 GB of Gaussian parameters
# (PaDiM Table VIII lists 0.17 and 3.8 including the CNN).
assert close(padim_bytes(100) / 1e9, 0.1266944, 1e-6) and close(padim_bytes(550) / 1e9, 3.8014592, 1e-6); checks += 1
# Check: storing only the upper triangle would bring d = 550 to ~1.90 GB.
assert close(POS * (550 + 550 * 551 // 2) * BYTES / 1e9, 1.9076288, 1e-6); checks += 1
# Check: the quadratic form costs 3136 * d^2 MACs per image: 31.36 M for d = 100, 948.6 M for d = 550.
assert POS * 100 ** 2 == 31_360_000 and POS * 550 ** 2 == 948_640_000; checks += 1
MVTEC_TRAIN_MAX, MVTEC_TRAIN_MIN = 391, 60   # hazelnut and toothbrush, MVTec Table 1
# Check: sample covariance rank <= N - 1, so every MVTec category is rank-deficient at d = 550,
# and toothbrush (N = 60) is rank-deficient even at d = 100.
assert MVTEC_TRAIN_MAX - 1 < 550 and MVTEC_TRAIN_MIN - 1 < 100; checks += 1
EPS = 0.01                                   # PaDiM default
delta, lam = 1.0, 4.0
m_null = delta / math.sqrt(EPS)
m_nominal = delta / math.sqrt(lam + EPS)
# Check: a unit deviation along a direction never seen in training scores 10, along a direction
# of nominal variance 4 it scores ~0.4994: a ratio of ~20.
assert close(m_null, 10.0, 1e-12) and close(m_nominal, 0.49938, 1e-5) and close(m_null / m_nominal, 20.025, 1e-3); checks += 1
# Check: under an exact Gaussian model E[M^2] = d, so a typical nominal score is ~10 for d = 100
# and ~23.45 for d = 550: raw thresholds do not transfer between embedding sizes.
assert close(math.sqrt(100), 10.0, 1e-12) and close(math.sqrt(550), 23.452, 1e-3); checks += 1

# --- Example D: golden template (variation model) and misregistration ---------
GRAD, SIGMA, TAU = 40.0, 4.0, 3.5            # grey levels per px at an edge; per-pixel std; z threshold
z = lambda shift: GRAD * shift / SIGMA        # first-order residual |grad I| * shift over sigma
# Check: a 0.5 px shift gives z = 5 (false alarm at tau = 3.5); a 0.1 px shift gives z = 1.
assert close(z(0.5), 5.0, 1e-12) and close(z(0.1), 1.0, 1e-12); checks += 1
# Check: the tolerable misregistration on that edge is tau * sigma / |grad I| = 0.35 px.
assert close(TAU * SIGMA / GRAD, 0.35, 1e-12); checks += 1

# --- Example E: what zero missed defects proves --------------------------------
def upper_bound_zero_failures(n, alpha=0.05):
    """One-sided (1 - alpha) upper bound on a rate after 0 failures in n trials: 1 - alpha**(1/n)."""
    return 1 - alpha ** (1 / n)
# Check: 0 misses on 20 defective parts bounds the miss rate only below ~13.9 % (95 %, one-sided).
assert close(upper_bound_zero_failures(20), 0.13911, 1e-5); checks += 1
n_needed = math.ceil(math.log(0.05) / math.log(1 - 0.01))
# Check: claiming a miss rate below 1 % at 95 % needs 299 defective parts with zero misses.
assert n_needed == 299 and upper_bound_zero_failures(299) < 0.01 <= upper_bound_zero_failures(298); checks += 1
# Check: MVTec AD has 1258 defective test images over 73 defect types, about 17 per type on average.
assert close(1258 / 73, 17.23, 1e-2); checks += 1

# --- Example F: cycle time --------------------------------------------------------
RATE = 2.0                                   # parts per second (constructed)
# Check: with PatchCore Table 5 mean times, 0.6 s/part overloads a 2 parts/s line (rho = 1.2)
# while 0.17 s/part uses 34 % of one server.
assert close(RATE * 0.6, 1.2, 1e-12) and close(RATE * 0.17, 0.34, 1e-12); checks += 1

# --- Example G: range of the PatchCore re-weighting (eq. 7) --------------------
def eq7_weight(d_star, d_others):
    """1 - exp(d*) / sum over N_b(m*) of exp(d), where N_b(m*) contains m* itself."""
    den = math.exp(d_star) + sum(math.exp(d) for d in d_others)
    return 1 - math.exp(d_star) / den
B = 9                                        # anomalib v2.3.0 default num_neighbors
# Check: when all b support features are as close as m*, the weight reaches its minimum 1 - 1/b = 0.8889.
assert close(eq7_weight(2.0, [2.0] * (B - 1)), 1 - 1 / B, 1e-12) and close(1 - 1 / B, 0.88889, 1e-5); checks += 1
# Check: an isolated m* (other supports at distance 4 instead of 2) keeps 98.3 % of s*.
assert close(eq7_weight(2.0, [4.0] * (B - 1)), 0.98336, 1e-5); checks += 1
# Check: eq. 7 is not scale-invariant: doubling every distance changes the weight (0.98336 -> 0.99772).
assert close(eq7_weight(4.0, [8.0] * (B - 1)), 0.99772, 1e-5); checks += 1

print(f"73-patchcore-padim: {checks} checks passed")
