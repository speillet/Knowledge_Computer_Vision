"""Recompute the constructed examples of CV-SORT (reference 111-sort).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/111-sort.py
Inputs come from SORT (arXiv 1602.00763v2, Sec. 3-4), the official code at commit 2236dff
(sort.py: noise settings L104-L112, association L154-L196, life cycle L199-L253) and the
filterpy KalmanFilter defaults P = Q = I, R = I (commit 5df4e09). The scenarios are constructed.
"""

import itertools


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


checks = 0

# --- Example A: noise settings and Kalman gains -----------------------------------------
R = [1.0, 1.0, 1.0 * 10, 1.0 * 10]                          # R[2:,2:] *= 10
P0 = [1.0 * 10] * 4 + [1.0 * 1000 * 10] * 3               # P[4:,4:] *= 1000, then P *= 10
Q = [1.0] * 4 + [0.01, 0.01, 1.0 * 0.01 * 0.01]            # Q[-1,-1] *= 0.01, then Q[4:,4:] *= 0.01
# Check 1: diagonal settings in mixed units (u, v in px^2; s in px^4; r dimensionless).
assert R == [1, 1, 10, 10] and P0 == [10, 10, 10, 10, 10000, 10000, 10000]
assert close(Q[4], 0.01, 1e-12) and close(Q[6], 1e-4, 1e-12)
checks += 1


def gains_2state(q_pos, q_vel, r, p_pos, p_vel, n):
    """Position-velocity block of SORT: F = [[1,1],[0,1]], H = [1, 0]. Returns (K_pos, K_vel) per step."""
    p00, p01, p11 = p_pos, 0.0, p_vel
    out = []
    for _ in range(n):
        a00 = p00 + 2 * p01 + p11 + q_pos
        a01 = p01 + p11
        a11 = p11 + q_vel
        s = a00 + r
        k0, k1 = a00 / s, a01 / s
        out.append((k0, k1))
        p00, p01, p11 = (1 - k0) * a00, (1 - k0) * a01, a11 - k1 * a01
    return out


g_u = gains_2state(Q[0], Q[4], R[0], P0[0], P0[4], 3000)
# Check 2: at the first update of the centre, K = (0.9999, 0.9988): the velocity becomes almost
# exactly the first observed displacement; in steady state K = (0.653, 0.0589).
assert close(g_u[0][0], 0.9999, 1e-4) and close(g_u[0][1], 0.9988, 1e-4)
assert close(g_u[-1][0], 0.6530, 1e-4) and close(g_u[-1][1], 0.0589, 1e-4)
checks += 1

g_s = gains_2state(Q[2], Q[6], R[2], P0[2], P0[6], 3000)
# Check 3: the area block (Q = 1 px^4, R = 10 px^4, Q_sdot = 1e-4) settles at K = (0.277, 0.0027),
# and its velocity gain needs hundreds of frames to converge (0.0028 after 200 updates).
assert close(g_s[-1][0], 0.2773, 1e-4) and close(g_s[-1][1], 0.00269, 1e-5)
assert close(g_s[199][1], 0.00280, 1e-5)
checks += 1

p = P0[3]
for _ in range(300):                                        # aspect ratio: random walk, no velocity
    pm = p + Q[3]
    k_r = pm / (pm + R[3])
    p = (1 - k_r) * pm
# Check 4: the aspect ratio settles at K = 0.270.
assert close(k_r, 0.2702, 1e-4)
checks += 1

# --- Example B: IoU tolerance and zero initial velocity --------------------------------


def iou_shift(w, h, dx, dy):
    """IoU of two w x h boxes offset by (dx, dy)."""
    iw, ih = max(0.0, w - abs(dx)), max(0.0, h - abs(dy))
    inter = iw * ih
    return inter / (2 * w * h - inter)


# Check 5: for a horizontal offset, IoU = (w - d)/(w + d) >= 0.3 requires d <= 0.538 w.
assert close((1 - 0.3) / (1 + 0.3), 0.5385, 1e-4)
assert iou_shift(40, 80, 21.5, 0) > 0.3 > iou_shift(40, 80, 21.6, 0)
checks += 1
# Check 6: a new track has zero velocity, so its first prediction lags by the full displacement:
# a 30 px wide box moving 20 px/frame gives IoU 0.2 < 0.3, and each frame starts a new track.
assert close(iou_shift(30, 60, 20, 0), 0.2)
checks += 1
# Check 7: halving the frame rate doubles the per-frame displacement: 12 px/frame (IoU 0.429)
# becomes 24 px/frame (IoU 0.111) for the same 30 px wide box.
assert close(iou_shift(30, 60, 12, 0), 0.4286, 1e-4) and close(iou_shift(30, 60, 24, 0), 0.1111, 1e-4)
checks += 1

# --- Example C: life cycle of the pinned implementation --------------------------------


def simulate(detected, max_age=1, min_hits=3, start_frame=10):
    """One target; detection present or not per frame; association always succeeds when both exist."""
    tracks, next_id, outputs = [], 1, {}
    for i, det in enumerate(detected):
        frame_count = start_frame + i
        for trk in tracks:                                  # predict()
            if trk["tsu"] > 0:
                trk["hit_streak"] = 0
            trk["tsu"] += 1
        if det and tracks:                                  # update() of the matched track
            trk = tracks[0]
            trk["tsu"], trk["hits"], trk["hit_streak"] = 0, trk["hits"] + 1, trk["hit_streak"] + 1
        elif det:                                           # unmatched detection -> new tracker
            tracks.append({"id": next_id, "tsu": 0, "hits": 0, "hit_streak": 0})
            next_id += 1
        out = []
        for trk in list(tracks):
            if trk["tsu"] < 1 and (trk["hit_streak"] >= min_hits or frame_count <= min_hits):
                out.append(trk["id"])
            if trk["tsu"] > max_age:
                tracks.remove(trk)
        outputs[frame_count] = out
    return outputs


# Frames 10..30, detected everywhere except frame 20.
one_miss = simulate([f != 20 for f in range(10, 31)])
shown = [f for f, o in one_miss.items() if o]
# Check 8: a track created at frame 10 is first output at frame 13 (creation + 3 updates); one missed
# detection hides it at frames 20, 21 and 22 (hit_streak restarts) and it returns at 23 with the same ID.
assert shown[0] == 13 and [f for f in range(13, 31) if not one_miss[f]] == [20, 21, 22]
assert {i for o in one_miss.values() for i in o} == {1}
checks += 1

two_miss = simulate([f not in (20, 21) for f in range(10, 31)])
# Check 9: two consecutive misses delete the track at frame 21; the detection at frame 22 creates
# ID 2, first output at frame 25: a 5-frame output gap and an identity change.
assert [f for f in range(13, 31) if not two_miss[f]] == [20, 21, 22, 23, 24]
assert two_miss[19] == [1] and two_miss[25] == [2]
checks += 1

# --- Example D: maximize IoU, then reject (card CV-SORT-005) ---------------------------
M = [[0.90, 0.31], [0.31, 0.0]]


def best_assignment(m):
    n = len(m)
    return max(itertools.permutations(range(n)), key=lambda perm: sum(m[i][perm[i]] for i in range(n)))


perm = best_assignment(M)
kept = [(i, perm[i]) for i in range(2) if M[i][perm[i]] >= 0.3]
# Check 10: the diagonal (sum 0.90) beats the crossed pairs (0.62); after rejection 1 pair remains,
# whereas the crossed assignment keeps 2 admissible pairs.
assert perm == (0, 1) and kept == [(0, 0)] and all(v > 0.3 for v in (M[0][1], M[1][0]))
checks += 1

# Check 11: the code's shortcut uses IoU > threshold while the final filter rejects IoU < threshold:
# with [[0.5, 0.0], [0.0, 0.3]] the shortcut path runs (one candidate per row and column) and the
# pair at exactly 0.3 stays unmatched, whereas a lone 0.3 pair goes through the solver and is kept.
a = [[1 if v > 0.3 else 0 for v in row] for row in [[0.5, 0.0], [0.0, 0.3]]]
assert max(map(sum, a)) == 1 and max(map(sum, zip(*a))) == 1 and a[1][1] == 0
lone = [[1 if 0.3 > 0.3 else 0]]
assert max(map(sum, lone)) == 0 and not (0.3 < 0.3)
checks += 1

# --- Example E: scalar update of card CV-SORT-003 ---------------------------------------
K = 25 / (25 + 9)
# Check 12: K = 25/34, u+ = 107.35 px, P+ = 6.62 px^2; with R = 100 px^2, u+ = 102 px.
assert close(100 + K * 10, 107.3529, 1e-4) and close((1 - K) * 25, 6.6176, 1e-4)
assert close(100 + 25 / 125 * 10, 102.0)
checks += 1

# --- Example F: MOTA weight of detection versus association -----------------------------
# Check 13: SORT on the MOT15 test set (Table 2): FN 32,615 and FP 7,318 against 1,001 ID switches,
# a 39.9 : 1 ratio, just below the 42.3 to 186.4 range that the HOTA authors report for MOT17 trackers.
assert close((32615 + 7318) / 1001, 39.89, 1e-2)
checks += 1

# Check 14: max_age = 1 frame is 33 ms at 30 frames/s and 100 ms at 10 frames/s.
assert close(1 / 30, 0.0333, 1e-4) and close(1 / 10, 0.1)
checks += 1

print(f"111-sort: {checks} checks passed")
