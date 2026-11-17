"""Recompute the constructed numbers added to CV-ANOMALIES-003 (reference 73-patchcore-padim, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/73-patchcore-padim.py
Image scores are modeled as Gaussians for the illustration only; real PatchCore and PaDiM
scores are maxima over patches and need not be Gaussian. The PaDiM amplification
1/sqrt(eps) with eps = 0.01 comes from the reference (PaDiM Sec. IV-B, worked example C).
"""
import math
from statistics import NormalDist

checks = 0

# 1. PaDiM: a unit deviation along a direction of zero training variance scores 1/sqrt(eps).
assert abs(1 / math.sqrt(0.01) - 10) < 1e-12
checks += 1

# 2. Threshold for 1% false rejections before the lighting change, and the defect recall.
good, bad = NormalDist(1.0, 0.2), NormalDist(2.0, 0.3)
tau = good.inv_cdf(0.99)
assert abs(tau - 1.465) < 5e-4
assert abs((1 - bad.cdf(tau)) - 0.963) < 5e-4
checks += 1

# 3. After the change: good parts shift by 0.5, defects by 0.2 (the populations get closer).
good2, bad2 = NormalDist(1.5, 0.2), NormalDist(2.2, 0.3)
assert abs((1 - good2.cdf(tau)) - 0.57) < 5e-3               # false rejections at the old tau
tau2 = good2.inv_cdf(0.99)
assert abs(tau2 - 1.965) < 5e-4
assert abs((1 - bad2.cdf(tau2)) - 0.783) < 5e-4               # recall after restoring 1% FRR
assert abs((1 - bad2.cdf(tau)) - 0.993) < 5e-4                # old tau: defects still caught, but 57% FRR
checks += 1

print(f"73-patchcore-padim (CV-ANOMALIES-003): {checks} checks passed")
