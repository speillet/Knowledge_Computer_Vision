"""Recompute the constructed examples of CV-METRIQUES-TEMPS (reference 132-tracking-trajectoires).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/132-tracking-trajectoires.py
Definitions follow CLEAR MOT (Bernardin and Stiefelhagen 2008, eqs. 1-2), IDF1
(Ristani et al. 2016, eqs. 6-11), HOTA (Luiten et al. 2021, eqs. 10-21) and the
trajectory errors of Sturm et al. 2012 (Sec. VII) and Zhang and Scaramuzza 2018
(Sec. III). The sequences are constructed; every box is assumed to overlap its
object perfectly, so matching is trivial and only identities vary.
"""

import itertools
import math


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


# A sequence is a list of frames; each frame is a list of (gt_id or None, pr_id or None).
# (g, p) is a TP, (g, None) a FN, (None, p) a FP.

def mota(seq):
    """MOTA = 1 - (FN + FP + IDSW) / GT; IDSW against the last matched prediction of each gt id."""
    fn = fp = idsw = n_gt = 0
    last = {}
    for frame in seq:
        for g, p in frame:
            if g is not None:
                n_gt += 1
            if g is not None and p is None:
                fn += 1
            elif g is None and p is not None:
                fp += 1
            elif g is not None and p is not None:
                if g in last and last[g] != p:
                    idsw += 1
                last[g] = p
    return 1 - (fn + fp + idsw) / n_gt, idsw


def idf1(seq):
    """IDF1 = 2 IDTP / (2 IDTP + IDFP + IDFN) with the best one-to-one gt-id to pr-id assignment."""
    co = {}
    n_g = n_p = 0
    gts, prs = set(), set()
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
    best = 0
    padded = prs + [None] * len(gts)
    for perm in itertools.permutations(padded, len(gts)):
        best = max(best, sum(co.get((g, p), 0) for g, p in zip(gts, perm) if p is not None))
    idtp = best
    idfn, idfp = n_g - idtp, n_p - idtp
    return 2 * idtp / (2 * idtp + idfp + idfn)


def hota_single_alpha(seq):
    """DetA, AssA and HOTA at one alpha (all TPs above it) from eqs. 13-21 of the HOTA paper."""
    tp = fn = fp = 0
    pair = {}
    g_count, p_count = {}, {}
    for frame in seq:
        for g, p in frame:
            if g is not None:
                g_count[g] = g_count.get(g, 0) + 1
            if p is not None:
                p_count[p] = p_count.get(p, 0) + 1
            if g is not None and p is not None:
                tp += 1
                pair[(g, p)] = pair.get((g, p), 0) + 1
            elif g is not None:
                fn += 1
            else:
                fp += 1
    det_a = tp / (tp + fn + fp)
    # A(c) = |TPA| / (|TPA| + |FNA| + |FPA|) = n_gp / (n_g + n_p - n_gp) for every TP c of the pair (g, p)
    ass_a = sum(n * n / (g_count[g] + p_count[p] - n) for (g, p), n in pair.items()) / tp
    return det_a, ass_a, math.sqrt(det_a * ass_a)


checks = 0
N = 10  # frames per scenario, two objects A and B

swap = [[("A", 1), ("B", 2)] if t < 5 else [("A", 2), ("B", 1)] for t in range(N)]
frag = [[("A", 1), ("B", 2)] if t < 5 else [("A", 3), ("B", 2)] for t in range(N)]
miss = [[("A", 1), ("B", 2)] if t < 5 else [("A", 1), ("B", None)] for t in range(N)]
fixed = [[("A", 2), ("B", 1)] if t in (5, 6) else [("A", 1), ("B", 2)] for t in range(N)]

# Check 1: an ID swap of two perfectly detected objects at frame 6 gives MOTA 0.90 (2 IDSW / 20 GT).
m, sw = mota(swap)
assert sw == 2 and close(m, 0.90)
checks += 1
# Check 2: ... IDF1 0.5 (best bijection explains only half of the frames).
assert close(idf1(swap), 0.5)
checks += 1
# Check 3: ... DetA 1, AssA 1/3, HOTA 0.5774.
d, a, h = hota_single_alpha(swap)
assert close(d, 1.0) and close(a, 1 / 3) and close(h, 0.57735)
checks += 1
# Check 4: a fragmentation (new ID for A from frame 6) gives MOTA 0.95, IDF1 0.75, AssA 0.75, HOTA 0.8660.
m, sw = mota(frag)
d, a, h = hota_single_alpha(frag)
assert sw == 1 and close(m, 0.95) and close(idf1(frag), 0.75)
assert close(a, 0.75) and close(h, 0.86603)
checks += 1
# Check 5: B missed in frames 6-10 with correct IDs gives MOTA 0.75, IDF1 0.8571, DetA 0.75, AssA 0.8333, HOTA 0.7906.
m, sw = mota(miss)
d, a, h = hota_single_alpha(miss)
assert sw == 0 and close(m, 0.75) and close(idf1(miss), 30 / 35)
assert close(d, 0.75) and close(a, 12.5 / 15) and close(h, 0.79057)
checks += 1
# Check 6: swapping at frame 6 and back at frame 8 doubles IDSW (MOTA 0.80 < 0.90) while IDF1 rises to 0.80
# and HOTA to 0.7454: MOTA penalizes the correction, identity metrics reward it.
m, sw = mota(fixed)
d, a, h = hota_single_alpha(fixed)
assert sw == 4 and close(m, 0.80) and close(idf1(fixed), 0.80)
assert close(a, (16 * 8 / 12 + 4 * 2 / 18) / 20) and close(h, 0.74536)
checks += 1

# --- Example C: frame-rate dependence of MOTA ----------------------------------
# Two objects for 100 frames; one object missed for 10 frames; 2 switches. Doubling the frame rate doubles
# the GT and FN counts but not the number of switch events.
gt_1x, fn_1x, idsw = 200, 10, 2
gt_2x, fn_2x = 400, 20
mota_1x = 1 - (fn_1x + idsw) / gt_1x
mota_2x = 1 - (fn_2x + idsw) / gt_2x
# Check 7: MOTA moves from 0.940 to 0.945 and the IDSW share of the error falls from 16.7 % to 9.1 %.
assert close(mota_1x, 0.94) and close(mota_2x, 0.945)
assert close(idsw / (fn_1x + idsw), 0.1667) and close(idsw / (fn_2x + idsw), 0.0909)
checks += 1

# --- HOTA aggregation counterexample (card CV-METRIQUES-TEMPS-002) --------------
pairs = [(1.0, 0.0), (0.0, 1.0)]
mean_of_roots = sum(math.sqrt(dd * aa) for dd, aa in pairs) / 2
root_of_means = math.sqrt((sum(dd for dd, _ in pairs) / 2) * (sum(aa for _, aa in pairs) / 2))
# Check 8: averaging per-threshold HOTA gives 0, recombining the averaged components gives 0.5.
assert close(mean_of_roots, 0.0) and close(root_of_means, 0.5)
checks += 1
# Check 9: Cauchy-Schwarz bound on random-looking profiles, with equality for proportional profiles.
prof_d, prof_a = [0.9, 0.7, 0.4], [0.8, 0.6, 0.3]
lhs = sum(math.sqrt(x * y) for x, y in zip(prof_d, prof_a)) / 3
rhs = math.sqrt(sum(prof_d) / 3 * sum(prof_a) / 3)
assert lhs <= rhs
prop_a = [0.5 * x for x in prof_d]
assert close(sum(math.sqrt(x * y) for x, y in zip(prof_d, prop_a)) / 3,
             math.sqrt(sum(prof_d) / 3 * sum(prop_a) / 3), 1e-12)
checks += 1

# --- Example B: trajectory alignment and scale ---------------------------------
xs = list(range(11))                         # ground truth: 11 poses on a 10 m straight line, 1 m apart
x_bar = sum(xs) / len(xs)


def rmse_line_after_rigid(scale, yaw_deg=0.0):
    """Estimate (scale * x, 0, 0) rotated by yaw, centroids aligned, against (x, 0, 0)."""
    c, s = math.cos(math.radians(yaw_deg)), math.sin(math.radians(yaw_deg))
    tot = 0.0
    for x in xs:
        ex, ey = scale * (x - x_bar) * c, scale * (x - x_bar) * s
        tot += (ex - (x - x_bar)) ** 2 + ey ** 2
    return math.sqrt(tot / len(xs))


ate_se3 = min(rmse_line_after_rigid(1.02, yaw) for yaw in [k / 10 for k in range(-50, 51)])
# Check 10: a 2 % scale error leaves ATE = 0.02 * sqrt(10) = 0.0632 m after the best rigid alignment
# (the yaw sweep confirms that no rotation does better than the identity) ...
assert close(ate_se3, 0.02 * math.sqrt(10)) and close(ate_se3, 0.06325)
assert close(rmse_line_after_rigid(1.02, 0.0), ate_se3, 1e-12)
checks += 1
# Check 11: ... and 0 after a Sim(3) alignment with s = 1/1.02.
assert close(rmse_line_after_rigid(1.02 * (1 / 1.02)), 0.0, 1e-12)
checks += 1
# Check 12: the translational RPE of that error grows with the interval: 0.02 m over 1 m, 0.10 m over 5 m.
assert close(1.02 * 1 - 1, 0.02) and close(1.02 * 5 - 5, 0.10)
checks += 1


def rmse_tilt_after_yaw_only(theta_deg, yaw_deg):
    """Estimate tilted by pitch theta in the x-z plane, aligned by a yaw rotation plus centroid translation."""
    th, ps = math.radians(theta_deg), math.radians(yaw_deg)
    tot = 0.0
    for x in xs:
        u = x - x_bar
        ex, ey, ez = u * math.cos(th) * math.cos(ps), u * math.cos(th) * math.sin(ps), u * math.sin(th)
        tot += (ex - u) ** 2 + ey ** 2 + ez ** 2
    return math.sqrt(tot / len(xs))


best_yaw = min(rmse_tilt_after_yaw_only(1.0, yaw) for yaw in [k / 10 for k in range(-50, 51)])
# Check 13: a 1 degree tilt survives a 4-DoF (yaw + translation) alignment as ATE = sqrt(10) * 2 sin(0.5 deg) = 0.0552 m,
# whereas a full rotation alignment would remove it.
assert close(best_yaw, math.sqrt(10) * 2 * math.sin(math.radians(0.5))) and close(best_yaw, 0.05519)
checks += 1


def rmse_yawed_line(offset_yaw_deg, align_yaw_deg):
    """Estimate = ground truth rotated by a gauge yaw; alignment applies another yaw plus centroid translation."""
    return rmse_line_after_rigid(1.0, offset_yaw_deg + align_yaw_deg)


# Check 14: a pure gauge change (10 degree yaw plus any translation) is removed exactly by the 4-DoF alignment.
assert close(min(rmse_yawed_line(10.0, a / 10) for a in range(-200, 201)), 0.0, 1e-9)
checks += 1

print(f"132-tracking-trajectoires: {checks} checks passed")
