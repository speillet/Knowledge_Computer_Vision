"""Recompute the constructed numbers added to CV-MEANSHIFT-004 and reference
115-meanshift-camshift (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/115-meanshift-camshift.py
CamShift box: length and width 4 sqrt(lambda) from the second moments of the weights in the
window enlarged by 10 px per side (OpenCV 4.13.0 camshift.cpp L115-L173). The blob and the
factorial results are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


def camshift_box(w, h):
    """Box of a uniformly weighted w x h blob on the pixel grid, axis-aligned (theta = 0)."""
    def var(n):
        xs = range(n)
        m = sum(xs) / n
        return sum((x - m) ** 2 for x in xs) / n
    return 4 * math.sqrt(var(w)), 4 * math.sqrt(var(h))


L, W = camshift_box(40, 20)
assert close(L, 4 * math.sqrt((40 ** 2 - 1) / 12)) and round(L, 1) == 46.2 and round(W, 1) == 23.1
checks += 1

# Tracked perfectly and centred, the box contains the tight annotation: IoU = area ratio.
iou = (40 * 20) / (L * W)
assert round(iou, 3) == 0.751 and close(12 / 16, 0.75)       # continuous limit (sqrt(12)/4)^2
assert round(4 / math.sqrt(12), 3) == 1.155
checks += 1
# A fixed MeanShift window of the initial 40 x 20 size, centred on an unchanged target, has IoU 1.
# On a sequence without scale change the adaptive arm therefore loses about 0.25 IoU by convention.
assert close(1 - iou, 0.249, 1e-3)
checks += 1

# 2 x 2 factorial, constructed mean IoU on the scale-change sequence.
cell = {("H1", "fixed"): 0.48, ("H1", "adaptive"): 0.60, ("H2", "fixed"): 0.56, ("H2", "adaptive"): 0.62}
adapt_h1 = cell[("H1", "adaptive")] - cell[("H1", "fixed")]
adapt_h2 = cell[("H2", "adaptive")] - cell[("H2", "fixed")]
hist_fixed = cell[("H2", "fixed")] - cell[("H1", "fixed")]
hist_adapt = cell[("H2", "adaptive")] - cell[("H1", "adaptive")]
one_shot = cell[("H2", "adaptive")] - cell[("H1", "fixed")]
assert close(one_shot, 0.14) and close(adapt_h1, 0.12) and close(adapt_h2, 0.06)
assert close((adapt_h1 + adapt_h2) / 2, 0.09) and close((hist_fixed + hist_adapt) / 2, 0.05)
assert close(adapt_h2 - adapt_h1, -0.06) and close(hist_adapt - hist_fixed, -0.06)   # interaction
assert close(one_shot, adapt_h1 + hist_adapt) and close(one_shot, hist_fixed + adapt_h2)
checks += 1

print(f"115-meanshift-camshift (CV-MEANSHIFT-004): {checks} checks passed")
