"""Recompute the constructed numbers added to CV-SEGMENTATION-002 (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/93-semantique-instances-panoptique.py
U-Net separation weight w0 * exp(-(d1 + d2)^2 / (2 sigma^2)), w0 = 10, sigma = 5 px:
Ronneberger et al. 2015, Sec. 3, eq. 2.
"""
import math
from collections import deque

checks = 0


def components(pixels, conn):
    steps = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if conn == 8:
        steps += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    seen, n = set(), 0
    for p in pixels:
        if p in seen:
            continue
        n += 1
        seen.add(p)
        q = deque([p])
        while q:
            r, c = q.popleft()
            for dr, dc in steps:
                nb = (r + dr, c + dc)
                if nb in pixels and nb not in seen:
                    seen.add(nb)
                    q.append(nb)
    return n


# Worked example D: two 50 x 50 parts touching along 50 px.
both = {(r, c) for r in range(50) for c in range(100)}
gt = {(r, c) for (r, c) in both if c != 50}          # one-pixel separating line carved
assert len(both) == 5000 and len(gt) == 4950
assert components(gt, 4) == 2 and components(gt, 8) == 2
pred = both                                           # prediction fills the line
assert components(pred, 4) == 1
iou = len(gt & pred) / len(gt | pred)
assert abs(iou - 0.99) < 1e-12
checks += 1

# Ground-truth check: corner contact gives 2 components (4-conn) or 1 (8-conn).
corner = {(0, 0), (1, 1)}
assert components(corner, 4) == 2 and components(corner, 8) == 1
checks += 1

# U-Net separation weight.
w0, sigma = 10.0, 5.0
w = lambda d: w0 * math.exp(-d ** 2 / (2 * sigma ** 2))
assert abs(w(2) - 9.23) < 0.005 and abs(w(2) - 10 * math.exp(-0.08)) < 1e-12
assert abs(w(20) - 0.00335) < 0.00001 and abs(w(20) - 10 * math.exp(-8)) < 1e-12
checks += 1

print(f"93-semantique-instances-panoptique (CV-SEGMENTATION-002): {checks} checks passed")
