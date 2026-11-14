"""Recompute the constructed examples of CV-MATCHING (reference 43-detecteurs-matchers).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/43-detecteurs-matchers.py
Inputs: Lowe 2004 Sec. 7.1 (ratio test), opencv 4.13.0 calib3d.hpp findHomography
defaults (ransacReprojThreshold 3, maxIters 2000, confidence 0.995), features2d.hpp
BFMatcher crossCheck semantics, Alcantarilla et al. 2013 Sec. 3.3 and Sec. 4 (M-LDB,
486 bits). The distance table and scenes are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: three filters on one constructed distance table ------------------
# Rows: query descriptors A0..A5; columns: train descriptors B0..B5 (distances, any unit).
D = [
    [20, 70, 80, 85, 90, 75],   # A0, true match B0
    [72, 25, 85, 80, 78, 60],   # A1, true match B1
    [80, 82, 30, 33, 88, 79],   # A2, true match B2 (repeated product with A3)
    [84, 79, 28, 31, 86, 80],   # A3, true match B3 (repeated product with A2)
    [90, 77, 87, 83, 35, 74],   # A4, true match B4
    [60, 66, 75, 77, 70, 45],   # A5, occluded in B: no true match (B5 is clutter)
]
truth = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
possible = len(truth)


def nn(i):
    order = sorted(range(6), key=lambda j: D[i][j])
    return order[0], D[i][order[0]], D[i][order[1]]


def best_query(j):
    return min(range(6), key=lambda i: D[i][j])


nn_pairs = {i: nn(i)[0] for i in range(6)}
ratio_pairs = {i: nn(i)[0] for i in range(6) if nn(i)[1] < 0.8 * nn(i)[2]}
mutual_pairs = {i: j for i, j in nn_pairs.items() if best_query(j) == i}
both_pairs = {i: j for i, j in ratio_pairs.items() if best_query(j) == i}


def scores(pairs):
    correct = sum(1 for i, j in pairs.items() if truth.get(i) == j)
    return correct, len(pairs), correct / len(pairs), correct / possible


# Check 1: nearest neighbor alone accepts 6 pairs, 4 correct: precision 0.667, recall 0.8.
assert scores(nn_pairs)[:2] == (4, 6) and close(scores(nn_pairs)[2], 0.667) and close(scores(nn_pairs)[3], 0.8)
# Check 2: the 0.8 ratio test keeps A0, A1, A4, A5: precision 0.75, recall 0.6; it drops both
# repeated products (ratios 0.909 and 0.903) and keeps the occluded A5 (ratio 0.75).
assert sorted(ratio_pairs) == [0, 1, 4, 5] and scores(ratio_pairs)[2:] == (0.75, 0.6)
assert close(30 / 33, 0.909) and close(28 / 31, 0.903) and close(45 / 60, 0.75)
# Check 3: mutual nearest neighbors keep 5 pairs, 3 correct (precision 0.6, recall 0.6);
# the wrong pair A3 -> B2 is mutual, and A5 -> B5 is mutual too.
assert mutual_pairs == {0: 0, 1: 1, 3: 2, 4: 4, 5: 5} and scores(mutual_pairs)[2:] == (0.6, 0.6)
# Check 4: ratio + mutual equals the ratio result here; neither filter rejects A5,
# which only geometric verification can remove.
assert both_pairs == ratio_pairs and 5 in both_pairs

# --- Example B: a periodic scene supports two translations ----------------------
def inliers(n_logos, shift, true_shift=20, period=100, tol=3.0):
    """Logos at x = k * period plus one unique mark; matches = nearest copy under `shift`."""
    observed = [k * period + true_shift for k in range(n_logos)]
    count = 0
    for k in range(n_logos):
        pred = k * period + shift
        if min(abs(pred - o) for o in observed) <= tol:
            count += 1
    mark_ok = abs((150 + shift) - (150 + true_shift)) <= tol
    return count + (1 if mark_ok else 0)


# Check 5: with 4 logos, the true shift (20 px) explains 5 points; the one-period shift
# (120 px) explains 3; the unique mark misses by 100 px under the wrong hypothesis.
assert inliers(4, 20) == 5 and inliers(4, 120) == 3 and abs(120 - 20) == 100
# Check 6: with 20 logos the margin stays 2 inliers (21 vs 19) while the ratio tends to 1.
assert inliers(20, 20) == 21 and inliers(20, 120) == 19 and close(19 / 21, 0.905)

# --- Example C: RANSAC budget under OpenCV's findHomography defaults -------------
def ransac_iters(w, s=4, p=0.995):
    return math.ceil(math.log(1 - p) / math.log(1 - w ** s))


def achieved_confidence(w, iters=2000, s=4):
    return 1 - (1 - w ** s) ** iters


# Check 7: 83 samples at w = 0.5, 1,354 at w = 0.25, 10,464 at w = 0.15 (p = 0.995, s = 4).
assert ransac_iters(0.5) == 83 and ransac_iters(0.25) == 1354 and ransac_iters(0.15) == 10464
# Check 8: capped at maxIters = 2000, w = 0.15 reaches only 0.637 confidence.
assert close(achieved_confidence(0.15), 0.637, 1e-3)

# --- Example D: brute-force cost and storage ---------------------------------------
n = m = 1000
# Check 9: 10^6 pairs cost 128 million multiply-adds for SIFT (128 floats) against
# 4 million 64-bit XOR+popcount operations for 256-bit binary descriptors.
assert n * m * 128 == 128_000_000 and n * m * (256 // 64) == 4_000_000
# Check 10: per descriptor, 512 bytes (128 float32) against 32 bytes (256 bits).
assert 128 * 4 == 512 and 256 // 8 == 32

# --- Example E: AKAZE M-LDB size -------------------------------------------------
# Check 11: 486 bits = 162 comparisons x 3 bits (intensity, d/dx, d/dy), stored in 61 bytes.
assert 486 == 162 * 3 and math.ceil(486 / 8) == 61

print("43-detecteurs-matchers: 11 checks passed")
