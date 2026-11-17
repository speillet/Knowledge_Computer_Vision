"""Recompute the constructed numbers added to CV-METRIQUES-TEMPS-001 and -003 and the
identity-switch figure of reference 132-tracking-trajectoires (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/132-tracking-trajectoires.py
Definitions: MOTA and IDSW as in Luiten et al. (HOTA paper) Sec. 4.1 and TrackEval clear.py at
12c8791 (IDSW against the last matched prediction of the same gt ID, L62-L97); IDF1 as in
Ristani et al. 2016 eqs. 3-11 (one-to-one ID bijection); HOTA eqs. 10-21 at one threshold.
Every box is assumed to overlap its object perfectly, so matching is trivial and only IDs vary.
ATE alignment groups: Zhang and Scaramuzza 2018, Sec. III-A and Table I.
"""

import itertools
import math
import os
import xml.dom.minidom

checks = 0


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


# A sequence is a list of frames; each frame is a list of (gt_id or None, pr_id or None).
def mota(seq):
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
    tp = fn = fp = 0
    pair, gc, pc = {}, {}, {}
    for frame in seq:
        for g, p in frame:
            if g is not None:
                gc[g] = gc.get(g, 0) + 1
            if p is not None:
                pc[p] = pc.get(p, 0) + 1
            if g is not None and p is not None:
                tp += 1
                pair[(g, p)] = pair.get((g, p), 0) + 1
            elif g is not None:
                fn += 1
            else:
                fp += 1
    det_a = tp / (tp + fn + fp)
    ass_a = sum(n * n / (gc[g] + pc[p] - n) for (g, p), n in pair.items()) / tp
    return det_a, ass_a, math.sqrt(det_a * ass_a)


def switch_at(k, frames=8):
    """A keeps ID 1 before frame k (1-based) and gets the new ID 3 from frame k; B keeps ID 2."""
    return [[("A", 1 if t < k else 3), ("B", 2)] for t in range(1, frames + 1)]


# --- CV-METRIQUES-TEMPS-001: one switch at frame 6 (the figure) -----------------------------
seq = switch_at(6)
m, sw, fn, fp = mota(seq)
assert (sw, fn, fp) == (1, 0, 0) and close(m, 1 - 1 / 16) and close(m, 0.9375)
checks += 1
f1, idtp, idfn, idfp, pairing = idf1(seq)
assert (idtp, idfn, idfp) == (13, 3, 3) and pairing == {"A": 1, "B": 2}
assert close(f1, 26 / 32) and round(f1, 2) == 0.81
checks += 1
d, a, h = hota_one_alpha(seq)
assert close(d, 1.0) and close(a, 98 / 128) and close(h, 0.875)   # AssA (25/8 + 9/8 + 8) / 16
checks += 1

# Events versus frames: MOTA ignores where the switch happens, IDF1 does not.
results = {k: (mota(switch_at(k))[0], idf1(switch_at(k))[0]) for k in range(2, 9)}
assert all(close(v[0], 0.9375) for v in results.values())
assert close(results[8][1], 30 / 32) and close(results[2][1], 30 / 32)
assert close(results[5][1], 24 / 32) and min(v[1] for v in results.values()) == results[5][1]
checks += 1

# Oracle association: replacing matched predicted IDs by the gt IDs removes the switch,
# so MOTA becomes MODA (= 1 here) and IDF1 reaches 1.
oracle = [[(g, g) for g, _ in frame] for frame in seq]
assert mota(oracle)[1] == 0 and close(mota(oracle)[0], 1.0) and close(idf1(oracle)[0], 1.0)
checks += 1

# --- Figure: read the IDs and colours drawn in the SVG and recompute from them ---------------
here = os.path.dirname(os.path.abspath(__file__))
svg = os.path.normpath(os.path.join(here, "..", "..", "..", "..", "vault", "99-Ressources",
                                    "cv-metriques-temps-id-switch.svg"))
dom = xml.dom.minidom.parse(svg)
col_centre = {98 + 48 * (k - 1): k for k in range(1, 9)}            # column k at x = 76 + 48 (k - 1)
for k in range(1, 9):
    rect = [r for r in dom.getElementsByTagName("rect") if r.getAttribute("id") == f"mt-p1-A{k}"][0]
    assert int(rect.getAttribute("x")) + 22 == 98 + 48 * (k - 1)
rows = {168: "A", 216: "B", 404: "A", 452: "B"}


def drawn_sequence(group_id):
    g = [e for e in dom.getElementsByTagName("g") if e.getAttribute("id") == group_id][0]
    cells = {}
    for t in g.getElementsByTagName("text"):
        x, y = int(t.getAttribute("x")), int(t.getAttribute("y"))
        colour = t.getAttribute("fill") or t.parentNode.getAttribute("fill")
        cells[(col_centre[x], rows[y])] = (int(t.firstChild.data), colour)
    assert len(cells) == 16
    return cells


p1, p2 = drawn_sequence("mt-p1-ids"), drawn_sequence("mt-p2-ids")
drawn = [[(r, p1[(k, r)][0]) for r in ("A", "B")] for k in range(1, 9)]
assert drawn == seq and drawn == [[(r, p2[(k, r)][0]) for r in ("A", "B")] for k in range(1, 9)]
# Panel 2: green cells are those explained by the chosen bijection, red ones are IDFN + IDFP.
green = [key for key, (pid, c) in p2.items() if c == "#15803d"]
red = [key for key, (pid, c) in p2.items() if c == "#b91c1c"]
assert len(green) == idtp == 13 and len(red) == idfn == idfp == 3
assert all(pairing[r] == p2[(k, r)][0] for k, r in green)
# Panel 1: the only red cell is the switch frame of A.
assert [key for key, (pid, c) in p1.items() if c == "#b91c1c"] == [(6, "A")]
checks += 1

# --- CV-METRIQUES-TEMPS-003: worked example B of the reference -------------------------------
xs = list(range(11))                         # 11 ground-truth poses 1 m apart on a 10 m line
u = [x - sum(xs) / len(xs) for x in xs]
assert close(sum(v * v for v in u) / len(u), 10.0)          # RMS of u is sqrt(10) m
ate_scale = math.sqrt(sum((0.02 * v) ** 2 for v in u) / len(u))
assert close(ate_scale, 0.02 * math.sqrt(10)) and round(ate_scale, 3) == 0.063
theta = math.radians(1.0)
ate_tilt = math.sqrt(sum((v * (math.cos(theta) - 1)) ** 2 + (v * math.sin(theta)) ** 2 for v in u) / len(u))
assert close(ate_tilt, math.sqrt(10) * 2 * math.sin(theta / 2)) and round(ate_tilt, 3) == 0.055
assert close(1.02 * 1 - 1, 0.02) and close(1.02 * 5 - 5, 0.10)   # RPE grows with the interval
assert close(1 / 1.02, 0.98, 1e-3)                               # Sim(3) scale that hides the error
checks += 1

print(f"132-tracking-trajectoires (CV-METRIQUES-TEMPS-001, -003, figure): {checks} checks passed")
