# Review — NeRF, 3D Gaussian Splatting and reconstruction — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 6 to revision 7 at its declared awareness depth (`profondeur: reperage`).
Highest severity per card before correction: 0 blocking, 0 important, 3 minor, 0 with
no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-RENDU3D-001 | Field with volume rendering versus optimized explicit Gaussians with splatting: confirmed (NeRF §3–4 eq. 1; 3DGS §4–6, eq. 6). Rendering equation and units correct. Mistranslations that obscure meaning: "Weight along the radius" and "for a radius" (*ray*), "scene/material" (*hardware*), "interrogated" | Comparison of representations | 2 criteria; 358 → 368 words | Aligned with the reference appendix | Minor | Language fixes; Source given equations and sections |
| CV-RENDU3D-002 | PSNR measures image agreement, not surface accuracy; scale gauge: consistent with NeRF §6.2 and 3DGS §7.2 (image metrics on held-out views); the gauge is a correct project deduction. "reserved units and angles", "rebuild quality", "Deduct" mistranslated | Evaluation: separate rendering and geometry | 2 criteria; 336 → 341 words | Aligned | Minor | Language fixes; Source given sections |
| CV-RENDU3D-003 | Coverage, poses, static scene, unconstrained regions: consistent with 3DGS §3 (static scene) and §7.4 (artifacts in poorly observed regions, no regularization); Source cited NeRF §§3–4, which does not address coverage. "exhibition changes" (*exposure*), "Survey built", "over-adjust" mistranslated | Diagnosis of view-dependent artifacts | 2 criteria; 353 → 360 words | Aligned | Minor | Language fixes; 3DGS limitations added to the Source |

No expected answer changed. Objective lines "Implicit and primitive representation"
and "Check out a little-observed scene" are not verb-object objectives; they are
protected and reported only. Proposed: "Distinguish implicit and primitive scene
representations" and "Diagnose a poorly observed scene".

## Reference findings

Revision 6 claims checked: position-only density and view-dependent colour in the
original NeRF, volume integration, explicit anisotropic primitives with densification
in 3DGS: confirmed. Imprecisions: "weights a color by density and transmittance along
the radius" (ray), "Authors' SPFs depend on the material" (frames per second,
hardware), "split angles reserved" (held-out angles). No scientific error found.

New verified content: NeRF eqs. 1–3, alpha-compositing interpretation, $L=10$ and
$L=4$ encodings, $N_c=64$ and $N_f=128$, 4096 rays per batch, COLMAP poses for real
data, 100–300k iterations and 1–2 days on a V100, held-out metrics; 3DGS static-scene
input, SfM initialization, eqs. 5–6, quaternion and scale parameterization, sigmoid and
exponential activations, loss with $\lambda=0.2$, densification (every 100
iterations, threshold 0.0002, split factor 1.6, opacity reset every 3000), 16×16 tile
rasterizer, 4 spherical-harmonic bands, A6000 timing of 35–45 min, test split of every
8th photo, and §7.4 limitations (poorly observed regions, splotchy Gaussians, popping,
no regularization, memory above 20 GB peak for large scenes, several hundred MB to
store).

## Reference depth

Body word counts (whitespace tokens, front matter excluded, H1 included, before the
first per-card appendix): 322 → 1,862. The length follows the note's awareness depth.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Inputs (poses, bounds, SfM), scale up to a similarity, outputs of both methods, pipeline role |
| Intuition | Shallow | Developed | Fog versus ellipsoids; constructed two-layer depth illustration |
| Prerequisites | Shallow (one link) | Developed | Links to CV-BA, CV-STEREO, CV-ICP |
| Assumptions | Shallow | Developed | Static scene, poses, coverage, gauge, degenerate cases |
| Procedure | Shallow | Developed | NeRF and 3DGS optimization loops with sourced settings and purposes |
| Mathematics | Shallow | Developed | Eqs. 1–3 with units, covariance construction and projection; worked examples A–D |
| Parameters | Shallow (list) | Developed | Parameter table with source values; tuning approach |
| Properties | Shallow | Developed | Photometric objective, depth ambiguity, primitives without normals, gauge, reported limitations |
| Cost and implementation | Shallow | Developed | Training and rendering costs with hardware; execution status |
| Evaluation | Shallow | Developed | Image protocol; metric-reference baseline with a removed angular sector as the controlled variation; limits |
| Failure modes and diagnosis | Shallow (one sentence) | Developed | Five-row symptom table |
| Alternatives and sources | Shallow | Developed | Conditional choices, industrial uses labelled as project reasoning, sources split |

Constructed examples are recomputed by
[`checks/123-nerf-gaussian-splatting.py`](checks/123-nerf-gaussian-splatting.py) (6
checks): weights 0.503 and 0.493 with mean depth 2.99 between two layers; invariance of
weights under the scale gauge $(t,\sigma)\to(at,\sigma/a)$; trace 10.01 and axis
variance 9 for $\Sigma=RSS^TR^T$; 59 floats and about 236 MB per million Gaussians.

## Applied corrections

- [Reference](../../../vault/120-generatif-multimodal/references/123-nerf-gaussian-splatting.md),
  revision 6 → 7: body rewritten; appendix language fixes identical to the card fixes
  ("Question of work" → "Working question", "Reference Response" → "Reference answer",
  "Comparison built" → "Constructed comparison", "Survey built" → "Constructed
  investigation", "Weight along the radius" → "Weight along the ray", "Scale gauge
  built" → "Constructed scale gauge", "exhibition" → "exposure", "reserve" → "hold
  out"); sources split; closing line replaced.
- [Cards](../../../vault/120-generatif-multimodal/123-nerf-gaussian-splatting.md):
  language fixes in explanations and blocking errors ("Assimilate both to a guaranteed
  metric mesh" → "Equating either representation with a guaranteed metric mesh",
  "Deduct an accuracy in millimeters from a perceptual score or pixel" → "Deducing
  millimetre accuracy from a perceptual or pixel score", "Consider training views as a
  complete validation" → "Treating training views as a complete validation"); Source
  lines given equations and sections, with 3DGS added. IDs, questions, objectives,
  families, tags and deck unchanged.

No other subject's card repeats a corrected claim.

## Proposals

To register as `pending` (register not edited in this pass):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-RENDU3D-01 | CV-RENDU3D | Explain, with the quadrature weights, why a depth read from a radiance field can lie between two surfaces where no matter exists | No card tests geometry extraction from a rendering representation, the main metrology pitfall | Reasoning | 1 card, 3 criteria | [NeRF §4, eqs. 1–3](https://arxiv.org/html/2003.08934v2) |

No defective question was found.

## Sources

Scientific sources: NeRF §3, §4 eqs. 1–3, §5.1–5.3, §6.1–6.2 (arXiv HTML v2); 3D
Gaussian Splatting §1, §3, §4 eqs. 5–6, §5.1–5.2, §6, §7.1, §7.2, §7.4 (arXiv HTML
v1). French pre-migration text from commit `b7142bb^` for "matériel" and "réservés".
Author project pages retained, not re-read.

Implementation sources: none; no library API is claimed. Context7 unavailable.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | Fails only on `70-reconnaissance-representations/references/75-embeddings-biometrie.md` (another subject in progress); no error in this subject's files |
| `python3 scripts/learning_path.py` | OK, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/123-nerf-gaussian-splatting.py` | 6 checks passed |
| `git diff --check -- vault/120-generatif-multimodal/` | No whitespace error |
| Inventory of the card file | 3 cards, 368 / 341 / 360 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical (25); front matter identical except `revision`; H1 and `### CV-…` headings unchanged; `$` balanced |

No training or rendering was executed; the protocol is proposed. Obsidian and
AnkiDroid rendering are unverified. Agent self-review, without independent validation
or measured learner proficiency. Export status: **to republish with `paquet-anki`**.

For the coordinator: `Suivi-pilote.md` entry — 2026-11-14, CV-RENDU3D revision 7,
cards 001–003, corrections above, Agent Claude Code self-review, to republish with
`paquet-anki`; proposal P-CV-RENDU3D-01.
