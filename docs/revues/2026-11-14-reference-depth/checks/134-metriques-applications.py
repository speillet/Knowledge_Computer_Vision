"""Recompute the constructed examples of CV-METRIQUES-APPLIQUEES (reference 134-metriques-applications).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/134-metriques-applications.py
PRO follows MVTec AD 2 (arXiv 2503.21622v1, Sec. IV-B1, eq. 1); the HD95 conventions
mirror MONAI 1.6.1 (max of the two directed percentiles, torch.quantile linear
interpolation) versus a pooled percentile; the cost threshold is derived from a 2x2
cost matrix (Elkan 2001, Sec. 1.3). All data are constructed.
"""

import math


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


checks = 0

# --- Example A: aggregation level of Dice ------------------------------------------


def dice(inter, n_ref, n_pred):
    return 2 * inter / (n_ref + n_pred)


d1 = dice(9500, 10000, 10000)    # large structure, 95 % overlap
d2 = dice(0, 100, 0)             # small structure entirely missed
# Check 1: per-image Dice 0.95 and 0, per-image mean 0.475.
assert close(d1, 0.95) and close(d2, 0.0) and close((d1 + d2) / 2, 0.475)
checks += 1
# Check 2: pooling all pixels first gives 2*9500/20100 = 0.9453, hiding the missed structure.
assert close(dice(9500, 10100, 10000), 0.94527)
checks += 1
# Check 3: Dice = 2 IoU / (1 + IoU) for one pair (IoU = 9500 / 10500).
iou = 9500 / (10000 + 10000 - 9500)
assert close(d1, 2 * iou / (1 + iou), 1e-12)
checks += 1
# Check 4: 99 empty/empty cases scored 1 and one missed object scored 0 give a mean of 0.99 (card 004).
assert close((99 * 1 + 0) / 100, 0.99)
checks += 1

# --- Example B: region weighting in inspection ---------------------------------------
regions = [(10000, 9000), (10, 0)]   # (defect pixels, detected pixels)
tpr = sum(d for _, d in regions) / sum(n for n, _ in regions)
pro = sum(d / n for n, d in regions) / len(regions)
# Check 5: pixel TPR 0.899 but PRO 0.45: the missed 10-pixel defect weighs one region out of two.
assert close(tpr, 0.89910) and close(pro, 0.45)
checks += 1
# Check 6: at FPR 0.05 on a 5-megapixel image, 250,000 false-positive pixels are 25,000 times a 10-pixel defect.
assert 5_000_000 * 0.05 == 250_000 and 250_000 / 10 == 25_000
checks += 1

# --- Example C: two HD95 conventions on the same boundaries --------------------------


def quantile_linear(values, q):
    """Linear interpolation between order statistics (torch.quantile / numpy default)."""
    s = sorted(values)
    pos = (len(s) - 1) * q
    lo = math.floor(pos)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


d_pred_to_ref = [0.0] * 94 + [10.0] * 6     # a thin protrusion: 6 of 100 predicted boundary points 10 px away
d_ref_to_pred = [0.0] * 100
max_of_directed = max(quantile_linear(d_pred_to_ref, 0.95), quantile_linear(d_ref_to_pred, 0.95))
pooled = quantile_linear(d_pred_to_ref + d_ref_to_pred, 0.95)
# Check 7: max of the directed 95th percentiles gives 10 px; the percentile of the pooled distances gives 0 px.
assert close(max_of_directed, 10.0) and close(pooled, 0.0)
checks += 1
# Check 8: with 0.5 mm pixels the first convention reports 5 mm; the plain Hausdorff distance is also 10 px.
assert close(max_of_directed * 0.5, 5.0) and max(d_pred_to_ref + d_ref_to_pred) == 10.0
checks += 1

# --- Example D: decision threshold from costs -----------------------------------------
c_fp, c_fn = 1.0, 50.0                  # cost of a false reject, cost of a shipped defect; correct decisions cost 0
p_star = c_fp / (c_fp + c_fn)
# Check 9: reject when the calibrated defect probability exceeds 1/51 = 0.0196.
assert close(p_star, 0.019608)
checks += 1
# Check 10: at p = p_star the expected costs of accepting (p * c_fn) and rejecting ((1 - p) * c_fp) are equal.
assert close(p_star * c_fn, (1 - p_star) * c_fp, 1e-12)
checks += 1

# --- Example E: length uncertainty from scale and pixel terms -------------------------
s, sigma_s = 0.05, 0.0002     # mm per pixel and its standard uncertainty (0.4 %)
p_len, sigma_p = 200.0, 0.3   # measured length in pixels and its repeatability
L = s * p_len
var_scale, var_pix = (p_len * sigma_s) ** 2, (s * sigma_p) ** 2
sigma_L = math.sqrt(var_scale + var_pix)
# Check 11: L = 10 mm, sigma_L = 0.0427 mm, and the scale term carries 88 % of the variance.
assert close(L, 10.0) and close(sigma_L, 0.04272) and close(var_scale / (var_scale + var_pix), 0.8767)
checks += 1
print(f"134-metriques-applications: {checks} checks passed")
