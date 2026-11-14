"""Recompute the constructed examples of CV-CANNY-HOUGH (reference 32-canny-hough).

Stdlib only. Run with:
    python3 docs/revues/2026-11-14-reference-depth/checks/32-canny-hough.py
Implementation rules mirrored from OpenCV 4.13.0 canny.cpp (TG22, threshold squaring) and
hough.cpp (rho range, number of angles, HoughLinesP length test). Edge chains, steps, images
and crops are constructed.
"""

import math
from collections import deque

checks = 0


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: hysteresis on a toy chain ---------------------------------------
def hysteresis(mag, low, high):
    """mag: dict pixel -> magnitude after non-maximum suppression; 8-connectivity."""
    keep = set()
    queue = deque(p for p, m in mag.items() if m > high)
    keep.update(queue)
    while queue:
        x, y = queue.popleft()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = (x + dx, y + dy)
                if q in mag and q not in keep and mag[q] > low:
                    keep.add(q)
                    queue.append(q)
    return keep


chain_a = {(0, 0): 120, (1, 0): 70, (2, 0): 60, (3, 0): 55}
chain_b = {(0, 5): 90, (1, 5): 80, (2, 5): 85}
mag = {**chain_a, **chain_b}
kept = hysteresis(mag, 50, 100)
# Check 1: with (50, 100), chain A survives entirely and chain B is discarded.
assert set(chain_a) <= kept and not (set(chain_b) & kept)
checks += 1
# Check 2: B's pixels are stronger than three of A's, so strength alone does not decide.
assert sum(1 for v in chain_a.values() if v < min(chain_b.values())) == 3
checks += 1
# Check 3: a single threshold of 100 keeps one pixel; a single threshold of 50 keeps both chains.
assert sum(1 for v in mag.values() if v > 100) == 1 and sum(1 for v in mag.values() if v > 50) == 7
checks += 1
# Check 4: a bridge of magnitude 60 connecting B to A rescues B.
bridged = {**mag, (1, 1): 60, (1, 2): 60, (1, 3): 60, (1, 4): 60}
assert set(chain_b) <= hysteresis(bridged, 50, 100)
checks += 1

# --- Gradient units ------------------------------------------------------------------
SOBEL_X = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]


def sobel_x_at(img, x, y):
    return sum(SOBEL_X[r][c] * img(x + c - 1, y + r - 1) for r in range(3) for c in range(3))


h = 40
step = lambda x, y: h if x >= 1 else 0
# Check 5: a vertical step of h DN gives 4h on the two straddling pixels and 0 elsewhere.
assert sobel_x_at(step, 0, 0) == 4 * h and sobel_x_at(step, 1, 0) == 4 * h and sobel_x_at(step, 3, 0) == 0
checks += 1
# Check 6: Canny thresholds 100 and 200 correspond to steps of 25 and 50 DN (aperture 3, L1, vertical edge).
assert close(100 / 4, 25) and close(200 / 4, 50)
checks += 1
# Check 7: for a diagonal gradient, L1 = sqrt(2) * L2 (gx = gy = 50 -> 100 versus 70.7).
assert close(abs(50) + abs(50), 100) and close(math.hypot(50, 50), 70.71, 1e-2) and close(100 / math.hypot(50, 50), math.sqrt(2))
checks += 1
# Check 8: TG22 = 13573 is tan(22.5 deg) in Q15 fixed point.
assert round(math.tan(math.radians(22.5)) * 2 ** 15) == 13573
checks += 1
# Check 9: with L2gradient OpenCV squares thresholds: comparing |g|^2 > t^2 is equivalent to |g| > t.
for g in (49.0, 50.0, 51.0):
    assert (g * g > 50.0 ** 2) == (g > 50.0)
checks += 1

# --- Hough geometry --------------------------------------------------------------------
# Check 10: a 1 deg angle error moves a point 500 px along the line by 8.7 px across it.
assert close(500 * math.radians(1), 8.727, 1e-3)
checks += 1
# Check 11: (rho, theta) and (-rho, theta + pi) describe the same line.
for (x, y) in ((10.0, 20.0), (-3.0, 7.0)):
    th = 0.7
    r = x * math.cos(th) + y * math.sin(th)
    assert close(-r, x * math.cos(th + math.pi) + y * math.sin(th + math.pi), 1e-12)
checks += 1
# Check 12: crop offset (100, 50); local vertical line x = 20 (theta = 0, rho = 20) has full-image rho 120.
x0, y0 = 100, 50
assert close(20 + x0 * math.cos(0) + y0 * math.sin(0), 120)
checks += 1
# Check 13: theta = pi/2 gives y = rho (horizontal line); theta = 0 gives x = rho (vertical line).
assert close(5 * math.cos(math.pi / 2) + 7 * math.sin(math.pi / 2), 7) and close(5 * math.cos(0) + 7 * math.sin(0), 5)
checks += 1

# --- Example B: sizing an accumulator ----------------------------------------------------
W, H = 1280, 720
theta_step = math.pi / 180
numangle = math.floor(math.pi / theta_step) + 1
if numangle > 1 and abs(math.pi - (numangle - 1) * theta_step) < theta_step / 2:
    numangle -= 1
numrho = round(((W + H) - (-(W + H)) + 1) / 1.0)
cells = (numangle + 2) * (numrho + 2)
# Check 14: 180 angles, 4001 rho bins, 182 x 4003 int32 cells = 2.9 MB.
assert numangle == 180 and numrho == 4001 and close(cells * 4 / 1e6, 2.914, 1e-3)
checks += 1
# Check 15: 50,000 edge pixels cost 9 million votes; halving the angle step doubles them.
assert 50_000 * numangle == 9_000_000 and 50_000 * 2 * numangle == 18_000_000
checks += 1


# --- Segment support and HoughLinesP length test -------------------------------------------
def support_segments(points, rho, theta, tol, max_gap):
    n = (math.cos(theta), math.sin(theta))
    d = (-math.sin(theta), math.cos(theta))
    p0 = (rho * n[0], rho * n[1])
    s = sorted(d[0] * (x - p0[0]) + d[1] * (y - p0[1])
               for x, y in points if abs(n[0] * x + n[1] * y - rho) <= tol)
    segs, start = [], s[0]
    for a, b in zip(s, s[1:]):
        if b - a > max_gap:
            segs.append((start, a))
            start = b
    segs.append((start, s[-1]))
    return segs


# Check 16: two collinear 10 px edges 100 px apart on x = 20 form two segments with a 5 px gap rule.
pts = [(20, y) for y in range(0, 10)] + [(20, y) for y in range(110, 120)]
assert support_segments(pts, 20, 0.0, 0.5, 5) == [(0, 9), (110, 119)]
checks += 1
# Check 17: OpenCV HoughLinesP accepts a segment if max(|dx|, |dy|) >= minLineLength: a diagonal
# segment (0,0)-(70,70) of Euclidean length 99 px is rejected with minLineLength = 80.
dx, dy = 70, 70
assert not (abs(dx) >= 80 or abs(dy) >= 80) and math.hypot(dx, dy) > 80
checks += 1

print(f"32-canny-hough: {checks} checks passed")
