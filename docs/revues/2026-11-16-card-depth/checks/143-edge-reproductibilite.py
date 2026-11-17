"""Recompute the constructed numbers added to CV-DEPLOIEMENT-001 (reference
143-edge-reproductibilite, worked example A and required stage speedup, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/143-edge-reproductibilite.py
Sequential model (1 - f) + f / s + c: project formalization of Amdahl 1967, p. 483.
"""
checks = 0


def overall(f, s, c=0.0):
    return 1.0 / ((1 - f) + f / s + c)


def required_s(f, S):
    denom = 1.0 / S - (1 - f)
    if denom <= 0:
        return float("inf")
    return f / denom


assert abs(overall(0.1, 2) - 1.0526) < 1e-4
assert abs(1 / 0.9 - 1.1111) < 1e-4
assert abs(overall(0.1, 2, 0.05) - 1.0) < 1e-12
checks += 1

assert abs(required_s(0.1, 1.05) - 1.909) < 1e-3
assert abs(required_s(0.1, 1.10) - 11.0) < 1e-9
assert required_s(0.1, 1 / 0.9) == float("inf")
assert abs(overall(0.6, 2) - 1.4286) < 1e-4
for S in (1.01, 1.05, 1.10, 1.11):                    # round trip of the inversion
    assert abs(overall(0.1, required_s(0.1, S)) - S) < 1e-9
checks += 1

# Worked example A: 40 ms path, inference 2.5x faster plus 2 ms reformatting.
stages = {"decode": 8, "pre": 6, "infer": 20, "post": 6}
after = dict(stages, infer=20 / 2.5 + 2)
lat0, lat1 = sum(stages.values()), sum(after.values())
assert (lat0, lat1) == (40, 30) and abs(lat0 / lat1 - 1.3333) < 1e-4
assert 1 - lat1 / lat0 == 0.25                          # latency shortened by a quarter
thr0, thr1 = 1000 / max(stages.values()), 1000 / max(after.values())
assert (thr0, thr1) == (50.0, 100.0)
checks += 1

# When another stage is slower than inference, pipelined throughput does not move.
slow = {"decode": 30, "infer": 10}
slow_after = dict(slow, infer=5)
assert max(slow.values()) == max(slow_after.values()) == 30
assert sum(slow_after.values()) < sum(slow.values())    # latency still improves
checks += 1

print(f"143-edge-reproductibilite (CV-DEPLOIEMENT-001): {checks} checks passed")
