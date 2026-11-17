"""Recompute the constructed numbers added to CV-QUANT-005 (reference
142-quantification-runtimes, worked example G and paired decisions, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/142-quantification-runtimes.py
Factor 4 for 8-bit weights: Krishnamoorthi 2018, abstract item 2. The 200 MB workspace and
the 200-defect comparison are project constructions; MB = 10^6 bytes.
"""
from math import comb

checks = 0
MB = 1e6

w_fp32 = 25e6 * 4 / MB
w_int8 = 25e6 * 1 / MB
assert w_fp32 == 100 and w_int8 == 25 and w_fp32 / w_int8 == 4
act_fp32 = 64 * 320 * 320 * 4 / MB
act_int8 = 64 * 320 * 320 * 1 / MB
assert abs(act_fp32 - 26.2) < 0.05 and abs(act_int8 - 6.6) < 0.05
checks += 1

work = 200.0
peak_fp32 = w_fp32 + 2 * act_fp32 + work
peak_w8 = w_int8 + 2 * act_fp32 + work
peak_all8 = w_int8 + 2 * act_int8 + work
assert round(peak_fp32) == 352 and round(peak_w8) == 277 and round(peak_all8) == 238
assert round(100 * (1 - peak_w8 / peak_fp32)) == 21 and round(100 * (1 - w_int8 / w_fp32)) == 75
assert round(100 * work / peak_all8) == 84
checks += 1

# Paired comparison: 200 defects, float finds 190, INT8 186; discordant 6 (INT8 only
# misses) and 2 (float only misses). Both found: 184; both missed: 4.
both_found, int8_only_miss, float_only_miss, both_missed = 184, 6, 2, 8
both_missed = 200 - both_found - int8_only_miss - float_only_miss
assert both_missed == 8
assert both_found + float_only_miss == 186           # INT8 finds
assert both_found + int8_only_miss == 190            # float finds
n = int8_only_miss + float_only_miss
tail = sum(comb(n, k) for k in range(int8_only_miss, n + 1)) / 2 ** n
assert sum(comb(n, k) for k in range(6, 9)) == 37
p_two_sided = min(1.0, 2 * tail)
assert abs(p_two_sided - 0.289) < 0.001
checks += 1

print(f"142-quantification-runtimes (CV-QUANT-005): {checks} checks passed")
