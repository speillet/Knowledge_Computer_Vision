"""Recompute the constructed numbers added to CV-WATERSHED-005 (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/91-otsu-distance-watershed.py
Matching rule (IoU strictly above 0.5): Kirillov et al. 2019, Sec. 4.1, Theorem 1.
Dam rule (a pixel reached by two different labels becomes -1): OpenCV 4.13.0
segmentation.cpp L265-L293, re-implemented below for a constant image (one queue level).
"""
from collections import deque

checks = 0


def iou(a, b):
    return len(a & b) / len(a | b)


def f1(tp, fp, fn):
    return 2 * tp / (2 * tp + fp + fn)


# Worked example C: a merged region against two ground-truth objects.
A = {(r, c) for r in range(10) for c in range(10)}
B = {(r, c) for r in range(10) for c in range(10, 20)}
merged = A | B
assert iou(merged, A) == 0.5 and iou(merged, B) == 0.5      # not strictly above 0.5
assert f1(0, 1, 2) == 0
A7 = {(r, c) for r in range(10) for c in range(14)}          # areas 70 / 30 per 10 rows
B3 = {(r, c) for r in range(10) for c in range(14, 20)}
assert abs(iou(A7 | B3, A7) - 0.7) < 1e-12 and iou(A7 | B3, B3) < 0.5
assert abs(f1(1, 0, 1) - 2 / 3) < 1e-12
checks += 1

# Worked example E: OpenCV's labelling rule on two touching 20 x 20 squares.
H, W = 20, 40
labels = [[0] * W for _ in range(H)]
for r in range(H):
    labels[r][0] = 2                                        # marker of the left square
    labels[r][W - 1] = 3                                    # marker of the right square
IN_QUEUE, WSHED = -2, -1
q = deque()
for r in range(H):
    for c in range(W):
        if labels[r][c] > 0:
            continue
        if any(0 <= r + dr < H and 0 <= c + dc < W and labels[r + dr][c + dc] > 0
               for dr, dc in ((0, -1), (0, 1), (-1, 0), (1, 0))):
            q.append((r, c))
            labels[r][c] = IN_QUEUE
while q:                                                    # constant image: FIFO order
    r, c = q.popleft()
    lab = 0
    for dr, dc in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < H and 0 <= cc < W and labels[rr][cc] > 0:
            t = labels[rr][cc]
            if lab == 0:
                lab = t
            elif t != lab:
                lab = WSHED
    labels[r][c] = lab
    if lab == WSHED:
        continue
    for dr, dc in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < H and 0 <= cc < W and labels[rr][cc] == 0:
            labels[rr][cc] = IN_QUEUE
            q.append((rr, cc))
dam = {(r, c) for r in range(H) for c in range(W) if labels[r][c] == WSHED}
assert len(dam) == 20 and len({c for _, c in dam}) == 1     # one full column of -1
gt_left = {(r, c) for r in range(H) for c in range(20)}
gt_right = {(r, c) for r in range(H) for c in range(20, 40)}
gt_fg = gt_left | gt_right
pred_fg = {(r, c) for r in range(H) for c in range(W) if labels[r][c] > 1}
assert len(pred_fg) == 780 and abs(iou(pred_fg, gt_fg) - 0.975) < 1e-12
p2 = {(r, c) for r in range(H) for c in range(W) if labels[r][c] == 2}
p3 = {(r, c) for r in range(H) for c in range(W) if labels[r][c] == 3}
ious = sorted([max(iou(p2, gt_left), iou(p2, gt_right)), max(iou(p3, gt_left), iou(p3, gt_right))])
assert abs(ious[0] - 0.95) < 1e-12 and ious[1] == 1.0       # both instances matched
checks += 1
# The merge: a single label and no dam; foreground IoU 1, no instance above 0.5.
assert iou(gt_fg, gt_fg) == 1.0 and iou(gt_fg, gt_left) == 0.5
checks += 1

print(f"91-otsu-distance-watershed (CV-WATERSHED-005): {checks} checks passed")
