"""Recompute the constructed numbers added to CV-FARNEBACK-003 (reference
103-farneback, worked example D, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/103-farneback.py
Convention prev(y, x) ~ next(y + flow[1], x + flow[0]): OpenCV 4.13.0 tracking.hpp L215-L217.
remap: dst(x, y) = src(map_x, map_y), relative with WARP_RELATIVE_MAP: imgproc.hpp
L2519-L2549. Sample warp_flow samples at x - flow; draw_hsv uses arctan2(fy, fx) + pi:
samples/python/opt_flow.py L38-L57.
"""
import math

checks = 0
f = (4.0, -2.0)                     # flow[y, x] = (u, v)
dt = 0.040

# Speed and on-screen direction.
speed = (f[0] / dt, f[1] / dt)
assert speed == (100.0, -50.0) and abs(math.hypot(*speed) - 111.80) < 0.01
ang = math.degrees(math.atan2(f[1], f[0]))
assert abs(ang + 26.565) < 1e-3      # negative: upward on screen, since y points down
hue = (math.atan2(f[1], f[0]) + math.pi) * (180 / math.pi / 2)
assert 0 <= hue < 180 and abs(hue - 76.7) < 0.05     # OpenCV 8-bit hue range [0, 180)
checks += 1


# Uniform translation model: next(p) = prev(p - f). A warp samples next at s(x);
# the result equals prev(s(x) - f), so the residual misalignment is s(x) - f - x.
def misalignment(sample_offset):
    return (sample_offset[0] - f[0], sample_offset[1] - f[1])


def norm(v):
    return math.hypot(*v)


correct = misalignment((f[0], f[1]))          # relative map +flow
none = misalignment((0.0, 0.0))               # no warp
inverted = misalignment((-f[0], -f[1]))       # sign error
swapped = misalignment((f[1], f[0]))          # (x + v, y + u) = (x - 2, y + 4)
assert correct == (0.0, 0.0)
assert none == (-4.0, 2.0) and abs(norm(none) - 4.472) < 1e-3
assert inverted == (-8.0, 4.0) and abs(norm(inverted) - 8.944) < 1e-3
assert swapped == (-6.0, 6.0) and abs(norm(swapped) - 8.485) < 1e-3
assert norm(correct) < norm(none) < min(norm(inverted), norm(swapped))
checks += 1

# With u = v a swap is invisible; with v = 0 a sign error on y is invisible.
g = (3.0, 3.0)
assert (g[1], g[0]) == g
h = (5.0, 0.0)
assert (h[0], -h[1]) == h          # flipping v changes nothing when v = 0
checks += 1

# Remapping prev with +f (expecting next) gives prev(x + f) = next(x + 2f).
# next(p) = prev(p - f) -> prev(q) = next(q + f) -> prev(x + f) = next(x + 2f)
assert (2 * f[0], 2 * f[1]) == (8.0, -4.0)
checks += 1


# Discrete 1-D illustration of the sign test on a non-repetitive signal.
def signal(x):
    return math.exp(-((x - 30.0) / 6.0) ** 2) + 0.5 * math.exp(-((x - 52.0) / 4.0) ** 2)


shift = 4.0
prev = [signal(x) for x in range(100)]
nxt = [signal(x - shift) for x in range(100)]


def sample(arr, pos):
    i = math.floor(pos)
    a = pos - i
    if i < 0 or i + 1 >= len(arr):
        return 0.0
    return (1 - a) * arr[i] + a * arr[i + 1]


def residual(offset):
    xs = range(15, 85)
    return sum((sample(nxt, x + offset) - prev[x]) ** 2 for x in xs)


r_correct, r_none, r_inv = residual(shift), residual(0.0), residual(-shift)
assert r_correct < 1e-12 < r_none < r_inv
checks += 1

print(f"103-farneback (CV-FARNEBACK-003): {checks} checks passed")
