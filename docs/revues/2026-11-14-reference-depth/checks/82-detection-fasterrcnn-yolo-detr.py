"""Recompute the constructed examples of CV-DETECTEURS (reference 82-detection-fasterrcnn-yolo-detr).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/82-detection-fasterrcnn-yolo-detr.py
Inputs come from Faster R-CNN (arXiv 1506.01497v3, Sec. III-A, eq. 2, Table V), RetinaNet / focal
loss (arXiv 1708.02002v2, Sec. 3.2, 4, 4.1), FCOS (arXiv 1904.01355v5, Sec. 3.1-3.3), DETR
(arXiv 2005.12872v3, Sec. 3.1, 4), YOLO (arXiv 1506.02640v5, Sec. 2), GIoU (arXiv 1902.09630v2,
Sec. 3) and torchvision v0.29.0 (transform.py, _utils.py, roi_heads.py, fcos.py, anchor_utils.py).
Every scenario (boxes, scores, costs, counts) is constructed; no detector is run.
"""

import itertools
import math

checks = 0


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    return inter / (area(a) + area(b) - inter)


def giou(a, b):
    c = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    union = area(a) + area(b) - ix * iy
    return iou(a, b) - (area(c) - union) / area(c)


# --- Example A: anchor assignment and box encoding (Faster R-CNN eq. 2) -------
anchor = (36.0, 36.0, 164.0, 164.0)     # 128 x 128 anchor centred at (100, 100), input pixels
gt = (60.0, 80.0, 200.0, 160.0)         # centre (130, 120), 140 x 80
a_iou = iou(anchor, gt)
# Check 1: intersection 104 x 80 = 8320 and union 16384 + 11200 - 8320 = 19264, so IoU = 0.432.
assert close(a_iou, 8320 / 19264) and close(a_iou, 0.4319, 1e-4)
checks += 1
# Check 2: the anchor is neither RPN-positive (> 0.7) nor RPN-negative (< 0.3), and falls in
# RetinaNet's ignored band [0.4, 0.5): it is ignored by both rules unless it is the best anchor of the GT.
assert 0.3 <= a_iou <= 0.7 and 0.4 <= a_iou < 0.5
checks += 1


def centre_size(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, b[2] - b[0], b[3] - b[1])


xa, ya, wa, ha = centre_size(anchor)
x, y, w, h = centre_size(gt)
t = ((x - xa) / wa, (y - ya) / ha, math.log(w / wa), math.log(h / ha))
# Check 3: eq. 2 targets are (0.234, 0.156, 0.090, -0.470), dimensionless.
assert close(t[0], 0.234375) and close(t[1], 0.15625)
assert close(t[2], 0.0896, 1e-4) and close(t[3], -0.4700, 1e-4)
checks += 1
weights = (10.0, 10.0, 5.0, 5.0)        # torchvision RoI-head BoxCoder weights
tw = tuple(wi * ti for wi, ti in zip(weights, t))
# Check 4: the same box gives a different regression tensor under the weighted coder.
assert close(tw[0], 2.34375) and close(tw[1], 1.5625)
assert close(tw[2], 0.4480, 1e-4) and close(tw[3], -2.3500, 1e-4)
checks += 1
dec = (xa + t[0] * wa, ya + t[1] * ha, wa * math.exp(t[2]), ha * math.exp(t[3]))
# Check 5: decoding the eq. 2 targets returns the GT centre and size exactly.
assert all(close(u, v, 1e-9) for u, v in zip(dec, (x, y, w, h)))
checks += 1
# Check 6: torchvision clamps dw, dh at log(1000/16) before exp, i.e. at most a 62.5x enlargement.
assert close(math.exp(math.log(1000.0 / 16)), 62.5)
checks += 1

# --- Example B: FCOS location targets, level ranges and centre sampling ----------
box = (20.0, 10.0, 90.0, 70.0)          # 70 x 60 px, centre (55, 40)


def ltrb(px, py, b):
    return (px - b[0], py - b[1], b[2] - px, b[3] - py)


d = ltrb(40, 30, box)
# Check 7: card CV-DETECTEURS-007, (l, t, r, b) = (20, 20, 50, 40); decoding restores the box.
assert d == (20, 20, 50, 40)
assert (40 - d[0], 30 - d[1], 40 + d[2], 30 + d[3]) == box
checks += 1
ctr = math.sqrt(min(d[0], d[2]) / max(d[0], d[2]) * min(d[1], d[3]) / max(d[1], d[3]))
# Check 8: centre-ness target sqrt(0.4 * 0.5) = sqrt(0.2) = 0.447 (FCOS eq. 3).
assert close(ctr, math.sqrt(0.2)) and close(ctr, 0.4472, 1e-4)
checks += 1
# Check 9: max(l, t, r, b) = 50 lies in P3's range [0, 64] (m2 = 0, m3 = 64), so this location
# would be supervised on P3 only, if it were a P3 location.
assert max(d) == 50 and 0 <= max(d) <= 64
checks += 1

RANGES = {3: (0, 64), 4: (64, 128), 5: (128, 256), 6: (256, 512), 7: (512, math.inf)}
STRIDES = {3: 8, 4: 16, 5: 32, 6: 64, 7: 128}


def positives_paper(b, level, grid=40):
    """FCOS Sec. 3.1-3.2: location floor(s/2) + k s, strictly inside, m_{i-1} <= max <= m_i."""
    s = STRIDES[level]
    lo, hi = RANGES[level]
    pos = 0
    for ky, kx in itertools.product(range(grid), range(grid)):
        px, py = s // 2 + kx * s, s // 2 + ky * s
        dd = ltrb(px, py, b)
        if min(dd) > 0 and lo <= max(dd) <= hi:
            pos += 1
    return pos


def positives_torchvision(b, level, radius=1.5, grid=40):
    """torchvision 0.29 FCOS matcher: point k s, centre sampling, strictly inside, 4s < max < 8s."""
    s = STRIDES[level]
    lo = 0 if level == 3 else 4 * s
    hi = math.inf if level == 7 else 8 * s
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    pos = 0
    for ky, kx in itertools.product(range(grid), range(grid)):
        px, py = kx * s, ky * s
        if max(abs(px - cx), abs(py - cy)) >= radius * s:
            continue
        dd = ltrb(px, py, b)
        if min(dd) > 0 and lo < max(dd) < hi:
            pos += 1
    return pos


paper = {lvl: positives_paper(box, lvl) for lvl in (3, 4, 5, 6, 7)}
# Check 10: under the paper's rule the 70 x 60 box is positive at all 64 interior P3 locations and
# at 6 edge locations of P4, i.e. one object is supervised on two levels.
assert paper == {3: 64, 4: 6, 5: 0, 6: 0, 7: 0}
checks += 1
tv = {lvl: positives_torchvision(box, lvl) for lvl in (3, 4, 5, 6, 7)}
# Check 11: torchvision's centre sampling (radius 1.5 strides) keeps a 3 x 3 block on P3 only.
assert tv == {3: 9, 4: 0, 5: 0, 6: 0, 7: 0}
checks += 1
# Check 12: a location whose largest distance is exactly 64 is positive on P3 and P4 under the
# paper's inclusive reading, and on neither level under torchvision's strict bounds (32 < 64 < 64 fails).
m = 64
assert (0 <= m <= 64) and (64 <= m <= 128)
assert not (0 < m < 64) and not (64 < m < 128)
checks += 1

# --- Example C: Hungarian matching versus greedy or per-target argmin -----------
cost = [[0.20, 0.30, 0.90],              # rows: GT g1, g2; columns: query slots q1, q2, q3
        [0.25, 0.90, 0.95]]
argmin = [min(range(3), key=lambda j: row[j]) for row in cost]
# Check 13: per-target argmin sends both objects to q1, i.e. duplicate supervision of one slot.
assert argmin == [0, 0]
checks += 1
best = min(itertools.permutations(range(3), 2), key=lambda p: cost[0][p[0]] + cost[1][p[1]])
best_cost = cost[0][best[0]] + cost[1][best[1]]
# Check 14: the one-to-one optimum is g1-q2, g2-q1 with total 0.55; q3 learns "no object".
assert best == (1, 0) and close(best_cost, 0.55)
checks += 1
pairs = sorted(((cost[i][j], i, j) for i in range(2) for j in range(3)))
used_i, used_j, greedy_cost = set(), set(), 0.0
for c, i, j in pairs:
    if i not in used_i and j not in used_j:
        used_i.add(i)
        used_j.add(j)
        greedy_cost += c
# Check 15: greedy smallest-cost-first matching takes g1-q1 then g2-q2, total 1.10 > 0.55.
assert close(greedy_cost, 1.10)
checks += 1

# --- Example D: focal-loss modulation and the dominance of easy negatives -------
gamma = 2.0
# Check 16: (1 - p_t)^2 = 0.01 at p_t = 0.9, 0.81 at 0.1, 1e-4 at 0.99 and 0.25 at 0.5.
for p, f in ((0.9, 0.01), (0.1, 0.81), (0.99, 1e-4), (0.5, 0.25)):
    assert close((1 - p) ** gamma, f, 1e-12)
checks += 1
# Check 17: at p_t ~ 0.968 the factor is ~1e-3, i.e. the "1000x lower" of focal loss Sec. 3.2.
assert close((1 - 0.968) ** gamma, 1.024e-3, 1e-9)
checks += 1
n_neg, p_neg = 100_000, 0.99           # constructed image: easy negatives
n_pos, p_pos = 100, 0.5                # and uncertain positives
ce_neg, ce_pos = n_neg * -math.log(p_neg), n_pos * -math.log(p_pos)
fl_neg = n_neg * (1 - p_neg) ** gamma * -math.log(p_neg)
fl_pos = n_pos * (1 - p_pos) ** gamma * -math.log(p_pos)
# Check 18: with cross entropy the easy negatives carry ~14.5x the positives' loss (1005 vs 69.3);
# with gamma = 2 the positives carry ~172x the negatives' loss (17.3 vs 0.10).
assert close(ce_neg, 1005.03, 0.01) and close(ce_pos, 69.31, 0.01) and close(ce_neg / ce_pos, 14.50, 0.01)
assert close(fl_neg, 0.1005, 1e-4) and close(fl_pos, 17.33, 0.01) and close(fl_pos / fl_neg, 172.4, 0.1)
checks += 1
prior = 0.01
bias = -math.log((1 - prior) / prior)
# Check 19: the prior initialisation b = -log((1 - pi) / pi) gives sigmoid(b) = 0.01, b = -4.595.
assert close(bias, -4.5951, 1e-4) and close(1 / (1 + math.exp(-bias)), prior, 1e-12)
checks += 1

# --- Example E: GIoU for disjoint boxes ----------------------------------------
A, B = (0.0, 0.0, 2.0, 2.0), (3.0, 0.0, 5.0, 2.0)
# Check 20: union 8, enclosing area 10, GIoU = -0.2 and loss 1.2; moving B to x0 = 2.5 gives loss 10/9.
assert close(giou(A, B), -0.2) and close(1 - giou(A, B), 1.2)
assert close(1 - giou(A, (2.5, 0.0, 4.5, 2.0)), 10 / 9) and iou(A, (2.5, 0.0, 4.5, 2.0)) == 0
checks += 1
# Check 21: unit boxes with gaps of 1 and 2 give GIoU -1/3 and -1/2 (2026-11-08 appendix of CV-DETECTEURS-009).
assert close(giou((0, 0, 1, 1), (2, 0, 3, 1)), -1 / 3) and close(giou((0, 0, 1, 1), (3, 0, 4, 1)), -1 / 2)
checks += 1

# --- Example F: same 2-px translation, different IoU (box-size table) -----------
cases = [((0, 0, 4, 4), (2, 0), 1 / 3), ((0, 0, 40, 40), (2, 0), 19 / 21),
         ((0, 0, 40, 4), (2, 0), 19 / 21), ((0, 0, 40, 4), (0, 2), 1 / 3)]
# Check 22: the four rows of the box-size table (4x4, 40x40, 40x4 shifted along x then y).
for g, (dx, dy), expected in cases:
    assert close(iou(g, (g[0] + dx, g[1] + dy, g[2] + dx, g[3] + dy)), expected)
checks += 1

# --- Example G: letterbox, torchvision resize and the NMS case -----------------
W0, H0, S = 1920, 1080, 640
scale = S / max(W0, H0)
pad_y = (S - H0 * scale) / 2
# Check 23: scale 1/3, useful image 640 x 360, 140 px padding above and below.
assert close(scale, 1 / 3) and close(H0 * scale, 360) and close(pad_y, 140)
checks += 1
g_orig = (900.0, 450.0, 912.0, 459.0)
G = (g_orig[0] * scale, g_orig[1] * scale + pad_y, g_orig[2] * scale, g_orig[3] * scale + pad_y)
back = (G[0] / scale, (G[1] - pad_y) / scale, G[2] / scale, (G[3] - pad_y) / scale)
# Check 24: the 12 x 9 GT becomes (300, 290, 304, 293), 4 x 3 px, and maps back exactly.
assert all(close(u, v, 1e-9) for u, v in zip(G, (300, 290, 304, 293)))
assert all(close(u, v, 1e-9) for u, v in zip(back, g_orig))
checks += 1
P, Q = (300.0, 290.0, 304.0, 293.0), (301.5, 290.0, 305.5, 293.0)
# Check 25: IoU(P, Q) = IoU(Q, G) = 7.5 / 16.5 = 5/11 > 0.4, so hard NMS at 0.4 keeps Q (score 0.9)
# and removes P (score 0.8); Q fails the 0.5 evaluation threshold and recall of this GT drops to 0.
assert close(iou(P, Q), 5 / 11) and close(iou(Q, G), 5 / 11) and iou(P, Q) > 0.4 and iou(Q, G) < 0.5
checks += 1
tv_scale = min(800 / min(W0, H0), 1333 / max(W0, H0))
# Check 26: torchvision's default transform (min_size 800, max_size 1333) uses scale 0.694 for a
# 1920 x 1080 frame, so the 12 x 9 object becomes about 8.3 x 6.2 px instead of 4 x 3 px.
assert close(tv_scale, 1333 / 1920) and close(12 * tv_scale, 8.331, 1e-3) and close(9 * tv_scale, 6.248, 1e-3)
checks += 1
# Check 27: both sizes are "small" for COCO (area < 32^2), so AP_S strata do not separate them.
assert 12 * 9 < 32 ** 2 and (12 * tv_scale) * (9 * tv_scale) < 32 ** 2 and 4 * 3 < 32 ** 2
checks += 1

# --- Example H: candidate and output counts ------------------------------------
# Check 28: YOLO v1 on VOC: S = 7, B = 2, C = 20 gives a 7 x 7 x 30 tensor and 98 boxes.
S7, B2, C20 = 7, 2, 20
assert S7 * S7 * (B2 * 5 + C20) == 1470 and S7 * S7 * B2 == 98
checks += 1
locs = sum((640 // STRIDES[lvl]) ** 2 for lvl in (3, 4, 5, 6, 7))
# Check 29: a 640 x 640 input has 8525 locations on P3-P7, hence 76,725 RetinaNet anchors (A = 9).
assert locs == 6400 + 1600 + 400 + 100 + 25 == 8525 and locs * 9 == 76_725
checks += 1
# Check 30: Faster R-CNN's "roughly 20000" anchors for a 1000 x 600 image is 60 x 40 x 9 = 21,600.
assert 60 * 40 * 9 == 21_600
checks += 1
tok32, tok16 = (640 // 32) ** 2, (640 // 16) ** 2
# Check 31: DETR encoder tokens at stride 32 versus the dilated C5 (stride 16): 400 vs 1600 tokens,
# so the (HW)^2 attention term grows 16x, as DETR Sec. 4 states for DC5.
assert tok32 == 400 and tok16 == 1600 and tok16 ** 2 // tok32 ** 2 == 16
checks += 1
# Check 32: Faster R-CNN Table V (VGG-16, K40): 141 + 10 + 47 = 198 ms, i.e. ~5 frames/s;
# ZF: 31 + 3 + 25 = 59 ms, i.e. ~17 frames/s; the region-wise stage is 24% of the VGG total.
assert 141 + 10 + 47 == 198 and close(1000 / 198, 5.05, 0.01)
assert 31 + 3 + 25 == 59 and close(1000 / 59, 16.95, 0.01) and close(47 / 198, 0.237, 0.001)
checks += 1

print(f"82-detection-fasterrcnn-yolo-detr: {checks} checks passed")
