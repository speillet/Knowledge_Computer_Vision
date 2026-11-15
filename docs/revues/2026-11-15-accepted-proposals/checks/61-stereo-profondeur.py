"""Recompute the constructed examples of CV-STEREO-005 (reference 61-stereo-profondeur).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-15-accepted-proposals/checks/61-stereo-profondeur.py

What is recomputed: the suggested OpenCV penalties for a grayscale 5x5 block, OpenCV's silent
correction of P2, the inertness of P1 when P2 < P1 in the SGM recursion, the single-path
condition for keeping a narrow structure (w * Delta > 2 * P2), and a small synthetic SGM run
(8 directions) sweeping P2 over 250, 800, 1600 and 3200 with P1 = 200.

Conventions fixed by the sources:
- Energy with P1 for |Dp - Dq| = 1 and P2 for |Dp - Dq| > 1, path recursion with the
  previous minimum subtracted, at least 8 directions, P2 >= P1 (Hirschmueller 2008, TPAMI 30(2),
  Section 2.2, eqs. 11-14).
- OpenCV 4.13.0 calib3d.hpp L3723-L3729: P1 for +-1 changes, P2 for larger changes, "requires
  P2 > P1", suggested 8 * channels * blockSize^2 and 32 * channels * blockSize^2.
- OpenCV 4.13.0 stereosgbm.cpp L500 (also L977-L978, L1229-L1230, L1639):
  P1 = P1 > 0 ? P1 : 2; P2 = max(P2 > 0 ? P2 : 5, P1 + 1); constant P2 in the aggregation loops
  (L676-L811).
The cost volume (0 at the true disparity, Delta elsewhere) and the scene are constructed; the toy
is a model of eqs. 12-14, not OpenCV's block-matching implementation.
"""

import random

checks = 0

# Check 1: suggested penalties for 1 channel and blockSize 5, and OpenCV's silent correction of
# a P2 that is not larger than P1.
c, b = 1, 5
P1s, P2s = 8 * c * b * b, 32 * c * b * b
assert (P1s, P2s, P2s // P1s) == (200, 800, 4)


def opencv_penalties(p1, p2):
    q1 = p1 if p1 > 0 else 2
    return q1, max(p2 if p2 > 0 else 5, q1 + 1)


assert opencv_penalties(200, 150) == (200, 201)       # P2 = 150 silently becomes 201
assert opencv_penalties(0, 0) == (2, 5) and opencv_penalties(200, 800) == (200, 800)
checks += 1


def path_costs(C, P1, P2):
    """Eq. 13 along one path: L(p,d) = C(p,d) + min(L(p-1,d), L(p-1,d+-1)+P1, min_i L(p-1,i)+P2) - min_k L(p-1,k)."""
    D = len(C[0])
    L = [list(C[0])]
    for c_p in C[1:]:
        prev = L[-1]
        m = min(prev)
        cur = []
        for d in range(D):
            best = prev[d]
            if d > 0:
                best = min(best, prev[d - 1] + P1)
            if d < D - 1:
                best = min(best, prev[d + 1] + P1)
            best = min(best, m + P2)
            cur.append(c_p[d] + best - m)
        L.append(cur)
    return L


# Check 2: if P2 < P1, the term min_i L(p-r, i) + P2 already covers d +- 1 more cheaply, so P1
# never acts: P1 = 800, P2 = 200 gives exactly the same path costs as P1 = P2 = 200 (every change,
# even of one pixel, costs P2).
rnd = random.Random(7)
C_rand = [[rnd.randint(0, 600) for _ in range(24)] for _ in range(60)]
assert path_costs(C_rand, 800, 200) == path_costs(C_rand, 200, 200)
assert path_costs(C_rand, 200, 800) != path_costs(C_rand, 800, 800)   # with P2 > P1, P1 matters
checks += 1


def scanline_optimum(C, P1, P2):
    """Exact minimum of eq. 11 on a 1-D chain (Viterbi), returning the disparity sequence."""
    D = len(C[0])
    cost = list(C[0])
    back = []
    for c_p in C[1:]:
        new, arg = [], []
        for d in range(D):
            cands = [(cost[d], d)]
            for e in range(D):
                if abs(e - d) == 1:
                    cands.append((cost[e] + P1, e))
                elif abs(e - d) > 1:
                    cands.append((cost[e] + P2, e))
            v, e = min(cands)
            new.append(c_p[d] + v)
            arg.append(e)
        cost = new
        back.append(arg)
    d = min(range(D), key=lambda k: cost[k])
    seq = [d]
    for arg in reversed(back):
        d = arg[d]
        seq.append(d)
    return seq[::-1]


# Check 3: one horizontal path crossing a 6 px structure at disparity 30 on a background at 10,
# with a cost advantage Delta = 400 per pixel. The path keeps the structure only if
# w * Delta = 2400 exceeds the 2 * P2 paid to enter and leave it: kept for P2 = 800 and 1000,
# lost for P2 = 1300 and 3200.
Dn, delta, w = 40, 400, 6
truth_row = [10] * 15 + [30] * w + [10] * 15
row_cost = [[0 if d == t else delta for d in range(Dn)] for t in truth_row]
for p2, kept in ((800, True), (1000, True), (1300, False), (3200, False)):
    seq = scanline_optimum(row_cost, 200, p2)
    assert (seq[15:15 + w] == [30] * w) == kept and (w * delta > 2 * p2) == kept
checks += 1

# Check 4: synthetic SGM (eq. 13 in 8 directions, summed as eq. 14, winner-take-all) on a
# 40 x 30 image, D = 40. Background at disparity 10; a 6 px wide, full-height upright at 30
# (cost advantage 400); four 3 x 3 blobs whose pixels have a spurious minimum (cost 0 at a wrong
# disparity, 200 at the true one).
W, H = 40, 30
DIRS8 = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def toy_cost():
    truth = [[30 if 18 <= x < 24 else 10 for x in range(W)] for _ in range(H)]
    C = [[[delta] * Dn for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            C[y][x][truth[y][x]] = 0
    blob = []
    for by, bx, dn in ((4, 4, 25), (4, 30, 3), (22, 5, 38), (24, 32, 2)):
        for y in range(by, by + 3):
            for x in range(bx, bx + 3):
                C[y][x][dn] = 0
                C[y][x][10] = delta // 2
                blob.append((y, x))
    return C, truth, blob


def sgm(C, P1, P2, dirs=DIRS8):
    S = [[[0] * Dn for _ in range(W)] for _ in range(H)]
    for dx, dy in dirs:
        L = [[None] * W for _ in range(H)]
        xs = range(W) if dx >= 0 else range(W - 1, -1, -1)
        ys = range(H) if dy >= 0 else range(H - 1, -1, -1)
        for y in ys:
            for x in xs:
                px, py = x - dx, y - dy
                if 0 <= px < W and 0 <= py < H:
                    cur = path_costs([L[py][px], C[y][x]], P1, P2)[1]
                    # path_costs treats its first row as costs already aggregated: exact eq. 13
                else:
                    cur = list(C[y][x])
                L[y][x] = cur
                for d in range(Dn):
                    S[y][x][d] += cur[d]
    return [[min(range(Dn), key=lambda d: S[y][x][d]) for x in range(W)] for y in range(H)]


C2, truth2, blob2 = toy_cost()
upright = [(y, x) for y in range(H) for x in range(W) if truth2[y][x] == 30]
results = {}
for p2 in (250, 800, 1600, 3200):
    disp = sgm(C2, 200, p2)
    kept = sum(abs(disp[y][x] - 30) <= 1 for y, x in upright) / len(upright)
    cleaned = sum(abs(disp[y][x] - 10) <= 1 for y, x in blob2) / len(blob2)
    results[p2] = (kept, cleaned)
# P2 = 250: blobs survive (0 % cleaned), upright kept; 800 and 1600: blobs removed, upright kept;
# 3200: blobs removed, upright erased (at most 5 % of its pixels kept).
assert results[250] == (1.0, 0.0)
assert results[800] == (1.0, 1.0) and results[1600] == (1.0, 1.0)
assert results[3200][1] == 1.0 and results[3200][0] <= 0.05
checks += 1

# Check 5: the directions disagree. The two horizontal paths alone lose the upright at P2 = 1600,
# as the single-path bound predicts (2400 < 3200); the two vertical paths, which run along the
# upright without any jump, keep it even at 3200; the 8-direction sum keeps it at 1600 and loses
# it at 3200.


def kept_fraction(dirs, p2):
    disp = sgm(C2, 200, p2, dirs)
    return sum(abs(disp[y][x] - 30) <= 1 for y, x in upright) / len(upright)


assert 6 * delta < 2 * 1600
assert kept_fraction([(1, 0), (-1, 0)], 1600) == 0.0
assert kept_fraction([(0, 1), (0, -1)], 3200) == 1.0
assert results[1600][0] == 1.0 and results[3200][0] <= 0.05; checks += 1

print(f"61-stereo-profondeur (CV-STEREO-005): {checks} checks passed")
