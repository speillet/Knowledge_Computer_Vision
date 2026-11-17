"""Recompute the constructed numbers added to CV-NMS-006 (reference 81-nms, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/81-nms.py
Conventions: continuous xyxy boxes, IoU without "+1", hard NMS suppresses when IoU > tau
(torchvision 0.29 `nms` contract, as in the reference). The containment ratio
|A n B| / min(|A|, |B|) is computed only as the counterexample of a different rule.
Boxes and scores are constructed.
"""
import math

checks = 0


def area(b):
    return (b[2] - b[0]) * (b[3] - b[1])


def inter(a, b):
    w = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    h = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    return w * h


def iou(a, b):
    i = inter(a, b)
    return i / (area(a) + area(b) - i)


def containment(a, b):
    return inter(a, b) / min(area(a), area(b))


def hard_nms(boxes, scores, tau, overlap=iou):
    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    kept = []
    while order:
        best = order.pop(0)
        kept.append(best)
        order = [i for i in order if overlap(boxes[best], boxes[i]) <= tau]
    return kept


def nested(a, b):
    return a[0] <= b[0] and a[1] <= b[1] and b[2] <= a[2] and b[3] <= a[3]


# 1. The card's pair: IoU = |B| / |A| = 0.04 for a nested box.
A, B = (0, 0, 100, 100), (40, 40, 60, 60)
assert nested(A, B) and iou(A, B) == area(B) / area(A) == 0.04
assert hard_nms([A, B], [0.9, 0.8], 0.5) == [0, 1]
checks += 1

# 2. Only the area ratio matters, not the position inside A.
for x in (0, 13, 20):
    for y in (0, 7, 20):
        Bp = (x, y, x + 80, y + 80)
        assert nested(A, Bp) and abs(iou(A, Bp) - 0.64) < 1e-12
assert hard_nms([A, (10, 10, 90, 90)], [0.9, 0.8], 0.5) == [0]       # 0.64 > 0.5: suppressed
assert hard_nms([A, (10, 10, 90, 90)], [0.9, 0.8], 0.7) == [0, 1]    # 0.64 <= 0.7: kept
checks += 1

# 3. Same aspect ratio, side ratio k: IoU = k^2, suppressed iff k > sqrt(tau).
assert round(math.sqrt(0.5), 3) == 0.707 and round(math.sqrt(0.7), 3) == 0.837
for k in (0.2, 0.5, 0.7, 0.71, 0.8, 0.83, 0.84, 0.9):
    side = 100 * k
    Bk = (0, 0, side, side)
    for tau in (0.5, 0.7):
        suppressed = hard_nms([A, Bk], [0.9, 0.8], tau) == [0]
        assert suppressed == (k * k > tau) == (k > math.sqrt(tau)), (k, tau)
assert abs(iou(A, (0, 0, 90, 90)) - 0.81) < 1e-12                       # shrunk duplicate
checks += 1

# 4. Counterexample: a containment ratio deletes a legitimate nested object.
adult, child = (0, 0, 100, 250), (30, 130, 80, 250)
assert nested(adult, child) and area(adult) == 25000 and area(child) == 6000
assert abs(iou(adult, child) - 0.24) < 1e-12 and containment(adult, child) == 1.0
assert hard_nms([adult, child], [0.9, 0.8], 0.5) == [0, 1]                # IoU rule keeps both
assert hard_nms([adult, child], [0.9, 0.8], 0.5, overlap=containment) == [0]   # child deleted
assert hard_nms([A, B], [0.9, 0.8], 0.5, overlap=containment) == [0]     # the card's B too
checks += 1

print(f"81-nms (CV-NMS-006): {checks} checks passed")
