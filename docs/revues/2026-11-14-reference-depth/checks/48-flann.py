"""Recompute the constructed examples of CV-FLANN (reference 48-flann).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/48-flann.py
Inputs: Muja and Lowe 2009/2014 (time-bounded search, precision definition), opencv
4.13.0 flann lsh_index.h (default table_number 12, key_size 20, multi_probe_level 2),
lsh_table.h (key = key_size randomly chosen bit positions), miniflann.hpp
(SearchParams checks = 32), Lowe 2004 Sec. 7.2 (200 candidates). Cost figures and
scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: amortizing an index ------------------------------------------------
B, A, E = 2.0, 0.001, 0.003   # build (s), indexed query (s), exhaustive query (s)
# Check 1: 100 queries: 2.1 s with the index against 0.3 s exhaustive.
assert close(B + 100 * A, 2.1) and close(100 * E, 0.3)
# Check 2: 10,000 queries: 12 s against 30 s.
assert close(B + 10_000 * A, 12.0) and close(10_000 * E, 30.0)
# Check 3: break-even at N_q = B / (E - A) = 1,000 queries.
assert close(B / (E - A), 1000.0)
# Check 4: a one-shot knnMatch(query, train) rebuilds the index on every call, so the
# per-call cost stays B + N_q * A: with 100 queries per frame the index never pays off.
assert B + 100 * A > 100 * E

# --- Example B: a missed second neighbor distorts the ratio ----------------------
# Check 5: exact (10, 11) gives 0.909 (rejected at 0.8); missing the second neighbor
# and returning (10, 30) gives 0.333 (accepted).
assert close(10 / 11, 0.909) and close(10 / 30, 0.333) and 10 / 11 > 0.8 > 10 / 30
# Check 6: with a returned second distance at most 10% too large (eps = 0.1), only
# measured ratios below 0.8 / 1.1 = 0.727 certify the exact ratio is below 0.8.
assert close(0.8 / 1.1, 0.7273, 1e-4)

# --- Example C: multi-probe LSH on 256-bit descriptors ---------------------------
n_bits, key, level, tables = 256, 20, 2, 12


def p_table(d):
    """Probability that at most `level` of the `key` sampled bit positions (without
    replacement) fall among the d differing bits: the query probes the right bucket."""
    total = math.comb(n_bits, key)
    return sum(math.comb(d, i) * math.comb(n_bits - d, key - i) for i in range(level + 1)) / total


def p_any(d):
    return 1 - (1 - p_table(d)) ** tables


# Check 7: each table is probed in 1 + 20 + 190 = 211 buckets (all keys within 2 bit flips).
assert sum(math.comb(key, i) for i in range(level + 1)) == 211
# Check 8: a true match 30 bits away is in a probed bucket of one table with p ~ 0.58,
# and of at least one of 12 tables with p > 0.9999.
assert close(p_table(30), 0.576, 0.005) and p_any(30) > 0.9999
# Check 9: a weaker match 60 bits away: ~0.11 per table, ~0.75 over 12 tables.
assert close(p_table(60), 0.110, 0.005) and close(p_any(60), 0.752, 0.005)
# Check 10: an unrelated descriptor (128 bits away) collides with p ~ 1.2e-4 per table,
# so about 0.14% of the database is examined over 12 tables (with repeats).
assert 1.1e-4 < p_table(128) < 1.3e-4 and close(tables * p_table(128), 0.00144, 0.0001)

# --- Example D: search budgets -----------------------------------------------------
# Check 11: OpenCV's default SearchParams examines 32 leaves, Lowe's BBF stopped after 200.
assert 200 / 32 == 6.25

# --- Example E: L2 and cosine for unit vectors ------------------------------------
a, b = (1.0, 0.0), (0.6, 0.8)
dot = a[0] * b[0] + a[1] * b[1]
sq = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
# Check 12: ||a - b||^2 = 2 - 2 a.b = 0.8 for unit vectors; FLANN's L2 returns this squared
# value, which FlannBasedMatcher converts with a square root (0.894).
assert close(sq, 2 - 2 * dot) and close(sq, 0.8) and close(math.sqrt(sq), 0.894)

# --- Example F: precision versus recall wording ------------------------------------
# Check 13: 940 of 1,000 queries recover their exact nearest neighbor: recall@1 = 0.94
# (Muja and Lowe call this precision); for k = 2, both exact neighbors must be counted.
assert close(940 / 1000, 0.94)

print("48-flann: 13 checks passed")
