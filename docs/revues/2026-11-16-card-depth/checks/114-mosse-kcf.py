"""Recompute the constructed numbers added to CV-CORRELATION-005 and reference
114-mosse-kcf (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/114-mosse-kcf.py
One-pass evaluation (OPE), success rate and AUC: Wu, Lim and Yang 2013, Sec. 4.
Resets after N_skip = 5 frames and N_burnin = 10 frames excluded from accuracy; NOR and WIR
estimators, eqs. 5-8: Kristan et al. 2016, Sec. 3 and Sec. 3.2.1.
The two trackers and the 300-frame sequence are constructed.
"""

checks = 0
N = 300


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


def one_pass(overlaps):
    mean = sum(overlaps) / len(overlaps)
    success_05 = sum(o > 0.5 for o in overlaps) / len(overlaps)
    return mean, success_05


def with_resets(iou_tracking, fail_frame, n=N, skip=5, burnin=10):
    """VOT-style: failure when the overlap drops to zero, re-initialization `skip` frames later,
    `burnin` frames after the re-initialization excluded from accuracy (1-based frames)."""
    valid = []
    failures = 0
    t = 1
    reinit = None
    while t <= n:
        if fail_frame is not None and t == fail_frame and failures == 0:
            failures += 1
            valid.append(0.0)                      # the failure frame itself (overlap 0)
            reinit = t + skip
            t = reinit
            continue
        if reinit is not None and reinit <= t < reinit + burnin:
            t += 1
            continue                                # burn-in: tracked but not counted
        valid.append(iou_tracking)
        t += 1
    return sum(valid) / len(valid), failures, len(valid)


# Tracker A: IoU 0.70 while tracking, lost for good at frame 101 (no reset); tracker B: 0.60, never fails.
a_ope = [0.70] * 100 + [0.0] * 200
b_ope = [0.60] * N
ma, sa = one_pass(a_ope)
mb, sb = one_pass(b_ope)
assert close(ma, 70 / 300) and round(ma, 2) == 0.23 and close(sa, 1 / 3)
assert close(mb, 0.60) and close(sb, 1.0)
checks += 1

# Success-plot AUC equals the mean overlap when thresholds cover [0, 1] uniformly (project
# derivation: integrate the indicator of IoU > t over t). Discrete check with 10,001 thresholds.
def auc(overlaps, steps=10000):
    return sum(sum(o > k / steps for o in overlaps) / len(overlaps) for k in range(steps + 1)) / (steps + 1)

assert close(auc(a_ope), ma, 2e-3) and close(auc(b_ope), mb, 2e-3)
checks += 1

acc_a, fail_a, n_valid = with_resets(0.70, 101)
acc_b, fail_b, _ = with_resets(0.60, None)
assert fail_a == 1 and fail_b == 0 and n_valid == 300 - 5 - 10 + 1   # frames 102-105 skipped, 106-115 burn-in
assert round(acc_a, 2) == 0.70 and close(acc_b, 0.60)
assert acc_a > acc_b and ma < mb                                     # the ranking flips with the protocol
checks += 1

# Timing of the failure changes the one-pass score: failing at frame 281 gives 0.653 > 0.60.
late = [0.70] * 280 + [0.0] * 20
assert close(one_pass(late)[0], 0.70 * 280 / 300) and one_pass(late)[0] > mb
checks += 1

# Kristan et al., eq. 5: expected NOR overlap mu_A (1 - p / 2) for a uniformly placed critical
# point; simulate the uniform failure position for p = 1 and mu_A = 0.7.
mu, p = 0.7, 1.0
expected = sum(mu * (k / N) for k in range(N)) / N                  # failure after k tracked frames
assert close(expected, mu * (1 - p / 2), 2e-3) and close(mu * (1 - p / 2), 0.35)
checks += 1

print(f"114-mosse-kcf (CV-CORRELATION-005): {checks} checks passed")
