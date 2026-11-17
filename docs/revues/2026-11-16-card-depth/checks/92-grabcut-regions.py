"""Recompute the constructed numbers added to CV-GRABCUT-001 to 003 and check the
geometry of the figure cv-grabcut-graph.svg (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/92-grabcut-regions.py
Constants gamma = 50 and lambda = 9 * gamma: OpenCV 4.13.0 grabcut.cpp L582-L583.
Mixture density in the t-links: grabcut.cpp L113-L119 and L483-L484.
"""
import math

checks = 0

# Worked example B (card 002): a definite pixel cannot be moved by the cut.
gamma = 50.0
lam = 9 * gamma
nsum = 4 * gamma + 4 * gamma / math.sqrt(2)      # eight n-links at zero contrast
assert abs(nsum - 341.42) < 0.01 and lam == 450 and lam > nsum
assert abs((1 + nsum) - 342.42) < 0.01            # Boykov and Jolly's K
checks += 1


# Worked example D (card 001): mixture weights decide the grey pixels.
def gauss3(z, mu, sigma):
    d2 = sum((a - b) ** 2 for a, b in zip(z, mu))
    return math.exp(-0.5 * d2 / sigma ** 2) / (sigma ** 3)   # common constant dropped


def mix(z, comps):
    return sum(w * gauss3(z, mu, s) for w, mu, s in comps)


grey, red = (128, 128, 128), (200, 30, 30)
fg = [(0.6, red, 10.0), (0.4, grey, 10.0)]
bg_only_grey = [(1.0, grey, 10.0)]
d_fg = -math.log(mix(grey, fg))
d_bg = -math.log(mix(grey, bg_only_grey))
assert abs((d_fg - d_bg) - math.log(1 / 0.4)) < 1e-9         # background cheaper
assert abs(math.log(1 / 0.4) - 0.92) < 0.005
bg_30 = [(0.3, grey, 10.0), (0.7, (240, 240, 240), 10.0)]     # grey only 30 % outside
d_bg30 = -math.log(mix(grey, bg_30))
assert abs((d_bg30 - d_fg) - math.log(0.4 / 0.3)) < 1e-9     # foreground cheaper
assert abs(math.log(0.4 / 0.3) - 0.29) < 0.005
# After the refit the foreground mixture holds only red: grey becomes very expensive.
fg_refit = [(1.0, red, 10.0)]
assert -math.log(max(mix(grey, fg_refit), 1e-300)) - d_bg > 100
checks += 1

# Worked example E (card 002): IoU ceiling when 20 rows fall outside the rectangle.
obj = 100 * 300
fixed_bg = 100 * 20
assert fixed_bg == 2000
assert abs((obj - fixed_bg) / obj - 0.9333) < 1e-4
checks += 1

# Worked example F (card 003): interaction budget and break-even operator time.
h = 4.0
cost_a = 6 * (h + 0.1)
cost_b = 2 * (h + 1.5)
assert abs(cost_a - 24.6) < 1e-9 and abs(cost_b - 11.0) < 1e-9
assert abs(1.5 / 0.1 - 15) < 1e-9
h_even = (2 * 1.5 - 6 * 0.1) / (6 - 2)
assert abs(h_even - 0.6) < 1e-9
assert abs(6 * (h_even + 0.1) - 2 * (h_even + 1.5)) < 1e-9
checks += 1

# Figure geometry: the cut polyline must cross exactly the links it severs.
S, T = (270.0, 96.0), (270.0, 464.0)
xs = [70.0, 170.0, 270.0, 370.0, 470.0]
P = [(x, 280.0) for x in xs]
links = {}
for i, p in enumerate(P, 1):
    links[f"S{i}"] = (S, p)
    links[f"T{i}"] = (p, T)
for i in range(4):
    links[f"N{i + 1}{i + 2}"] = (P[i], P[i + 1])
cut = [(16, 400), (285, 400), (320, 280), (345, 200), (524, 200)]


def inter(p1, p2, q1, q2):
    """Intersection point of two closed segments, or None (no collinear overlap here)."""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, q1, q2
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / den
    if -1e-12 <= t <= 1 + 1e-12 and -1e-12 <= u <= 1 + 1e-12:
        return (round(x1 + t * (x2 - x1), 6), round(y1 + t * (y2 - y1), 6))
    return None


crossed = {}
for name, (a, b) in links.items():
    pts = set()
    for c1, c2 in zip(cut, cut[1:]):
        q = inter(c1, c2, a, b)
        if q is not None:
            pts.add(q)
    if pts:
        crossed[name] = pts
assert set(crossed) == {"T1", "T2", "T3", "N34", "S4", "S5"}, crossed
assert all(len(v) == 1 for v in crossed.values())
# Every crossing lies outside the node circles (radius 22) and terminals (radius 24).
for name, pts in crossed.items():
    (x, y), = pts
    assert all(math.hypot(x - px, y - py) > 22 for px, py in P)
    assert math.hypot(x - S[0], y - S[1]) > 24 and math.hypot(x - T[0], y - T[1]) > 24
checks += 1

print(f"92-grabcut-regions (CV-GRABCUT-001, CV-GRABCUT-002, CV-GRABCUT-003, figure): {checks} checks passed")
