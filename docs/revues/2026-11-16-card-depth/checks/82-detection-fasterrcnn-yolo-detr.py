"""Recompute the numbers added to CV-DETECTEURS-002 and CV-DETECTEURS-012 (2026-11-16).

Stdlib only. Run with:
    python3 -I docs/revues/2026-11-16-card-depth/checks/82-detection-fasterrcnn-yolo-detr.py
Decoders: YOLOv3 arXiv 1804.02767v1 Sec. 2.1 (b_x = sigmoid(t_x) + c_x, b_w = p_w exp(t_w),
grid units); YOLOX tag 0.3.0 yolox/models/yolo_head.py L249-L250
((t + grid) * stride, exp(t) * stride). YOLOX Table 2 and TIDE Table 5 numbers are copied
from the papers. The AP accumulation mirrors pycocotools cocoeval.py at 8c9bcc3
(L375-L408) with exact fractions. The ranked lists are constructed.
"""
import math
from fractions import Fraction

checks = 0

# 1. Same raw output, two decoders (cell (10, 7) of a stride-32 level).
t, cell, stride = (0.0, 0.0, 0.0, 0.0), (10, 7), 32
sig = lambda v: 1 / (1 + math.exp(-v))
v3_centre = ((sig(t[0]) + cell[0]) * stride, (sig(t[1]) + cell[1]) * stride)
prior = (116, 90)                                  # any prior: the decoded size equals it
v3_size = (prior[0] * math.exp(t[2]), prior[1] * math.exp(t[3]))
yx_centre = ((t[0] + cell[0]) * stride, (t[1] + cell[1]) * stride)
yx_size = (math.exp(t[2]) * stride, math.exp(t[3]) * stride)
assert v3_centre == (336.0, 240.0) and v3_size == (116.0, 90.0)
assert yx_centre == (320.0, 224.0) and yx_size == (32.0, 32.0)
assert (v3_centre[0] - yx_centre[0], v3_centre[1] - yx_centre[1]) == (stride / 2, stride / 2)
checks += 1

# 2. YOLOX Table 2: NMS-free variant against the SimOTA model.
assert round(46.5 - 47.3, 1) == -0.8 and round(13.5 - 11.1, 1) == 2.4
checks += 1

# 3. TIDE Table 5 (Mask R-CNN, COCO, 100 most confident errors per type).
table5 = {"Loc": (22, 8, 2), "Bkgnd": (3, 34, 20)}   # crowd flag, bad annotation, ambiguous
assert sum(table5["Loc"]) == 32 and sum(table5["Bkgnd"]) == 57
checks += 1


# 4. A missing annotation can reverse a model ranking; correcting it must re-score every model.
def ap(statuses, n_gt):
    tp = fp = 0
    rc, pr = [], []
    for s in statuses:
        tp, fp = (tp + 1, fp) if s == "TP" else (tp, fp + 1)
        rc.append(Fraction(tp, n_gt)); pr.append(Fraction(tp, tp + fp))
    for i in range(len(pr) - 1, 0, -1):
        pr[i - 1] = max(pr[i - 1], pr[i])
    q = []
    for m in range(101):
        idx = next((i for i, r in enumerate(rc) if r >= Fraction(m, 100)), None)
        q.append(pr[idx] if idx is not None else 0)
    return sum(q) / 101


model_a_old = ["TP", "FP", "TP", "TP", "TP"]      # rank 2 is the real but unannotated object
model_a_new = ["TP"] * 5
model_b = ["TP"] * 4                               # misses the unannotated object
assert ap(model_a_old, 4) == Fraction(86, 101) and ap(model_b, 4) == 1
assert ap(model_a_new, 5) == 1 and ap(model_b, 5) == Fraction(81, 101)
assert round(float(Fraction(86, 101)), 3) == 0.851 and round(float(Fraction(81, 101)), 3) == 0.802
checks += 1

print(f"82-detection-fasterrcnn-yolo-detr (CV-DETECTEURS-002, CV-DETECTEURS-012): {checks} checks passed")
