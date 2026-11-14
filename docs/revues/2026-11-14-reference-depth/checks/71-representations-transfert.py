"""Recompute the constructed examples of CV-REPRESENTATIONS (reference 71-representations-transfert).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/71-representations-transfert.py
Inputs: ViT N = HW/P^2 (arXiv 2010.11929v2, Sec. 3.1), Swin eqs. 1-2 with M = 7 and 4x4 patches
(arXiv 2103.14030v2, Sec. 3.1-3.2), DINOv2 patch size 14 and 518 px hub default (arXiv 2304.07193v2;
facebookresearch/dinov2 hub/backbones.py), MAE 75% masking (arXiv 2111.06377), LoRA r(d+k)
(arXiv 2106.09685v2, Sec. 4.1), HOG default detector (Dalal and Triggs 2005, Sec. 6),
torchvision 0.20 ImageNet mean/std. Image and defect sizes are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: tokens, resolution and defect footprint ---------------------------
def tokens(h, w, p):
    assert h % p == 0 and w % p == 0
    return (h // p) * (w // p)


n224, n448 = tokens(224, 224, 16), tokens(448, 448, 16)
# Check 1: ViT-B/16 has 196 image tokens at 224 px and 784 at 448 px (x4); the N^2 term grows x16.
assert (n224, n448) == (196, 784) and (n448 / n224) ** 2 == 16
# Check 2: a /14 model has 256 tokens at 224 px and 1,369 (37 x 37) at the 518 px hub default.
assert tokens(224, 224, 14) == 256 and tokens(518, 518, 14) == 1369
# Check 3: 2048 px of a part image resized to 224 px makes one 14 px patch cover ~128 original pixels;
# a 20 px scratch spans ~0.16 of a patch side (~2.4% of its area).
orig, net, p = 2048, 224, 14
patch_in_orig = p * orig / net
assert close(patch_in_orig, 128.0, 1e-9)
assert close(20 / patch_in_orig, 0.156, 1e-3) and close((20 / patch_in_orig) ** 2, 0.0244, 1e-4)
# Check 4: tiling the 2048 px image into 224 px crops at native resolution keeps the scratch at 20/14 ~ 1.4 patches,
# at the cost of ceil(2048/224)^2 = 100 crops.
assert close(20 / 14, 1.4286, 1e-4) and math.ceil(2048 / 224) ** 2 == 100

# --- Example B: global versus window attention (Swin eqs. 1-2) --------------------
def omega_msa(h, w, c):
    return 4 * h * w * c * c + 2 * (h * w) ** 2 * c


def omega_wmsa(h, w, c, m=7):
    return 4 * h * w * c * c + 2 * m * m * h * w * c


# Stage 1 of a 4x4-patch hierarchy: a 224 px image gives 56 x 56 tokens, 448 px gives 112 x 112.
for side, ratio in ((56, 64), (112, 256)):
    quad_global = 2 * (side * side) ** 2
    quad_window = 2 * 49 * side * side
    # Check 5/6: the attention term of global MSA is hw/M^2 times that of 7x7 windows: 64 at 56x56, 256 at 112x112.
    assert quad_global // quad_window == ratio
# Check 7: with C = 96 channels (a constructed width), global MSA at 56 x 56 costs ~13.8x W-MSA in total multiply-adds,
# because the 4hwC^2 projection term is shared.
assert close(omega_msa(56, 56, 96) / omega_wmsa(56, 56, 96), 13.81, 1e-2)

# --- Example C: MAE encoder cost with 75% masking ----------------------------------
visible = round(196 * 0.25)
# Check 8: masking 75% of 196 patches leaves 49 tokens: 1/4 of the per-token terms and 1/16 of the N^2 term.
assert visible == 49 and (visible / 196) == 0.25 and (visible / 196) ** 2 == 1 / 16

# --- Example D: LoRA parameter count -----------------------------------------------
d = k = 768
r = 8
# Check 9: a rank-8 update of a 768 x 768 projection trains 12,288 parameters instead of 589,824 (2.08%).
assert r * (d + k) == 12_288 and d * k == 589_824 and close(r * (d + k) / (d * k), 0.02083, 1e-5)

# --- Example E: preprocessing contract -----------------------------------------------
mean, std = (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)


def normalize(rgb, divide=True):
    return tuple(((v / 255.0 if divide else v) - m) / s for v, m, s in zip(rgb, mean, std))


ok = normalize((128, 128, 128))
bug = normalize((128, 128, 128), divide=False)
# Check 10: a mid-grey pixel maps near 0.07 on the red channel when divided by 255, but to ~557 when a float
# 0-255 tensor skips the division; the slope dz/dx is 255x larger.
assert close(ok[0], 0.0741, 1e-4) and close(bug[0], 556.83, 1e-2)
assert close((1 / std[0]) / (1 / (255 * std[0])), 255.0, 1e-9)
red_rgb = normalize((255, 0, 0))
red_bgr = normalize((0, 0, 255))      # the same pixel read with swapped channels
# Check 11: a constant-colour test image exposes a channel swap: pure red gives (+2.25, -2.04, -1.80)
# in RGB order but (-2.12, -2.04, +2.64) after a BGR swap.
assert close(red_rgb[0], 2.249, 1e-3) and close(red_rgb[2], -1.804, 1e-3)
assert close(red_bgr[0], -2.118, 1e-3) and close(red_bgr[2], 2.640, 1e-3)

# --- Example F: HOG descriptor size (default detector) ------------------------------
win_w, win_h, cell, block_cells, stride, bins = 64, 128, 8, 2, 8, 9
blocks_x = (win_w - block_cells * cell) // stride + 1
blocks_y = (win_h - block_cells * cell) // stride + 1
dim = blocks_x * blocks_y * block_cells * block_cells * bins
# Check 12: 7 x 15 overlapping blocks of 2 x 2 cells with 9 bins give a 3,780-dimensional descriptor.
assert (blocks_x, blocks_y, dim) == (7, 15, 3780)

print("71-representations-transfert: 12 checks passed "
      f"(tokens {n224}->{n448}, patch footprint {patch_in_orig:.0f} px, Swin ratio 64/256, "
      f"LoRA {r * (d + k)} params, unscaled input {bug[0]:.0f} vs {ok[0]:.3f}, HOG {dim})")
