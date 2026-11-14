"""Recompute the constructed examples of CV-FIABILITE (reference 133-donnees-generalisation).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/133-donnees-generalisation.py
ECE follows Guo et al. 2017 (Sec. 2, eq. 3, bins ((m-1)/M, m/M]); temperature scaling
follows eq. 9; the detection correctness event follows Kuppers et al. 2020 (eq. 1).
The design effect and the selection-bias integral are project derivations; all data
are constructed.
"""

import math


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


checks = 0

# --- Example A: frames are not independent observations --------------------------
G, m, p = 50, 200, 0.9            # 50 sequences of 200 frames, frame-level accuracy 0.9
n = G * m


def design_effect(m_per_group, rho):
    """Variance inflation of a mean over groups of size m with exchangeable intra-group correlation rho."""
    return 1 + (m_per_group - 1) * rho


se_naive = math.sqrt(p * (1 - p) / n)
# Check 1: treating 10,000 frames as independent gives SE 0.003 and a 95 % half-width of 0.0059.
assert close(se_naive, 0.003) and close(1.96 * se_naive, 0.00588)
checks += 1
deff = design_effect(m, 0.3)
# Check 2: with rho = 0.3 the design effect is 60.7, the effective sample size about 165 frames,
# and the 95 % half-width grows to about 0.046.
assert close(deff, 60.7) and close(n / deff, 164.74, 0.01)
assert close(1.96 * se_naive * math.sqrt(deff), 0.0458, 1e-4)
checks += 1
# Check 3: even a weak correlation rho = 0.05 divides the effective size by about 11 (913 frames).
assert close(design_effect(m, 0.05), 10.95) and close(n / design_effect(m, 0.05), 913.2, 0.1)
checks += 1
# Check 4: the variance formula follows from summing m variances and m(m-1) covariances per group.
var_sum = G * (m * p * (1 - p) + m * (m - 1) * 0.3 * p * (1 - p))
assert close(var_sum / n ** 2, (p * (1 - p) / n) * deff, 1e-12)
checks += 1

# --- Example B: ECE depends on the bins and on the correctness event -------------


def ece(conf, correct, M):
    """Guo et al. eq. 3 with M equal-width bins ((m-1)/M, m/M]."""
    total = 0.0
    nn = len(conf)
    for b in range(1, M + 1):
        lo, hi = (b - 1) / M, b / M
        idx = [i for i, c in enumerate(conf) if lo < c <= hi]
        if not idx:
            continue
        acc = sum(correct[i] for i in idx) / len(idx)
        cf = sum(conf[i] for i in idx) / len(idx)
        total += len(idx) / nn * abs(acc - cf)
    return total


conf = [0.95] * 40 + [0.55] * 40
correct = [1] * 30 + [0] * 10 + [1] * 30 + [0] * 10   # 75 % correct in both groups
# Check 5: overconfident (0.95 vs 0.75) and underconfident (0.55 vs 0.75) groups cancel in 1 or 2 bins (ECE 0) ...
assert close(ece(conf, correct, 1), 0.0) and close(ece(conf, correct, 2), 0.0)
checks += 1
# Check 6: ... but give ECE 0.20 with 5 or 15 bins.
assert close(ece(conf, correct, 5), 0.20) and close(ece(conf, correct, 15), 0.20)
checks += 1
# Check 7: the same 100 detections at confidence 0.8 are calibrated if "correct" means IoU >= 0.5 (80 of 100)
# and overconfident by 0.2 if it means IoU >= 0.75 (60 of 100).
ious = [0.9] * 60 + [0.6] * 20 + [0.3] * 20
c08 = [0.8] * 100
assert close(ece(c08, [int(v >= 0.5) for v in ious], 10), 0.0)
assert close(ece(c08, [int(v >= 0.75) for v in ious], 10), 0.2)
checks += 1


def softmax(z):
    mx = max(z)
    e = [math.exp(v - mx) for v in z]
    s = sum(e)
    return [v / s for v in e]


logits = [2.0, 1.0, 0.1]
p1, p2 = softmax(logits), softmax([v / 2.0 for v in logits])
# Check 8: temperature T = 2 lowers the top confidence from 0.659 to 0.502 without changing the predicted class.
assert p1.index(max(p1)) == p2.index(max(p2)) == 0
assert close(max(p1), 0.6590) and close(max(p2), 0.5017)
checks += 1

# --- Example C: optimism of picking the best of K runs on the same test set --------


def phi(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def expected_max_std_normal(K, lo=-10.0, hi=10.0, steps=20000):
    """E[max of K independent N(0,1)] = integral of x K phi(x) Phi(x)^(K-1), Simpson's rule."""
    h = (hi - lo) / steps
    s = 0.0
    for i in range(steps + 1):
        x = lo + i * h
        w = 1 if i in (0, steps) else (4 if i % 2 else 2)
        s += w * x * K * phi(x) * Phi(x) ** (K - 1)
    return s * h / 3


sigma = math.sqrt(0.9 * 0.1 / 1000)   # SE of an accuracy of 0.9 on 1,000 independent test images
e20, e5 = expected_max_std_normal(20), expected_max_std_normal(5)
# Check 9: E[max of 20 standard normals] = 1.8675 and of 5 = 1.1630.
assert close(e20, 1.8675) and close(e5, 1.1630)
checks += 1
# Check 10: 20 equally good configurations scored on the same 1,000 images inflate the best score by about
# 1.8 points (0.0177) under independence; 5 configurations by about 1.1 points.
assert close(sigma, 0.009487) and close(e20 * sigma, 0.01772) and close(e5 * sigma, 0.01103)
checks += 1

print(f"133-donnees-generalisation: {checks} checks passed")
