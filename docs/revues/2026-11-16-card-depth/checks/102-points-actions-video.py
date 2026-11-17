"""Recompute the constructed numbers added to CV-VIDEO-002 (reference
102-points-actions-video, worked example B refinements, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/102-points-actions-video.py
Sampling steps: TimeSformer section 4 (8 frames at a rate of 1/32); SlowFast section 3.1
(one out of tau = 16 frames) and section 3.2 (alpha = 8). The phase model is a project
construction: uniform phase, instantaneous capture.
"""
import math
from fractions import Fraction

checks = 0
fps = 30.0
d = 0.100


def p_hit(d, step):
    return min(1.0, d / step)


steps = {"timesformer": 32 / fps, "slow": 16 / fps, "fast": 2 / fps}
assert abs(steps["timesformer"] - 1.0667) < 1e-4 and abs(p_hit(d, steps["timesformer"]) - 0.094) < 5e-4
assert abs(steps["slow"] - 0.5333) < 1e-4 and abs(p_hit(d, steps["slow"]) - 0.1875) < 1e-9
assert abs(steps["fast"] * 1000 - 66.67) < 0.01 and p_hit(d, steps["fast"]) == 1.0
assert abs(p_hit(d, 1.0) - 0.1) < 1e-12
checks += 1


# Exact distribution of the number of samples inside [s, s + d) for a grid k * step,
# integrating over the phase s in [0, step) with rational arithmetic.
def count_distribution(d, step, n_phase=10000):
    counts = {}
    for i in range(n_phase):
        s = (Fraction(i) + Fraction(1, 2)) / n_phase * step   # midpoints of phase cells
        k_first = math.ceil(s / step)
        k_last = math.ceil((s + d) / step) - 1                # samples t with s <= t < s + d
        n = max(0, k_last - k_first + 1)
        counts[n] = counts.get(n, 0) + 1
    return {n: Fraction(c, n_phase) for n, c in counts.items()}


dist = count_distribution(Fraction(1, 10), Fraction(1, 25))  # 100 ms at 25 frames/s
assert dist == {2: Fraction(1, 2), 3: Fraction(1, 2)}
checks += 1
dist1 = count_distribution(Fraction(1, 10), Fraction(1))     # 1 frame/s
assert dist1 == {0: Fraction(9, 10), 1: Fraction(1, 10)}
checks += 1
# A rule needing 3 consecutive frames with a perfect detector: misses with probability 0.5.
assert dist.get(3, 0) == Fraction(1, 2)
checks += 1

# Averaging each second instead of decimating: weight d / step of the event.
weight = d / 1.0
assert abs(weight - 0.10) < 1e-12 and abs(50 * weight - 5.0) < 1e-12
# Discrete check at 30 frames/s: 3 of 30 frames carry +50 grey levels.
frames = [50.0 if 10 <= k < 13 else 0.0 for k in range(30)]
assert abs(sum(frames) / len(frames) - 5.0) < 1e-12
checks += 1

print(f"102-points-actions-video (CV-VIDEO-002): {checks} checks passed")
