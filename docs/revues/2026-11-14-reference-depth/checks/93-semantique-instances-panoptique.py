"""Recompute the constructed examples of CV-SEGMENTATION (reference 93-semantique-instances-panoptique).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/93-semantique-instances-panoptique.py
Formulas come from Kirillov et al. 2019 (PQ, eqs. 1-2, Theorem 1), Long et al. 2015 (IU metrics),
Cordts et al. 2016 (dataset-level IoU), Cheng et al. 2021 (Boundary IoU, eq. 1) and
Chen et al. 2018 (DeepLabv3+, Table 5). The segments, images and disks are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: panoptic quality on a constructed image ------------------------
car_matched_ious = [0.9, 0.6]          # two matched pairs (IoU > 0.5)
car_fp, car_fn = 2, 1                  # one stray prediction + one prediction at IoU 0.45; one missed car
tp = len(car_matched_ious)
sq = sum(car_matched_ious) / tp
rq = tp / (tp + 0.5 * car_fp + 0.5 * car_fn)
pq_car = sum(car_matched_ious) / (tp + 0.5 * car_fp + 0.5 * car_fn)
# Check 1: SQ = 0.75, RQ = 2 / 3.5 = 0.571 and PQ = SQ x RQ = 0.429 for the car class.
assert close(sq, 0.75, 1e-12) and close(rq, 0.5714, 1e-4) and close(pq_car, 0.4286, 1e-4)
assert close(pq_car, sq * rq, 1e-12)
# Check 2: RQ equals the F1 score 2TP / (2TP + FP + FN).
assert close(rq, 2 * tp / (2 * tp + car_fp + car_fn), 1e-12)
pq_road = 0.95                         # one stuff segment matched at IoU 0.95
# Check 3: the class average gives the single road segment as much weight as all cars: PQ = 0.689.
assert close((pq_car + pq_road) / 2, 0.6893, 1e-4)
# Check 4: a prediction at IoU 0.45 can never be matched, and two disjoint predictions cannot both exceed 0.5 with one
# segment (Theorem 1): IoU(p1, g) + IoU(p2, g) <= 1 for disjoint p1, p2.
g = 100
for a1, a2, extra1, extra2 in ((60, 40, 0, 0), (55, 45, 10, 0), (51, 49, 0, 0)):
    iou1 = a1 / (g + extra1)
    iou2 = a2 / (g + extra2)
    assert iou1 + iou2 <= 1 + 1e-12

# --- Example B: aggregation and Dice ------------------------------------------
# Image 1: object of 10,000 px, 9,000 TP, 1,000 FN, 0 FP.  Image 2: object of 100 px, fully missed.
tp1, fn1, fp1 = 9000, 1000, 0
tp2, fn2, fp2 = 0, 100, 0
iou1 = tp1 / (tp1 + fp1 + fn1)
iou2 = tp2 / (tp2 + fp2 + fn2)
dataset_iou = (tp1 + tp2) / (tp1 + tp2 + fp1 + fp2 + fn1 + fn2)
# Check 5: dataset-level accumulation gives 0.891, the per-image mean 0.45.
assert close(dataset_iou, 0.8911, 1e-4) and close((iou1 + iou2) / 2, 0.45, 1e-12)


def dice_from_iou(j):
    return 2 * j / (1 + j)


# Check 6: Dice = 2 IoU / (1 + IoU): IoU 0.818 <-> Dice 0.9, IoU 0.5 <-> Dice 0.667, and Dice >= IoU.
assert close(dice_from_iou(9 / 11), 0.9, 1e-12) and close(dice_from_iou(0.5), 2 / 3, 1e-12)
assert all(dice_from_iou(j / 100) >= j / 100 for j in range(101))
# Check 7: the identity holds on counts: 2TP/(2TP+FP+FN) with TP=9000, FP=0, FN=1000 equals dice_from_iou(0.9).
assert close(2 * tp1 / (2 * tp1 + fp1 + fn1), dice_from_iou(iou1), 1e-12)

# --- Example C: Mask IoU against Boundary IoU for a one-pixel shrink -----------
def mask_iou_shrink(r, delta):
    return (r - delta) ** 2 / r ** 2


def boundary_iou_shrink(r, delta, d):
    """Concentric disks, prediction radius r - delta; bands of width d inside each mask (d <= r - delta)."""
    inter = (r - delta) ** 2 - (r - d) ** 2
    union = r ** 2 - (r - delta - d) ** 2
    return inter / union


# Check 8: Mask IoU rewards size: 0.9025 for r = 20 px and 0.9801 for r = 100 px with the same 1-px error.
assert close(mask_iou_shrink(20, 1), 0.9025, 1e-12) and close(mask_iou_shrink(100, 1), 0.9801, 1e-12)
# Check 9: Boundary IoU is (d - delta) / (d + delta) = 0.875 for d = 15 px, whatever the radius.
for r in (20, 50, 100, 400):
    assert close(boundary_iou_shrink(r, 1, 15), 14 / 16, 1e-12)
# Check 10: d = 2 % of the diagonal of a 640 x 480 image is about 16 px (the paper reports 15 px on average).
assert close(0.02 * math.hypot(640, 480), 16.0, 1e-9)

# --- Cost figures -----------------------------------------------------------------
# Check 11: float32 logits for 19 classes on a 2048 x 1024 image take 159.4 MB (10^6 bytes).
assert close(19 * 2048 * 1024 * 4 / 1e6, 159.38, 0.01)
# Check 12: DeepLabv3+ Table 5 (Xception, single scale, no decoder): eval OS 8 costs 240.85 / 68.00 = 3.54x for +0.47 mIoU.
assert close(240.85 / 68.00, 3.542, 1e-3) and close(79.64 - 79.17, 0.47, 1e-9)
# Check 13: a 10-px-wide structure spans 10/16 = 0.625 feature cells at output stride 16 and 1.25 at stride 8.
assert 10 / 16 == 0.625 and 10 / 8 == 1.25
# Check 14: a 28 x 28 Mask R-CNN mask resized to a 560-px box gives 20 px per mask cell.
assert 560 / 28 == 20

print("93-semantique-instances-panoptique: 14 checks passed")
