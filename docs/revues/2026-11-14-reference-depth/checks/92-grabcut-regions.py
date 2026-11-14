"""Recompute the constructed examples of CV-GRABCUT (reference 92-grabcut-regions).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/92-grabcut-regions.py
Formulas come from Rother et al. 2004 (eqs. 4, 5, 9, 11), Boykov and Jolly 2001 (K = 1 + max sum of
n-links) and OpenCV 4.13.0 grabcut.cpp (gamma = 50, lambda = 9 * gamma, gamma / sqrt(2) on diagonals,
beta denominator). The contrast ratios, strand and likelihood ratio are constructed scenarios.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


GAMMA = 50.0                 # Rother et al. Sec. 2.1; grabcut.cpp L582
LAMBDA = 9 * GAMMA           # hard-constraint t-link weight in grabcut.cpp L583


def nlink(rho, diagonal=False):
    """n-link weight for a squared colour difference equal to rho times the image mean (beta = 1 / (2 mean))."""
    w = GAMMA * math.exp(-rho / 2)
    return w / math.sqrt(2) if diagonal else w


# --- Example A: contrast-normalised n-links ------------------------------------
# Check 1: weights for rho = 0, 1, 2, 4 are 50, 30.33, 18.39 and 6.77.
assert [round(nlink(r), 2) for r in (0, 1, 2, 4)] == [50.0, 30.33, 18.39, 6.77]

# Check 2: beta = 1 / (2 <d^2>) makes the weights invariant to a global colour scaling z -> s z.
diffs = [3.0, 10.0, 25.0, 4.0, 60.0]            # constructed neighbour colour differences (levels)
def weights(ds):
    beta = 1 / (2 * sum(d * d for d in ds) / len(ds))
    return [GAMMA * math.exp(-beta * d * d) for d in ds]
assert all(close(a, b, 1e-9) for a, b in zip(weights(diffs), weights([0.5 * d for d in diffs])))

# Check 3: OpenCV averages over 4WH - 3W - 3H + 2 eight-neighbour pairs (calcBeta, L273); enumerate to confirm.
def pairs(w, h):
    count = 0
    for y in range(h):
        for x in range(w):
            count += (x > 0) + (x > 0 and y > 0) + (y > 0) + (y > 0 and x < w - 1)
    return count
for w, h in ((3, 2), (5, 4), (17, 9)):
    assert pairs(w, h) == 4 * w * h - 3 * w - 3 * h + 2
# Check 4: the graph stores each pair as two directed edges (edgeCount, L468).
assert 2 * pairs(5, 4) == 2 * (4 * 5 * 4 - 3 * (5 + 4) + 2)

# --- Example B: are OpenCV's hard constraints hard? -----------------------------
max_nlinks = 4 * GAMMA + 4 * GAMMA / math.sqrt(2)  # 4 axial + 4 diagonal neighbours at zero contrast
# Check 5: the largest possible n-link sum of one pixel is 341.42, below lambda = 450.
assert close(max_nlinks, 341.421, 1e-3) and LAMBDA == 450 and LAMBDA > max_nlinks
# Check 6: Boykov and Jolly's K = 1 + max sum would be 342.42; 450 exceeds it.
assert close(1 + max_nlinks, 342.421, 1e-3) and LAMBDA > 1 + max_nlinks

# --- Example C: boundary cost against data gain (shrinking bias) ----------------
def boundary_cost_per_px(rho):
    """Cut cost per pixel of a straight axis-aligned boundary: 1 axial + 2 diagonal links."""
    return nlink(rho) + 2 * nlink(rho, diagonal=True)


# Check 7: per-pixel boundary cost is (1 + sqrt 2) * gamma = 120.7 at zero contrast and 16.3 at rho = 4.
assert close(boundary_cost_per_px(0), (1 + math.sqrt(2)) * GAMMA, 1e-9)
assert close(boundary_cost_per_px(0), 120.71, 0.01) and close(boundary_cost_per_px(4), 16.34, 0.01)
# Check 8: a 1-px strand cuts links on both sides: 2 axial + 4 diagonal = 2 (1 + sqrt 2) gamma = 241.4 per pixel.
assert close(2 * GAMMA + 4 * GAMMA / math.sqrt(2), 2 * boundary_cost_per_px(0), 1e-9)
assert close(2 * boundary_cost_per_px(0), 241.42, 0.01)

# Check 9: log-likelihood ratio at the foreground mean for two unit-variance 1-D Gaussians 4 sigma apart is 8 nats.
d = 4.0
llr = -0.5 * 0.0 ** 2 + 0.5 * d ** 2
assert llr == 8.0
# Check 10: a 1-px strand with this gain survives only if 2 c(rho) < 8, i.e. rho > 6.82.
rho_min = 2 * math.log(2 * (1 + math.sqrt(2)) * GAMMA / llr)
assert close(rho_min, 6.82, 0.01)
assert 2 * boundary_cost_per_px(rho_min + 0.01) < llr < 2 * boundary_cost_per_px(rho_min - 0.01)

# --- GMM bookkeeping in OpenCV --------------------------------------------------
# Check 11: each model stores 5 components x (1 weight + 3 mean + 9 covariance) = 65 doubles (L63, L92, tutorial (1,65)).
assert 5 * (1 + 3 + 9) == 65

print("92-grabcut-regions: 11 checks passed")
