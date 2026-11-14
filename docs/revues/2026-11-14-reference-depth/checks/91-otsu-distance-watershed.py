"""Recompute the constructed examples of CV-WATERSHED (reference 91-otsu-distance-watershed).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/91-otsu-distance-watershed.py
Formulas come from Otsu 1979 (eqs. 2-18), the OpenCV 4.13.0 distanceTransform
documentation (chamfer weights) and the OpenCV watershed tutorial (0.7 * max rule).
The histograms, disks and matchings are constructed scenarios, not measured data.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def otsu(hist):
    """Return (k*, sigma_B^2(k*), sigma_T^2, {k: sigma_B^2(k)}) with class C0 = levels <= k."""
    n = sum(hist)
    p = [h / n for h in hist]
    mu_t = sum(i * pi for i, pi in enumerate(p))
    var_t = sum((i - mu_t) ** 2 * pi for i, pi in enumerate(p))
    w = mu = 0.0
    best_k, best = None, -1.0
    table = {}
    for k, pk in enumerate(p):
        w += pk
        mu += k * pk
        if w <= 1e-12 or w >= 1 - 1e-12:
            continue
        sb = (mu_t * w - mu) ** 2 / (w * (1 - w))      # Otsu eq. 18
        table[k] = sb
        if sb > best:                                   # strict '>' keeps the first maximum, as OpenCV does
            best_k, best = k, sb
    return best_k, best, var_t, table


def band_with_defect(n_defect):
    """Background: 100 px at each level 100..140; defect: n_defect px at level 40."""
    h = [0] * 256
    for v in range(100, 141):
        h[v] = 100
    h[40] = n_defect
    return h


# --- Example A: Otsu with a small dark defect ---------------------------------
# Check 1: decomposition sigma_T^2 = sigma_W^2 + sigma_B^2 (Otsu eq. 16) at an arbitrary threshold.
h = band_with_defect(50)
k_test = 118
n = sum(h)
p = [x / n for x in h]
w0 = sum(p[: k_test + 1]); w1 = 1 - w0
m0 = sum(i * p[i] for i in range(k_test + 1)) / w0
m1 = sum(i * p[i] for i in range(k_test + 1, 256)) / w1
v0 = sum((i - m0) ** 2 * p[i] for i in range(k_test + 1)) / w0
v1 = sum((i - m1) ** 2 * p[i] for i in range(k_test + 1, 256)) / w1
_, _, var_t, table = otsu(h)
assert close(w0 * v0 + w1 * v1 + w0 * w1 * (m0 - m1) ** 2, var_t, 1e-9)
# Check 2: eq. 18 equals the explicit form w0*w1*(mu0-mu1)^2 (eq. 14 after eq. 9).
assert close(table[k_test], w0 * w1 * (m0 - m1) ** 2, 1e-9)

k50, sb50, vt50, t50 = otsu(band_with_defect(50))
# Check 3: with 50 defect pixels (1.2 % of the image) Otsu cuts the background band at 118.
assert k50 == 118 and close(50 / sum(band_with_defect(50)), 0.0120, 1e-4)
# (the band alone: 4,100 px, mean 120, standard deviation sqrt((41^2 - 1) / 12) = 11.8 levels)
band = band_with_defect(0)
assert sum(band) == 4100 and close(math.sqrt((41 ** 2 - 1) / 12), 11.83, 0.01)
assert close(sum(i * x for i, x in enumerate(band)) / 4100, 120.0, 1e-12)
# Check 4: isolating the defect (k = 40) scores 76.2 against 123.5 for the band split.
assert close(t50[40], 76.18, 0.01) and close(sb50, 123.53, 0.01)
# Check 5: the separability eta* = sigma_B^2 / sigma_T^2 (Otsu eq. 12) is 0.576 in this failing case.
assert close(sb50 / vt50, 0.576, 1e-3)

k100, sb100, vt100, t100 = otsu(band_with_defect(100))
# Check 6: with 100 defect pixels (2.4 %) the threshold isolates the defect (k* = 40, eta* = 0.521).
assert k100 == 40 and close(sb100, 148.75, 0.01) and close(sb100 / vt100, 0.521, 1e-3)
# Check 7: the switch happens at 96 defect pixels (2.29 % of the image), not earlier.
first = next(nd for nd in range(1, 500) if otsu(band_with_defect(nd))[0] == 40)
assert first == 96 and close(96 / sum(band_with_defect(96)), 0.0229, 1e-4)
# Check 8: halving a uniform band of width W scores W^2/16, i.e. 3/4 of its variance W^2/12 (continuous limit);
# for a Gaussian mode split at its mean the score is (2/pi) sigma^2 ~ 0.64 sigma^2.
W = 41.0
assert close((W ** 2 / 16) / (W ** 2 / 12), 0.75, 1e-12) and close(2 / math.pi, 0.6366, 1e-4)

# --- Example B: distance-transform markers for two disks ----------------------
def saddle(R, d):
    """Distance at the midpoint of two equal disks of radius R with centre distance d < 2R."""
    return math.sqrt(R * R - d * d / 4)


def separated(R, d, alpha):
    """sure_fg = D > alpha * max D has two components iff the saddle value is <= alpha * R."""
    return saddle(R, d) <= alpha * R


# Check 9: with alpha = 0.7, equal disks separate iff d >= 2R*sqrt(1 - 0.49) = 1.428 R.
assert close(2 * math.sqrt(1 - 0.7 ** 2), 1.4283, 1e-4)
# Check 10: R = 20 px: d = 30 px gives saddle 13.23 <= 14 (two markers); d = 26 px gives 15.20 > 14 (one marker).
assert close(saddle(20, 30), 13.229, 1e-3) and separated(20, 30, 0.7)
assert close(saddle(20, 26), 15.199, 1e-3) and not separated(20, 26, 0.7)
# Check 11: a 10 px disk next to a 15 px disk loses its marker at alpha = 0.7 (10 < 10.5) but keeps it at 0.6 (10 > 9).
assert 10 <= 0.7 * 15 and 10 > 0.6 * 15
# Check 12: lowering alpha to 0.6 requires d >= 1.6 R for equal disks, i.e. 24 px for R = 15 px.
assert close(2 * math.sqrt(1 - 0.6 ** 2) * 15, 24.0, 1e-9)
# Check 13: with alpha = 0.5 the separation bound becomes 2*sqrt(0.75) = 1.732 R, so pairs with
# 1.43 <= d/R < 1.73 are separated at 0.7 but merged at 0.5 (proposed controlled variation).
assert close(2 * math.sqrt(1 - 0.5 ** 2), 1.7321, 1e-4)
assert separated(1.0, 1.5, 0.7) and not separated(1.0, 1.5, 0.5)

# --- Chamfer approximation of the Euclidean distance (OpenCV distanceTransform weights) ---
def chamfer3(dx, dy, a=0.955, b=1.3693):
    big, small = max(abs(dx), abs(dy)), min(abs(dx), abs(dy))
    return a * (big - small) + b * small


def chamfer5(dx, dy, a=1.0, b=1.4, c=2.1969):
    big, small = max(abs(dx), abs(dy)), min(abs(dx), abs(dy))
    if big >= 2 * small:
        return c * small + a * (big - 2 * small)
    return c * (big - small) + b * (2 * small - big)


err3 = [chamfer3(1000, j) / math.hypot(1000, j) - 1 for j in range(1001)]
err5 = [chamfer5(1000, j) / math.hypot(1000, j) - 1 for j in range(1001)]
# Check 14: along straight lines, the 3x3 mask errs between -4.5 % (axes) and +4.1 %.
assert close(min(err3), -0.0450, 1e-4) and close(max(err3), 0.0410, 2e-4)
# Check 15: the 5x5 mask errs between -1.75 % and +1.92 %.
assert close(min(err5), -0.0175, 2e-4) and close(max(err5), 0.0192, 2e-4)

# --- Example C: a merge seen by foreground IoU and by instance matching --------
# Two ground-truth objects A and B, predicted as one region equal to A u B.
def merge_scores(area_a, area_b, thr=0.5):
    union = area_a + area_b
    ious = [area_a / union, area_b / union]
    tp = sum(1 for v in ious if v > thr)          # IoU > 0.5 makes the matching unique
    fp = 1 - min(tp, 1)
    fn = 2 - tp
    f1 = 2 * tp / (2 * tp + fp + fn)
    return ious, tp, fp, fn, f1


ious, tp, fp, fn, f1 = merge_scores(500, 500)
# Check 16: equal objects: IoU 0.5 with each, no match above 0.5 -> TP 0, FP 1, FN 2, F1 0; foreground IoU stays 1.
assert ious == [0.5, 0.5] and (tp, fp, fn) == (0, 1, 2) and f1 == 0
ious, tp, fp, fn, f1 = merge_scores(700, 300)
# Check 17: 70/30 objects: the merged region matches the larger one (IoU 0.7) -> TP 1, FN 1, F1 = 2/3.
assert close(ious[0], 0.7, 1e-12) and (tp, fp, fn) == (1, 0, 1) and close(f1, 2 / 3, 1e-12)

print("91-otsu-distance-watershed: 17 checks passed")
