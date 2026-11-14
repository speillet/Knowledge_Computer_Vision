"""Recompute the constructed examples of CV-MEANSHIFT (reference 115-meanshift-camshift).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/115-meanshift-camshift.py
Formulas: centroid of a back-projection (OpenCV 4.13.0 camshift.cpp L83-L90), CamShift box
length and width 4*sqrt(eigenvalue) with a 10-pixel moment margin (L115, L128-L173, L187-L197),
Bhattacharyya coefficient and mean-shift weights (Comaniciu et al. 2003, eqs. 7, 10, 13).
All scenes are constructed.
"""

import math

# --- Example A: weighted centroid --------------------------------------------------
# Check 1: masses 1 and 3 at x = 10 and 14 px give a centroid at 13 px, not the midpoint 12 px.
assert (1 * 10 + 3 * 14) / (1 + 3) == 13
# Check 2: scaling all weights by 5 keeps the centroid; adding 1 to both weights moves it to 12.67, toward the midpoint.
assert (5 * 10 + 15 * 14) / 20 == 13 and (2 * 10 + 4 * 14) / 6 == 76 / 6
assert abs(76 / 6 - 12.6667) < 1e-4


def moments(weights):
    """Raw and central moments of a dict {(x, y): weight}."""
    m00 = sum(weights.values())
    xc = sum(x * w for (x, y), w in weights.items()) / m00
    yc = sum(y * w for (x, y), w in weights.items()) / m00
    mu20 = sum((x - xc) ** 2 * w for (x, y), w in weights.items())
    mu02 = sum((y - yc) ** 2 * w for (x, y), w in weights.items())
    mu11 = sum((x - xc) * (y - yc) * w for (x, y), w in weights.items())
    return m00, xc, yc, mu20, mu02, mu11


def camshift_box(weights):
    """Length, width and orientation as computed in OpenCV 4.13.0 camshift.cpp L153-L181."""
    m00, _, _, mu20, mu02, mu11 = moments(weights)
    a, b, c = mu20 / m00, mu11 / m00, mu02 / m00
    square = math.sqrt(4 * b * b + (a - c) ** 2)
    theta = math.atan2(2 * b, a - c + square)
    cs, sn = math.cos(theta), math.sin(theta)
    rot_a = max(0.0, cs * cs * mu20 + 2 * cs * sn * mu11 + sn * sn * mu02)
    rot_c = max(0.0, sn * sn * mu20 - 2 * cs * sn * mu11 + cs * cs * mu02)
    length, width = 4 * math.sqrt(rot_a / m00), 4 * math.sqrt(rot_c / m00)
    if length < width:
        length, width, theta = width, length, math.pi / 2 - theta
    return length, width, theta


# --- Example B: CamShift box of a uniform rectangle -------------------------------
rect = {(x, y): 1.0 for x in range(40) for y in range(20)}      # 40 x 20 px, uniform weight
length, width, theta = camshift_box(rect)
# Check 3: for a uniform W x H blob the variance is (W^2 - 1)/12 on a pixel grid, so the box is
# about 4/sqrt(12) = 1.155 times the blob: 46.2 x 23.1 px for 40 x 20 px, axis-aligned.
assert abs(length - 4 * math.sqrt((40 ** 2 - 1) / 12)) < 1e-9 and abs(length - 46.17) < 0.01
assert abs(width - 23.07) < 0.01 and abs(theta) < 1e-12
assert abs(4 / math.sqrt(12) - 1.1547) < 1e-4

# --- Example C: window growth on a uniform same-colour background -----------------
TOL = 10                                    # pixels added on each side before the moments (L115)
w = 40.0
sizes = []
for _ in range(4):
    span = w + 2 * TOL                     # moments taken over the enlarged window
    w = 4 * math.sqrt((span ** 2 - 1) / 12) + 2   # box length + 2 px becomes the next width (L190-L191)
    sizes.append(round(w, 1))
# Check 4: starting from 40 px over a uniform field, the window grows to about 71, 107, 149, 197 px.
assert sizes == [71.3, 107.4, 149.1, 197.2], sizes

# --- Example D: round blob, orientation ill-conditioned ---------------------------
disc = {(x, y): 1.0 for x in range(-10, 11) for y in range(-10, 11) if x * x + y * y <= 100}
l_d, w_d, _ = camshift_box(disc)
# Check 5: a disc gives equal eigenvalues: length equals width, so the angle carries no information.
assert abs(l_d - w_d) < 1e-9

# --- Example E: Bhattacharyya coefficient and mean-shift weights -------------------
q = [0.5, 0.3, 0.2, 0.0]                    # target model over 4 colour bins
p = [0.2, 0.3, 0.2, 0.3]                    # candidate at y0
rho = sum(math.sqrt(a * b) for a, b in zip(p, q))
# Check 6: rho = sqrt(.10) + .3 + .2 + 0 = 0.816; distance sqrt(1 - rho) = 0.429 (eqs. 6-7).
assert abs(rho - 0.8162) < 1e-4 and abs(math.sqrt(1 - rho) - 0.4287) < 1e-4
weights = [math.sqrt(a / b) if b > 0 else 0.0 for a, b in zip(q, p)]
# Check 7: eq. 10 weights are sqrt(q_u / p_u): 1.581 for an under-represented model colour,
# 1 for a matched colour, 0 for a colour absent from the model.
assert [round(v, 3) for v in weights] == [1.581, 1.0, 1.0, 0.0]

print("115-meanshift-camshift: 7 checks passed (centroid, CamShift box, window growth, disc, Bhattacharyya)")
