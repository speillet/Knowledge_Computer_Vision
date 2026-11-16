"""Recompute the constructed examples of CV-FUSION-007 (reference 13-kalman-ekf-eskf).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-09-four-proposals/checks/13-kalman-ekf-eskf.py

Checks:
- traces A and B: NIS per epoch, sample means, population centered covariances, and the
  decomposition mean(|e|^2) = tr(Cov) + |mean|^2 on their empirical distributions;
- periodic structure of B when its four-vector pattern is repeated (circular sample
  autocorrelation of each component);
- chi-square with m = 2: mean 2, 95% quantile -2 ln 0.05;
- effect of a NIS gate on the accepted population when the true innovation covariance is
  k S instead of S: NIS = k X with X ~ chi2_2 (exponential, mean 2), so
  E[NIS | NIS <= c] = k (2 - t e^{-t/2} / (1 - e^{-t/2})) with t = c / k, and the
  rejection rate is e^{-c / (2k)}.
Squares of the trace components are exact (2 = sqrt(2)^2 handled through exact squares);
the chi-square quantities use floats with explicit tolerances.
"""

import math
from fractions import Fraction as F

checks = 0


def check(cond, label):
    global checks
    assert cond, label
    checks += 1


# Traces are stored through exact squared components and signs, so that sqrt(2) stays exact.
# A: (sqrt2, 0) four times; B: (1, 1), (1, -1), (-1, 1), (-1, -1).
SQRT2 = math.sqrt(2.0)
A = [(SQRT2, 0.0)] * 4
A_SQ = [(F(2), F(0))] * 4                    # exact squared components of A
B = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

# NIS per epoch = squared norm of the whitened innovation.
nis_a = [x2 + y2 for x2, y2 in A_SQ]
nis_b = [F(x * x + y * y) for x, y in B]
check(nis_a == [2, 2, 2, 2], "trace A has NIS 2 at every epoch")
check(nis_b == [2, 2, 2, 2], "trace B has NIS 2 at every epoch")
check(sum(nis_a) / 4 == 2 and sum(nis_b) / 4 == 2, "both mean NIS equal 2, the chi2_2 mean")

# Sample means.
mean_a = (sum(x for x, _ in A) / 4, sum(y for _, y in A) / 4)
mean_b = (F(sum(x for x, _ in B), 4), F(sum(y for _, y in B), 4))
check(math.isclose(mean_a[0], SQRT2, rel_tol=1e-15) and mean_a[1] == 0, "A mean (sqrt2, 0)")
check(mean_b == (0, 0), "B mean is zero")

# Population centered covariances (divide by n): A is degenerate, B is the identity.
cov_a = [[sum((p[i] - mean_a[i]) * (p[j] - mean_a[j]) for p in A) / 4 for j in range(2)]
         for i in range(2)]
cov_b = [[F(sum((p[i] - mean_b[i]) * (p[j] - mean_b[j]) for p in B), 4) for j in range(2)]
         for i in range(2)]
check(all(abs(v) < 1e-15 for row in cov_a for v in row), "A centered covariance is zero")
check(cov_b == [[1, 0], [0, 1]], "B centered covariance is I_2")

# mean(|e|^2) = tr(Cov) + |mean|^2 on each empirical distribution.
mean_sq_norm_a = 2.0                                        # exact, from A_SQ
check(math.isclose(cov_a[0][0] + cov_a[1][1] + mean_a[0] ** 2 + mean_a[1] ** 2,
                   mean_sq_norm_a, rel_tol=1e-15), "A: 0 + 2 = 2 (all bias)")
check(cov_b[0][0] + cov_b[1][1] + mean_b[0] ** 2 + mean_b[1] ** 2 == 2,
      "B: 2 + 0 = 2 (all centered variance)")


# Repeating B forever: circular sample autocorrelation of each component.
def circ_autocorr(seq, lag):
    n = len(seq)
    return F(sum(seq[i] * seq[(i + lag) % n] for i in range(n)), sum(v * v for v in seq))


b1 = [x for x, _ in B]          # 1, 1, -1, -1
b2 = [y for _, y in B]          # 1, -1, 1, -1
check(circ_autocorr(b2, 1) == -1, "B second component: lag-1 autocorrelation -1")
check(circ_autocorr(b1, 1) == 0 and circ_autocorr(b1, 2) == -1,
      "B first component: lag-1 autocorrelation 0, lag-2 autocorrelation -1")
check(circ_autocorr(b1, 4) == 1 and circ_autocorr(b2, 4) == 1, "period 4: lag-4 autocorrelation 1")

# Chi-square with two degrees of freedom: exponential with mean 2.
c95 = -2.0 * math.log(0.05)
check(abs(c95 - 5.991) < 5e-4, "chi2_{2,0.95} = 5.991")
check(abs((1.0 - math.exp(-c95 / 2.0)) - 0.95) < 1e-12, "CDF at the quantile is 0.95")


def gated_mean(k, c):
    """E[k X | k X <= c] for X ~ chi2_2."""
    t = c / k
    return k * (2.0 - t * math.exp(-t / 2.0) / (1.0 - math.exp(-t / 2.0)))


def rejection_rate(k, c):
    return math.exp(-c / (2.0 * k))


# Correct covariance: the gate alone lowers the accepted mean below 2.
check(abs(gated_mean(1.0, c95) - 1.685) < 5e-4, "k = 1: accepted NIS mean 1.685")
check(abs(rejection_rate(1.0, c95) - 0.05) < 1e-12, "k = 1: 5% rejected")
# Overconfident filter, true covariance 1.4 S: ungated mean 2.8, accepted mean ~2.00.
check(math.isclose(1.4 * 2.0, 2.8), "k = 1.4: ungated NIS mean 2.8")
check(abs(gated_mean(1.4, c95) - 2.00) < 5e-3, "k = 1.4: accepted NIS mean about 2.00")
check(abs(rejection_rate(1.4, c95) - 0.118) < 5e-4, "k = 1.4: 11.8% rejected instead of 5%")

# Monte Carlo cross-check of the closed form (seeded, stdlib random).
import random
rng = random.Random(20261116)
draws = [1.4 * rng.expovariate(0.5) for _ in range(400_000)]
kept = [d for d in draws if d <= c95]
check(abs(sum(kept) / len(kept) - gated_mean(1.4, c95)) < 0.01, "Monte Carlo accepted mean")
check(abs(1 - len(kept) / len(draws) - rejection_rate(1.4, c95)) < 0.003, "Monte Carlo rejection")

print(f"gated mean k=1: {gated_mean(1.0, c95):.4f}; k=1.4: {gated_mean(1.4, c95):.4f}; "
      f"rejection k=1.4: {rejection_rate(1.4, c95):.4f}")
print(f"{checks} checks passed")
