"""Recompute the constructed example of CV-ECC-004 (reference 45-recalage-ecc).

Stdlib only. Run with: python3 -I docs/revues/2026-11-15-accepted-proposals/checks/45-recalage-ecc.py
Conventions checked against OpenCV 4.13.0:
- findTransformECC: x' = W [x, y, 1]^T maps template coordinates (x, y) to input
  coordinates (x', y') (video/tracking.hpp L341-L346; inverse warping advised at L356-L358).
- warpAffine / warpPerspective: dst(x) = src(M x) with WARP_INVERSE_MAP; otherwise M is
  inverted first, so dst(x) = src(M^-1 x) (imgproc/imgproc.hpp L2457-L2473, L2491-L2507).
Images are modelled as functions of continuous coordinates; no image is processed.
"""

import math


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def apply(h, p):
    x, y = p
    u = h[0][0] * x + h[0][1] * y + h[0][2]
    v = h[1][0] * x + h[1][1] * y + h[1][2]
    w = h[2][0] * x + h[2][1] * y + h[2][2]
    return (u / w, v / w)


def inv3(m):
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]]


def close(p, q, tol=1e-9):
    return abs(p[0] - q[0]) <= tol and abs(p[1] - q[1]) <= tol


def template(p):
    """A single bright corner at (100, 50): returns the distance to it."""
    return math.hypot(p[0] - 100.0, p[1] - 50.0)


def make_input(w):
    """Input such that input(W x) = template(x), i.e. input(z) = template(W^-1 z)."""
    w_inv = inv3(w)
    return lambda z: template(apply(w_inv, z))


def warp(src, m, inverse_map):
    """OpenCV semantics of warpAffine/warpPerspective as a coordinate pull-back."""
    pull = m if inverse_map else inv3(m)
    return lambda x: src(apply(pull, x))


checks = 0

# Example: input content appears 10 px to the right of the template content.
W = [[1.0, 0.0, 10.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
I = make_input(W)

# Check 1: W maps a template point to the input point showing the same content.
assert template((100.0, 50.0)) == 0.0 and I(apply(W, (100.0, 50.0))) == 0.0
assert close(apply(W, (100.0, 50.0)), (110.0, 50.0)); checks += 1

# Check 2: with WARP_INVERSE_MAP the warped input equals the template everywhere tested.
aligned = warp(I, W, inverse_map=True)
for p in [(100.0, 50.0), (0.0, 0.0), (37.5, 81.25), (250.0, 10.0)]:
    assert abs(aligned(p) - template(p)) < 1e-9
checks += 1

# Check 3: without the flag the corner lands at x = 120: 20 px off, twice the motion,
# worse than the 10 px of the unwarped input.
wrong = warp(I, W, inverse_map=False)
assert abs(wrong((120.0, 50.0))) < 1e-9 and wrong((100.0, 50.0)) > 19.999
assert abs(I((110.0, 50.0))) < 1e-9; checks += 1

# Check 4: in general the default call returns template o W^-2, i.e. the motion applied
# twice. Euclidean case: rotation 4 deg about (320, 240) plus a (6, -3) px shift.
th = math.radians(4.0)
c, s = math.cos(th), math.sin(th)
R = [[c, -s, 320 - 320 * c + 240 * s + 6.0], [s, c, 240 - 320 * s - 240 * c - 3.0], [0, 0, 1]]
I2 = make_input(R)
wrong2 = warp(I2, R, inverse_map=False)
R2 = mat_mul(R, R)
for p in [(100.0, 50.0), (400.0, 300.0), (10.0, 470.0)]:
    assert abs(wrong2(p) - template(apply(inv3(R2), p))) < 1e-9
# Residual rotation of the wrong overlay is 8 deg, twice the estimated 4 deg.
assert abs(math.degrees(math.atan2(R2[1][0], R2[0][0])) - 8.0) < 1e-9; checks += 1

# Check 5: same semantics for a homography (warpPerspective).
H = [[1.02, 0.01, 8.0], [-0.015, 0.99, -4.0], [2e-5, -1e-5, 1.0]]
I3 = make_input(H)
assert abs(warp(I3, H, True)((100.0, 50.0))) < 1e-9
assert warp(I3, H, False)((100.0, 50.0)) > 1.0; checks += 1

# Check 6: mapping detections. A detection at input pixel q maps to the template frame
# through W^-1 (cv2.invertAffineTransform), not through W.
q = (110.0, 50.0)
assert close(apply(inv3(W), q), (100.0, 50.0)) and close(apply(W, q), (120.0, 50.0)); checks += 1

print(f"45-recalage-ecc (CV-ECC-004): {checks} checks passed")
