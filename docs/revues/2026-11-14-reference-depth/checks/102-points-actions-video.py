"""Recompute the constructed examples of CV-VIDEO (reference 102-points-actions-video).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/102-points-actions-video.py
Inputs come from TAP-Vid (arXiv 2211.03726v2, Sec. 3 and 4.3), CoTracker (2307.07635v3,
Sec. 3.3), CoTracker3 (2410.11831v1, Sec. 3) and the official co-tracker predictor
(commit 82e02e8: online window 16, step 8), SlowFast (1812.03982v3, Sec. 3.1-3.2),
TimeSformer (2102.05095v4, Sec. 4) and ActionFormer (2202.07925v2, Sec. 4).
The scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


checks = 0

# --- Example A: TAP-Vid metrics on one constructed track ------------------------------
# 10 frames. Ground truth visible on frames 1-8, occluded on 9-10.
# Prediction visible on frames 1-9, occluded on 10; within threshold on 1-6, too far on 7-8.
gt_visible = [True] * 8 + [False] * 2
pred_visible = [True] * 9 + [False]
within = [True] * 6 + [False] * 2 + [False] * 2   # only meaningful where both are visible

tp = sum(1 for g, p, w in zip(gt_visible, pred_visible, within) if g and p and w)
fp = sum(1 for g, p, w in zip(gt_visible, pred_visible, within) if p and (not g or not w))
fn = sum(1 for g, p, w in zip(gt_visible, pred_visible, within) if g and (not p or not w))
jaccard = tp / (tp + fp + fn)
delta = sum(1 for g, w in zip(gt_visible, within) if g and w) / sum(gt_visible)
oa = sum(1 for g, p in zip(gt_visible, pred_visible) if g == p) / len(gt_visible)
# Check 1: TP = 6, FP = 3 (two far points and one point predicted visible while occluded), FN = 2.
assert (tp, fp, fn) == (6, 3, 2)
checks += 1
# Check 2: Jaccard 6/11 = 0.545, position accuracy on visible frames 6/8 = 0.75, occlusion accuracy 0.9:
# a far prediction counts both as a false positive and as a false negative.
assert close(jaccard, 0.5455, 1e-4) and delta == 0.75 and oa == 0.9
checks += 1

# Check 3: TAP-Vid evaluates at 256x256; for a 1920x1080 source the 1 px threshold is 7.5 px
# horizontally and 4.22 px vertically, and the 16 px threshold is 120 px by 67.5 px.
sx, sy = 1920 / 256, 1080 / 256
assert close(sx, 7.5) and close(sy, 4.219, 1e-3) and close(16 * sx, 120) and close(16 * sy, 67.5)
checks += 1

# --- Example B: sampling grids and short events ----------------------------------------


def p_seen(duration_s, step_s):
    """Uniform phase, instantaneous capture: probability that a sample falls inside the event."""
    return min(1.0, duration_s / step_s)


FPS = 30.0
# Check 4: the card case, 100 ms event and one frame per second, gives 0.1.
assert close(p_seen(0.100, 1.0), 0.1)
checks += 1
# Check 5: TimeSformer samples 8 frames at a rate of 1/32: at 30 frames/s the step is 1.067 s,
# the first-to-last span is 7 x 32 = 224 frames (7.47 s) and a 100 ms event is sampled with p = 0.094.
step_tsf = 32 / FPS
assert close(step_tsf, 1.0667, 1e-4) and close(7 * 32 / FPS, 7.4667, 1e-4)
assert close(p_seen(0.100, step_tsf), 0.09375, 1e-5)
checks += 1
# Check 6: SlowFast 4x16 with alpha = 8 covers T x tau = 64 raw frames (2.13 s at 30 frames/s);
# the Slow pathway samples every 16 frames (p = 0.1875 for a 100 ms event), the Fast pathway every
# tau/alpha = 2 frames (66.7 ms), so any event of 100 ms contains at least one Fast sample.
T, TAU, ALPHA = 4, 16, 8
assert T * TAU == 64 and close(T * TAU / FPS, 2.1333, 1e-4)
assert close(p_seen(0.100, TAU / FPS), 0.1875) and p_seen(0.100, (TAU / ALPHA) / FPS) == 1.0
assert ALPHA * T == 32
checks += 1

# --- Example C: latency of windowed point tracking -------------------------------------
# Check 7: five future frames at 30 frames/s impose at least 167 ms of waiting (card CV-VIDEO-003).
assert close(5 / FPS, 0.1667, 1e-4)
checks += 1

WINDOW, STEP = 16, 8   # CoTracker3 online predictor: window_len = 16, step = window_len // 2


def first_and_revised_delay(t):
    """Windows end at frames STEP*k - 1 (k >= 2) and span WINDOW frames; return waits in frames."""
    first_end = max(WINDOW - 1, math.ceil((t + 1) / STEP) * STEP - 1)
    return first_end - t, first_end + STEP - t


delays = [first_and_revised_delay(t) for t in range(WINDOW, WINDOW + 64)]
# Check 8: in steady state a frame waits 0-7 frames for its first estimate and 8-15 frames until the
# next overlapping window revises it: up to 233 ms and 500 ms at 30 frames/s, before computation time.
assert min(d[0] for d in delays) == 0 and max(d[0] for d in delays) == 7
assert min(d[1] for d in delays) == 8 and max(d[1] for d in delays) == 15
assert close(7 / FPS, 0.2333, 1e-4) and close(15 / FPS, 0.5)
checks += 1


def n_windows(t_video, t_window):
    """CoTracker Sec. 3.3: J = ceil(2 T' / T - 1) windows of length T with overlap T/2."""
    return math.ceil(2 * t_video / t_window - 1)


# Check 9: a 24-frame training video with T = 8 needs 5 windows; a 100-frame video needs 24.
assert n_windows(24, 8) == 5 and n_windows(100, 8) == 24
checks += 1

# --- Example D: attention cost of TimeSformer's default clip ----------------------------
patches = (224 // 16) ** 2
tokens = 8 * patches
joint = tokens * tokens
divided = tokens * (8 + patches)
# Check 10: 196 patches per frame and 1,568 tokens; joint space-time attention compares 2.46 M pairs
# per layer and head, divided attention 0.32 M (7.7 times fewer), class token ignored.
assert patches == 196 and tokens == 1568 and joint == 2_458_624 and divided == 319_872
assert close(joint / divided, 7.686, 1e-3)
checks += 1

# --- Example E: temporal IoU and the THUMOS14 threshold range ---------------------------


def tiou(a, b):
    inter = max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
    union = max(a[1], b[1]) - min(a[0], b[0])
    return inter / union


gt, pred = (2.0, 6.0), (3.0, 6.5)
score = tiou(gt, pred)
thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
# Check 11: tIoU = 3.0 / 4.5 = 0.667: a true positive at 0.3-0.6 and a false positive at 0.7,
# so the same detection contributes to four of the five THUMOS14 thresholds.
assert close(score, 0.6667, 1e-4) and [score >= t for t in thresholds] == [True] * 4 + [False]
checks += 1

# --- Example F: averaging frame predictions ignores order -------------------------------
frames = [[0.2, 0.8], [0.6, 0.4], [0.9, 0.1]]
mean = [sum(f[i] for f in frames) / len(frames) for i in range(2)]
rev = list(reversed(frames))
mean_rev = [sum(f[i] for f in rev) / len(rev) for i in range(2)]
# Check 12: z = (1/L) sum f(I_t) is identical for a sequence and its reversal.
assert all(close(a, b, 1e-12) for a, b in zip(mean, mean_rev))
checks += 1

print(f"102-points-actions-video: {checks} checks passed")
