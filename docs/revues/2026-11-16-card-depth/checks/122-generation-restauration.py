"""Recompute the constructed example added to CV-DIFFUSION-003 (reference
122-generation-restauration, example E, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/122-generation-restauration.py
Model: one low-resolution pixel is the mean of 4 high-resolution columns (H = box average).
MMSE = posterior mean: Blau and Michaeli 2018, section 3.1.
"""
from fractions import Fraction as F

checks = 0
BG = 100                                   # background grey level (any value works)


def crack(width, depth, start=0):
    return [BG - depth if start <= i < start + width else BG for i in range(4)]


def H(col):
    return F(sum(col), 4)


y = BG - 10
cands = [crack(1, 40), crack(2, 20), crack(4, 10)]
assert all(H(c) == y for c in cands)                       # identical measurement
assert all(w * a == 40 for w, a in ((1, 40), (2, 20), (4, 10)))
assert all(H(crack(1, 40, s)) == y for s in range(4))      # position also unobservable
checks += 1

# Posterior mean over the three widths (equal weights, left-aligned): depths per column.
mmse = [sum(F(BG - c[i]) for c in cands) / 3 for i in range(4)]
assert [round(float(v), 1) for v in mmse] == [23.3, 10.0, 3.3, 3.3]
assert sum(mmse) == 40                                     # same integrated darkness
assert all(mmse != [BG - v for v in c] for c in cands)     # matches none of the candidates
checks += 1

# Consistency H x_hat = y holds for the MMSE profile too.
assert H([BG - v for v in mmse]) == y
checks += 1

print(f"122-generation-restauration (CV-DIFFUSION-003): {checks} checks passed")
