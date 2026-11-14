"""Recompute the constructed examples of CV-FAST-BRIEF (reference 47-fast-brief).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/47-fast-brief.py
Sources of the inputs: Rosten and Drummond 2006 (Sec. 2.1 segment test, compass
pixels 1, 5, 9, 13), Calonder et al. 2010 (eq. 1-2, Sec. 3.2 sampling sigma^2 = S^2/25),
opencv 4.13.0 modules/features2d/src/fast.cpp (pretest L212-L231, opposite-pair logic)
and fast_score.cpp (circle offsets L50-L81), opencv_contrib 4.13.0 brief.cpp
(PATCH_SIZE 48, KERNEL_SIZE 9). Scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def arcs(n_circle, length):
    """All sets of `length` contiguous positions on a circle of `n_circle` pixels."""
    return [{(s + k) % n_circle for k in range(length)} for s in range(n_circle)]


# --- Example A: what the fast pretests can and cannot reject ------------------
compass = {0, 4, 8, 12}  # pixels 1, 5, 9, 13 of the paper, 0-based
# Check 1: every 12-arc on the 16-pixel circle contains at least 3 compass pixels,
# which justifies the original FAST-12 pretest ("at least three of these").
assert min(len(a & compass) for a in arcs(16, 12)) == 3
# Check 2: a 9-arc may contain only 2 compass pixels, so that pretest cannot serve FAST-9.
assert min(len(a & compass) for a in arcs(16, 9)) == 2


def opencv_pretest_passes(pattern, arc):
    """OpenCV's shared pretest (fast.cpp L216-L231) for a ring whose `arc` pixels are
    brighter and whose other pixels are similar. Offsets k >= pattern wrap (makeOffsets)."""
    pairs = [(0, 8), (2, 10), (4, 12), (6, 14), (1, 9), (3, 11), (5, 13), (7, 15)]
    return all((a % pattern) in arc or (b % pattern) in arc for a, b in pairs)


# Check 3: for the 16-pixel circle, every 9-arc meets each diametric pair (k, k+8),
# so the pretest never rejects a valid FAST-9 corner.
assert all(opencv_pretest_passes(16, a) for a in arcs(16, 9))
# Check 4: the same pretest applied to the 12-pixel circle accepts a valid 7-arc for
# only 4 of its 12 starting positions (0, 9, 10, 11), as the probe run reproduced.
passing12 = [s for s, a in enumerate(arcs(12, 7)) if opencv_pretest_passes(12, a)]
assert passing12 == [0, 9, 10, 11]
# Check 5: applied to the 8-pixel circle it rejects every valid 5-arc; only a full ring passes.
assert not any(opencv_pretest_passes(8, a) for a in arcs(8, 5))
assert opencv_pretest_passes(8, set(range(8)))

# --- Example B: the arc must wrap around the circle ---------------------------
wrap_arc = {12, 13, 14, 15, 0, 1, 2, 3, 4}


def longest_run(states, wrap):
    seq = states + states if wrap else states
    best = run = 0
    for s in seq:
        run = run + 1 if s else 0
        best = max(best, run)
    return min(best, len(states))


ring = [k in wrap_arc for k in range(16)]
# Check 6: the wrapping 9-arc is found when the ring is scanned circularly ...
assert longest_run(ring, wrap=True) == 9
# Check 7: ... but a linear scan of positions 0..15 only sees runs of 5 and 4.
assert longest_run(ring, wrap=False) == 5
# Check 8: OpenCV extends the ring to N = 16 + 9 = 25 entries for this purpose.
assert 16 + 16 // 2 + 1 == 25

# --- Example C: Hamming distance on the card's toy strings ---------------------
a, b = 0b101101, 0b100001
# Check 9: XOR = 001100, two differing bits.
assert a ^ b == 0b001100 and bin(a ^ b).count("1") == 2
# Check 10: the integer difference (45 - 33 = 12) has no meaning for descriptors.
assert (a, b, a - b) == (45, 33, 12)
# Check 11: a permutation applied to both strings preserves the Hamming distance.
perm = [5, 3, 0, 4, 1, 2]
pa = sum(((a >> i) & 1) << perm[i] for i in range(6))
pb = sum(((b >> i) & 1) << perm[i] for i in range(6))
assert bin(pa ^ pb).count("1") == 2 and pa - pb != a - b

# --- Example D: an independence model for 256-bit distances --------------------
nd = 256
# Check 12: two unrelated strings with independent fair bits: mean 128, sd 8.
assert nd * 0.5 == 128 and close(math.sqrt(nd * 0.25), 8.0)


def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


# Check 13: under that model, a distance <= 64 happens with probability ~2.4e-16 ...
p_random_64 = binom_cdf(64, nd, 0.5)
assert 2e-16 < p_random_64 < 3e-16
# Check 14: ... while a true match whose bits flip with probability 0.1 has mean 25.6,
# sd 4.8, and stays <= 64 with probability above 0.999999.
assert close(nd * 0.1, 25.6) and close(math.sqrt(nd * 0.1 * 0.9), 4.8)
assert binom_cdf(64, nd, 0.1) > 0.999999

# --- Example E: displacement of a BRIEF sample under in-plane rotation ---------
S = 48                      # OpenCV patch size (brief.cpp PATCH_SIZE)
sigma = S / 5               # Calonder et al. G II: sigma^2 = S^2 / 25
mean_radius = sigma * math.sqrt(math.pi / 2)   # mean of a 2-D isotropic Gaussian radius


def shift(r, deg):
    return 2 * r * math.sin(math.radians(deg) / 2)


# Check 15: sigma = 9.6 px and a sample lies on average 12.0 px from the keypoint.
assert close(sigma, 9.6) and close(mean_radius, 12.03, 1e-2)
# Check 16: at that radius a rotation moves the sample by 2.1 px (10 deg), 3.1 px (15 deg)
# and 6.2 px (30 deg), against a 4 px half-width of OpenCV's 9x9 smoothing box.
assert close(shift(mean_radius, 10), 2.10, 1e-2)
assert close(shift(mean_radius, 15), 3.14, 1e-2)
assert close(shift(mean_radius, 30), 6.23, 1e-2)
# Check 17: at the patch border (r = 24 px) the shifts are 4.2 px and 6.3 px for 10 and 15 deg.
assert close(shift(24, 10), 4.18, 1e-2) and close(shift(24, 15), 6.27, 1e-2)

# --- Example F: RANSAC sample budget of the 2026-11-08 appendix ----------------
def ransac_n(w, s=4, p=0.99):
    return math.ceil(math.log(1 - p) / math.log(1 - w ** s))


# Check 18: homography (s = 4), p = 0.99: 72 samples at w = 0.5 and 1177 at w = 0.25.
assert ransac_n(0.5) == 72 and ransac_n(0.25) == 1177

# --- Example G: storage and OpenCL keypoint cap --------------------------------
# Check 19: 10^6 descriptors take 32 MB as BRIEF-32 against 256 MB as SURF-64 floats.
assert 10 ** 6 * 32 == 32_000_000 and 10 ** 6 * 64 * 4 == 256_000_000
# Check 20: the UMat path keeps at most max(H*W/100, 1000) keypoints (fast.cpp L444):
# 3,072 at 640x480 and 20,736 at 1920x1080.
assert max(640 * 480 // 100, 1000) == 3072 and max(1920 * 1080 // 100, 1000) == 20736

# --- Straight step edges on the 16-pixel circle --------------------------------
circle16 = [(0, 3), (1, 3), (2, 2), (3, 1), (3, 0), (3, -1), (2, -2), (1, -3),
            (0, -3), (-1, -3), (-2, -2), (-3, -1), (-3, 0), (-3, 1), (-2, 2), (-1, 3)]
best = 0
for k in range(3600):
    phi = math.radians(k / 10)
    nx, ny = math.cos(phi), math.sin(phi)
    for c in (1e-6, 0.5):  # edge line at distance c from the centre, centre on the dark side
        best = max(best, longest_run([nx * x + ny * y > c for x, y in circle16], wrap=True))
# Check 21: a straight step edge never leaves more than 8 contiguous brighter circle pixels,
# so FAST-9 rejects it while n <= 8 can fire on it.
assert best == 8

print("47-fast-brief: 21 checks passed")
