"""Recompute the constructed numbers added to CV-FIABILITE-002 and -005 and the corrected
temperature-scaling statement of reference 133-donnees-generalisation (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/133-donnees-generalisation.py
ECE: Guo et al. 2017, Sec. 2, eq. 3; temperature scaling: Sec. 4.2, eq. 9 (argmax unchanged).
Coverage and selective risk: Geifman and El-Yaniv 2017, Sec. 2, eq. 1. All data are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


def ece(conf, correct, bins):
    n, total = len(conf), 0.0
    for m in range(1, bins + 1):
        lo, hi = (m - 1) / bins, m / bins
        idx = [i for i, c in enumerate(conf) if lo < c <= hi]
        if idx:
            acc = sum(correct[i] for i in idx) / len(idx)
            cf = sum(conf[i] for i in idx) / len(idx)
            total += len(idx) / n * abs(acc - cf)
    return total


# --- CV-FIABILITE-002: worked example B of the reference --------------------------------------
conf = [0.95] * 40 + [0.55] * 40
correct = ([1] * 30 + [0] * 10) * 2                   # each group 75 % correct
assert close(ece(conf, correct, 1), 0.0) and close(ece(conf, correct, 2), 0.0)
assert close(ece(conf, correct, 5), 0.20) and close(ece(conf, correct, 15), 0.20)
checks += 1
scores = [0.8] * 100
iou = [0.8] * 60 + [0.6] * 20 + [0.3] * 20            # 80 reach IoU 0.5, 60 reach IoU 0.75
for thr, gap in ((0.5, 0.0), (0.75, 0.2)):
    freq = sum(v >= thr for v in iou) / len(iou)
    assert close(0.8 - freq, gap)
checks += 1


def softmax(z, t=1.0):
    e = [math.exp(v / t) for v in z]
    return [v / sum(e) for v in e]


assert round(max(softmax([2, 1, 0.1])), 3) == 0.659 and round(max(softmax([2, 1, 0.1], 2)), 3) == 0.502
checks += 1

# Correction of the reference: temperature keeps each sample's argmax (Guo Sec. 4.2) but can
# reorder the top-class probability across samples when there are three or more classes.
a, b = [1.0, 0.0, 0.0], [10.0, 9.4, 0.0]            # top-class margins (1, 1) and (0.6, 10)
pa1, pb1 = max(softmax(a)), max(softmax(b))
pa01, pb01 = max(softmax(a, 0.1)), max(softmax(b, 0.1))
assert round(pa1, 3) == 0.576 and round(pb1, 3) == 0.646 and pb1 > pa1
assert pa01 > pb01 and round(pa01, 4) == 0.9999 and round(pb01, 4) == 0.9975
assert all(max(range(3), key=lambda k: softmax(z, t)[k]) == 0 for z in (a, b) for t in (0.1, 1, 10))
# With a single logit (sigmoid), dividing by T > 0 is monotone, so the ranking is preserved.
logits = [-2.0, -0.3, 0.4, 1.7, 3.1]
for t in (0.1, 0.5, 2.0, 10.0):
    sig = [1 / (1 + math.exp(-z / t)) for z in logits]
    assert sig == sorted(sig)
checks += 1

# --- CV-FIABILITE-005: risk and coverage before and after a sensor change ---------------------
n_old, acc_old, err_old = 1000, 800, 16
n_new, acc_new, err_new = 1000, 850, 85
assert close(acc_old / n_old, 0.80) and close(err_old / acc_old, 0.02)
assert close(acc_new / n_new, 0.85) and close(err_new / acc_new, 0.10)
assert close((err_new / acc_new) / (err_old / acc_old), 5.0)
checks += 1

print(f"133-donnees-generalisation (CV-FIABILITE-002, -005): {checks} checks passed")
