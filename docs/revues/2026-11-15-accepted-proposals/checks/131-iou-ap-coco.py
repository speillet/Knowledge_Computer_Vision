"""Recompute the constructed examples of CV-IOU-AP-008 (reference 131-iou-ap-coco).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-15-accepted-proposals/checks/131-iou-ap-coco.py

Re-implements, for one category and one IoU threshold, the parts of pycocotools cocoeval.py at
commit 8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9 that fix the conventions:
- evaluate L153-L154: evaluateImg receives maxDet = maxDets[-1];
- evaluateImg L259-L260: detections of one image and category sorted by decreasing score
  (stable mergesort) and truncated to maxDet; L272-L296: greedy matching in that order;
- accumulate L362-L370: per-image lists cut at maxDet, concatenated, stable-sorted by score;
  L384-L408: rc = tp/npig, pr = tp/(tp+fp), right-to-left envelope, left searchsorted on the
  101 recall thresholds, levels beyond the last recall left at 0.
Matching is simplified: each detection names the ground truth it would match (or none); the
first detection in score order to claim a ground truth is a TP, later claimants are FPs. Exact
fractions replace floats. No pycocotools code is executed.
"""

import random
from fractions import Fraction as F

checks = 0
REC_THRS = [F(m, 100) for m in range(101)]


def ap_from_flags(flags, n_gt):
    """accumulate L384-L408 for one (t, k, a, m) cell; flags are TP booleans in rank order."""
    tp = fp = 0
    rc, pr = [], []
    for f in flags:
        tp += f
        fp += not f
        rc.append(F(tp, n_gt))
        pr.append(F(tp, tp + fp))
    for i in range(len(pr) - 1, 0, -1):          # right-to-left envelope
        if pr[i] > pr[i - 1]:
            pr[i - 1] = pr[i]
    q = []
    for thr in REC_THRS:                          # searchsorted(rc, thr, side='left')
        idx = next((i for i, r in enumerate(rc) if r >= thr), None)
        q.append(pr[idx] if idx is not None else F(0))
    return sum(q) / len(q)


def evaluate(images, n_gt, score_thr, cap):
    """images: list of lists of (score, gt_id or None). Returns (merged TP flags, scores)."""
    merged = []
    for dets in images:
        kept = [d for d in dets if d[0] >= score_thr]
        kept = sorted(kept, key=lambda d: -d[0])[:cap]      # stable sort, truncate per image
        claimed = set()
        for score, gid in kept:                              # greedy matching in score order
            is_tp = gid is not None and gid not in claimed
            if is_tp:
                claimed.add(gid)
            merged.append((score, is_tp))
    merged.sort(key=lambda d: -d[0])                         # stable merge across images
    return [f for _, f in merged], [s for s, _ in merged]


def operating_point(flags, scores, thr, n_gt):
    tp = sum(f for f, s in zip(flags, scores) if s >= thr)
    n = sum(1 for s in scores if s >= thr)
    return F(tp, n), F(tp, n_gt)


# --- Card example: 4 objects, deployed threshold 0.5 ---------------------------------------
# Image 1: objects a, b; image 2: object c; image 3: object d.
images = [
    [(0.90, "a"), (0.60, None), (0.02, None)],
    [(0.80, "c"), (0.04, None)],
    [(0.01, "d")],
]
before, s_before = evaluate(images, 4, 0.5, 100)
after, s_after = evaluate(images, 4, 0.001, 100)

# Check 1: ranked lists are TP, TP, FP and TP, TP, FP, FP, FP, TP, as stated in the question.
assert before == [True, True, False] and after == [True, True, False, False, False, True]
checks += 1

# Check 2: AP before = 51/101 = 0.505; after = 63.5/101 = 0.629.
ap_b, ap_a = ap_from_flags(before, 4), ap_from_flags(after, 4)
assert ap_b == F(51, 101) and ap_a == F(127, 202)
assert (round(float(ap_b), 3), round(float(ap_a), 3)) == (0.505, 0.629)
checks += 1

# Check 3: the old prefix keeps its (R, P) points; the new levels 0.51-0.75 get envelope 1/2.
assert after[:3] == before
checks += 1

# Check 4: precision and recall at the deployed threshold 0.5 are 2/3 and 1/2 in both files.
assert operating_point(before, s_before, 0.5, 4) == operating_point(after, s_after, 0.5, 4) == (F(2, 3), F(1, 2))
checks += 1

# Check 5: appending only FPs leaves AP unchanged (reference example D logic).
assert ap_from_flags(before + [False, False], 4) == ap_b
checks += 1

# --- Per-image cap: added detections beyond the evaluator cap are dropped ------------------
# Check 6: with a cap of 2 per image, image 1 keeps 0.90 and 0.60 at threshold 0.001 and drops
# 0.02; the old detections are never displaced, so AP still cannot fall.
capped, _ = evaluate(images, 4, 0.001, 2)
assert capped[:3] == before and ap_from_flags(capped, 4) >= ap_b
checks += 1

# --- Raising a per-image cap is not covered by the argument --------------------------------
# Image A: TP 0.95, FP 0.90; image B: TP 0.50; two objects. Cap 1 -> TP, TP; cap 2 -> TP, FP, TP.
two = [[(0.95, "a"), (0.90, None)], [(0.50, "b")]]
cap1, _ = evaluate(two, 2, 0.0, 1)
cap2, _ = evaluate(two, 2, 0.0, 2)
# Check 7: AP falls from 1 to (51 + 50 * 2/3) / 101 = 0.835 when the cap is raised.
assert cap1 == [True, True] and cap2 == [True, False, True]
assert ap_from_flags(cap1, 2) == 1 and ap_from_flags(cap2, 2) == F(253, 303)
assert round(float(ap_from_flags(cap2, 2)), 3) == 0.835
checks += 1

# --- Randomized property check (deterministic seed) ----------------------------------------
# Check 8: over 3000 random instances, lowering the score threshold never lowers AP, whatever
# the per-image cap; raising the cap lowers AP in some instances.
rng = random.Random(20261115)
cap_drops = 0
for _ in range(3000):
    n_img = rng.randint(1, 4)
    imgs, gts = [], 0
    for i in range(n_img):
        g = rng.randint(0, 3)
        ids = [f"{i}-{j}" for j in range(g)]
        gts += g
        dets = [(round(rng.random(), 3), rng.choice(ids + [None]) if ids else None)
                for _ in range(rng.randint(0, 6))]
        imgs.append(dets)
    if gts == 0:
        continue
    cap = rng.randint(1, 4)
    hi, lo = sorted((rng.random(), rng.random()), reverse=True)
    f_hi, _ = evaluate(imgs, gts, hi, cap)
    f_lo, _ = evaluate(imgs, gts, lo, cap)
    assert ap_from_flags(f_lo, gts) >= ap_from_flags(f_hi, gts)
    f_c1, _ = evaluate(imgs, gts, lo, cap)
    f_c2, _ = evaluate(imgs, gts, lo, cap + 2)
    cap_drops += ap_from_flags(f_c2, gts) < ap_from_flags(f_c1, gts)
assert cap_drops > 0
checks += 1

print(f"131-iou-ap-coco (CV-IOU-AP-008): {checks} checks passed")
