"""Recompute the constructed numbers added to CV-PIPELINE-001 and the two figures
of reference 141-contrats-profiling-video (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/141-contrats-profiling-video.py
Age definition Delta(t) = t - u(t): Yates and Kaul, arXiv 1608.08622v2, Sec. I.
Fluid backlog Q(t) = Q(0) + (lambda - mu) t and the leaky-queue wait C/lambda: reference,
"Queues and freshness". Letterbox numbers: reference worked example F.
"""

checks = 0

# Sawtooth age under constant latency L and output period 1/X: mean L + 1/(2X).
def mean_age(L, X, steps=200000):
    T = 1.0 / X
    return sum(L + (k + 0.5) * T / steps for k in range(steps)) / steps

assert abs(mean_age(0.050, 30) - (0.050 + 1 / 60)) < 1e-9
assert abs((0.050 + 1 / 60) * 1000 - 66.67) < 0.01 and abs((0.050 + 1 / 30) * 1000 - 83.33) < 0.01
checks += 1

# Backlog that never drains: lambda = mu = 240 frames/s, 2 s warm-up.
lam = mu = 240.0
q = lam * 2.0                      # frames accumulated while nothing is served
assert q == 480
for t in (1.0, 10.0, 600.0):
    assert q + (lam - mu) * t == 480   # fluid model: no drift
wait = q / mu
assert wait == 2.0; checks += 1
# Mean age with latency ~2 s plus service, at 240 outputs/s: 2 + 1/480 s.
assert abs((2.0 + 1 / (2 * 240)) - 2.00208) < 1e-5; checks += 1
# Little's law: N = lambda * W  ->  W = 480 / 240 = 2 s.
assert 480 / 240 == 2.0; checks += 1
# Dropping the oldest frame with a queue of 2: wait about C/lambda.
assert abs(2 / 240 * 1000 - 8.33) < 0.01; checks += 1

# Discrete simulation of the warm-up backlog: FIFO, one frame served per arrival.
from collections import deque
queue = deque(range(480))          # frame indices captured during the warm-up
ages = []
for n in range(480, 480 + 2400):   # 10 s more of capture at 240 frames/s
    queue.append(n)
    served = queue.popleft()
    ages.append((n - served) / 240.0)
assert all(abs(a - 2.0) < 1e-12 for a in ages); checks += 1

# Letterbox figure (worked example F): r = 1/3, p_y = 140.
r, py = 1 / 3, 140
def inv(y): return (y - py) / r
assert (round(inv(290)), round(inv(350))) == (450, 630)
assert (round(290 / r), round(350 / r)) == (870, 1050)      # padding forgotten
assert round(py / r) == 420; checks += 1
# Figure geometry: input drawn at 0.375 px/unit from y = 58; source at 0.25 px/unit from y = 370.
assert abs(58 + 290 * 0.375 - 166.75) < 1e-9 and abs(58 + 140 * 0.375 - 110.5) < 1e-9
assert abs(370 + 450 * 0.25 - 482.5) < 1e-9 and abs(370 + 870 * 0.25 - 587.5) < 1e-9
assert abs(30 + 960 * 0.25 - 270) < 1e-9; checks += 1

print(f"141-contrats-profiling-video (CV-PIPELINE-001, figures): {checks} checks passed")
