"""Recompute the constructed size check added to CV-VLM-002 (reference 121-vlm-grounding,
2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/121-vlm-grounding.py
Sizes from BLIP-2 section 3.1: 32 queries of dimension 768; ViT-L/14 features 257 x 1024.
The per-patch count (224 / 14)^2 is a project calculation for a LLaVA-style projection.
"""
checks = 0

z = 32 * 768
vit = 257 * 1024
assert z == 24576 and vit == 263168
assert abs(vit / z - 10.7) < 0.01
checks += 1

patches = (224 // 14) ** 2
assert 224 % 14 == 0 and patches == 256 and patches + 1 == 257   # plus the class token
assert patches / 32 == 8
checks += 1

print(f"121-vlm-grounding (CV-VLM-002): {checks} checks passed")
