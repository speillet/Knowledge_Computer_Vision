"""Recompute the constructed numbers added to CV-OCR-003 (reference 74-ocr-documents, 2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/74-ocr-documents.py
Classic CER = (i + s + d) / n with the Levenshtein dynamic program of the reference
(OCR-D, Text Evaluation); line breaks count as characters. The line-matched score
imitates the idea of Flexible Character Accuracy (match lines, then average their CER);
it is not the full OCR-D algorithm. Lines and coordinates are constructed.
"""
checks = 0


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


left = [("Invoice 2026-118", 40, 100), ("Supplier Acme Tools", 40, 140), ("Due 30 November", 40, 180)]
right = [("Net 1,033.33", 420, 102), ("VAT 206.67", 420, 142), ("Total 1,240.00", 420, 182)]
lines = left + right                                   # (text, x of left edge, y of top) in px

# 1. A global sort by top coordinate interleaves the columns.
by_y = [t for t, _, _ in sorted(lines, key=lambda l: l[2])]
assert by_y == [left[0][0], right[0][0], left[1][0], right[1][0], left[2][0], right[2][0]]
# Column first (split at the horizontal gap), then top coordinate: the reference order.
col = lambda l: 0 if l[1] < 230 else 1
by_col = [t for t, _, _ in sorted(lines, key=lambda l: (col(l), l[2]))]
assert by_col == [t for t, _, _ in left + right]
checks += 1

# 2. Every line exact, page CER about 52%; line-matched error 0.
ref, hyp = "\n".join(by_col), "\n".join(by_y)
assert len(ref) == 91 and lev(hyp, ref) == 47
assert round(47 / 91, 3) == 0.516
matched = sum(min(lev(h, r) for r in by_col) for h in by_y)
assert matched == 0
assert lev("\n".join(by_col), ref) == 0                # oracle order: CER 0
checks += 1

print(f"74-ocr-documents (CV-OCR-003): {checks} checks passed")
