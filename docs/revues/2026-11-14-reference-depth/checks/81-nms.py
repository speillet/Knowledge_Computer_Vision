"""Recompute the constructed examples of CV-NMS (reference 81-nms).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/81-nms.py
Conventions follow torchvision 0.29 (xyxy, continuous coordinates, suppression when
IoU > threshold) and, for comparison, the inclusive "+1" convention of the original
Soft-NMS code (commit b8e69bd). Soft-NMS formulas come from Bodla et al., Sec. 4;
the CUDA mask layout from torchvision v0.29.2 nms_kernel.cu (64 boxes per word).
Boxes, scores and sizes are constructed.
"""

import math
import random


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def area(b, plus_one=False):
    e = 1 if plus_one else 0
    return (b[2] - b[0] + e) * (b[3] - b[1] + e)


def iou(a, b, plus_one=False):
    e = 1 if plus_one else 0
    w = max(0.0, min(a[2], b[2]) - max(a[0], b[0]) + e)
    h = max(0.0, min(a[3], b[3]) - max(a[1], b[1]) + e)
    inter = w * h
    return inter / (area(a, plus_one) + area(b, plus_one) - inter)


def hard_nms(boxes, scores, tau, plus_one=False):
    """Greedy NMS; ties broken by input index; suppress when IoU > tau (torchvision convention)."""
    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    kept = []
    while order:
        best = order.pop(0)
        kept.append(best)
        order = [i for i in order if iou(boxes[best], boxes[i], plus_one) <= tau]
    return kept


checks = 0

# --- Example A: the pilot example (also executed by examples/pilot_math.py) --------
A, B, C = (0, 0, 10, 10), (2, 0, 12, 10), (20, 0, 30, 10)
S = [0.9, 0.8, 0.7]
# Check: intersection 80, union 120, IoU 2/3; NMS keeps A, C at 0.5 and A, B, C at 0.7.
assert close(iou(A, B), 2 / 3, 1e-12) and hard_nms([A, B, C], S, 0.5) == [0, 2] and hard_nms([A, B, C], S, 0.7) == [0, 1, 2]; checks += 1

# --- Example B: the "+1" pixel convention changes IoU and decisions -----------------
inc = iou(A, B, plus_one=True)
# Check: inclusive coordinates give 99 / 143 = 0.6923 instead of 0.6667.
assert close(inc, 99 / 143, 1e-12) and close(inc, 0.69231, 1e-5); checks += 1
# Check: at tau = 0.68 the continuous convention keeps B, the inclusive one suppresses it.
assert hard_nms([A, B, C], S, 0.68) == [0, 1, 2] and hard_nms([A, B, C], S, 0.68, plus_one=True) == [0, 2]; checks += 1

# --- Example C: two equal boxes side by side ----------------------------------------
def shift_limit(w, tau):
    """Largest horizontal shift d for which IoU = (w - d) / (w + d) still exceeds tau."""
    return w * (1 - tau) / (1 + tau)


# Check: IoU of two w-wide boxes shifted by d is (w - d)/(w + d): w = 10, d = 2 gives 2/3.
assert close(iou((0, 0, 10, 10), (2, 0, 12, 10)), (10 - 2) / (10 + 2), 1e-12); checks += 1
# Check: at tau = 0.5 a neighbour is suppressed when closer than w/3; at 0.7, closer than 0.176 w.
assert close(shift_limit(1, 0.5), 1 / 3, 1e-12) and close(shift_limit(1, 0.7), 0.17647, 1e-5); checks += 1
# Check: for 40 px wide pedestrians the limits are 13.3 px (tau 0.5) and 7.06 px (tau 0.7).
assert close(shift_limit(40, 0.5), 13.333, 1e-3) and close(shift_limit(40, 0.7), 7.0588, 1e-4); checks += 1

# --- Example D: inclusion -------------------------------------------------------------
big, small = (0, 0, 100, 100), (40, 40, 60, 60)
# Check: IoU = |B|/|A| = 400/10000 = 0.04 while intersection / area(small) = 1.
assert close(iou(big, small), 0.04, 1e-12) and close(400 / area(small), 1.0, 1e-12); checks += 1
# Check: a contained box is suppressed at tau only if |B| > tau |A|: a 75 x 75 box inside 100 x 100 is (0.5625 > 0.5).
assert iou(big, (0, 0, 75, 75)) > 0.5 and hard_nms([big, (0, 0, 75, 75)], [0.9, 0.8], 0.5) == [0]; checks += 1

# --- Example E: Soft-NMS rescoring (Bodla et al., Sec. 4) ------------------------------
def gaussian(s, u, sigma):
    return s * math.exp(-u * u / sigma)


def linear(s, u, nt):
    return s * (1 - u) if u >= nt else s


# Check: score 0.8 at IoU 0.8 becomes 0.2224 (Gaussian, sigma 0.5) and 0.16 (linear, N_t 0.3).
assert close(gaussian(0.8, 0.8, 0.5), 0.22243, 1e-5) and close(linear(0.8, 0.8, 0.3), 0.16, 1e-12); checks += 1
# Check: at IoU 0.5 the Gaussian multiplier is exp(-0.5) = 0.6065; zero overlap keeps the score.
assert close(math.exp(-0.25 / 0.5), 0.60653, 1e-5) and gaussian(0.7, 0.0, 0.5) == 0.7; checks += 1

# --- Example F: greedy selection is not transitive -------------------------------------
P, Q, R = (0, 0, 10, 10), (3, 0, 13, 10), (6, 0, 16, 10)
# Check: IoU(P,Q) = IoU(Q,R) = 7/13 > 0.5 but IoU(P,R) = 0.25: NMS keeps P and R.
assert close(iou(P, Q), 7 / 13, 1e-12) and close(iou(P, R), 0.25, 1e-12) and hard_nms([P, Q, R], [0.9, 0.8, 0.7], 0.5) == [0, 2]; checks += 1

# --- Example G: kept boxes are pairwise below the threshold; NMS is idempotent ----------
rng = random.Random(81)
for _ in range(200):
    n = rng.randint(2, 12)
    boxes = []
    for _ in range(n):
        x, y = rng.uniform(0, 50), rng.uniform(0, 50)
        boxes.append((x, y, x + rng.uniform(5, 30), y + rng.uniform(5, 30)))
    scores = [rng.random() for _ in range(n)]
    kept = hard_nms(boxes, scores, 0.5)
    assert all(iou(boxes[i], boxes[j]) <= 0.5 for i in kept for j in kept if i < j)
    sub = [boxes[i] for i in kept]
    assert hard_nms(sub, [scores[i] for i in kept], 0.5) == list(range(len(sub))) or \
        sorted(hard_nms(sub, [scores[i] for i in kept], 0.5)) == list(range(len(sub)))
# Check: on 200 random configurations, kept boxes have pairwise IoU <= 0.5 and a second pass keeps them all.
checks += 1

# --- Example H: IoU invariance and the batched coordinate trick -------------------------
def scale(b, sx, sy, tx=0.0, ty=0.0):
    return (b[0] * sx + tx, b[1] * sy + ty, b[2] * sx + tx, b[3] * sy + ty)


# Check: a common translation and axis-wise scaling (2, 0.5) leave IoU(A, B) = 2/3.
assert close(iou(scale(A, 2, 0.5, 7, -3), scale(B, 2, 0.5, 7, -3)), 2 / 3, 1e-12); checks += 1


def coordinate_trick(boxes, labels):
    m = max(max(b) for b in boxes)
    return [tuple(c + lab * (m + 1) for c in b) for b, lab in zip(boxes, labels)]


ok = coordinate_trick([(0, 0, 100, 10), (20, 0, 60, 10)], [0, 1])
# Check: with non-negative coordinates the shifted boxes of two classes do not overlap.
assert iou(ok[0], ok[1]) == 0.0; checks += 1
bad = coordinate_trick([(0, 0, 100, 10), (-100, -101, -1, -91)], [0, 1])
# Check: the offset shifts x and y together, so a class-1 box with negative x and y (before clipping)
# lands on the class-0 box (IoU 0.99): the documented 0 <= x1, 0 <= y1 precondition matters.
assert close(iou(bad[0], bad[1]), 0.99, 1e-12) and hard_nms(bad, [0.9, 0.8], 0.5) == [0]; checks += 1

# --- Example I: costs -------------------------------------------------------------------
n = 10_000
col_blocks = math.ceil(n / 64)
# Check: the CUDA suppression mask for 10,000 boxes holds 10,000 x 157 64-bit words, 12.56 MB.
assert col_blocks == 157 and n * col_blocks * 8 == 12_560_000; checks += 1
# Check: batched_nms switches to the per-class loop above 4,000 tensor elements on CPU (1,000 boxes)
# and 100,000 on GPU (25,000 boxes).
assert 4000 // 4 == 1000 and 100_000 // 4 == 25_000; checks += 1
# Check: n(n-1)/2 = 49,995,000 IoU evaluations in the worst case for 10,000 boxes.
assert n * (n - 1) // 2 == 49_995_000; checks += 1

print(f"81-nms: {checks} checks passed")
