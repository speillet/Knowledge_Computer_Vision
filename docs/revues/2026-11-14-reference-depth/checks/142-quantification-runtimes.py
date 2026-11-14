"""Recompute the constructed examples of CV-QUANT (reference 142-quantification-runtimes).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/142-quantification-runtimes.py
Inputs: Nagel et al., arXiv 2106.08295 (eqs. 4-8, rounding error in [-s/2, s/2]);
Jacob et al., arXiv 1712.05877 (eqs. 1-5, M = 2^-n M0 with M0 in [0.5, 1), Table 4.4);
Krishnamoorthi, arXiv 1806.08342 (abstract, factor-4 model size); Micikevicius et al.,
arXiv 2209.05433 (Table 1, E4M3 and E5M2); ONNX Runtime quantization FAQ (reduce_range, 7-bit
weights); the PMADDUBSW definition (pairs of u8 x s8 products summed into a saturated int16).
All scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def round_half_even(x):
    return round(x)  # Python's round() rounds ties to even, as ONNX QuantizeLinear and TensorRT do


def quant_affine(x, s, z, qmin, qmax):
    """Nagel eq. 7 with clamp before dequantization: s * (clamp(round(x/s) + z) - z)."""
    q = max(qmin, min(qmax, round_half_even(x / s) + z))
    return s * (q - z)


checks = 0

# --- Example A: range against resolution (uint8, alpha = 0) --------------------------
s_wide = 60 / 255   # min-max range [0, 60] because of rare outliers
s_clip = 6 / 255    # range clipped at 6
# Check 1: the step is 0.235 with min-max and 0.0235 when clipping at 6; the maximal rounding
# error inside the range is s/2 (0.118 against 0.0118).
assert close(s_wide, 0.2353, 1e-4) and close(s_wide / 2, 0.1176, 1e-4)
assert close(s_clip, 0.02353, 1e-5) and close(s_clip / 2, 0.01176, 1e-5)
checks += 1
# Check 2: for errors uniform on [-s/2, s/2] the RMS error is s/sqrt(12): 0.068 against 0.0068.
n = 100000
mean_sq = sum(((i + 0.5) / n - 0.5) ** 2 for i in range(n)) / n  # uniform on [-1/2, 1/2], s = 1
assert close(mean_sq, 1 / 12, 1e-6)
assert close(s_wide / math.sqrt(12), 0.0679, 1e-4) and close(s_clip / math.sqrt(12), 0.00679, 1e-5)
checks += 1
# Check 3: the worst rounding error of 0.118 is 23.5% of a typical value of 0.5; clipping at 6
# turns an outlier of 60 into 6 (error 54).
assert close((s_wide / 2) / 0.5, 0.235, 1e-3)
assert close(quant_affine(60, s_clip, 0, 0, 255), 6.0, 1e-9) and close(60 - 6, 54)
checks += 1

# --- Example B: per-tensor against per-channel weights -------------------------------
s_tensor = 2.0 / 127   # symmetric int8 scale set by the channel with weights in [-2, 2]
codes_small = round_half_even(0.05 / s_tensor)
# Check 4: per-tensor, the channel with weights in [-0.05, 0.05] uses only codes -3..3 (7 levels),
# a step of 31% of its range; per-channel, its own scale is 0.05/127 = 0.000394.
assert codes_small == 3 and 2 * codes_small + 1 == 7
assert close(s_tensor / 0.05, 0.315, 1e-3) and close(0.05 / 127, 0.000394, 1e-6)
checks += 1

# --- Example C: INT8 against FP8 E4M3 on a heavy-tailed tensor ----------------------


def e4m3_round(v):
    """Round |v| to the nearest E4M3 value (bias 7, 3 mantissa bits, max 448), ties to even."""
    a = abs(v)
    if a >= 448:
        return math.copysign(448.0, v)
    if a < 2 ** -6:
        step = 2 ** -9                      # subnormals
    else:
        step = 2 ** (math.floor(math.log2(a)) - 3)
    return math.copysign(round_half_even(a / step) * step, v)


# Check 5: E4M3 maximum normal 1.75 * 2^8 = 448, E5M2 maximum 1.75 * 2^15 = 57344 (Table 1);
# a 3-bit mantissa bounds the relative rounding error of normal numbers by 2^-4 = 6.25%.
assert 1.75 * 2 ** 8 == 448 and 1.75 * 2 ** 15 == 57344
worst = max(abs(e4m3_round(x) - x) / x for x in (1 + k / 997 for k in range(997)))
assert worst <= 2 ** -4 + 1e-12
checks += 1
s_int8 = 6 / 127
s_fp8 = 6 / 448
x_small = 0.01
int8_hat = quant_affine(x_small, s_int8, 0, -128, 127)
fp8_hat = e4m3_round(x_small / s_fp8) * s_fp8
# Check 6: with both formats scaled so that 6 is the largest value, 0.01 becomes 0 in INT8
# (100% error) but 0.75 * (6/448) = 0.010045 in FP8 (0.45% error).
assert int8_hat == 0.0
assert close(x_small / s_fp8, 0.7467, 1e-4) and close(fp8_hat, 0.010045, 1e-6)
assert close(abs(fp8_hat - x_small) / x_small, 0.0045, 1e-4)
checks += 1

# --- Example D: integer-only requantization multiplier ------------------------------
S1, S2, S3 = 0.02, 0.005, 0.1
M = S1 * S2 / S3
nshift = 0
while M * 2 ** (nshift + 1) < 1:
    nshift += 1
M0 = M * 2 ** nshift
# Check 7: M = 0.001 = 2^-9 * 0.512 with M0 in [0.5, 1); as int32 fixed point, round(2^31 * M0)
# is at least 2^30, i.e. at least 30 bits of relative accuracy (Jacob et al. sec. 2.2).
assert close(M, 0.001, 1e-12) and nshift == 9 and close(M0, 0.512, 1e-12) and 0.5 <= M0 < 1
assert round(2 ** 31 * M0) >= 2 ** 30
checks += 1

# --- Example E: 16-bit saturation of paired u8 x s8 products --------------------------
INT16_MAX = 32767
# Check 8: two products 255 * 127 sum to 64770 > 32767 and saturate; with 7-bit weights
# (reduce_range, |w| <= 63) the pair sums to at most 32130 and fits.
assert 2 * 255 * 127 == 64770 > INT16_MAX
assert 2 * 255 * 63 == 32130 <= INT16_MAX
checks += 1

# --- Example F: published speedups depend on core and width (Jacob et al. Table 4.4) ---
# Check 9: MobileNet SSD, depth multiplier 100%: 778 -> 687 ms (1.13x) on LITTLE and 370 -> 272 ms
# (1.36x) on big cores; 50%: 270 -> 146 (1.85x) and 121 -> 61 (1.98x); mAP 22.1 -> 21.7 is a
# relative loss of 1.8%.
assert close(778 / 687, 1.132, 1e-3) and close(370 / 272, 1.360, 1e-3)
assert close(270 / 146, 1.849, 1e-3) and close(121 / 61, 1.984, 1e-3)
assert close((22.1 - 21.7) / 22.1, 0.018, 1e-3)
checks += 1

# --- Example G: memory ---------------------------------------------------------------
params = 25_000_000
# Check 10: 25 M parameters take 100 MB in FP32, 50 MB in FP16, 25 MB in INT8, 12.5 MB in INT4
# (the factor 4 of Krishnamoorthi's abstract for 8-bit weights).
assert (params * 4, params * 2, params * 1, params // 2) == (100_000_000, 50_000_000, 25_000_000, 12_500_000)
checks += 1
fmap = 64 * 320 * 320
# Check 11: one 64x320x320 activation map takes 26.2 MB in FP32, 13.1 MB in FP16, 6.6 MB in INT8;
# weight-only quantization leaves this term unchanged.
assert fmap * 4 == 26_214_400 and fmap * 2 == 13_107_200 and fmap == 6_553_600
checks += 1

# --- Example H: decision sensitivity of a detector -----------------------------------


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


logit_step = 0.05
# Check 12: near a 0.5 threshold the sigmoid slope is 1/4, so a logit step of 0.05 moves the score
# by about 0.0125; scores within about +-0.00625 of the threshold can flip.
assert close(sigmoid(logit_step) - 0.5, 0.0125, 1e-4) and close(sigmoid(logit_step / 2) - 0.5, 0.00625, 1e-5)
checks += 1
s_box = 640 / 255
err = s_box / 2
side = 10.0
inter = (side - err) ** 2
iou = inter / (2 * side * side - inter)
# Check 13: box coordinates in [0, 640] px stored in uint8 have a step of 2.51 px; a 10x10 px box
# whose corners move by the worst-case 1.25 px in x and y keeps IoU 0.62 with the original:
# above 0.5, below 0.75.
assert close(s_box, 2.5098, 1e-4) and close(err, 1.2549, 1e-4)
assert close(iou, 0.619, 1e-3) and 0.5 < iou < 0.75
checks += 1
# Check 14: int8 x int8 products with weights restricted to [-127, 127] stay below 2^14 in absolute
# value (128 * 127 = 16256), the property Jacob et al. use to pair products in int16 (App. B).
assert 128 * 127 == 16256 < 2 ** 14
checks += 1

# Check 15 (2026-11-08 appendix of CV-QUANT-004, re-verified): inference at 20% of a sequential
# pipeline made twice as fast gives 1/(0.8 + 0.1) = 1.11x; adding conversions worth 10% of the old
# total brings the speedup back to 1.0.
assert close(1 / (0.8 + 0.2 / 2), 1.111, 1e-3) and close(1 / (0.8 + 0.2 / 2 + 0.1), 1.0, 1e-12)
checks += 1

print(f"CV-QUANT checks: {checks} groups passed")
