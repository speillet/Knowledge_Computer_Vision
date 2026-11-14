"""Recompute the constructed examples of CV-SOT (reference 113-tracking-monoobjet).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/113-tracking-monoobjet.py
Inputs come from SiamFC (arXiv 1606.09549v2, Sec. 2.4 eq. 7, Table 1, Sec. 4.1),
KCF (arXiv 1404.7584v3, Table II), MOSSE (Bolme et al. 2010, Sec. 3.4) and
opencv_contrib 4.13.0 mosseTracker.cpp (rate = 0.2). The scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: SiamFC capture range -------------------------------------------
EXEMPLAR, SEARCH = 127, 255          # crop sizes in pixels (Sec. 2.4)
FEAT_Z, FEAT_X = 6, 22               # conv5 spatial sizes for exemplar and search (Table 1)
STRIDE = 8                           # total network stride (Sec. 2.4)
UPSAMPLED = 272                      # bicubic upsampling of the score map (Sec. 4.1)

score_side = FEAT_X - FEAT_Z + 1
# Check 1: valid cross-correlation of a 6x6 template over a 22x22 map gives 17x17 (Sec. 4.1 states 17x17).
assert score_side == 17
centre = (score_side - 1) // 2
max_offset_crop = centre * STRIDE
# Check 2: the farthest score cell lies 8 cells x stride 8 = 64 px from the crop centre,
# which equals half the size difference between search and exemplar crops.
assert max_offset_crop == 64 == (SEARCH - EXEMPLAR) // 2
# Check 3: one upsampled score cell is 0.5 px of the resampled crop.
assert close(STRIDE * score_side / UPSAMPLED, 0.5)


def siamfc_scale(w, h):
    """Scale factor s of eq. 7 with context p = (w + h) / 4 and A = 127^2."""
    p = (w + h) / 4
    return EXEMPLAR / math.sqrt((w + 2 * p) * (h + 2 * p))


s_sq = siamfc_scale(50, 50)
# Check 4: a 50x50 px target gets context-padded side 100 px, hence s = 1.27.
assert close(s_sq, 1.27)
capture_sq = max_offset_crop / s_sq
# Check 5: 64 crop px correspond to about 50.4 frame px, i.e. about one target width.
assert close(capture_sq, 50.394, 1e-3) and close(capture_sq / 50, 1.008, 1e-3)
# Check 6: for any square target the capture range is 128/127 of its width (size-independent ratio).
for side in (20, 50, 200):
    assert close(max_offset_crop / siamfc_scale(side, side) / side, 128 / 127, 1e-9)
capture_20 = max_offset_crop / siamfc_scale(20, 20)
# Check 7: a 20 px target can move at most ~20.2 px per frame, i.e. ~605 px/s at 30 frames/s,
# and the limit per second halves if the frame rate halves.
assert close(capture_20, 20.157, 1e-3) and close(capture_20 * 30, 604.7, 0.1)
s_rect = siamfc_scale(80, 40)
capture_rect = max_offset_crop / s_rect
# Check 8: an 80x40 target gets the same ~59.6 px range on both axes: 0.75 width but 1.49 heights.
assert close(capture_rect, 59.63, 1e-2)
assert close(capture_rect / 80, 0.745, 1e-3) and close(capture_rect / 40, 1.491, 1e-3)

# --- Example B: memory of a linearly interpolated appearance model -----------
L = 10  # consecutive contaminated updates (about 0.33 s at 30 frames/s)
rates = {"KCF HOG": 0.02, "KCF raw / OpenCV KCF": 0.075, "MOSSE paper": 0.125, "OpenCV MOSSE": 0.2}
expected_share = {0.02: 0.1829, 0.075: 0.5414, 0.125: 0.7369, 0.2: 0.8926}
expected_half_life = {0.02: 34.31, 0.075: 8.89, 0.125: 5.19, 0.2: 3.11}
for eta in rates.values():
    share = 1 - (1 - eta) ** L
    # Check 9: weight of the L latest observations in m_t = (1-eta) m_{t-1} + eta x_t is 1-(1-eta)^L.
    weights = [eta * (1 - eta) ** k for k in range(L)]
    assert close(sum(weights), share, 1e-12)
    # Check 10: tabulated contaminated shares after 10 updates.
    assert close(share, expected_share[eta], 1e-4)
    # Check 11: half-life in updates, ln 0.5 / ln(1 - eta).
    assert close(math.log(0.5) / math.log(1 - eta), expected_half_life[eta], 1e-2)

# Check 12: keeping the same time constant after dropping every second frame
# requires eta' = 1 - (1 - eta)^2, e.g. 0.075 -> 0.144375.
assert close(1 - (1 - 0.075) ** 2, 0.144375, 1e-9)

# --- Example C: centre precision versus overlap under an unmodelled scale change
def iou_centred(w1, h1, w2, h2):
    inter = min(w1, w2) * min(h1, h2)
    return inter / (w1 * h1 + w2 * h2 - inter)


# Check 13: a fixed 40x40 box on a target grown by 1.5x per side, same centre:
# centre error 0 px (counts for precision at 20 px) but IoU 1/2.25 = 0.444 < 0.5.
iou = iou_centred(40, 40, 60, 60)
assert close(iou, 1 / 2.25, 1e-12) and iou < 0.5

# --- Example D: SiamFC cross-correlation cost against the first convolution --
corr_macs = score_side ** 2 * FEAT_Z ** 2 * 256   # upper bound with 256 channels
conv1_macs = 123 * 123 * 96 * 11 * 11 * 3         # conv1 on the 255x255 search crop (Table 1)
# Check 14: per scale, the correlation layer costs < 1 % of conv1 alone.
assert corr_macs == 2_663_424 and conv1_macs == 527_215_392
assert corr_macs / conv1_macs < 0.01

print("113-tracking-monoobjet: 14 checks passed (SiamFC capture range, update memory, IoU vs centre, correlation cost)")
