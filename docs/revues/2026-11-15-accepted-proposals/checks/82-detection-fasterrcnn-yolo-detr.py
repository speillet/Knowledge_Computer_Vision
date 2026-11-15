"""Recompute the constructed example of CV-DETECTEURS-014 (reference 82-detection-fasterrcnn-yolo-detr).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-15-accepted-proposals/checks/82-detection-fasterrcnn-yolo-detr.py

Conventions checked at their sources:
- Faster R-CNN (arXiv 1506.01497v3, §III-A2, eq. 2): t_x = (x - x_a)/w_a, t_y = (y - y_a)/h_a,
  t_w = log(w/w_a), t_h = log(h/h_a) with centres and sizes; RPN positive for the highest-IoU
  anchor(s) of a ground truth or IoU higher than 0.7, negative below 0.3 for all ground truths,
  otherwise ignored.
- RetinaNet (arXiv 1708.02002v2, §4 "Anchors"): positive at IoU 0.5, background in [0, 0.4),
  ignored in [0.4, 0.5).
- torchvision v0.29.0 models/detection/_utils.py: encode_boxes multiplies the targets by the
  weights (L103-L116); BoxCoder.decode_single divides by them, clamps dw and dh at
  log(1000/16), then applies the inverse of eq. 2 with widths x2 - x1 and centres
  x1 + 0.5 w (L183-L224); Matcher uses >= high and < low (L339-L345, L384-L387).
  Weights (1,1,1,1) in rpn.py L164 and retinanet.py L244, L470; (10,10,5,5) in roi_heads.py
  L542-L544.
No network or torchvision code is executed; the formulas are re-implemented here.
"""

import math

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    area = lambda z: (z[2] - z[0]) * (z[3] - z[1])
    return inter, area(a) + area(b) - inter, inter / (area(a) + area(b) - inter)


def encode(gt, ref, w):
    """torchvision encode_boxes: weights multiply eq. 2."""
    rw, rh = ref[2] - ref[0], ref[3] - ref[1]
    rx, ry = ref[0] + 0.5 * rw, ref[1] + 0.5 * rh
    gw, gh = gt[2] - gt[0], gt[3] - gt[1]
    gx, gy = gt[0] + 0.5 * gw, gt[1] + 0.5 * gh
    return (w[0] * (gx - rx) / rw, w[1] * (gy - ry) / rh,
            w[2] * math.log(gw / rw), w[3] * math.log(gh / rh))


def decode(code, ref, w, clip=math.log(1000.0 / 16)):
    """torchvision BoxCoder.decode_single: divide by weights, clamp, invert eq. 2."""
    rw, rh = ref[2] - ref[0], ref[3] - ref[1]
    rx, ry = ref[0] + 0.5 * rw, ref[1] + 0.5 * rh
    dx, dy = code[0] / w[0], code[1] / w[1]
    dw, dh = min(code[2] / w[2], clip), min(code[3] / w[3], clip)
    cx, cy = rx + dx * rw, ry + dy * rh
    pw, ph = math.exp(dw) * rw, math.exp(dh) * rh
    return (cx - 0.5 * pw, cy - 0.5 * ph, cx + 0.5 * pw, cy + 0.5 * ph)


def rpn_label(v, best=False):
    """Paper rule: positive if highest-IoU anchor or IoU > 0.7; negative if < 0.3."""
    if best or v > 0.7:
        return "positive"
    return "negative" if v < 0.3 else "ignored"


def retina_label(v):
    """Paper rule (§4): positive at >= 0.5, background in [0, 0.4), ignored in [0.4, 0.5)."""
    if v >= 0.5:
        return "positive"
    return "negative" if v < 0.4 else "ignored"


anchor = (36.0, 36.0, 164.0, 164.0)   # 128 x 128, centre (100, 100)
gt = (36.0, 60.0, 196.0, 156.0)       # 160 x 96, centre (116, 108)
RPN_W, ROI_W = (1.0, 1.0, 1.0, 1.0), (10.0, 10.0, 5.0, 5.0)

# Check 1: intersection 128 x 96 = 12288, union 19456, IoU = 0.6316.
inter, union, v = iou(anchor, gt)
assert inter == 12288 and union == 19456 and close(v, 12288 / 19456) and round(v, 3) == 0.632
checks += 1

# Check 2: labels. Another anchor has IoU 0.78 with this ground truth, so this anchor is not the
# highest-IoU one: RPN ignored (between 0.3 and 0.7), RetinaNet positive (>= 0.5).
assert rpn_label(v, best=False) == "ignored" and retina_label(v) == "positive"
# The reference's worked example A (IoU 0.432) is ignored by both rules.
_, _, v_a = iou(anchor, (60.0, 80.0, 200.0, 160.0))
assert round(v_a, 3) == 0.432 and rpn_label(v_a) == "ignored" and retina_label(v_a) == "ignored"
checks += 1

# Check 3: eq. 2 targets (0.125, 0.0625, log 1.25, log 0.75) = (0.125, 0.0625, 0.223, -0.288).
t = encode(gt, anchor, RPN_W)
assert close(t[0], 0.125) and close(t[1], 0.0625)
assert close(t[2], math.log(1.25)) and close(t[3], math.log(0.75))
assert (round(t[2], 3), round(t[3], 3)) == (0.223, -0.288)
checks += 1

# Check 4: torchvision's R-CNN head targets for the same pair: (1.25, 0.625, 1.116, -1.438).
t_roi = encode(gt, anchor, ROI_W)
assert [round(c, 3) for c in t_roi] == [1.25, 0.625, 1.116, -1.438]
checks += 1

# Check 5: each code decoded with its own weights returns the ground truth exactly.
for code, w in ((t, RPN_W), (t_roi, ROI_W)):
    assert all(close(a, b, 1e-9) for a, b in zip(decode(code, anchor, w), gt))
checks += 1

# Check 6: head output (10,10,5,5)-encoded but decoded with (1,1,1,1): centre shifted by
# (160, 80) px instead of (16, 8), sizes x 1.25^5 and x 0.75^5 -> (64.7, 164.8, 455.3, 195.2).
bad = decode(t_roi, anchor, RPN_W)
cx, cy = (bad[0] + bad[2]) / 2, (bad[1] + bad[3]) / 2
assert close(cx, 260.0) and close(cy, 180.0)
assert close(bad[2] - bad[0], 128 * 1.25 ** 5) and close(bad[3] - bad[1], 128 * 0.75 ** 5)
assert [round(c, 1) for c in bad] == [64.7, 164.8, 455.3, 195.2]
_, _, v_bad = iou(bad, gt)
assert v_bad < 0.1
checks += 1

# Check 7: the reverse mistake (RPN code decoded with (10,10,5,5)) stays near the anchor:
# offsets / 10, log sizes / 5 -> (34.7, 40.4, 168.5, 161.2).
bad2 = decode(t, anchor, ROI_W)
assert [round(c, 1) for c in bad2] == [34.7, 40.4, 168.5, 161.2]
assert close(bad2[2] - bad2[0], 128 * 1.25 ** 0.2) and close(bad2[3] - bad2[1], 128 * 0.75 ** 0.2)
checks += 1

# Check 8: a perfect proposal (t = 0) decodes identically under any weights, so the bug hides
# when proposals already fit their objects.
assert decode((0.0, 0.0, 0.0, 0.0), anchor, RPN_W) == decode((0.0, 0.0, 0.0, 0.0), anchor, ROI_W) == anchor
checks += 1

# Check 9: the clamp log(1000/16) = 4.135 does not act in this example (|dw|, |dh| <= 1.44).
assert close(math.log(1000 / 16), 4.135166556742356) and max(abs(c) for c in t_roi[2:]) < 4.135
checks += 1

# Check 10: weights (10,10,5,5) are equivalent to dividing the targets by standard deviations
# (0.1, 0.1, 0.2, 0.2) without mean subtraction (arithmetic identity).
assert all(close(a / s, b) for a, s, b in zip(t, (0.1, 0.1, 0.2, 0.2), t_roi))
checks += 1

print(f"82-detection-fasterrcnn-yolo-detr (CV-DETECTEURS-014): {checks} checks passed")
