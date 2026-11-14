"""Recompute the constructed examples of CV-OCR (reference 74-ocr-documents).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/74-ocr-documents.py
Inputs come from CTC (Graves et al. 2006, Sec. 3.1 and 4.1), CRNN (arXiv 1507.05717,
Sec. 2.3 and 3.2: 100x32 input, 25 frames), DBNet (arXiv 1911.08947, eqs. 6 and 10:
r = 0.4, r' = 1.5), OpenCV 4.13.0 model.cpp (unclipRatio 2.0) and OCR-D's evaluation
specification (classic and normalized CER). Strings, sizes and probabilities are constructed.
"""

import itertools
import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


checks = 0
BLANK = "-"


def collapse(path):
    """CTC map B: merge repeated labels, then remove blanks (Graves 2006, Sec. 3.1)."""
    out, prev = [], None
    for c in path:
        if c != prev and c != BLANK:
            out.append(c)
        prev = c
    return "".join(out)


# --- Example A: CTC alignments and minimum frame count --------------------------
# Check: B maps "--hh-e-l-ll-oo--" (CRNN Sec. 2.3.1) and "-aa--abb" (Graves Sec. 3.1) as published.
assert collapse("--hh-e-l-ll-oo--") == "hello" and collapse("-aa--abb") == "aab"; checks += 1


def min_frames(label):
    """Fewest frames that can emit `label`: one per label plus one blank between equal neighbours."""
    return len(label) + sum(1 for a, b in zip(label, label[1:]) if a == b)


# Check: "hello" needs 6 frames, "1000" needs 6, "abc" needs 3.
assert (min_frames("hello"), min_frames("1000"), min_frames("abc")) == (6, 6, 3); checks += 1
# Check: brute force confirms that no 5-frame path over {-,h,e,l,o} collapses to "hello", and a 6-frame one does.
alphabet = [BLANK, "h", "e", "l", "o"]
assert not any(collapse(p) == "hello" for p in itertools.product(alphabet, repeat=5))
assert any(collapse(p) == "hello" for p in itertools.product(alphabet, repeat=6)); checks += 1
# Check: "ab" over T = 3 frames has exactly 5 valid paths (aab, abb, -ab, a-b, ab-).
paths_ab = sorted("".join(p) for p in itertools.product([BLANK, "a", "b"], repeat=3) if collapse(p) == "ab")
assert paths_ab == sorted(["aab", "abb", "-ab", "a-b", "ab-"]); checks += 1


def ctc_forward(label, probs):
    """Graves 2006 eqs. 5-8: alpha recursion over the blank-augmented label l' of length 2|l| + 1."""
    ext = [BLANK]
    for c in label:
        ext += [c, BLANK]
    S, T = len(ext), len(probs)
    alpha = [[0.0] * S for _ in range(T)]
    alpha[0][0] = probs[0][BLANK]
    if S > 1:
        alpha[0][1] = probs[0][ext[1]]
    for t in range(1, T):
        for s in range(S):
            a = alpha[t - 1][s] + (alpha[t - 1][s - 1] if s >= 1 else 0.0)
            if s >= 2 and ext[s] != BLANK and ext[s] != ext[s - 2]:
                a += alpha[t - 1][s - 2]
            alpha[t][s] = a * probs[t][ext[s]]
    return alpha[T - 1][S - 1] + (alpha[T - 1][S - 2] if S > 1 else 0.0)


probs = [
    {BLANK: 0.5, "a": 0.4, "b": 0.1},
    {BLANK: 0.3, "a": 0.3, "b": 0.4},
    {BLANK: 0.6, "a": 0.1, "b": 0.3},
]
brute = sum(
    math.prod(probs[t][c] for t, c in enumerate(p))
    for p in itertools.product([BLANK, "a", "b"], repeat=3) if collapse(p) == "ab"
)
# Check: the forward recursion equals the brute-force sum over the 5 paths: p("ab") = 0.261.
assert close(ctc_forward("ab", probs), brute, 1e-12) and close(brute, 0.261, 1e-9); checks += 1
two = [{BLANK: 0.6, "a": 0.4}, {BLANK: 0.6, "a": 0.4}]
best_path = "".join(max(pt, key=pt.get) for pt in two)
p_a = sum(math.prod(two[t][c] for t, c in enumerate(p))
          for p in itertools.product([BLANK, "a"], repeat=2) if collapse(p) == "a")
# Check: with blank 0.6 in both frames, best-path decoding returns the empty string (path "--", 0.36)
# while the labeling "a" has probability 0.64 (paths a-, -a, aa): the best path is not the best labeling.
assert best_path == "--" and collapse(best_path) == "" and close(p_a, 0.64, 1e-12); checks += 1
# Check: the forward recursion gives the same 0.64 for "a".
assert close(ctc_forward("a", two), 0.64, 1e-12); checks += 1

# CRNN geometry: 100 px wide, 32 px high input gives 25 frames, i.e. 4 input px per frame (Sec. 3.2).
FRAMES, WIDTH = 25, 100
STRIDE = WIDTH / FRAMES
# Check: 4 px per frame; a 4-character "1000" printed 4 px per character spans 4 frames < 6 needed.
assert STRIDE == 4.0 and (4 * 4) / STRIDE < min_frames("1000"); checks += 1
# Check: at 10 px per character the same string spans 10 frames, enough for the 6 required.
assert (4 * 10) / STRIDE >= min_frames("1000"); checks += 1

# --- Example B: classic versus normalized CER (OCR-D) ---------------------------
def cer_classic(i, s, d, n):
    return (i + s + d) / n


def cer_normalized(i, s, d, c):
    return (i + s + d) / (i + s + d + c)


# Check: 5 correct characters plus 10 inserted ones: classic CER 2.0 (200 %), normalized CER 2/3.
assert close(cer_classic(10, 0, 0, 5), 2.0, 1e-12) and close(cer_normalized(10, 0, 0, 5), 2 / 3, 1e-12); checks += 1
# Check: one substitution in a 2,000-character invoice: classic CER 0.05 %, normalized 0.05 % too (c = 1,999).
assert close(cer_classic(0, 1, 0, 2000), 0.0005, 1e-12) and close(cer_normalized(0, 1, 0, 1999), 0.0005, 1e-12); checks += 1


def levenshtein(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


# Check: OCR-D's example "ſind" versus "fmd" has distance 3.
assert levenshtein("ſind", "fmd") == 3; checks += 1
# Check: a collapsed repeat ("1000" read as "100") is one deletion, CER 1/4, but the amount is off by a factor 10.
assert levenshtein("1000", "100") == 1 and close(1 / 4, 0.25, 1e-12) and 1000 / 100 == 10; checks += 1

# --- Example C: print size, scan resolution and CRNN height normalization --------
def line_height_px(points, dpi):
    return points / 72 * dpi          # 1 pt = 1/72 inch


# Check: a 10 pt em at 300 dpi is 41.7 px, rescaled by 0.768 to 32 px; at 150 dpi it is 20.8 px, upsampled 1.536 times.
assert close(line_height_px(10, 300), 41.667) and close(32 / line_height_px(10, 300), 0.768, 1e-9)
assert close(line_height_px(10, 150), 20.833) and close(32 / line_height_px(10, 150), 1.536, 1e-9); checks += 1
# Check: 6 pt at 150 dpi is 12.5 px, upsampled 2.56 times to 32 px.
assert close(line_height_px(6, 150), 12.5, 1e-9) and close(32 / 12.5, 2.56, 1e-12); checks += 1

# --- Example D: DBNet shrink and unclip on rectangles ----------------------------
def shrink_unclip(w, h, r=0.4, r_prime=1.5):
    """Shrink a w x h box by D = A(1 - r^2)/L, then dilate by D' = A' r'/L' (DBNet eqs. 6 and 10)."""
    D = w * h * (1 - r * r) / (2 * (w + h))
    ws, hs = w - 2 * D, h - 2 * D
    Dp = ws * hs * r_prime / (2 * (ws + hs))
    return D, (ws, hs), (ws + 2 * Dp, hs + 2 * Dp)


D, kernel, out = shrink_unclip(40, 40)
# Check: a 40 x 40 square shrinks by 8.4 px to 23.2 px and comes back at 40.6 px (101.5 %).
assert close(D, 8.4) and close(kernel[0], 23.2) and close(out[0], 40.6); checks += 1
D, kernel, out = shrink_unclip(120, 40)
# Check: a 3:1 word box 120 x 40 comes back at about 114.0 x 34.0 px (85 % of its height).
assert close(D, 12.6) and close(out[0], 114.0, 0.05) and close(out[1], 34.0, 0.05); checks += 1
D, kernel, out = shrink_unclip(400, 40)
# Check: a 10:1 text line 400 x 40 shrinks to a 9.45 px high kernel and comes back only 23.3 px high (58 %).
assert close(kernel[1], 9.4545, 1e-3) and close(out[1], 23.28, 0.01) and close(out[1] / 40, 0.582, 1e-3); checks += 1
_, _, out2 = shrink_unclip(400, 40, r_prime=2.0)
# Check: OpenCV's default unclip ratio 2.0 brings that line back to 27.9 px (70 %).
assert close(out2[1], 27.89, 0.01) and close(out2[1] / 40, 0.697, 1e-3); checks += 1

print(f"74-ocr-documents: {checks} checks passed")
