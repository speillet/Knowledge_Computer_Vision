"""Recompute the constructed examples of CV-VLM (reference 121-vlm-grounding).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/121-vlm-grounding.py
Inputs: BLIP-2 Sec. 3.1 (32 x 768 queries, 257 x 1024 ViT-L/14 features), Florence-2 Sec. 3
(1,000 location bins), RT-2 Sec. 3.2 and OpenVLA Sec. 3.2 (256 action bins), pi0 Sec. IV
(chunks of H = 50 actions), POPE Sec. 5.1 (1:1 yes/no balance). Scenes and numbers are constructed.
"""

# --- Example A: visual token budget and the resolution of small objects -------------
patch, side = 14, 224
grid = side // patch
# Check 1: ViT-L/14 at 224 px gives a 16 x 16 grid, 256 patch tokens + 1 class token = 257 (BLIP-2 Sec. 3.1).
assert grid == 16 and grid * grid + 1 == 257
# Check 2: the Q-Former output 32 x 768 holds about 10.7 times fewer values than 257 x 1024.
assert round(257 * 1024 / (32 * 768), 1) == 10.7
# Check 3: a 4000 px wide image resized to 224 px puts 250 original px in one 14 px patch;
# a 20 px defect covers 0.08 of a patch width.
assert 4000 / grid == 250 and 20 / (4000 / grid) == 0.08

# --- Example B: sampling a long video for indexing ----------------------------------
hours, step_s, tokens_per_frame = 8, 1, 256
frames = hours * 3600 // step_s
# Check 4: 8 h sampled every 1 s gives 28,800 frames and 7,372,800 visual tokens at 256 per frame.
assert frames == 28_800 and frames * tokens_per_frame == 7_372_800
# Check 5: with a uniformly random sampling phase, an event of duration d < step contains a sample
# with probability d / step: 2 s events seen with probability 0.4 at a 5 s step.
assert 2 / 5 == 0.4

# --- Example C: location tokens and action tokens --------------------------------------
# Check 6: 1,000 location bins over a 4000 px wide image are 4 px wide (Florence-2 Sec. 3);
# rounding to a bin centre gives up to 2 px error per coordinate.
assert 4000 / 1000 == 4 and 4000 / 1000 / 2 == 2
# Check 7: 256 bins between the 1st and 99th percentiles of a +/-5 cm action range are about 0.39 mm wide.
assert abs(0.10 / 256 * 1000 - 0.39) < 0.01
# Check 8: an action chunk of H = 50 at 50 Hz spans 1 s of control.
assert 50 / 50 == 1.0

# --- Example D: why POPE reports the "yes" ratio --------------------------------------
n_pos = n_neg = 500                      # 1:1 balance of present and absent objects
tp, fp, fn, tn = n_pos, n_neg, 0, 0      # a model that always answers "yes"
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)
accuracy = (tp + tn) / (n_pos + n_neg)
# Check 9: always "yes" gives accuracy 0.5, precision 0.5, recall 1.0, F1 0.667, yes-ratio 1.0
# ("yes" taken as the positive class).
assert accuracy == 0.5 and precision == 0.5 and recall == 1.0 and abs(f1 - 2 / 3) < 1e-12

print("121-vlm-grounding: 9 checks passed (token budget, video sampling, location and action bins, yes bias)")
