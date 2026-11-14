"""Recompute the constructed examples of CV-SAM (reference 94-sam-sam2).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/94-sam-sam2.py
Inputs come from SAM (arXiv 2304.02643v1, App. A: 1024 x 1024 input, 64 x 64 embedding, masks 4x
below the input), the segment-anything code at commit dca509f (ResizeLongestSide rounding, bottom/right
padding, 256 x 256 low-resolution logits) and SAM 2 (arXiv 2408.00714v2: N = 6 memories, 43.8 and
30.2 FPS, Nclick = 3, Table 9a). The frame size, click, frame rates and budgets are constructed.
"""


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def preprocess_shape(h, w, long_side=1024):
    """segment_anything.utils.transforms.ResizeLongestSide.get_preprocess_shape."""
    scale = long_side * 1.0 / max(h, w)
    return int(h * scale + 0.5), int(w * scale + 0.5)


# --- Example A: the data contract of one SAM prompt ---------------------------
H, W = 1080, 1920                       # constructed full-HD frame
new_h, new_w = preprocess_shape(H, W)
# Check 1: the long side becomes 1024 and the short side 576; 448 rows of padding are added at the bottom.
assert (new_h, new_w) == (576, 1024) and 1024 - new_h == 448
# Check 2: a click at the image centre (960, 540) maps to (512, 288) in the resized input (apply_coords).
x, y = 960 * (new_w / W), 540 * (new_h / H)
assert close(x, 512.0, 1e-9) and close(y, 288.0, 1e-9)
# Check 3: the 64 x 64 embedding has a 16-pixel stride on the 1024 input; the 256 x 256 logits a 4-pixel stride.
assert 1024 // 64 == 16 and 1024 // 256 == 4
# Check 4: one low-resolution logit cell spans 4 / (1024 / 1920) = 7.5 original pixels.
assert close(4 / (new_w / W), 7.5, 1e-9)
# Check 5: only 576 / 4 = 144 of the 256 logit rows cover the image; the rest covers padding.
assert new_h // 4 == 144
# Check 6: a 3-px-wide cable occupies 0.4 of a logit cell; a 30-px part spans 4 cells.
assert close(3 / 7.5, 0.4, 1e-12) and close(30 / 7.5, 4.0, 1e-12)

# --- Example B: memory span of SAM 2 ------------------------------------------
N_MEM = 6                                # default number of recent-frame memories (App. A.2)
# Check 7: six recent frames cover 0.2 s at 30 frames/s and 0.4 s at 15 frames/s.
assert close(N_MEM / 30, 0.2, 1e-12) and close(N_MEM / 15, 0.4, 1e-12)
# Check 8: an occlusion of 1 s at 30 frames/s lasts 30 frames, five times the recent-memory window.
assert 30 * 1.0 / N_MEM == 5.0

# --- Example C: interaction budgets and speed ------------------------------------
# Check 9: Nclick = 3 on up to 8 interacted frames is at most 24 clicks per object (Sec. 6.1).
assert 3 * 8 == 24
# Check 10: 43.8 and 30.2 frames/s correspond to 22.8 and 33.1 ms per frame (A100, batch 1, Sec. 7).
assert close(1000 / 43.8, 22.83, 0.01) and close(1000 / 30.2, 33.11, 0.01)
# Check 11: Table 9a: going from 512 to 1024 input divides the speed by 1 / 0.22 = 4.5 for +1.6 J&F
# (9 zero-shot) and +1.8 mIoU (SA-23) in the ablation model.
assert close(1 / 0.22, 4.545, 1e-3) and close(72.3 - 70.7, 1.6, 1e-9) and close(61.5 - 59.7, 1.8, 1e-9)
# Check 12: a 1024 x 1024 input has 4x the pixels of 512 x 512, consistent with a speed ratio near 1/4.
assert (1024 * 1024) / (512 * 512) == 4

print("94-sam-sam2: 12 checks passed")
