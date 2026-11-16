"""Recompute the constructed example of CV-SEGMENTATION-005 (reference 93-semantique-instances-panoptique).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-09-four-proposals/checks/93-semantique-instances-panoptique.py

Re-implements, with exact fractions, the parts of panopticapi panopticapi/evaluation.py at commit
7bb4655548f98f3fedc07bf37e9040a992b054b0 that fix the conventions:
- L110-L116: joint histogram of (ground-truth id, predicted id) pixel counts, id 0 = void;
- L121-L138: pairs skipped when the ground truth is crowd or the categories differ;
  IoU = |p & g| / (|p| + |g| - |p & g| - |p & void|); every pair with IoU > 0.5 is a TP
  (no assignment step: Theorem 1 of Kirillov et al. 2019 makes the match unique);
- L141-L149: unmatched non-crowd ground truth is an FN, crowd ground truth is ignored;
- L151-L163: an unmatched prediction is ignored when (void pixels + pixels in the crowd segment
  of its category) / its area > 0.5, otherwise it is an FP;
- L49-L73: per category PQ = sum IoU / (TP + FP/2 + FN/2), SQ = sum IoU / TP, RQ = TP / (...);
  categories with TP + FP + FN = 0 are skipped; PQ, SQ and RQ are averaged separately.
The image, its segments and pixel counts are constructed; no panopticapi code is executed.
"""

import random
from fractions import Fraction as F

checks = 0
VOID = 0


def evaluate(hist, gt_segs, pred_segs, threshold_strict=True, remove_void=True):
    """hist: {(gt_id, pred_id): pixels}; gt_segs: {id: (category, iscrowd)}; pred_segs: {id: category}.

    Returns per-category stats {cat: [iou_sum, tp, fp, fn]} and the matched pairs with their IoU.
    """
    gt_area, pred_area = {}, {}
    for (g, p), n in hist.items():
        gt_area[g] = gt_area.get(g, 0) + n
        if p != VOID:
            pred_area[p] = pred_area.get(p, 0) + n
    stats = {}

    def cat_stat(c):
        return stats.setdefault(c, [F(0), 0, 0, 0])

    matched_g, matched_p, pairs = set(), set(), {}
    for (g, p), inter in hist.items():
        if g not in gt_segs or p not in pred_segs:
            continue
        cat, crowd = gt_segs[g]
        if crowd or cat != pred_segs[p]:
            continue
        void_p = hist.get((VOID, p), 0) if remove_void else 0
        iou = F(inter, pred_area[p] + gt_area[g] - inter - void_p)
        matched = (iou > F(1, 2)) if threshold_strict else (iou >= F(1, 2))
        if matched:
            s = cat_stat(cat)
            s[0] += iou
            s[1] += 1
            matched_g.add(g)
            matched_p.add(p)
            pairs[(g, p)] = iou
    crowd_of = {}
    for g, (cat, crowd) in gt_segs.items():
        if g in matched_g:
            continue
        if crowd:
            crowd_of[cat] = g
            continue
        cat_stat(cat)[3] += 1
    for p, cat in pred_segs.items():
        if p in matched_p:
            continue
        ignored = hist.get((VOID, p), 0)
        if cat in crowd_of:
            ignored += hist.get((crowd_of[cat], p), 0)
        if F(ignored, pred_area[p]) > F(1, 2):
            continue
        cat_stat(cat)[2] += 1
    return stats, pairs


def per_category(stat):
    iou, tp, fp, fn = stat
    denom = tp + F(fp, 2) + F(fn, 2)
    return iou / denom, (iou / tp if tp else F(0)), tp / denom


def average(stats):
    rows = [per_category(s) for s in stats.values() if s[1] + s[2] + s[3] > 0]
    n = len(rows)
    return tuple(sum(r[i] for r in rows) / n for i in range(3))


# --- Card image: car (thing) and road (stuff), treated as the whole evaluation set -----------
# Ground-truth ids: 0 void, 1-3 cars g1-g3, 4 road.  Predicted ids: 11-14 cars p1-p4, 15 road.
CAR, ROAD = "car", "road"
gt_segs = {1: (CAR, False), 2: (CAR, False), 3: (CAR, False), 4: (ROAD, False)}
pred_segs = {11: CAR, 12: CAR, 13: CAR, 14: CAR, 15: ROAD}
hist = {
    (1, 11): 80, (4, 11): 10,                 # p1: 80 px on g1, 10 px on road
    (2, 12): 45, (0, 12): 30, (4, 12): 15,    # p2: 45 px on g2, 30 px void, 15 px on road
    (3, 13): 40, (4, 13): 20,                 # p3: 40 px on g3, 20 px on road
    (4, 14): 30,                              # p4: 30 px entirely on road
    (1, 15): 10, (2, 15): 15, (3, 15): 20,    # road prediction covers the rest of g1-g3
    (4, 15): 1080,                            # and 1080 px of road
}
areas_gt = {g: sum(n for (a, _), n in hist.items() if a == g) for g in (1, 2, 3, 4)}
areas_pred = {p: sum(n for (_, b), n in hist.items() if b == p) for p in (11, 12, 13, 14, 15)}

# Check 1: the histogram realizes the areas stated in the question (90, 60, 60 / 90, 90, 60, 30 px)
# and every pixel has exactly one ground-truth id and one predicted id.
assert [areas_gt[g] for g in (1, 2, 3)] == [90, 60, 60]
assert [areas_pred[p] for p in (11, 12, 13, 14)] == [90, 90, 60, 30]
assert sum(areas_gt.values()) + 30 == sum(areas_pred.values()) == 1395  # + 30 void ground-truth px
checks += 1

stats, pairs = evaluate(hist, gt_segs, pred_segs)
# Check 2: IoU p1/g1 = 80/100 = 0.8, p2/g2 = 45/75 = 0.6 after void removal, road = 1080/1200 = 0.9;
# p3/g3 = 40/80 = 0.5 exactly and is not matched.
assert pairs == {(1, 11): F(4, 5), (2, 12): F(3, 5), (4, 15): F(9, 10)}
assert F(40, 60 + 60 - 40) == F(1, 2)
checks += 1

# Check 3: car TP = 2, FP = 2 (p3, p4), FN = 1 (g3); road TP = 1, FP = FN = 0.
assert stats[CAR][1:] == [2, 2, 1] and stats[ROAD][1:] == [1, 0, 0]
checks += 1

pq_car, sq_car, rq_car = per_category(stats[CAR])
pq_road, sq_road, rq_road = per_category(stats[ROAD])
# Check 4: car SQ = 0.7, RQ = 4/7 = 0.571, PQ = 1.4/3.5 = 0.4 = SQ x RQ; RQ equals F1 = 2TP/(2TP+FP+FN).
assert (sq_car, rq_car, pq_car) == (F(7, 10), F(4, 7), F(2, 5)) and pq_car == sq_car * rq_car
assert rq_car == F(2 * 2, 2 * 2 + 2 + 1) and round(float(rq_car), 3) == 0.571
checks += 1

# Check 5: road SQ 0.9, RQ 1, PQ 0.9; reported PQ = (0.4 + 0.9)/2 = 0.65, SQ 0.8, RQ 11/14 = 0.786;
# mean SQ x mean RQ = 0.629 is not the reported PQ.
pq_all, sq_all, rq_all = average(stats)
assert (pq_road, sq_road, rq_road) == (F(9, 10), F(9, 10), F(1))
assert (pq_all, sq_all, rq_all) == (F(13, 20), F(4, 5), F(11, 14))
assert round(float(sq_all * rq_all), 3) == 0.629 and sq_all * rq_all != pq_all
assert round(float(rq_all), 3) == 0.786
checks += 1

# --- Blocking-error variants ----------------------------------------------------------------
# Check 6: matching at IoU >= 0.5 counts p3: car TP 3, FP 1, FN 0, PQ = 1.9/3.5 = 0.543.
s_ge, _ = evaluate(hist, gt_segs, pred_segs, threshold_strict=False)
assert s_ge[CAR][1:] == [3, 1, 0] and per_category(s_ge[CAR])[0] == F(19, 35)
assert round(float(F(19, 35)), 3) == 0.543
checks += 1

# Check 7: keeping void pixels in the union gives p2/g2 = 45/105 = 0.43, car TP 1, FP 3, FN 2,
# PQ = 0.8/3.5 = 0.229.
s_void, pairs_void = evaluate(hist, gt_segs, pred_segs, remove_void=False)
assert F(45, 90 + 60 - 45) == F(3, 7) and round(3 / 7, 2) == 0.43 and (2, 12) not in pairs_void
assert s_void[CAR][1:] == [1, 3, 2] and per_category(s_void[CAR])[0] == F(8, 35)
assert round(float(F(8, 35)), 3) == 0.229
checks += 1

# Check 8: pooling the segments of both categories into one count gives 2.3/4.5 = 0.511.
pooled = [stats[CAR][i] + stats[ROAD][i] for i in range(4)]
assert per_category(pooled)[0] == F(23, 45) and round(float(F(23, 45)), 3) == 0.511
checks += 1

# --- Constructed variants of the decomposition --------------------------------------------
# Check 9: if p3 reached IoU 0.55, car TP 3, FP 1, FN 0: SQ falls 0.7 -> 0.65, RQ rises to 6/7,
# PQ rises 0.4 -> 1.95/3.5 = 0.557 (SQ and RQ are not independent).
var = [F(4, 5) + F(3, 5) + F(11, 20), 3, 1, 0]
pq_v, sq_v, rq_v = per_category(var)
assert (sq_v, rq_v, pq_v) == (F(13, 20), F(6, 7), F(39, 70)) and round(float(pq_v), 3) == 0.557
checks += 1

# Check 10: removing p4 alone (30 px) gives car TP 2, FP 1, FN 1: PQ = 1.4/3 = 0.467.
no_p4 = {k: v for k, v in hist.items() if k[1] != 14}
no_p4[(4, 15)] += 30                         # those road pixels are now predicted as road
s_np4, _ = evaluate(no_p4, gt_segs, {k: v for k, v in pred_segs.items() if k != 14})
assert s_np4[CAR][1:] == [2, 1, 1] and per_category(s_np4[CAR])[0] == F(7, 15)
assert round(float(F(7, 15)), 3) == 0.467
checks += 1

# --- Void and crowd rules for unmatched predictions ------------------------------------------
# Check 11: an unmatched car prediction of 40 px with 15 px void and 10 px in a car crowd region
# is ignored (25/40 > 0.5), although neither fraction alone exceeds 0.5; the crowd segment is not
# an FN. Without the crowd pixels (15/40) it is an FP.
# Ground truth: g1 car (60 px), g5 car crowd (30 px), g6 road (5 px); prediction p21 car (40 px).
g2 = {1: (CAR, False), 5: (CAR, True), 6: (ROAD, False)}
h2 = {
    (1, 21): 10, (0, 21): 15, (5, 21): 10, (6, 21): 5,   # p21: 10 on g1, 15 void, 10 crowd, 5 road
    (1, VOID): 50, (5, VOID): 20,                        # rest of g1 and of the crowd unpredicted
}
s2, pairs2 = evaluate(h2, g2, {21: CAR})
assert pairs2 == {} and F(10, 40 + 60 - 10 - 15) < F(1, 2)   # p21/g1 IoU = 10/75
assert s2[CAR][1:] == [0, 0, 1]              # only g1 is an FN; p21 ignored; crowd g5 ignored
assert F(15, 40) <= F(1, 2) and F(10, 40) <= F(1, 2) and F(25, 40) > F(1, 2)
g2_nocrowd = dict(g2)
g2_nocrowd[5] = (ROAD, True)                 # same pixels, crowd of another category
s3, _ = evaluate(h2, g2_nocrowd, {21: CAR})
assert s3[CAR][1:] == [0, 1, 1]
checks += 1

# --- Theorem 1 and the strict threshold ------------------------------------------------------
# Check 12: a 2-pixel segment split between two disjoint 1-pixel predictions gives two pairs at
# IoU exactly 0.5: with >= 0.5 both match, with > 0.5 neither does.
h_tie = {(1, 11): 1, (1, 12): 1}
gt_tie, pred_tie = {1: (CAR, False)}, {11: CAR, 12: CAR}
s_tie_ge, p_tie_ge = evaluate(h_tie, gt_tie, pred_tie, threshold_strict=False)
s_tie_gt, p_tie_gt = evaluate(h_tie, gt_tie, pred_tie)
assert set(p_tie_ge.values()) == {F(1, 2)} and len(p_tie_ge) == 2 and s_tie_ge[CAR][1] == 2
assert p_tie_gt == {} and s_tie_gt[CAR][1:] == [0, 2, 1]
checks += 1

# Check 13: on 3000 random 1-D panoptic pairs with void and crowd, the void-adjusted IoU > 0.5
# never matches a ground-truth segment twice or a prediction twice (Theorem 1 survives void
# removal); with >= 0.5, double matches occur.
rng = random.Random(20261116)
double_ge = 0
for _ in range(3000):
    n = rng.randint(2, 12)
    gt_ids = [rng.randint(0, 3) for _ in range(n)]          # 0 = void
    pr_ids = [rng.randint(0, 4) + 10 for _ in range(n)]     # 10 = unlabelled prediction
    pr_ids = [VOID if p == 10 else p for p in pr_ids]
    h = {}
    for g, p in zip(gt_ids, pr_ids):
        h[(g, p)] = h.get((g, p), 0) + 1
    cats = {i: rng.choice((CAR, ROAD)) for i in range(1, 15)}
    gts = {g: (cats[g], rng.random() < 0.2) for g in set(gt_ids) if g != VOID}
    prs = {p: cats[p] for p in set(pr_ids) if p != VOID}
    for strict in (True, False):
        _, pr = evaluate(h, gts, prs, threshold_strict=strict)
        gs = [g for g, _ in pr]
        ps = [p for _, p in pr]
        unique = len(gs) == len(set(gs)) and len(ps) == len(set(ps))
        if strict:
            assert unique
        else:
            double_ge += not unique
assert double_ge > 0
checks += 1

print(f"93-semantique-instances-panoptique (CV-SEGMENTATION-005): {checks} checks passed")
