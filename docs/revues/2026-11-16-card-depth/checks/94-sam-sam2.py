"""Recompute the sizes and constructed numbers added to CV-SAM-001 and CV-SAM-002 and
shown in the figure cv-sam-architecture.svg (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/94-sam-sam2.py
Sizes: Kirillov et al. 2023, App. A; segment-anything at dca509f, build_sam.py L62-L65,
prompt_encoder.py L50-L59, mask_decoder.py L49-L69 and L101-L107.
Data-engine figures: Ravi et al. 2024 (arXiv v2), Sec. 5.1, Table 1, App. E.2.2.
"""

checks = 0

# Figure sizes (schematic layout, factual sizes).
image_size, patch = 1024, 16
emb = image_size // patch
assert emb == 64                                   # 64 x 64 embedding, stride 16
upscaled = emb * 2 * 2                             # two stride-2 transposed convolutions
assert upscaled == 256                             # 256 x 256 low-resolution logits
assert upscaled * 4 == image_size                  # logits at a quarter of the input
mask_prompt = 4 * emb                              # mask input at 4x the embedding size
assert mask_prompt == 256 and mask_prompt // 2 // 2 == emb   # two 2x2 stride-2 convs
transformer_dim = 256
assert transformer_dim // 4 == 64 and transformer_dim // 8 == 32   # 64 then 32 channels
checks += 1

# Token selection: 3 multimask outputs + 1 single-output token; slice(1, None) or slice(0, 1).
num_mask_tokens = 3 + 1
tokens = list(range(num_mask_tokens))
assert tokens[slice(1, None)] == [1, 2, 3] and tokens[slice(0, 1)] == [0]
checks += 1

# Data engine (Table 1): Phase 1 SAM per frame vs Phase 3 SAM 2 in the loop.
t1, t3 = 37.8, 4.5
assert abs(t1 / t3 - 8.4) < 1e-9
frames = 20 * 6                                    # 20-s clip at the 6 frames/s annotation rate
assert frames == 120
assert abs(frames * t1 / 60 - 75.6) < 1e-9 and abs(frames * t3 / 60 - 9.0) < 1e-9
edited = 0.1904 * frames
assert round(edited) == 23 and abs(edited - 22.848) < 1e-9
checks += 1

print(f"94-sam-sam2 (CV-SAM-001, CV-SAM-002, figure): {checks} checks passed")
