"""Recompute the constructed example of CV-MATCHING-005 (reference 43-detecteurs-matchers)
and the nominal confidences added to the reference's worked example C.

Stdlib only. Run with: python3 -I docs/revues/2026-11-15-accepted-proposals/checks/43-detecteurs-matchers.py
Conventions checked against OpenCV 4.13.0:
- findHomography defaults: method=0, ransacReprojThreshold=3, maxIters=2000,
  confidence=0.995 (calib3d/include/opencv2/calib3d.hpp L841-L844); minimal samples of
  four pairs (fundam.cpp L407).
- RANSACUpdateNumIters (calib3d/src/ptsetreg.cpp L55-L75): ep is the outlier ratio,
  the required count is round(log(1-p)/log(1-(1-ep)^s)), and the function returns
  maxIters when that count would exceed it (L74). The loop starts at niters=maxIters
  (L166) and only lowers it (L233).
- A hypothesis becomes the best one when its inlier count exceeds max(best, s-1)
  (ptsetreg.cpp L228); inliers have squared transfer error <= threshold^2 (L85-L101).
The 400-pair, 60-inlier scenario is a project construction; no OpenCV call is made here.
"""

import math
import random


def required_ceil(p, w, s=4):
    """Nominal number of samples (ceiling formula used in the vault)."""
    return math.ceil(math.log(1 - p) / math.log(1 - w ** s))


def opencv_update(p, ep, model_points, max_iters):
    """Port of RANSACUpdateNumIters, ptsetreg.cpp L55-L75 (cvRound -> round)."""
    p = min(max(p, 0.0), 1.0)
    ep = min(max(ep, 0.0), 1.0)
    num = max(1.0 - p, 2.2250738585072014e-308)
    denom = 1.0 - (1.0 - ep) ** model_points
    if denom < 2.2250738585072014e-308:
        return 0
    num = math.log(num)
    denom = math.log(denom)
    return max_iters if (denom >= 0 or -num >= max_iters * (-denom)) else round(num / denom)


def solve(a, b):
    """Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        for r in range(n):
            if r != c:
                f = m[r][c] / m[c][c]
                for k in range(c, n + 1):
                    m[r][k] -= f * m[c][k]
    return [m[i][n] / m[i][i] for i in range(n)]


def homography_from_4(src, dst):
    """Exact homography (h33 = 1) through four correspondences."""
    a, b = [], []
    for (x, y), (u, v) in zip(src, dst):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    h = solve(a, b) + [1.0]
    return [h[0:3], h[3:6], h[6:9]]


def transfer_sq(h, p, q):
    x, y = p
    w = h[2][0] * x + h[2][1] * y + h[2][2]
    u = (h[0][0] * x + h[0][1] * y + h[0][2]) / w
    v = (h[1][0] * x + h[1][1] * y + h[1][2]) / w
    return (u - q[0]) ** 2 + (v - q[1]) ** 2


checks = 0
n, n_in, p, cap, s = 400, 60, 0.995, 2000, 4
w = n_in / n

# Check 1: inlier ratio of the scenario and the probability of an all-inlier sample.
assert abs(w - 0.15) < 1e-12 and abs(w ** 4 - 5.0625e-4) < 1e-12; checks += 1

# Check 2: nominal requirement at 0.995 is 10,464 samples, above the default cap.
assert required_ceil(p, w) == 10464 and required_ceil(p, w) > cap; checks += 1

# Check 3: OpenCV's update returns the cap itself in that situation, so the loop
# runs all 2000 iterations; with w = 0.5 it would stop early (82 iterations).
assert opencv_update(p, 1 - w, s, cap) == cap
assert opencv_update(p, 0.5, s, cap) == 82; checks += 1

# Check 4: nominal confidence reached within the cap is 0.637, and the expected
# number of all-inlier samples in the whole budget is about one.
conf = 1 - (1 - w ** 4) ** cap
assert abs(conf - 0.637) < 5e-4 and abs(cap * w ** 4 - 1.0125) < 1e-9; checks += 1

# Check 5: with the defaults the cap binds whenever the inlier ratio is below 0.227.
w_min = (1 - (1 - p) ** (1 / cap)) ** (1 / s)
assert abs(w_min - 0.227) < 5e-4
assert required_ceil(p, 0.226) > cap and required_ceil(p, 0.228) <= cap
assert opencv_update(p, 1 - 0.226, s, cap) == cap and opencv_update(p, 1 - 0.228, s, cap) < cap
checks += 1

# Check 6: a minimal sample is fitted exactly by its own homography, so even pure
# outliers give a hypothesis with at least four inliers at 3 px: the acceptance test
# goodCount > max(best, s - 1) always has a candidate, and a model is returned.
rng = random.Random(7)
for _ in range(50):
    src = [(rng.uniform(0, 640), rng.uniform(0, 480)) for _ in range(4)]
    dst = [(rng.uniform(0, 640), rng.uniform(0, 480)) for _ in range(4)]
    h = homography_from_4(src, dst)
    good = sum(transfer_sq(h, a, b) <= 3.0 ** 2 for a, b in zip(src, dst))
    assert good == 4 and good > max(0, s - 1)
checks += 1

# Check 7: nominal confidences quoted next to the synthetic success counts in the
# reference (worked example C): 0.637, 0.181 and 0.061 at w = 0.15, 0.10 and 0.075.
for w_k, expected in ((0.15, 0.637), (0.10, 0.181), (0.075, 0.061)):
    assert abs(1 - (1 - w_k ** 4) ** cap - expected) < 5e-4
checks += 1

print(f"43-detecteurs-matchers (CV-MATCHING-005): {checks} checks passed")
