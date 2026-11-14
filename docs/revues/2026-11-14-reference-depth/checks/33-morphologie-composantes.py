"""Recompute the constructed examples of CV-MORPHO (reference 33-morphologie-composantes).

Stdlib only. Run with:
    python3 docs/revues/2026-11-14-reference-depth/checks/33-morphologie-composantes.py
Set definitions follow Haralick, Sternberg and Zhuang 1987 (Definitions 1, 17, 35, 36);
the OpenCV variant follows the documented min/max formulas of erode and dilate in
imgproc.hpp 4.13.0 (offsets relative to the anchor, same offsets for both). Shapes, gaps
and resolutions are constructed; no OpenCV call is executed.
"""

from collections import deque

checks = 0


def square(k):
    r = (k - 1) // 2
    return {(dx, dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1)}


def dilate(A, B):
    """Minkowski sum (Haralick Definition 1)."""
    return {(a[0] + b[0], a[1] + b[1]) for a in A for b in B}


def erode(A, B):
    """Positions where B translated fits in A (Haralick Definition 17)."""
    cand = {(a[0] - b[0], a[1] - b[1]) for a in A for b in B}
    return {x for x in cand if all((x[0] + b[0], x[1] + b[1]) in A for b in B)}


def opening(A, B):
    return dilate(erode(A, B), B)


def closing(A, B):
    return erode(dilate(A, B), B)


def components(A, conn):
    nb4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    nb = nb4 + ([(1, 1), (1, -1), (-1, 1), (-1, -1)] if conn == 8 else [])
    seen, count = set(), 0
    for p in A:
        if p in seen:
            continue
        count += 1
        q = deque([p])
        seen.add(p)
        while q:
            x, y = q.popleft()
            for dx, dy in nb:
                n = (x + dx, y + dy)
                if n in A and n not in seen:
                    seen.add(n)
                    q.append(n)
    return count


def two_squares(gap, side=6):
    left = {(x, y) for x in range(side) for y in range(side)}
    right = {(x + side + gap, y) for x in range(side) for y in range(side)}
    return left | right


# --- Example A: gaps, kernel size and resolution --------------------------------------
results = {}
for gap in (2, 3, 4, 5):
    for k in (3, 5):
        results[(gap, k)] = components(closing(two_squares(gap), square(k)), 8)
# Check 1: closing with a k x k square merges gaps up to k - 1 pixels (table of worked example A).
assert results == {(2, 3): 1, (2, 5): 1, (3, 3): 2, (3, 5): 1, (4, 3): 2, (4, 5): 1, (5, 3): 2, (5, 5): 2}
checks += 1
# Check 2: 0.2 mm is 2 px at 0.1 mm/px and 4 px at 0.05 mm/px.
assert round(0.2 / 0.1) == 2 and round(0.2 / 0.05) == 4
checks += 1
strip = lambda w: {(x, y) for x in range(w) for y in range(20)}
# Check 3: opening with 3x3 removes a 2 px wide strip and keeps a 3 px wide strip unchanged;
# at the finer resolution the same scratch is 4 px wide and survives.
assert opening(strip(2), square(3)) == set()
assert opening(strip(3), square(3)) == strip(3) and opening(strip(4), square(3)) == strip(4)
checks += 1
# Check 4: opening is anti-extensive, closing extensive, both idempotent (Haralick Props 41-42, Thms 38, 40).
A = two_squares(3) | {(20, 20), (21, 20)}
B = square(3)
o, c = opening(A, B), closing(A, B)
assert o <= A <= c and opening(o, B) == o and closing(c, B) == c
checks += 1
# Check 5: chain rule: two erosions by 3x3 equal one erosion by 5x5 (Haralick Corollary 31).
big = {(x, y) for x in range(12) for y in range(9)}
assert erode(erode(big, square(3)), square(3)) == erode(big, square(5))
checks += 1
# Check 6: duality (A erode B)^c = A^c dilate reflect(B), checked inside a bounding window.
win = {(x, y) for x in range(-4, 16) for y in range(-4, 13)}
Bas = {(0, 0), (1, 0), (0, 1)}
refl = {(-b[0], -b[1]) for b in Bas}
lhs = win - erode(big, Bas)
rhs = dilate(win - big, refl) & win
inner = {(x, y) for x in range(-2, 14) for y in range(-2, 11)}
assert lhs & inner == rhs & inner
checks += 1

# --- Example B: connectivity changes counts and holes ---------------------------------
corner = {(0, 0), (1, 1)}
# Check 7: two corner-touching pixels: 2 components (4-conn), 1 (8-conn); OpenCV-style N adds background.
assert components(corner, 4) == 2 and components(corner, 8) == 1
assert components(corner, 4) + 1 == 3 and components(corner, 8) + 1 == 2
checks += 1
diag = {(i, i) for i in range(10)}
# Check 8: a diagonal line of 10 pixels: 10 components (4-conn), 1 (8-conn).
assert components(diag, 4) == 10 and components(diag, 8) == 1
checks += 1
ring = {(1, 0), (0, 1), (2, 1), (1, 2)}
box = {(x, y) for x in range(-1, 4) for y in range(-1, 4)}
background = box - ring
# Check 9: the diamond ring is one 8-connected component; its empty centre is a separate background
# component (a hole) under 4-connectivity, but joins the outside under 8-connectivity.
assert components(ring, 8) == 1 and components(ring, 4) == 4
assert components(background, 4) == 2 and components(background, 8) == 1
checks += 1

# --- Example C: an asymmetric element with OpenCV's documented formulas ---------------
run = set(range(0, 5))
offsets = [-1, 0]  # 2-pixel element, default anchor ksize/2 = 1


def cv_erode_1d(S):
    lo, hi = min(S) - 3, max(S) + 3
    return {x for x in range(lo, hi) if all(x + o in S for o in offsets)}


def cv_dilate_1d(S):
    lo, hi = min(S) - 3, max(S) + 3
    return {x for x in range(lo, hi) if any(x + o in S for o in offsets)}


set_B = {(o, 0) for o in offsets}
set_open = {p[0] for p in opening({(x, 0) for x in run}, set_B)}
cv_open = cv_dilate_1d(cv_erode_1d(run))
# Check 10: set opening returns {0..4}; OpenCV-formula opening returns {1..5}, not inside A.
assert set_open == set(range(0, 5)) and cv_open == set(range(1, 6)) and not cv_open <= run
checks += 1
# Check 11: with a symmetric, centred 3-pixel element both agree.
offsets = [-1, 0, 1]
set_B3 = {(o, 0) for o in offsets}
assert {p[0] for p in opening({(x, 0) for x in run}, set_B3)} == cv_dilate_1d(cv_erode_1d(run)) == run
checks += 1

# --- Iterations ------------------------------------------------------------------------
# Check 12: n iterations of a full k x k rectangle equal one rectangle of side k + (n-1)(k-1)
# (morph.dispatch.cpp L1009-L1017): 3x3 twice -> 5x5; 5x5 three times -> 13x13.
assert 3 + (2 - 1) * (3 - 1) == 5 and 5 + (3 - 1) * (5 - 1) == 13
assert dilate(dilate(square(1), square(3)), square(3)) == square(5)
checks += 1

print(f"33-morphologie-composantes: {checks} checks passed")
