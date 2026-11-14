"""Recompute the constructed examples of CV-ASSOCIATION (reference 112-deepsort-bytetrack).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/112-deepsort-bytetrack.py
Inputs come from DeepSORT (arXiv 1703.07402v1, Sec. 2.2-2.3, Sec. 3) and its official code
(nwojke/deep_sort at f08cf1d: kalman_filter.py noise weights 1/20 and 1/160, chi2inv95),
ByteTrack (arXiv 2110.06864v3, Sec. 3, 4.1, 4.2) and its official code (ifzhang/ByteTrack at
d1bf019: byte_tracker.py, matching.fuse_score, tools/track.py defaults).
The scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


checks = 0

# --- Gate thresholds: chi-square quantiles with even degrees of freedom -------------------


def chi2_cdf_even(x, k):
    """Closed form for even k: 1 - exp(-x/2) * sum_{i < k/2} (x/2)^i / i!."""
    half = x / 2
    return 1 - math.exp(-half) * sum(half ** i / math.factorial(i) for i in range(k // 2))


# Check 1: DeepSORT's gate t(1) = 9.4877 is the 95% quantile of chi-square with 4 dof (position-only
# gating uses 5.9915 with 2 dof).
assert close(chi2_cdf_even(9.4877, 4), 0.95, 1e-5) and close(chi2_cdf_even(5.9915, 2), 0.95, 1e-5)
checks += 1

# Check 2: the cosine threshold 0.2 of the reference application means an angle of 36.9 degrees
# between unit embeddings (1 - cos(theta) <= 0.2).
assert close(math.degrees(math.acos(1 - 0.2)), 36.87, 1e-2)
checks += 1

# --- Example A: Mahalanobis distance and track age (DeepSORT Sec. 2.3) --------------------
H = 100.0                                   # box height in px
SW_POS, SW_VEL = 1 / 20, 1 / 160            # kalman_filter.py
Q = ((SW_POS * H) ** 2, (SW_VEL * H) ** 2)  # process noise per frame for x and its velocity
R = (SW_POS * H) ** 2                       # measurement noise on x in project()
P0 = ((2 * SW_POS * H) ** 2, (10 * SW_VEL * H) ** 2)


def run(updates, misses):
    """1-D x-axis of the DeepSORT filter: `updates` corrected frames, then `misses` predictions."""
    p00, p01, p11 = P0[0], 0.0, P0[1]

    def predict(p00, p01, p11):
        return p00 + 2 * p01 + p11 + Q[0], p01 + p11, p11 + Q[1]

    for _ in range(updates):
        p00, p01, p11 = predict(p00, p01, p11)
        s = p00 + R
        k0, k1 = p00 / s, p01 / s
        p00, p01, p11 = (1 - k0) * p00, (1 - k0) * p01, p11 - k1 * p01
    for _ in range(misses + 1):              # the frame being associated is also a prediction
        p00, p01, p11 = predict(p00, p01, p11)
    return p00 + R                           # innovation variance S on x


s_recent = run(30, 0)
s_old = run(30, 9)
offset = 20.0                                 # px between prediction and detection on x
d2_recent, d2_old = offset ** 2 / s_recent, offset ** 2 / s_old
# Check 3: with h = 100 px, a 20 px offset is 2.3 standard deviations from a track seen in the
# previous frame (S = 73.7 px^2, d^2 = 5.43) but 0.7 from a track unseen for 9 frames
# (S = 794 px^2, d^2 = 0.50): uncertainty growth makes the stale track the closer one,
# which motivates the matching cascade.
assert close(s_recent, 73.72, 0.01) and close(s_old, 794.32, 0.01)
assert close(d2_recent, 5.426, 0.001) and close(d2_old, 0.504, 0.001) and d2_old < d2_recent
checks += 1
# Check 4: noise scales with box height: halving h quarters every variance, so the same offset in
# units of box height gives the same Mahalanobis distance (SORT's constants do not scale).
ratio = (SW_POS * 50) ** 2 / (SW_POS * 100) ** 2
assert close(ratio, 0.25, 1e-12)
checks += 1

# --- Example B: ByteTrack thresholds of the official code --------------------------------
TRACK_THRESH = 0.6            # tools/track.py default, also tau in the paper
DET_THRESH = TRACK_THRESH + 0.1
LOW = 0.1


def route(score):
    if score > TRACK_THRESH:
        return "high"
    if LOW < score < TRACK_THRESH:
        return "low"
    return "dropped"


# Check 5: 0.65 goes to the first association but cannot start a track (needs >= 0.7); 0.3 can only
# extend a tracked object; 0.05 is discarded; a score of exactly 0.6 falls in neither set.
assert route(0.65) == "high" and 0.65 < DET_THRESH and route(0.3) == "low"
assert route(0.05) == "dropped" and route(0.6) == "dropped"
checks += 1


def fused_cost(iou, score):
    """matching.fuse_score: cost = 1 - IoU * score (first association and unconfirmed tracks)."""
    return 1 - iou * score


# Check 6: with fused costs, IoU 0.5 at score 0.65 costs 0.675, accepted under match_thresh 0.9;
# an unconfirmed track (threshold 0.7) needs IoU * score >= 0.3; the second association uses raw
# IoU with threshold 0.5, i.e. IoU >= 0.5.
assert close(fused_cost(0.5, 0.65), 0.675) and fused_cost(0.5, 0.65) <= 0.9
assert fused_cost(0.45, 0.65) > 0.7 and fused_cost(0.47, 0.65) <= 0.7
checks += 1

# Check 7: the lost-track buffer is int(frame_rate / 30 * 30) frames: 30 at 30 frames/s, 15 at 15,
# i.e. always 1 s, whereas SORT's max_age = 1 and DeepSORT's A_max = 30 are counted in frames.
assert int(30 / 30.0 * 30) == 30 and int(15 / 30.0 * 30) == 15 and int(60 / 30.0 * 30) == 60
checks += 1

# --- Example C: published effects, read with their side effects -------------------------
# Check 8: DeepSORT on MOT16 test: ID switches 1423 -> 781 (-45%), but false positives
# 8698 -> 12852 (+48%) and fragmentations 1835 -> 2008 (+9%) [Table 2].
assert close((781 - 1423) / 1423, -0.451, 1e-3) and close((12852 - 8698) / 8698, 0.478, 1e-3)
assert close((2008 - 1835) / 1835, 0.094, 1e-3)
checks += 1
# Check 9: ByteTrack's BYTE against SORT on MOT17 validation with the same detector:
# IDs 291 -> 159 (-45%), IDF1 76.9 -> 79.3, MOTA 74.6 -> 76.6 [Sec. 4.2].
assert close((159 - 291) / 291, -0.454, 1e-3) and close(79.3 - 76.9, 2.4) and close(76.6 - 74.6, 2.0)
checks += 1

# --- Example D: cascade versus a global assignment ---------------------------------------
# One detection, two tracks gated in: the recent track (d^2 = 5.43) and the stale one (d^2 = 0.50).
# Check 10: a global minimum-cost assignment on Mahalanobis cost gives the detection to the stale
# track; the cascade (age 1 first) gives it to the recent track before the stale one is considered.
costs = {"recent": d2_recent, "stale": d2_old}
global_choice = min(costs, key=costs.get)
cascade_choice = "recent" if d2_recent <= 9.4877 else "stale"
assert global_choice == "stale" and cascade_choice == "recent"
checks += 1

print(f"112-deepsort-bytetrack: {checks} checks passed")
