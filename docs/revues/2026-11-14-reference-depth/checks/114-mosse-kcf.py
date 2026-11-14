"""Recompute the constructed examples of CV-CORRELATION (reference 114-mosse-kcf).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/114-mosse-kcf.py
Formulas come from KCF (arXiv 1404.7584v3, eqs. 2, 6, 12, App. A-A) and MOSSE
(Bolme et al. 2010, Sec. 3.5). Signals, thresholds and paddings below are constructed.
"""

import cmath
import math

# --- Example A: ridge regression on cyclic shifts, direct solve versus DFT ----------
n, lam = 8, 0.1
x = [0.2, 1.0, 0.6, -0.3, 0.1, -0.5, 0.4, 0.0]                         # base sample
y = [math.exp(-0.5 * min(i, n - i) ** 2) for i in range(n)]              # Gaussian label, peak at index 0


def circulant(v):
    """Rows are cyclic shifts of v to the right, as in KCF eq. 6."""
    return [[v[(j - i) % n] for j in range(n)] for i in range(n)]


def solve(a, b):
    """Gauss-Jordan elimination with partial pivoting."""
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c:
                f = m[r][c] / m[c][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def dft(v):   # NumPy / OpenCV sign convention: exp(-2*pi*i*k*t/n)
    return [sum(v[t] * cmath.exp(-2j * math.pi * k * t / n) for t in range(n)) for k in range(n)]


def idft(v):
    return [sum(v[k] * cmath.exp(2j * math.pi * k * t / n) for k in range(n)).real / n for t in range(n)]


X = circulant(x)
gram = [[sum(X[k][i] * X[k][j] for k in range(n)) + (lam if i == j else 0.0) for j in range(n)] for i in range(n)]
w_direct = solve(gram, [sum(X[k][i] * y[k] for k in range(n)) for i in range(n)])   # KCF eq. 2

xh, yh = dft(x), dft(y)
w_fourier = idft([a * b / (a.conjugate() * a + lam) for a, b in zip(xh, yh)])
w_mirror = idft([a.conjugate() * b / (a.conjugate() * a + lam) for a, b in zip(xh, yh)])
# Check 1: with this DFT sign and the eq. 6 shift direction, x_hat * y_hat / (|x_hat|^2 + lambda)
# reproduces the direct O(n^3) solution to machine precision.
assert max(abs(p - q) for p, q in zip(w_direct, w_fourier)) < 1e-12
# Check 2: putting the conjugate on the numerator's x_hat instead gives the time-reversed filter.
assert max(abs(w_mirror[i] - w_direct[(-i) % n]) for i in range(n)) < 1e-12


def responses(w, shift):
    """Regression outputs for all cyclic shifts of z = x shifted right by `shift`."""
    z = [x[(t - shift) % n] for t in range(n)]
    return [sum(row[j] * w[j] for j in range(n)) for row in circulant(z)]


r0 = responses(w_direct, 0)
rm = responses(w_mirror, 0)
# Check 3: the correct filter applied to its own training patch peaks at zero shift (index 0);
# the mirrored filter peaks at index 6 with a lower value. This is a cheap unit test.
assert max(range(n), key=lambda i: r0[i]) == 0 and max(range(n), key=lambda i: rm[i]) == 6
assert round(max(r0), 3) == 0.954 and round(max(rm), 3) == 0.788
# Check 4: a patch shifted right by s produces its peak at index -s mod n (wrap-around reading).
for s in (1, 2, -2):
    r = responses(w_direct, s)
    assert max(range(n), key=lambda i: r[i]) == (-s) % n

# --- Example B: PSR, paper definition versus whole-map statistics -------------------
def mean_std(v):
    m = sum(v) / len(v)
    return m, math.sqrt(sum((u - m) ** 2 for u in v) / len(v))


# Check 5: card example, peak 0.8, sidelobe mean 0.2, sidelobe std 0.1 -> PSR 6.
assert abs((0.8 - 0.2) / 0.1 - 6.0) < 1e-12
sidelobe = [0.1, 0.3] * 49                     # 98 values, mean 0.2, population std 0.1
peak = 1.0
m_sl, s_sl = mean_std(sidelobe)
psr_paper = (peak - m_sl) / s_sl               # sidelobe excludes the peak region (here: the peak)
m_all, s_all = mean_std(sidelobe + [peak])     # OpenCV legacy MOSSE: whole response map
psr_whole = (peak - m_all) / s_all
# Check 6: the same map gives PSR 8.0 with the paper's exclusion but about 6.2 over the whole map.
assert abs(psr_paper - 8.0) < 1e-9 and abs(psr_whole - 6.2) < 0.05 and psr_whole < psr_paper
# Check 7: an affine rescaling r' = a r + b with a > 0 leaves both PSR definitions unchanged.
a, b = 2.0, 0.5
m2, s2 = mean_std([a * u + b for u in sidelobe])
assert abs((a * peak + b - m2) / s2 - psr_paper) < 1e-9

# --- Example C: displacement that a padded window can represent ---------------------
for padding, represent, inside in ((1.0, 0.5, 0.0), (2.0, 1.0, 0.5), (2.5, 1.25, 0.75)):
    # Check 8: a window of `padding` target widths represents shifts up to padding/2 widths
    # (half the cyclic period) and keeps the whole target inside only up to (padding-1)/2.
    assert padding / 2 == represent and (padding - 1) / 2 == inside

print("114-mosse-kcf: 8 checks passed (circulant ridge regression, conjugate convention, PSR definitions, padding)")
