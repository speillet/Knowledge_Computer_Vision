"""Recompute the constructed numbers added to CV-IOU-AP-003 and CV-IOU-AP-007, and the
coordinates of vault/99-Ressources/cv-iou-ap-duplicate-envelope.svg (2026-11-16).

Stdlib only. Run from the repository root with:
    python3 -I docs/revues/2026-11-16-card-depth/checks/131-iou-ap-coco.py
The accumulation mirrors pycocotools cocoeval.py at commit 8c9bcc3: cumulative TP and FP
(L375-L379), precision tp / (tp + fp + eps) (L384-L385), right-to-left envelope (L398-L400),
left-sided searchsorted over recThrs = linspace(0, 1, 101) with zero for unreachable levels
(L402-L408, L507); greedy matching per IoU threshold in score order (L272-L296).
"""
import xml.dom.minidom as minidom
from fractions import Fraction
from math import comb
from pathlib import Path

checks = 0
EPS = 2.220446049250313e-16                       # np.spacing(1)
REC_THRS = [i * 0.01 for i in range(100)] + [1.0]  # np.linspace(0, 1, 101): i * step, last = stop
IOU_THRS = [0.5 + i * (0.45 / 9) for i in range(9)] + [0.95]


def accumulate(statuses, n_gt, exact=False):
    """Return recalls, precisions, envelope and the 101 samples q_m for one ranked list."""
    tp = fp = 0
    rc, pr = [], []
    for s in statuses:
        if s == "TP":
            tp += 1
        else:
            fp += 1
        if exact:
            rc.append(Fraction(tp, n_gt)); pr.append(Fraction(tp, tp + fp))
        else:
            rc.append(tp / n_gt); pr.append(tp / (fp + tp + EPS))
    env = pr[:]
    for i in range(len(env) - 1, 0, -1):
        if env[i] > env[i - 1]:
            env[i - 1] = env[i]
    thrs = [Fraction(m, 100) for m in range(101)] if exact else REC_THRS
    q = []
    for t in thrs:
        idx = next((i for i, r in enumerate(rc) if r >= t), None)
        q.append(env[idx] if idx is not None else 0)
    return rc, pr, env, q


def ap(statuses, n_gt, exact=False):
    q = accumulate(statuses, n_gt, exact)[3]
    return sum(q) / 101 if not exact else Fraction(sum(q)) / 101


# 1. The figure's two lists (4 objects): duplicate at rank 2, then ranked last.
A = ["TP", "FP", "TP", "TP", "TP"]
B = ["TP", "TP", "TP", "TP", "FP"]
rc, pr, env, q = accumulate(A, 4, exact=True)
assert rc == [Fraction(1, 4), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), 1]
assert pr == [1, Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5)]
assert env == [1, Fraction(4, 5), Fraction(4, 5), Fraction(4, 5), Fraction(4, 5)]
assert q.count(1) == 26 and q.count(Fraction(4, 5)) == 75
assert ap(A, 4, exact=True) == Fraction(86, 101)
assert abs(ap(A, 4) - 86 / 101) < 1e-12 and round(86 / 101, 3) == 0.851
assert Fraction(101, 101) - Fraction(86, 101) == Fraction(75, 101) * Fraction(1, 5)
assert round(15 / 101, 3) == 0.149
assert ap(B, 4, exact=True) == 1 and abs(ap(B, 4) - 1) < 1e-12
checks += 1

# 2. Rank effect: a duplicate right after the k-th TP of N costs 1/(N+1) on every recall
#    level above k/N, because the best later precision is N/(N+1).
for N in range(1, 11):
    for k in range(1, N + 1):
        lst = ["TP"] * k + ["FP"] + ["TP"] * (N - k)
        _, _, env, q = accumulate(lst, N, exact=True)
        affected = sum(1 for m in range(101) if Fraction(m, 100) > Fraction(k, N))
        assert ap(lst, N, exact=True) == 1 - Fraction(affected, 101) * Fraction(1, N + 1)
        if k < N:
            assert env[k] == Fraction(N, N + 1)
        same = abs(ap(lst, N) - float(ap(lst, N, exact=True))) < 1e-12
        # Float recall levels follow numpy: 70 * 0.01 = 0.7000000000000001 > 0.7, so the
        # level 0.70 skips a rank whose recall is exactly 7/10 (observation, not in the cards).
        assert same == ((N, k) != (10, 7)), (N, k)
quirk = ["TP"] * 7 + ["FP"] + ["TP"] * 3
assert abs(float(ap(quirk, 10, exact=True)) - ap(quirk, 10) - 1 / 1111) < 1e-12
four = [ap(["TP"] * k + ["FP"] + ["TP"] * (4 - k), 4, exact=True) for k in (1, 2, 3, 4)]
assert four == [Fraction(86, 101), Fraction(91, 101), Fraction(96, 101), 1]
assert ap(["TP", "FP", "TP"], 2, exact=True) == Fraction(51, 101) + Fraction(50, 101) * Fraction(2, 3)
checks += 1


# 3. Which box is the duplicate depends on the IoU threshold (one ordinary object).
def match(ious_by_score, t):
    """Greedy matching of evaluateImg for one GT: returns TP/FP per detection in score order."""
    taken, out = False, []
    for iou in ious_by_score:
        thr = min(t, 1 - 1e-10)
        if not taken and not iou < thr:
            taken = True; out.append("TP")
        else:
            out.append("FP")
    return out


per_t = [match([0.72, 0.88], t) for t in IOU_THRS]
assert per_t[:5] == [["TP", "FP"]] * 5            # t = 0.50 ... 0.70
assert per_t[5:8] == [["FP", "TP"]] * 3           # t = 0.75, 0.80, 0.85
assert per_t[8:] == [["FP", "FP"]] * 2            # t = 0.90, 0.95
aps = [ap(s, 1, exact=True) for s in per_t]
assert aps == [1] * 5 + [Fraction(1, 2)] * 3 + [0] * 2
assert sum(aps) / 10 == Fraction(13, 20)          # COCO AP of this category: 0.65
assert abs(sum(ap(s, 1) for s in per_t) / 10 - 0.65) < 1e-12
checks += 1

# 4. Figure coordinates: X = 90 + 400 r, Y = base - 180 p, base 300 (A) and 610 (B).
svg = Path(__file__).resolve().parents[4] / "vault/99-Ressources/cv-iou-ap-duplicate-envelope.svg"
dom = minidom.parse(str(svg))
groups = {g.getAttribute("id"): g for g in dom.getElementsByTagName("g") if g.hasAttribute("id")}
paths = {p.getAttribute("id"): p.getAttribute("d") for p in dom.getElementsByTagName("path") if p.hasAttribute("id")}
for panel, lst, base in (("A", A, 300), ("B", B, 610)):
    rc, pr, env, q = accumulate(lst, 4, exact=True)
    circles = groups[f"apdup-{panel}-samples"].getElementsByTagName("circle")
    assert len(circles) == 101
    for m, c in enumerate(circles):
        assert abs(float(c.getAttribute("cx")) - (90 + 4 * m)) < 1e-9
        assert abs(float(c.getAttribute("cy")) - (base - 180 * float(q[m]))) < 1e-9
    raw = groups[f"apdup-{panel}-raw"].getElementsByTagName("circle")
    assert len(raw) == 5
    for c, r, p, s in zip(raw, rc, pr, lst):
        assert abs(float(c.getAttribute("cx")) - (90 + 400 * float(r))) < 1e-9
        assert abs(float(c.getAttribute("cy")) - (base - 180 * float(p))) < 0.01
        assert (c.getAttribute("fill") == "#b91c1c") == (s == "FP")
assert paths["apdup-A-envelope"] == "M90,120 H190 V156 H490"     # 1 up to recall 0.25, then 0.8
assert paths["apdup-B-envelope"] == "M90,430 H490"
lost = [r for r in dom.getElementsByTagName("rect") if r.getAttribute("id") == "apdup-A-lost"][0]
assert (lost.getAttribute("x"), lost.getAttribute("y"), lost.getAttribute("width"), lost.getAttribute("height")) == ("190", "120", "300", "36")
checks += 1

# 5. CV-IOU-AP-007: an unweighted category mean can rise while the critical class falls.
mean_a = (4 * Fraction(85, 100) + Fraction(30, 100)) / 5
mean_b = (4 * Fraction(90, 100) + Fraction(20, 100)) / 5
assert (mean_a, mean_b) == (Fraction(74, 100), Fraction(76, 100))
checks += 1


# 6. CV-IOU-AP-007: evidence for recall on a critical subgroup (exact binomial, one-sided 95%).
def lower_bound(x, n, alpha=0.05):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        tail = sum(comb(n, j) * mid ** j * (1 - mid) ** (n - j) for j in range(x, n + 1))
        lo, hi = (mid, hi) if tail < alpha else (lo, mid)
    return lo


lb = lower_bound(19, 20)
assert abs(lb - 0.784) < 5e-4, lb                # 19 of 20 found: recall may be as low as 0.78
assert 0.95 ** 59 < 0.05 < 0.95 ** 58             # 59 of 59 needed to show recall >= 0.95
checks += 1

print(f"131-iou-ap-coco (CV-IOU-AP-003, CV-IOU-AP-007, figure): {checks} checks passed")
