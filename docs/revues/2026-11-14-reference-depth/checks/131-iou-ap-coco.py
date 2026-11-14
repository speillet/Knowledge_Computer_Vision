"""Recompute the constructed examples of CV-IOU-AP (reference 131-iou-ap-coco).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/131-iou-ap-coco.py
The matching and accumulation below mirror pycocotools at commit 8c9bcc3
(cocoeval.py evaluateImg L235-L313, accumulate L315-L420, Params L502-L511;
maskApi.c bbIou L109-L120) for one image and one category, without ignore flags.
All scenarios are constructed; no dataset is evaluated.
"""

import math


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def iou_xyxy(a, b):
    """Continuous-coordinate IoU of two (x1, y1, x2, y2) boxes, no +1 convention."""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    inter = w * h
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return inter / (area_a + area_b - inter)


def xywh_to_xyxy(b):
    return (b[0], b[1], b[0] + b[2], b[1] + b[3])


IOU_THRS = [0.50 + 0.05 * i for i in range(10)]
REC_THRS = [i / 100 for i in range(101)]


def match(det_ious, n_gt, t):
    """Greedy matching in score order: each detection takes the best still-free GT with IoU >= t.

    det_ious: list (score-sorted) of lists of IoU with each GT. Returns list of booleans (TP).
    """
    taken = [False] * n_gt
    out = []
    for ious in det_ious:
        best, m = min(t, 1 - 1e-10), -1
        for g in range(n_gt):
            if taken[g]:
                continue
            if ious[g] < best:
                continue
            best, m = ious[g], g
        if m >= 0:
            taken[m] = True
        out.append(m >= 0)
    return out


def ap101(tp_flags, n_gt):
    """COCO 101-point interpolated AP for one score-sorted TP/FP list (accumulate L375-L408)."""
    tp = fp = 0
    rc, pr = [], []
    for f in tp_flags:
        tp += f
        fp += not f
        rc.append(tp / n_gt)
        pr.append(tp / (tp + fp))
    for i in range(len(pr) - 1, 0, -1):          # right-to-left precision envelope
        pr[i - 1] = max(pr[i - 1], pr[i])
    q = []
    for r in REC_THRS:
        idx = next((i for i, x in enumerate(rc) if x >= r), None)   # searchsorted(side='left')
        q.append(pr[idx] if idx is not None else 0.0)               # unreachable recall -> 0
    return sum(q) / len(q)


def voc11(tp_flags, n_gt):
    """VOC2007 11-point AP (Everingham et al. 2010, eqs. 1-2) for comparison."""
    tp = fp = 0
    pts = []
    for f in tp_flags:
        tp += f
        fp += not f
        pts.append((tp / n_gt, tp / (tp + fp)))
    vals = []
    for r in [i / 10 for i in range(11)]:
        cands = [p for (rr, p) in pts if rr >= r]
        vals.append(max(cands) if cands else 0.0)
    return sum(vals) / 11


checks = 0

# --- Example A: format ambiguity --------------------------------------------
nums = (10, 20, 30, 40)
as_xyxy = nums
as_xywh = xywh_to_xyxy(nums)
# Check 1: the same four numbers read as xyxy (20x20 box) or xywh (30x40 box) overlap with IoU 1/3 only.
assert close(iou_xyxy(as_xyxy, as_xywh), 1 / 3)
checks += 1
# Check 2: areas are 400 and 1200 square pixels.
assert (as_xyxy[2] - as_xyxy[0]) * (as_xyxy[3] - as_xyxy[1]) == 400
assert (as_xywh[2] - as_xywh[0]) * (as_xywh[3] - as_xywh[1]) == 1200
checks += 1
# Check 3: a common scaling by 2.5 (resize) leaves IoU unchanged for continuous boxes.
a, b = (3.0, 4.0, 13.0, 17.0), (5.0, 6.0, 16.0, 15.0)
s = 2.5
assert close(iou_xyxy(a, b), iou_xyxy(tuple(s * v for v in a), tuple(s * v for v in b)))
checks += 1

# --- Example B: geometric tolerance per IoU threshold ------------------------
def max_shift_ratio(tau):
    """Largest one-axis shift / side for two equal squares to keep IoU >= tau."""
    return (1 - tau) / (1 + tau)


def max_scale_ratio(tau):
    """Largest side ratio of two concentric squares to keep IoU >= tau."""
    return 1 / math.sqrt(tau)


# Check 4: one-axis shift allowance is 1/3, 1/7 and 1/39 of the side at IoU 0.50, 0.75, 0.95.
assert close(max_shift_ratio(0.5), 1 / 3) and close(max_shift_ratio(0.75), 1 / 7)
assert close(max_shift_ratio(0.95), 1 / 39)
checks += 1
# Check 5: the shifted-square IoU (a - d) / (a + d) equals the box IoU at the allowance.
side = 32.0
d = side * max_shift_ratio(0.95)
assert close(iou_xyxy((0, 0, side, side), (d, 0, side + d, side)), 0.95)
checks += 1
# Check 6: allowances in pixels for squares of side 10, 32 and 96 px.
table = {sd: [round(sd * max_shift_ratio(t), 2) for t in (0.5, 0.75, 0.95)] for sd in (10, 32, 96)}
assert table[10] == [3.33, 1.43, 0.26]
assert table[32] == [10.67, 4.57, 0.82]
assert table[96] == [32.0, 13.71, 2.46]
checks += 1
# Check 7: concentric scale allowance 1.414, 1.155, 1.026 at IoU 0.50, 0.75, 0.95.
assert [round(max_scale_ratio(t), 3) for t in (0.5, 0.75, 0.95)] == [1.414, 1.155, 1.026]
checks += 1
# Check 8: one pixel of shift on a 10 px square gives IoU 9/11, two pixels 8/12 (card CV-IOU-AP-006).
assert close(iou_xyxy((0, 0, 10, 10), (1, 0, 11, 10)), 9 / 11)
assert close(iou_xyxy((0, 0, 10, 10), (2, 0, 12, 10)), 8 / 12)
checks += 1

# --- Example C: AP101 over the IoU thresholds --------------------------------
# Two GT; detections sorted by score: d1 (IoU 0.82 with GT1), d2 (IoU 0.60 with GT1), d3 (IoU 0.72 with GT2).
dets = [[0.82, 0.0], [0.60, 0.0], [0.0, 0.72]]
per_t = [ap101(match(dets, 2, t), 2) for t in IOU_THRS]
# Check 9: at IoU 0.50 the list is TP, FP (duplicate), TP and AP101 = (51 + 50 * 2/3) / 101.
assert match(dets, 2, 0.5) == [True, False, True]
assert close(per_t[0], (51 + 50 * 2 / 3) / 101) and close(per_t[0], 0.834983, 1e-6)
checks += 1
# Check 10: at IoU 0.75 the third detection fails and AP101 = 51/101.
assert match(dets, 2, 0.75) == [True, False, False]
assert close(per_t[5], 51 / 101) and close(per_t[5], 0.504950, 1e-6)
checks += 1
# Check 11: AP is 0.834983 for 5 thresholds, 0.504950 for 2 and 0 for 3; mean 0.518482.
assert [round(v, 6) for v in per_t] == [0.834983] * 5 + [0.50495] * 2 + [0.0] * 3
assert close(sum(per_t) / 10, 0.518482, 1e-6)
checks += 1
# Check 12: one GT found out of two gives 51/101 even with precision 1 (reference example).
assert close(ap101([True], 2), 51 / 101)
checks += 1
# Check 13: VOC 11-point AP of TP, FP, TP is (6 + 5 * 2/3) / 11 = 0.848485, not the COCO value.
assert close(voc11([True, False, True], 2), (6 + 5 * 2 / 3) / 11) and close(voc11([True, False, True], 2), 0.848485, 1e-6)
checks += 1
# Check 14: moving the duplicate after both TPs gives AP101 = 1.
assert close(ap101([True, True, False], 2), 1.0)
checks += 1

# --- Example D: a low-score tail never lowers interpolated AP ----------------
base = [True, False, True]                        # three GT this time
# Check 15: with 3 GT, TP, FP, TP gives (34 + 33 * 2/3) / 101 = 56/101.
assert close(ap101(base, 3), 56 / 101) and close(ap101(base, 3), 0.554455, 1e-6)
checks += 1
# Check 16: appending FP, TP below every retained score raises AP to 76.4/101 = 0.756436.
assert close(ap101(base + [False, True], 3), 76.4 / 101) and close(ap101(base + [False, True], 3), 0.756436, 1e-6)
checks += 1
# Check 17: appending only FPs leaves AP unchanged (the envelope keeps earlier points).
assert close(ap101(base + [False, False, False], 3), ap101(base, 3))
checks += 1
# Check 18: AP101 is bounded by the share of recall levels reachable: (floor(100 R_max) + 1) / 101.
for flags, n in ((base, 3), ([True], 2), (base + [False, True], 3)):
    r_max = sum(flags) / n
    assert ap101(flags, n) <= (math.floor(100 * r_max + 1e-9) + 1) / 101 + 1e-12
checks += 1

# --- Example E: crowd overlap ------------------------------------------------
crowd = (0, 0, 100, 100)
small = (40, 40, 50, 50)
# Check 19: a 10x10 detection inside a 100x100 crowd region has IoU 0.01 but crowd overlap |D n G| / |D| = 1.
assert close(iou_xyxy(small, crowd), 0.01)
inter = 10 * 10
assert close(inter / 100, 1.0)
checks += 1

# --- Example G: greedy matching is not a maximum matching --------------------
# d1 (higher score) overlaps GT1 0.60 and GT2 0.70; d2 overlaps only GT2 (0.65).
greedy = match([[0.60, 0.70], [0.0, 0.65]], 2, 0.5)
# Check 20: the evaluator's greedy rule gives d1 -> GT2 and leaves d2 as FP ...
assert greedy == [True, False]
# ... although the one-to-one assignment d1 -> GT1, d2 -> GT2 has two pairs above 0.5.
assert min(0.60, 0.65) >= 0.5
checks += 1

# --- Example H: size of the accumulated precision array -----------------------
T, R, K, A, M = 10, 101, 80, 4, 3
# Check 21: precision[T, R, K, A, M] holds 969,600 entries for the COCO defaults and 80 categories.
assert T * R * K * A * M == 969_600
checks += 1

# --- Example F: alert precision at low prevalence (card CV-IOU-AP-007) ---------
pi, r, f = 0.001, 0.99, 0.01
ppv = r * pi / (r * pi + f * (1 - pi))
# Check 22: precision of alerts is about 9.0 %.
assert close(ppv, 0.0902, 1e-4)
checks += 1

print(f"131-iou-ap-coco: {checks} checks passed")
