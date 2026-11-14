"""Recompute the constructed examples of CV-ORB (reference 42-orb).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/42-orb.py
Inputs: Rublee et al. 2011 (eqs. 1-3, circular moments, 12-degree steering table,
Sec. 6.1 timings), opencv 4.13.0 modules/features2d/src/orb.cpp (ICAngles L181-L216,
descriptor L220-L350, per-level budget L842-L855, pyramid L1124-L1137, keypoint scaling
L996-L1001), core/base.hpp (NORM_HAMMING2), imgproc resize.cpp (centre-aligned linear
mapping). Scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: intensity-centroid orientation -----------------------------------
R = 15  # half patch size for patchSize = 31


def ic_angle(img):
    """Angle in degrees of (m10, m01) over the disc of radius R, image y downward."""
    m10 = m01 = 0.0
    for v in range(-R, R + 1):
        for u in range(-R, R + 1):
            if u * u + v * v <= R * R:
                val = img(u, v)
                m10 += u * val
                m01 += v * val
    return math.degrees(math.atan2(m01, m10)) % 360, m10, m01


# Check 1: a bright quadrant (x >= 0, y >= 0) gives 45 degrees in the y-down frame.
ang, _, _ = ic_angle(lambda u, v: 200 if (u >= 0 and v >= 0) else 50)
assert close(ang, 45.0, 1e-6)
# Check 2: rotating the pattern by 90 degrees (bright quadrant x <= 0, y >= 0) moves the angle to 135.
ang, _, _ = ic_angle(lambda u, v: 200 if (u <= 0 and v >= 0) else 50)
assert close(ang, 135.0, 1e-6)


def ramp(a, d):
    return lambda u, v: 100 + a * u / R + d * v / R


# Check 3: a weak ramp (1 level over 15 px) perturbed by 0.5 level along y turns by 26.6 deg;
# a strong ramp (50 levels) perturbed the same way turns by 0.57 deg: |C| controls stability.
assert close(ic_angle(ramp(1, 0.5))[0], math.degrees(math.atan(0.5)), 1e-6)
assert close(math.degrees(math.atan(0.5)), 26.57, 1e-2) and close(math.degrees(math.atan(0.5 / 50)), 0.573, 1e-3)
assert close(ic_angle(ramp(50, 0.5))[0], 0.573, 1e-3)

# --- Example B: orientation error and sampling -----------------------------------
# Check 4: a 5 deg error moves a test point at r = 15 px by about r * dtheta = 1.31 px
# (2026-11-08 appendix); the paper's 12 deg steering table has a worst case of 6 deg (1.57 px).
assert close(15 * math.radians(5), 1.309, 1e-3) and close(15 * math.radians(6), 1.571, 1e-3)
# Check 5: OpenCV rounds rotated sample positions to the nearest pixel: at most 0.71 px of rounding.
assert close(math.hypot(0.5, 0.5), 0.7071, 1e-4)

# --- Example C: feature budget across pyramid levels -------------------------------
nfeat, s, nlev = 500, 1.2, 8
f = 1 / s
per = nfeat * (1 - f) / (1 - f ** nlev)
levels, total = [], 0
for lvl in range(nlev - 1):
    n = round(per)
    levels.append(n)
    total += n
    per *= f
levels.append(max(nfeat - total, 0))
# Check 6: OpenCV's geometric split of 500 features over 8 levels at scale factor 1.2.
assert levels == [109, 90, 75, 63, 52, 44, 36, 31] and sum(levels) == 500
# Check 7: the 8 levels span a factor 1.2^7 = 3.58; a 640x480 image shrinks to about 179x134.
assert close(s ** 7, 3.583, 1e-3) and round(640 / s ** 7) == 179 and round(480 / s ** 7) == 134
# Check 8: the paper's five scales with factor sqrt(2) span a factor 4.
assert close(math.sqrt(2) ** 4, 4.0)

# --- Example D: Hamming and Hamming2 ----------------------------------------------
def hamming(a, b):
    return bin(a ^ b).count("1")


def hamming2(a, b):
    """Count 2-bit groups that differ (core/base.hpp NORM_HAMMING2 definition)."""
    x = a ^ b
    mask = int("55" * 32, 16)  # even bit of every 2-bit group over 256 bits
    return bin((x | (x >> 1)) & mask).count("1")


# Check 9: bytes 0 vs 128: one test differs but the numeric gap is 128; 0 vs 3: two tests,
# numeric gap 3. The numeric ranking reverses the Hamming ranking.
assert (hamming(0, 128), 128 - 0) == (1, 128) and (hamming(0, 3), 3 - 0) == (2, 3)
# Check 10: with WTA_K = 4, symbols 00 and 11 are one disagreement for NORM_HAMMING2,
# two for NORM_HAMMING.
assert hamming2(0b00, 0b11) == 1 and hamming(0b00, 0b11) == 2 and hamming2(0b00, 0b01) == 1
# Check 11: a 32-byte descriptor holds 256 tests (WTA_K = 2) or 128 symbols (WTA_K = 3, 4).
assert 32 * 8 == 256 and 32 * 8 // 2 == 128
full = int("ff" * 32, 16)
assert hamming(0, full) == 256 and hamming2(0, full) == 128

# --- Example E: ratio test and cross-check disagree --------------------------------
# Check 12: query A (10, 11) fails a 0.8 ratio (0.909); query B (10, 30) passes (0.333).
assert 10 / 11 > 0.8 and close(10 / 11, 0.9091, 1e-4) and close(10 / 30, 0.3333, 1e-4)
# Check 13: 2,000 descriptors of 32 bytes hold 64,000 bytes of raw descriptor data.
assert 2000 * 32 == 64_000

# --- Example F: coarse-level position bias in OpenCV's pyramid ---------------------
def level_bias(level, scale=1.2):
    """Centre-aligned resize gives x0 = (xl + 0.5) s^l - 0.5; ORB reports xl * s^l."""
    return 0.5 * (scale ** level - 1)


# Check 14: the reported level-0 position lags the centre-aligned one by 0.1 px at level 1,
# 0.54 px at level 4 and 1.29 px at level 7.
assert close(level_bias(1), 0.1) and close(level_bias(4), 0.537, 1e-3) and close(level_bias(7), 1.292, 1e-3)

# --- Example G: published timings ---------------------------------------------------
# Check 15: Rublee et al. Sec. 6.1: pyramid 4.43 + oFAST 8.68 + rBRIEF 2.12 = 15.23 ms
# (reported 15.3 ms per 640x480 frame), against 217.3 ms (SURF) and 5228.7 ms (SIFT).
assert close(4.43 + 8.68 + 2.12, 15.23) and close(217.3 / 15.3, 14.2, 0.1) and close(5228.7 / 15.3, 341.7, 0.1)
# Check 16: on the 1 GHz phone, matching (72.8 ms) costs more than extraction (66.6 ms).
assert 72.8 > 66.6

# Check 17: pyramid pixels: sum of s^(-2l) over 8 levels is 3.10 W H, below the bound
# 1 / (1 - s^-2) = 3.27 W H for s = 1.2.
assert close(sum(1.2 ** (-2 * l) for l in range(8)), 3.10, 0.01) and close(1 / (1 - 1.2 ** -2), 3.273, 1e-3)

print("42-orb: 17 checks passed")
