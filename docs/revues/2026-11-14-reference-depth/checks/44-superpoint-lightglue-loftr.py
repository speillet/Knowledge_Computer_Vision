"""Recompute the constructed examples of CV-MATCH-APPRIS (reference 44-superpoint-lightglue-loftr).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/44-superpoint-lightglue-loftr.py
Inputs come from SuperPoint (arXiv 1712.07629, Sec. 3, 3.4, 6, 7.1, Table 4), LightGlue
(arXiv 2306.13643, Sec. 3.3, App. C eq. 12-13), LoFTR (arXiv 2104.00680, Sec. 3.1, 3.4, 3.6),
the LightGlue repository at tag v0.2 (lightglue.py normalize_keypoints, confidence_threshold;
utils.py Extractor.extract) and the LoFTR repository at commit df7ca80 (cvpr_ds_config.py,
coarse_matching.py, fine_matching.py). The scenarios are constructed.
"""

import math


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def apply(h, p):
    x, y = p
    v = [h[0][0] * x + h[0][1] * y + h[0][2],
         h[1][0] * x + h[1][1] * y + h[1][2],
         h[2][0] * x + h[2][1] * y + h[2][2]]
    return (v[0] / v[2], v[1] / v[2])


def scale_pad(s, px, py):
    """Original pixels -> network pixels: x' = s x + px, y' = s y + py."""
    return [[s, 0.0, px], [0.0, s, py], [0.0, 0.0, 1.0]]


def inv_scale_pad(s, px, py):
    return [[1 / s, 0.0, -px / s], [0.0, 1 / s, -py / s], [0.0, 0.0, 1.0]]


checks = 0

# --- Example A: preprocessing round trip (card CV-MATCH-APPRIS-005) -----------
A = scale_pad(0.5, 20, 10)
net = apply(A, (100, 60))
# Check 1: half-size resize then padding (20, 10) sends (100, 60) to (70, 40).
assert close(net[0], 70) and close(net[1], 40); checks += 1
back = apply(inv_scale_pad(0.5, 20, 10), net)
# Check 2: subtracting the padding before dividing by s recovers the original point.
assert close(back[0], 100) and close(back[1], 60); checks += 1
wrong = (net[0] / 0.5 - 20, net[1] / 0.5 - 10)
# Check 3: dividing first gives (120, 70); the error equals p (1/s - 1) = (20, 10) px.
assert close(wrong[0], 120) and close(wrong[1], 70); checks += 1

# Composition H_orig = B^-1 H_net A on a constructed network homography.
B = scale_pad(0.25, 0, 64)            # second image: other scale and padding
H_orig_true = [[1.02, 0.03, 15.0], [-0.02, 0.98, -7.0], [1e-5, 2e-5, 1.0]]
# Network homography implied by the true one: H_net = B H_orig A^-1.
H_net = matmul(matmul(B, H_orig_true), inv_scale_pad(0.5, 20, 10))
H_rec = matmul(matmul(inv_scale_pad(0.25, 0, 64), H_net), A)
p = (812.0, 433.0)
# Check 4: B^-1 H_net A maps an original point of image A exactly as the true homography does.
assert all(close(u, v, 1e-6) for u, v in zip(apply(H_rec, p), apply(H_orig_true, p))); checks += 1

# --- Example B: LightGlue v0.2 wrapper, resize and pixel-centre convention ----
W, H, LONG = 1920, 1080, 1024
s = LONG / W
new_h = H * s
# Check 5: resizing the long side to 1024 px gives 1024 x 576 and the same factor on both axes.
assert close(s, 0.533333, 1e-6) and close(new_h, 576.0); checks += 1


def to_original(k, s):
    """utils.py Extractor.extract: (k + 0.5) / s - 0.5."""
    return (k + 0.5) / s - 0.5


# Check 6: the network pixel (511.5, 287.5) maps back to (959.5, 539.5), the image centre.
assert close(to_original(511.5, s), 959.5) and close(to_original(287.5, s), 539.5); checks += 1
# Check 7: dropping the half-pixel terms (k / s) shifts every point by 0.5 (1/s - 1):
# 0.4375 px at s = 1024/1920 and 1.5 px at s = 1/4.
assert close(to_original(511.5, s) - 511.5 / s, 0.5 * (1 / s - 1))
assert close(0.5 * (1 / s - 1), 0.4375) and close(0.5 * (1 / 0.25 - 1), 1.5); checks += 1

# --- Example C: LightGlue keypoint normalization (lightglue.py normalize_keypoints)
def normalize(k, size):
    shift = (size[0] / 2, size[1] / 2)
    scale = max(size) / 2
    return ((k[0] - shift[0]) / scale, (k[1] - shift[1]) / scale)


n = normalize((1919.5, 539.5), (1920, 1080))
# Check 8: with the true image size the long axis spans [-1, 1] and the aspect ratio is kept.
assert close(n[0], 0.999479, 1e-6) and close(n[1], -0.000521, 1e-6); checks += 1
# Without image_size the code uses 1 + max - min of the keypoints as the size.
kx = (100.0, 1100.0)
ky = (50.0, 650.0)
size_est = (1 + kx[1] - kx[0], 1 + ky[1] - ky[0])
ratio = (max(1920, 1080) / 2) / (max(size_est) / 2)
# Check 9: keypoints spanning 1001 x 601 px give a scale of 500.5 instead of 960,
# so every relative offset seen by the rotary encoding is 1.92 times larger.
assert size_est == (1001.0, 601.0) and close(ratio, 1.918082, 1e-6); checks += 1

# --- Example D: LightGlue adaptive depth thresholds (paper eq. 12, code) -----
L = 9
lam = [0.8 + 0.1 * math.exp(-4 * l / L) for l in range(L)]
# Check 10: the confidence threshold decays from 0.900 at layer 0 to 0.803 at layer 8.
assert close(lam[0], 0.9) and close(lam[8], 0.802856, 1e-6); checks += 1
# Check 11: width_confidence 0.99 is the paper's matchability threshold beta = 1 - 0.99 = 0.01.
assert close(1 - 0.99, 0.01); checks += 1
# Check 12: one cross-attention similarity for M = N = 2048 and d = 256 costs about 1.07e9
# multiply-accumulates; pruning 30% of the points of each image leaves 0.49 of it.
macs = 2048 * 2048 * 256
assert macs == 1_073_741_824 and close((0.7 * 2048) ** 2 * 256 / macs, 0.49); checks += 1

# --- Example E: LoFTR grid geometry (paper Sec. 3.1, 3.4, 3.6; official config) ---
w_img, h_img = 640, 480
wc, hc = w_img // 8, h_img // 8
cells = wc * hc
# Check 13: a 640x480 image gives 80x60 = 4800 coarse cells; full attention would need
# 4800^2 = 23,040,000 scores per head and layer.
assert cells == 4800 and cells ** 2 == 23_040_000; checks += 1
border_rm = 2
# Check 14: removing 2 cells at every border (border_rm = 2) leaves 76x56 = 4256 candidate cells.
assert (wc - 2 * border_rm) * (hc - 2 * border_rm) == 4256; checks += 1
window, fine_stride = 5, 2
max_offset = (window // 2) * fine_stride
# Check 15: the fine expectation lies inside the 5x5 window at stride 2, so refinement
# moves the image-B point by at most 4 px per axis, half of the 8 px coarse cell.
assert max_offset == 4 and max_offset * 2 == 8; checks += 1

# --- Example F: SuperPoint grid and published localization numbers ------------
hs, ws = 480, 640
# Check 16: a 480x640 input gives 60x80 cells; the 256-D descriptor map then holds
# 1,228,800 floats (4.9 MB in float32).
assert (hs // 8) * (ws // 8) == 4800 and 4800 * 256 == 1_228_800
assert close(1_228_800 * 4 / 1e6, 4.9152); checks += 1
# Check 17: Table 4 of SuperPoint: SIFT is better at eps = 1 px (.424 vs .310), SuperPoint at
# eps = 3 and 5 px; SIFT's mean localization error is lower (0.833 vs 1.158 px).
sp = {"e1": 0.310, "e3": 0.684, "e5": 0.829, "mle": 1.158}
sift = {"e1": 0.424, "e3": 0.676, "e5": 0.759, "mle": 0.833}
assert sift["e1"] > sp["e1"] and sp["e3"] > sift["e3"] and sp["e5"] > sift["e5"]
assert sift["mle"] < sp["mle"]; checks += 1

print(f"44-superpoint-lightglue-loftr: {checks} checks passed")
