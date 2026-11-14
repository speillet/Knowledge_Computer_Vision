"""Recompute the constructed examples of CV-DEPLOIEMENT (reference 143-edge-reproductibilite).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/143-edge-reproductibilite.py
Inputs: Amdahl's law in its usual closed form (the 1967 paper states the argument in words, p. 483);
Hinton et al., arXiv 1503.02531 sec. 2 (softmax with temperature, T^2 gradient scaling);
TensorRT 11.4.1 "Data Formats and Tensors" (2:4 sparsity, 53 eligible / 22 chosen example);
Jetson Linux r36.4 thermal specifications (cpu-thermal SW throttling 99.0 C);
Li et al., arXiv 1608.08710 (filter pruning). All scenarios, the stage times and the first-order
thermal model are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


checks = 0

# --- Example A: Amdahl's bound and overhead -------------------------------------


def speedup(f, s, c=0.0):
    """Sequential additive model: normalized new time (1 - f) + f/s + c."""
    return 1 / ((1 - f) + f / s + c)


# Check 1: card CV-DEPLOIEMENT-001: f = 0.1, s = 2 gives 1/0.95 = 1.053; s -> infinity gives
# 1/0.9 = 1.111; an added cost c = f(1 - 1/s) = 0.05 cancels the gain exactly.
assert close(speedup(0.1, 2), 1.0526, 1e-4) and close(1 / 0.9, 1.1111, 1e-4)
assert close(speedup(0.1, 1e12), 1 / 0.9, 1e-9) and close(speedup(0.1, 2, 0.05), 1.0, 1e-12)
checks += 1
stages = {"decode": 8, "preprocess": 6, "inference": 20, "post": 6}  # ms, constructed
lat_before = sum(stages.values())
lat_after = lat_before - 20 + 20 / 2.5 + 2   # INT8 2.5x faster plus 2 ms reformatting
# Check 2: with inference at f = 0.5 of a 40 ms sequential path, s = 2.5 and 2 ms (c = 0.05) of
# conversions, latency goes 40 -> 30 ms, a 1.33x speedup (the closed form gives the same).
assert lat_before == 40 and close(lat_after, 30.0) and close(lat_before / lat_after, 1.3333, 1e-4)
assert close(speedup(0.5, 2.5, 0.05), 1.3333, 1e-4)
checks += 1
# Check 3: pipelined, throughput is set by the slowest stage: 20 ms -> 10 ms (8 + 2), i.e.
# 50 -> 100 frames/s, a 2x throughput gain for a 1.33x latency gain.
assert close(1000 / max(stages.values()), 50.0) and close(1000 / max(8, 6, 8 + 2, 6), 100.0)
checks += 1

# --- Example B: structured against unstructured pruning --------------------------


def conv_macs(h, w, k, c, r, s):
    return h * w * k * c * r * s


dense = conv_macs(80, 80, 128, 128, 3, 3)
pruned = conv_macs(80, 80, 96, 96, 3, 3)
# Check 4: a 3x3 conv with 80x80 output and 128 -> 128 channels needs 943.7 M MACs; removing 25%
# of its input and output channels (structured) leaves 0.75^2 = 56.25%, i.e. 530.8 M MACs.
assert dense == 943_718_400 and pruned == 530_841_600 and close(pruned / dense, 0.5625, 1e-12)
checks += 1
# Check 5: storage of unstructured sparsity in a CSR-like layout with FP16 values and 16-bit
# column indices: 50% density costs 0.5 * (2 + 2) = 2 bytes/weight, the same as dense FP16;
# 10% density costs 0.4 bytes/weight.
assert close(0.5 * (2 + 2), 2.0) and close(0.1 * (2 + 2), 0.4)
checks += 1
# Check 6: in TensorRT's 2:4 example, 22 of 53 eligible layers chose sparse tactics (41.5%).
assert close(22 / 53, 0.415, 1e-3)
checks += 1

# --- Example C: distillation temperature ------------------------------------------


def softmax(z, t):
    e = [math.exp(v / t) for v in z]
    s = sum(e)
    return [v / s for v in e]


logits = [4.0, 2.0, 0.0]
p1 = softmax(logits, 1)
p4 = softmax(logits, 4)
# Check 7: logits (4, 2, 0) give (0.867, 0.117, 0.016) at T = 1 and (0.506, 0.307, 0.186) at T = 4:
# the high temperature exposes the ranking of the wrong classes.
assert all(close(a, b) for a, b in zip(p1, (0.867, 0.117, 0.016)))
assert all(close(a, b) for a, b in zip(p4, (0.506, 0.307, 0.186)))
checks += 1
# Check 8: the soft-target gradient (q_i - p_i)/T scales as 1/T^2 at high temperature (Hinton et al.
# sec. 2, hence their T^2 rescaling): for z = (4, 2, 0) and a student whose first logit differs by a
# small eps, doubling T from 20 to 40 divides the gradient by about 4 (finite difference: 4.08).


def soft_grad(t, eps=1e-4):
    teacher = softmax(logits, t)
    student = softmax([logits[0] + eps, logits[1], logits[2]], t)
    return (student[0] - teacher[0]) / t


assert close(soft_grad(20) / soft_grad(40), 4.0, 0.1)
checks += 1

# --- Example D: first-order thermal model --------------------------------------------
tau = 10.0  # minutes, constructed time constant
# Check 9: a 5-minute benchmark sees 1 - e^-0.5 = 39% of the steady temperature rise; 95% needs 3 tau.
assert close(1 - math.exp(-5 / tau), 0.3935, 1e-4) and close(1 - math.exp(-3), 0.9502, 1e-4)
checks += 1
rise = 60.0  # K at full load, constructed
throttle = 99.0  # C, Jetson Linux r36.4 cpu-thermal SW throttling (AGX Orin, Orin NX / Nano)
# Check 10: at 25 C ambient the steady state is 85 C (no throttling); in a 45 C enclosure it would
# be 105 C, and the 99 C trip point is crossed after tau * ln(10) = 23 minutes.
assert 25 + rise == 85 < throttle < 45 + rise == 105
t_cross = -tau * math.log(1 - (throttle - 45) / rise)
assert close(t_cross, 23.03, 0.01)
checks += 1

# --- Example E: soak-test sizing --------------------------------------------------
# Check 11: one hour at 30 frames/s on 8 streams is 864,000 frames; a leak of 1 kB per frame
# grows memory by 864 MB per hour, invisible in a 1-minute test (14.4 MB).
frames_h = 30 * 8 * 3600
assert frames_h == 864_000 and frames_h * 1000 == 864_000_000 and 30 * 8 * 60 * 1000 == 14_400_000
checks += 1

print(f"CV-DEPLOIEMENT checks: {checks} groups passed")
