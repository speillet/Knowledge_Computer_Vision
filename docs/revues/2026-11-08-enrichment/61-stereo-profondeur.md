# Review — Rectified stereo, SGM and depth — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 2 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-STEREO-001 | Principal-point offsets change effective disparity: retained explanation sufficient for this extension | Calculate a rectified depth. | 2 recall criteria; 305 → 305 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-STEREO-002 | Small disparities produce asymmetric depth errors: supported mechanism; additional case is a project deduction | Interpreting the uncertainty of depth. | 2 recall criteria; 275 → 351 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed small disparities produce asymmetric depth errors |
| CV-STEREO-003 | A fixed-point mistake gives a predictable scale error: retained explanation sufficient for this extension | decode a fixed disparity. | 2 recall criteria; 275 → 275 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-STEREO-004 | Rectification does not resolve an occluded pixel: supported mechanism; additional case is a project deduction | Separate rectification and matching. | 2 recall criteria; 277 → 350 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed rectification does not resolve an occluded pixel |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV stereo](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html) — rectified disparity/depth relationship. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [OpenCV calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) — stereoRectify Q matrix and reprojectImageTo3D disparity scaling. Accessed or attempted 2026-11-08, with failures qualified explicitly.

## Proposals

No new ID is created. See the [proposal register](../propositions.md) and
[overview](00-bilan.md) for the four existing pending decisions.

## Checks and limitations

Scope-wide checks and protected-field comparisons appear in the [overview](00-bilan.md).
The evidence concerns the named mechanisms and corrections, not every retained
historical sentence or implementation claim. [Pre-merge review](65-pre-merge-review.md)
removed redundant draft additions and corrected two new wording inaccuracies.
This is agent self-review, without independent scientific validation, learner
mastery, a new CV experiment or AnkiDroid rendering. Export status:
**to republish with `paquet-anki`**.
