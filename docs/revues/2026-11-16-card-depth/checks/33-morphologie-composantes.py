"""Recompute the constructed examples added to CV-MORPHO-001 (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/33-morphologie-composantes.py
Set definitions, Theorem 43 and Propositions 44-45: Haralick, Sternberg and Zhuang 1987, Sec. III.
Grey-level erode = minimum and dilate = maximum over the element: OpenCV 4.13.0
imgproc.hpp L2325-L2362; MORPH_OPEN = erode then dilate.
"""
import random

checks = 0


def dil(A, B):
    return {tuple(a + b for a, b in zip(x, y)) for x in A for y in B}


def ero(A, B, U):
    return {x for x in U if all(tuple(a + b for a, b in zip(x, y)) in A for y in B)}


# Worked example D (1-D): the order of opening and closing.
U1 = {(x,) for x in range(-10, 20)}
A1 = {(x,) for x in range(0, 6)} | {(7,)}
B1 = {(-1,), (0,), (1,)}
op = lambda A: dil(ero(A, B1, U1), B1)
cl = lambda A: ero(dil(A, B1), B1, U1)
assert ero(A1, B1, U1) == {(x,) for x in range(1, 5)}
assert op(A1) == {(x,) for x in range(0, 6)}
assert cl(op(A1)) == {(x,) for x in range(0, 6)}             # open then close: length 6
assert dil(A1, B1) == {(x,) for x in range(-1, 9)}
assert cl(A1) == {(x,) for x in range(0, 8)}
assert op(cl(A1)) == {(x,) for x in range(0, 8)}             # close then open: length 8
checks += 1

# Theorem 43 and Propositions 44-45 on random 2-D sets, inside a margin.
random.seed(43)
mismatch = 0
U = {(r, c) for r in range(-12, 32) for c in range(-12, 32)}
inner = {(r, c) for r in range(-3, 23) for c in range(-3, 23)}
for B in ({(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)},          # symmetric 3x3
          {(0, 0), (0, 1), (1, 1)}):                                        # asymmetric
    Bref = {(-a, -b) for a, b in B}
    for _ in range(5):
        A = {(r, c) for r in range(20) for c in range(20) if random.random() < 0.6}
        Ac = U - A
        closing = ero(dil(A, B), B, U)
        opening_c = dil(ero(Ac, Bref, U), Bref)
        assert ((U - closing) & inner) == (opening_c & inner)                # Theorem 43
        opening = dil(ero(A, B, U), B)
        union_fits = set()
        for y in U:
            By = {(y[0] + b[0], y[1] + b[1]) for b in B}
            if By <= A:
                union_fits |= By
        assert opening == union_fits                                          # Prop. 44
        # Prop. 45: x is in the closing iff every translate of the REFLECTED element
        # that covers x meets A (identical to B for a symmetric element).
        prop45, prop45_wrong = set(), set()
        for x in inner:
            cov_ref = [{(x[0] - b[0] + d[0], x[1] - b[1] + d[1]) for d in Bref} for b in Bref]
            cov_b = [{(x[0] - b[0] + d[0], x[1] - b[1] + d[1]) for d in B} for b in B]
            if all(Bx & A for Bx in cov_ref):
                prop45.add(x)
            if all(Bx & A for Bx in cov_b):
                prop45_wrong.add(x)
        assert prop45 == (closing & inner)                                    # Prop. 45
        if B == Bref:
            assert prop45_wrong == prop45
        else:
            mismatch += prop45_wrong != prop45
assert mismatch > 0          # with B instead of its reflection, Prop. 45 fails
checks += 1

# Polarity: OpenCV-style MORPH_OPEN (min then max, 3x3) on objects = 0, background = 255.
H = W = 21
img = [[255] * W for _ in range(H)]
for r in range(3, 12):
    for c in range(3, 12):
        img[r][c] = 0                                   # 9 x 9 object
img[7][7] = 255                                         # one-pixel hole in the object
img[16][16] = 0                                         # one-pixel speck object


def morph(im, f):
    out = [[0] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            vals = [im[r + dr][c + dc] for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                    if 0 <= r + dr < H and 0 <= c + dc < W]          # neutral border
            out[r][c] = f(vals)
    return out


opened = morph(morph(img, min), max)
assert opened[7][7] == 0                                # hole filled: a closing of the objects
assert opened[16][16] == 0                              # speck kept
assert all(opened[r][c] == img[r][c] for r in range(H) for c in range(W) if (r, c) != (7, 7))
checks += 1

print(f"33-morphologie-composantes (CV-MORPHO-001): {checks} checks passed")
