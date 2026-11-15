"""Recompute the constructed example of CV-PIPELINE-006 (reference 141-contrats-profiling-video).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-15-accepted-proposals/checks/141-contrats-profiling-video.py

Conventions (project choices, stated in the card and in the reference's example F):
- continuous coordinates with the origin at the top-left corner of the first pixel; integer
  pixel index u has its centre at u + 0.5;
- letterbox with r = min(S/W, S/H), content round(rW) x round(rH), padding split equally;
- forward map x' = r x + p_x, inverse x = (x' - p_x) / r.
Checked against OpenCV 4.13.0, modules/imgproc/src/resize.cpp:
- L4101: bilinear source index fx = (dx + 0.5) * scale_x - 0.5 (pixel-centre convention);
- L4216-L4221: when dsize is given, inv_scale_x = dsize.width / ssize.width, i.e. the applied
  scale comes from the integer sizes, not from r.
No image is processed and no OpenCV call is executed.
"""

from fractions import Fraction as F

checks = 0

W, H, S = 1920, 1080, 640
r = min(F(S, W), F(S, H))
cw, ch = round(r * W), round(r * H)
px, py = F(S - cw, 2), F(S - ch, 2)

# Check 1: scale 1/3, content 640x360, padding 0 and 140, 43.75 % of the input is padding.
assert r == F(1, 3) and (cw, ch) == (640, 360) and (px, py) == (0, 140)
assert 1 - F(ch, S) == F(4375, 10000)
checks += 1

# Check 2: the applied scale per axis (content / source sizes, resize.cpp L4218-L4219)
# equals r here, so the inverse may use r on both axes.
assert F(cw, W) == r and F(ch, H) == r
checks += 1


def inverse(box, sx=r, sy=r, ox=px, oy=py):
    x1, y1, x2, y2 = box
    return ((x1 - ox) / sx, (y1 - oy) / sy, (x2 - ox) / sx, (y2 - oy) / sy)


def forward(box):
    x1, y1, x2, y2 = box
    return (r * x1 + px, r * y1 + py, r * x2 + px, r * y2 + py)


model_box = (320, 290, 416, 350)
src_box = inverse(model_box)

# Check 3: the card's box maps back to (960, 450, 1248, 630) and the forward map returns it.
assert src_box == (960, 450, 1248, 630) and forward(src_box) == model_box
checks += 1

# Check 4: forgetting the padding shifts y by p_y / r = 420 px, constant, x and sizes unchanged.
no_pad = inverse(model_box, ox=0, oy=0)
assert no_pad == (960, 870, 1248, 1050)
assert [a - b for a, b in zip(no_pad, src_box)] == [0, 420, 0, 420] and py / r == 420
checks += 1

# Check 5: with the padding forgotten, content rows y' in [140, 500] land at [420, 1500]:
# nothing reaches the top 420 rows, and a true y above 660 is pushed past the 1080 px edge.
assert (F(140) / r, F(500) / r) == (420, 1500)
# The wrong y equals H = 1080 at model row y' = 360, whose true y is (360 - 140) * 3 = 660.
y_edge = H * r
assert y_edge == 360 and inverse((0, y_edge, 0, y_edge))[1] == 660
for y_model in (F(361), F(450), F(499)):
    wrong_y, true_y = y_model / r, (y_model - py) / r
    assert wrong_y > H and true_y > 660
checks += 1

# Check 6: the reference's example F box (100, 200, 300, 400) -> (300, 180, 900, 780).
assert inverse((100, 200, 300, 400)) == (300, 180, 900, 780)
checks += 1

# Check 7: wrong order (divide first, then subtract the padding in source pixels) leaves
# p_y (1/r - 1) = 280 px of offset.
wrong_order_y1 = F(290) / r - py
assert wrong_order_y1 - 450 == 280 and py * (1 / r - 1) == 280
checks += 1

# Check 8: a stretch inverse (separate factors 3 and 1.6875, no padding) on a letterboxed input
# gives y = 489.375 and 590.625 instead of 450 and 630: an error that varies with position.
stretch = inverse(model_box, sx=F(S, W), sy=F(S, H), ox=0, oy=0)
assert F(H, S) == F(16875, 10000)
assert stretch == (960, F(489375, 1000), 1248, F(590625, 1000))
assert stretch[1] - 450 != stretch[3] - 630
checks += 1

# Check 9: integer pixel indices. For destination row d of the 640x360 content, OpenCV's
# bilinear resize samples source row (d + 0.5) * 3 - 0.5 = 3d + 1 (L4101, scale_y = 1080/360).
# The model row is u' = d + 140, and u = (u' + 0.5 - p_y) / r - 0.5 returns the same row.
scale_y = F(H, ch)
for d in (0, 150, 359):
    src_row = (d + F(1, 2)) * scale_y - F(1, 2)
    u_model = d + py
    assert (u_model + F(1, 2) - py) / r - F(1, 2) == src_row == 3 * d + 1
# Ignoring the half-pixel terms (u = (u' - p_y) / r) is off by (1/r - 1)/2 = 1 source pixel.
assert ((290 + F(1, 2) - py) / r - F(1, 2)) - (290 - py) / r == (1 / r - 1) / 2 == 1
checks += 1

# Check 10: an odd padding total needs a split rule; half a model pixel is 1.5 source px here.
assert F(1, 2) / r == F(3, 2)
checks += 1

# Check 11: reference example of an odd total: 1920x1088 gives r = 1/3, content
# round(362.67) = 363 rows and 277 padding rows. Splitting 138/139 or 139/138 moves every box
# by one input row, i.e. 1088/363 = 2.997 source rows (about 1/r), the applied scale being
# 363/1088 (resize.cpp L4218-L4219).
r2 = min(F(640, 1920), F(640, 1088))
ch2 = round(r2 * 1088)
assert r2 == F(1, 3) and ch2 == 363 and 640 - ch2 == 277
s_y2 = F(ch2, 1088)
shift = (139 - 138) / s_y2
assert abs(float(shift) - 2.997) < 1e-3 and abs(float(shift - 1 / r2)) < 0.01
checks += 1

print(f"141-contrats-profiling-video (CV-PIPELINE-006): {checks} checks passed")
