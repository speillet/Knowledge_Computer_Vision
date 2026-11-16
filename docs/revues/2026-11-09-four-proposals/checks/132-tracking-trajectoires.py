"""Recompute the constructed examples of CV-METRIQUES-TEMPS-006 (reference 132-tracking-trajectoires).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-09-four-proposals/checks/132-tracking-trajectoires.py

Definitions:
- identity measures, Ristani et al. 2016 (arXiv 1609.01775v2), Sec. 3.3 eqs. 3-5: bipartite graph with one
  regular node per true and per computed trajectory, one false-positive node f+ per computed trajectory and one
  false-negative node f- per true trajectory; the cost of (tau, gamma) counts the false-negative frames of tau
  and the false-positive frames of gamma; (tau, f-_tau) costs len(tau), (f+_gamma, gamma) len(gamma),
  (f+, f-) zero; the minimum-cost one-to-one solution gives IDTP, IDFN and IDFP; Sec. 3.4 eqs. 6-11 give
  IDP, IDR and IDF1;
- TrackEval trackeval/metrics/identity.py at commit 12c8791b303e0a0b50f753af204249e622d0281a, L52-L85 and
  L134: per-pair counts of frames above the threshold, padded (G+P) x (G+P) cost matrix, one assignment,
  IDF1 = IDTP / (IDTP + 0.5 IDFP + 0.5 IDFN); re-implemented here, not executed;
- CLEAR MOT, Bernardin and Stiefelhagen 2008, Sec. 2.1.3 (a mismatch is counted when a new correspondence
  contradicts the stored mapping of that object, whatever the gap) and Sec. 2.2 eq. 2 (MOTA).
The sequences are constructed project examples. Every predicted box overlaps its own pedestrian above the
matching threshold and never the other pedestrian, so each frame's correspondences are given by the labels.
The assignments are found by brute force over permutations, with exact fractions.
"""

import itertools
from fractions import Fraction as F

checks = 0
N_FRAMES = 10


# A sequence is a list of frames; each frame is a list of (gt_id or None, pr_id or None).
# (g, p) is a correspondence above the threshold, (g, None) a missed object, (None, p) an extra box.

def counts(seq):
    """Detections per gt id, per predicted id, and frames where a (gt, pr) pair corresponds."""
    n_g, n_p, co = {}, {}, {}
    for frame in seq:
        for g, p in frame:
            if g is not None:
                n_g[g] = n_g.get(g, 0) + 1
            if p is not None:
                n_p[p] = n_p.get(p, 0) + 1
            if g is not None and p is not None:
                co[(g, p)] = co.get((g, p), 0) + 1
    return n_g, n_p, co


def identity_ristani(seq):
    """Minimum-cost solution of the Ristani et al. bipartite graph (Sec. 3.3), by brute force."""
    n_g, n_p, co = counts(seq)
    gts, prs = sorted(n_g), sorted(n_p)
    left = [("tau", g) for g in gts] + [("fpos", p) for p in prs]      # V_T
    right = [("gamma", p) for p in prs] + [("fneg", g) for g in gts]   # V_C
    INF = None

    def cost(u, v):
        if u[0] == "tau" and v[0] == "gamma":
            m = co.get((u[1], v[1]), 0)
            return (n_g[u[1]] - m) + (n_p[v[1]] - m)    # false-negative frames + false-positive frames
        if u[0] == "tau" and v[0] == "fneg":
            return n_g[u[1]] if u[1] == v[1] else INF
        if u[0] == "fpos" and v[0] == "gamma":
            return n_p[u[1]] if u[1] == v[1] else INF
        return 0                                         # (f+, f-): both empty

    best = None
    for perm in itertools.permutations(right):
        c = [cost(u, v) for u, v in zip(left, perm)]
        if INF in c:
            continue
        total = sum(c)
        if best is None or total < best[0]:
            best = (total, list(zip(left, perm)))
    total, match = best
    pairs = {u[1]: v[1] for u, v in match if u[0] == "tau" and v[0] == "gamma"}
    idtp = sum(co.get((g, p), 0) for g, p in pairs.items())
    idfn = sum(n_g.values()) - idtp                        # eq. 8
    idfp = sum(n_p.values()) - idtp
    assert idfn + idfp == total                            # overall cost = mis-assigned detections (Sec. 3.3)
    return {"pairs": pairs, "IDTP": idtp, "IDFN": idfn, "IDFP": idfp, "cost": total,
            "IDP": F(idtp, idtp + idfp), "IDR": F(idtp, idtp + idfn),
            "IDF1": F(2 * idtp, 2 * idtp + idfp + idfn)}


def identity_max_overlap(seq):
    """Same IDTP as the maximum one-to-one sum of co-occurrence counts (procedure pseudocode of the reference)."""
    n_g, n_p, co = counts(seq)
    gts, prs = sorted(n_g), sorted(n_p)
    padded = prs + [None] * len(gts)
    return max(sum(co.get((g, p), 0) for g, p in zip(gts, perm) if p is not None)
               for perm in itertools.permutations(padded, len(gts)))


def identity_trackeval(seq):
    """TrackEval identity.py L63-L85 cost matrix, solved by brute force instead of linear_sum_assignment."""
    n_g, n_p, co = counts(seq)
    gts, prs = sorted(n_g), sorted(n_p)
    G, P = len(gts), len(prs)
    BIG = 10 ** 10
    size = G + P
    fp_mat = [[0] * size for _ in range(size)]
    fn_mat = [[0] * size for _ in range(size)]
    for i in range(G, size):                              # L68
        for j in range(P):
            fp_mat[i][j] = BIG
    for i in range(G):                                    # L69
        for j in range(P, size):
            fn_mat[i][j] = BIG
    for gi, g in enumerate(gts):                          # L70-L72
        for j in range(P):
            fn_mat[gi][j] = n_g[g]
        fn_mat[gi][P + gi] = n_g[g]
    for pj, p in enumerate(prs):                          # L73-L75
        for i in range(G):
            fp_mat[i][pj] = n_p[p]
        fp_mat[pj + G][pj] = n_p[p]
    for gi, g in enumerate(gts):                          # L76-L77
        for pj, p in enumerate(prs):
            fn_mat[gi][pj] -= co.get((g, p), 0)
            fp_mat[gi][pj] -= co.get((g, p), 0)
    best = min(itertools.permutations(range(size)),
               key=lambda cols: sum(fn_mat[r][c] + fp_mat[r][c] for r, c in enumerate(cols)))
    idfn = sum(fn_mat[r][c] for r, c in enumerate(best))  # L83
    idfp = sum(fp_mat[r][c] for r, c in enumerate(best))  # L84
    idtp = sum(n_g.values()) - idfn                       # L85
    return idtp, idfn, idfp, F(idtp) / (idtp + F(idfp, 2) + F(idfn, 2))   # L134


def clear_mot(seq):
    """Mismatches counted against the stored mapping of each object (CLEAR MOT Sec. 2.1.3) and MOTA (eq. 2)."""
    mapping, mme, misses, fps, n_gt = {}, 0, 0, 0, 0
    for frame in seq:
        for g, p in frame:
            n_gt += g is not None
            if g is not None and p is None:
                misses += 1
            elif g is None and p is not None:
                fps += 1
            elif g is not None:
                if g in mapping and mapping[g] != p:
                    mme += 1
                mapping[g] = p
    return mme, 1 - F(misses + fps + mme, n_gt)


def fragment_from(k):
    """A keeps ID 1 in frames 1..k-1 and gets the new ID 3 from frame k to frame 10; B keeps ID 2."""
    return [[("A", 1 if t < k else 3), ("B", 2)] for t in range(1, N_FRAMES + 1)]


def check_identity(seq):
    r = identity_ristani(seq)
    assert identity_max_overlap(seq) == r["IDTP"]
    idtp, idfn, idfp, idf1 = identity_trackeval(seq)
    assert (idtp, idfn, idfp) == (r["IDTP"], r["IDFN"], r["IDFP"]) and idf1 == r["IDF1"]
    return r


# --- Card CV-METRIQUES-TEMPS-006 -----------------------------------------------------------------
x = fragment_from(9)        # tracker X: ID 1 in frames 1-8, ID 3 in frames 9-10
y = fragment_from(5)        # tracker Y: ID 1 in frames 1-4, ID 3 in frames 5-10

# Check 1: X matches A to ID 1 (8 frames) and B to ID 2; IDTP 18, IDFN 2, IDFP 2, IDF1 = 36/40 = 0.90.
rx = check_identity(x)
assert rx["pairs"] == {"A": 1, "B": 2}
assert (rx["IDTP"], rx["IDFN"], rx["IDFP"]) == (18, 2, 2) and rx["IDF1"] == F(9, 10)
assert rx["IDP"] == rx["IDR"] == F(9, 10)
checks += 1

# Check 2: Y matches A to the later, longer ID 3 (6 frames); IDTP 16, IDFN 4, IDFP 4, IDF1 = 32/40 = 0.80.
ry = check_identity(y)
assert ry["pairs"] == {"A": 3, "B": 2}
assert (ry["IDTP"], ry["IDFN"], ry["IDFP"]) == (16, 4, 4) and ry["IDF1"] == F(4, 5)
assert ry["IDP"] == ry["IDR"] == F(4, 5)
checks += 1

# Check 3: graph costs for Y: A-1 costs 6 + 0 and leaves ID 3 on its f+ node (6), total 12;
# A-3 costs 4 + 0 and leaves ID 1 on its f+ node (4), total 8 = IDFN + IDFP, the minimum.
n_g, n_p, co = counts(y)
cost_a1 = (n_g["A"] - co[("A", 1)]) + (n_p[1] - co[("A", 1)]) + n_p[3]
cost_a3 = (n_g["A"] - co[("A", 3)]) + (n_p[3] - co[("A", 3)]) + n_p[1]
assert (cost_a1, cost_a3) == (12, 8) and ry["cost"] == 8
checks += 1

# Check 4: CLEAR MOT counts one mismatch for each tracker; MOTA = 1 - 1/20 = 0.95 for both.
assert clear_mot(x) == clear_mot(y) == (1, F(19, 20))
checks += 1

# Check 5: for a new ID from frame k (k = 2..10), IDF1 = 1 - min(k-1, 11-k)/20 (0.95 at k = 2 or 10,
# 0.80 at k = 5 or 7, 0.75 at k = 6) while CLEAR MOT counts one mismatch and MOTA stays 0.95.
for k in range(2, N_FRAMES + 1):
    r = check_identity(fragment_from(k))
    assert r["IDF1"] == 1 - F(min(k - 1, N_FRAMES + 1 - k), 20)
    assert r["IDFN"] == r["IDFP"] == min(k - 1, N_FRAMES + 1 - k)
    assert clear_mot(fragment_from(k)) == (1, F(19, 20))
assert [float(check_identity(fragment_from(k))["IDF1"]) for k in (2, 5, 6, 7, 10)] == [0.95, 0.8, 0.75, 0.8, 0.95]
checks += 1

# Check 6: a one-frame relabel (ID 3 in frame 5 only, then ID 1 again) costs CLEAR two mismatches,
# MOTA 0.90, but IDF1 only one frame on each side: IDTP 19, IDF1 0.95. MOTA and IDF1 order this blip
# and tracker Y in opposite ways.
blip = [[("A", 3 if t == 5 else 1), ("B", 2)] for t in range(1, N_FRAMES + 1)]
rb = check_identity(blip)
assert clear_mot(blip) == (2, F(9, 10))
assert (rb["IDTP"], rb["IDFN"], rb["IDFP"]) == (19, 1, 1) and rb["IDF1"] == F(19, 20)
assert clear_mot(blip)[1] < clear_mot(y)[1] and rb["IDF1"] > ry["IDF1"]
checks += 1

# Check 7: blocking-error values. Anchoring A to its first ID in Y gives IDTP 14 and IDF1 0.70;
# letting A keep both IDs (no one-to-one constraint) gives IDF1 1; counting each mis-identified frame
# only once (IDFN without IDFP) gives 36/38 for X instead of 36/40.
n_g, n_p, co = counts(y)
idtp_first = co[("A", 1)] + co[("B", 2)]
assert idtp_first == 14 and F(2 * idtp_first, 2 * idtp_first + 6 + 6) == F(7, 10)
idtp_many = co[("A", 1)] + co[("A", 3)] + co[("B", 2)]
assert F(2 * idtp_many, 2 * idtp_many + (20 - idtp_many) * 2) == 1
assert F(2 * 18, 2 * 18 + 2) == F(18, 19) and round(float(F(18, 19)), 3) == 0.947
checks += 1

# --- Worked example A of the reference (IDF1 and MOTA rows, rechecked as the card's basis) ----------
swap = [[("A", 1), ("B", 2)] if t < 5 else [("A", 2), ("B", 1)] for t in range(N_FRAMES)]
frag = fragment_from(6)
gap = [[("A", 1), ("B", 2)] if t < 5 else [("A", 1), ("B", None)] for t in range(N_FRAMES)]
fixed = [[("A", 2), ("B", 1)] if t in (5, 6) else [("A", 1), ("B", 2)] for t in range(N_FRAMES)]
# Check 8: IDF1 0.50, 0.75, 0.857 (30/35) and 0.80; MOTA 0.90, 0.95, 0.75 and 0.80.
assert [check_identity(s)["IDF1"] for s in (swap, frag, gap, fixed)] == [F(1, 2), F(3, 4), F(6, 7), F(4, 5)]
assert [clear_mot(s) for s in (swap, frag, gap, fixed)] == [(2, F(9, 10)), (1, F(19, 20)), (0, F(3, 4)),
                                                          (4, F(4, 5))]
checks += 1

print(f"132-tracking-trajectoires (CV-METRIQUES-TEMPS-006): {checks} checks passed")
