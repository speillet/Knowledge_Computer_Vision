"""Recompute every intermediate value shown by the clarified CV-METRIQUES-TEMPS cards and by
the merged "One fragment: events versus frames" paragraph of reference 132 (2026-11-17).

Stdlib only. Run with: python3 -I docs/revues/2026-11-17-clarity/checks/132-tracking-trajectoires.py
Definitions: MOTA and IDSW as in Bernardin and Stiefelhagen 2008, eq. 2, and TrackEval clear.py at
12c8791 (IDSW against the last matched prediction of the same gt ID); IDF1 as in Ristani et al.
2016, eqs. 3-11 (one-to-one ID bijection, brute force here); HOTA at one threshold, Luiten et al.
eqs. 10-21. Every box overlaps its object perfectly, so matching is trivial and only IDs vary.
"""

import itertools
import math
import random

checks = 0


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


def mota(seq):
    """seq: list of frames, each a list of (gt_id, pr_id); returns MOTA, IDSW, FN, FP."""
    fn = fp = idsw = n_gt = 0
    last = {}
    for frame in seq:
        for g, p in frame:
            n_gt += g is not None
            if g is not None and p is None:
                fn += 1
            elif g is None and p is not None:
                fp += 1
            elif g is not None:
                if g in last and last[g] != p:
                    idsw += 1
                last[g] = p
    return 1 - (fn + fp + idsw) / n_gt, idsw, fn, fp


def idf1(seq):
    co, n_g, n_p, gts, prs = {}, 0, 0, set(), set()
    for frame in seq:
        for g, p in frame:
            if g is not None:
                n_g += 1
                gts.add(g)
            if p is not None:
                n_p += 1
                prs.add(p)
            if g is not None and p is not None:
                co[(g, p)] = co.get((g, p), 0) + 1
    gts, prs = sorted(gts), sorted(prs)
    best, pairing = -1, None
    for perm in itertools.permutations(prs + [None] * len(gts), len(gts)):
        val = sum(co.get((g, p), 0) for g, p in zip(gts, perm) if p is not None)
        if val > best:
            best, pairing = val, dict(zip(gts, perm))
    idtp = best
    idfn, idfp = n_g - idtp, n_p - idtp
    return 2 * idtp / (2 * idtp + idfp + idfn), idtp, idfn, idfp, pairing


def hota_one_alpha(seq):
    tp, pair, gc, pc = 0, {}, {}, {}
    for frame in seq:
        for g, p in frame:
            gc[g] = gc.get(g, 0) + 1
            pc[p] = pc.get(p, 0) + 1
            tp += 1
            pair[(g, p)] = pair.get((g, p), 0) + 1
    ass_a = sum(n * n / (gc[g] + pc[p] - n) for (g, p), n in pair.items()) / tp
    return 1.0, ass_a, math.sqrt(ass_a)          # DetA = 1: no FN, no FP


def takeover(k, n):
    """A keeps ID 1 before frame k (1-based) and has the new ID 3 from frame k; B keeps ID 2."""
    return [[("A", 1 if t < k else 3), ("B", 2)] for t in range(1, n + 1)]


# --- General formula of the merged reference paragraph: pieces a = k - 1 and b = n - k + 1 ----
for n in (8, 10):
    for k in range(2, n + 1):
        a, b = k - 1, n - k + 1
        m, sw, fn, fp = mota(takeover(k, n))
        f1, idtp, idfn, idfp, _ = idf1(takeover(k, n))
        assert sw == 1 and fn == fp == 0 and close(m, 1 - 1 / (2 * n))
        assert idtp == max(a, b) + n and idfn == idfp == min(a, b)
        assert close(2 * idtp, 2 * (2 * n - min(a, b))) and close(2 * idtp + idfp + idfn, 4 * n)
        assert close(f1, 1 - min(a, b) / (2 * n))
checks += 1

# --- CV-METRIQUES-TEMPS-001: the figure case, n = 8, takeover at frame 6 --------------------
seq = takeover(6, 8)
m, sw, fn, fp = mota(seq)
assert 2 * 8 == 16 and (sw, fn, fp) == (1, 0, 0) and close(m, 15 / 16) and round(m, 2) == 0.94
f1, idtp, idfn, idfp, pairing = idf1(seq)
assert pairing == {"A": 1, "B": 2} and (idtp, idfn, idfp) == (13, 3, 3) and 5 + 8 == 13
assert close(f1, 26 / (26 + 3 + 3)) and round(f1, 2) == 0.81
d, a, h = hota_one_alpha(seq)
assert close(a, 98 / 128) and round(a, 2) == 0.77 and close(h, 0.875)
f8, idtp8, idfn8, idfp8, _ = idf1(takeover(8, 8))
assert (idtp8, idfn8, idfp8) == (15, 1, 1) and 7 + 8 == 15 and close(f8, 30 / 32)
f5, idtp5, idfn5, idfp5, _ = idf1(takeover(5, 8))
assert (idtp5, idfn5, idfp5) == (12, 4, 4) and 4 + 8 == 12 and close(f5, 24 / 32) and close(f5, 0.75)
assert all(close(mota(takeover(k, 8))[0], 15 / 16) for k in (5, 8))
oracle = [[(g, g) for g, _ in frame] for frame in seq]      # relabelled replay
assert mota(oracle)[1] == 0 and close(mota(oracle)[0], 1.0) and close(idf1(oracle)[0], 1.0)
checks += 1

# --- CV-METRIQUES-TEMPS-002: counterexample and the direction of the general inequality --------
profiles = [(1.0, 0.0), (0.0, 1.0)]
per_threshold = [math.sqrt(dd * aa) for dd, aa in profiles]
assert per_threshold == [0.0, 0.0] and sum(per_threshold) / 2 == 0.0
mean_d = sum(dd for dd, _ in profiles) / 2
mean_a = sum(aa for _, aa in profiles) / 2
assert (mean_d, mean_a) == (0.5, 0.5) and close(math.sqrt(mean_d * mean_a), 0.5)
rng = random.Random(132)
for _ in range(2000):
    ds = [rng.random() for _ in range(19)]
    as_ = [rng.random() for _ in range(19)]
    hota = sum(math.sqrt(x * y) for x, y in zip(ds, as_)) / 19
    recombined = math.sqrt(sum(ds) / 19 * sum(as_) / 19)
    assert hota <= recombined + 1e-12                       # recombination never below HOTA
ratio = [0.8 * c for c in (0.2, 0.5, 0.9)]                  # same DetA/AssA ratio everywhere
hota = sum(math.sqrt(x * (x / 0.8)) for x in ratio) / 3
assert close(hota, math.sqrt(sum(ratio) / 3 * sum(x / 0.8 for x in ratio) / 3))
checks += 1

# --- CV-METRIQUES-TEMPS-003: worked example B, step by step ----------------------------------
xs = list(range(11))
centroid = sum(xs) / len(xs)
u = [x - centroid for x in xs]
assert centroid == 5 and u[0] == -5 and u[-1] == 5
assert sum(v * v for v in u) == 2 * (1 + 4 + 9 + 16 + 25) == 110
assert sum(v * v for v in u) / 11 == 10 and round(math.sqrt(10), 2) == 3.16
est = [1.02 * x for x in xs]                                  # 2 % scale error
t = sum(est) / 11 - centroid                                  # best translation: match centroids
res = [e - t - x for e, x in zip(est, xs)]
assert all(close(r, 0.02 * v) for r, v in zip(res, u))
ate = math.sqrt(sum(r * r for r in res) / 11)
assert close(ate, 0.02 * math.sqrt(10)) and round(ate, 3) == 0.063
s = 1 / 1.02
res_sim = [s * e - (s * sum(est) / 11 - centroid) - x for e, x in zip(est, xs)]
assert all(close(r, 0.0) for r in res_sim) and round(s, 2) == 0.98
theta = math.radians(1.0)
tilt = math.sqrt(10) * 2 * math.sin(theta / 2)
assert round(tilt, 3) == 0.055
assert close(1.02 * 1 - 1, 0.02) and close(1.02 * 5 - 5, 0.10)
checks += 1


# --- CV-METRIQUES-TEMPS-004: a common change of world frame cancels in relative motions -------
def pose(x, y, a):
    c, s_ = math.cos(a), math.sin(a)
    return [[c, -s_, x], [s_, c, y], [0.0, 0.0, 1.0]]


def mul(p, q):
    return [[sum(p[i][k] * q[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def inv(p):
    r = [[p[0][0], p[1][0]], [p[0][1], p[1][1]]]
    t_ = [-(r[0][0] * p[0][2] + r[0][1] * p[1][2]), -(r[1][0] * p[0][2] + r[1][1] * p[1][2])]
    return [[r[0][0], r[0][1], t_[0]], [r[1][0], r[1][1], t_[1]], [0.0, 0.0, 1.0]]


ti, tj, world = pose(1.0, 2.0, 0.3), pose(4.0, -1.0, 1.1), pose(-7.0, 3.0, 2.0)
direct = mul(inv(ti), tj)
moved = mul(inv(mul(world, ti)), mul(world, tj))
assert all(close(direct[i][j], moved[i][j], 1e-9) for i in range(3) for j in range(3))
checks += 1

# --- CV-METRIQUES-TEMPS-006: trackers X and Y over n = 10 frames --------------------------------
x_seq, y_seq = takeover(9, 10), takeover(5, 10)
fx, idtp, idfn, idfp, px = idf1(x_seq)
assert px["A"] == 1 and (idtp, idfn, idfp) == (18, 2, 2) and close(fx, 36 / 40) and close(fx, 0.90)
fy, idtp, idfn, idfp, py = idf1(y_seq)
assert py["A"] == 3 and (idtp, idfn, idfp) == (16, 4, 4) and close(fy, 32 / 40) and close(fy, 0.80)
cost_a1, cost_a3 = 6 + 6, 4 + 4                               # unexplained frames of each choice
assert (cost_a1, cost_a3) == (12, 8)
assert close(mota(x_seq)[0], 0.95) and close(mota(y_seq)[0], 0.95)
inner = [[("A", 3 if t == 5 else 1), ("B", 2)] for t in range(1, 11)]
assert mota(inner)[1] == 2 and close(mota(inner)[0], 0.90) and close(idf1(inner)[0], 0.95)
assert close((2 * 14) / (2 * 14 + 6 + 6), 0.70)               # blocking error: A paired with ID 1 in Y
assert close((2 * 18) / (2 * 18 + 2), 36 / 38)                # blocking error: only IDFN counted in X
checks += 1

print(f"132-tracking-trajectoires (clarity pass, CV-METRIQUES-TEMPS-001 to -006): {checks} checks passed")
