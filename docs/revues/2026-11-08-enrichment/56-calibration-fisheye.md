# Review — Fisheye calibration — angular projection and off-center validation — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 4 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FISHEYE-001 | Zero coefficients still leave an angular camera: supported mechanism; additional case is a project deduction | distinguish projection fisheye and pinhole. | 2 recall criteria; 306 → 378 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed zero coefficients still leave an angular camera |
| CV-FISHEYE-002 | Peripheral views need usable corner localization: supported mechanism; additional case is a project deduction | design wide angle calibration views. | 3 recall criteria; 305 → 377 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed peripheral views need usable corner localization |
| CV-FISHEYE-003 | An average weights regions by observation count: supported mechanism; additional case is a project deduction | Locate a camera model defect. | 3 recall criteria; 298 → 374 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed an average weights regions by observation count |
| CV-FISHEYE-004 | Rectification rotation changes the ray frame: retained explanation sufficient for this extension | Propagating the contract after rectification. | 2 recall criteria; 311 → 311 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-FISHEYE-005 | More visible field can mean fewer samples per angle: supported mechanism; additional case is a project deduction | interpret the rectified field parameter. | 2 recall criteria; 284 → 363 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed more visible field can mean fewer samples per angle |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV fisheye](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html) — angular projection, remap/rectification and balance definition; checked with Context7. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
