# Review — Epipolar geometry, PnP and triangulation — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 5 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-EPIPOLAIRE-001 | The matrix relation fixes the coordinate contract: supported mechanism; additional case is a project deduction | distinguish E and F. | 2 recall criteria; 283 → 354 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the matrix relation fixes the coordinate contract |
| CV-EPIPOLAIRE-002 | A cheirality choice does not establish metric scale: supported mechanism; additional case is a project deduction | Interpret the translation scale. | 2 recall criteria; 296 → 368 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a cheirality choice does not establish metric scale |
| CV-EPIPOLAIRE-003 | The two problems fail for different missing evidence: supported mechanism; additional case is a project deduction | choose PnP or triangulation. | 2 recall criteria; 290 → 363 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the two problems fail for different missing evidence |
| CV-EPIPOLAIRE-004 | Depth error grows faster than disparity error: supported mechanism; additional case is a project deduction | detect a low parallax. | 2 recall criteria; 283 → 357 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed depth error grows faster than disparity error |
| CV-EPIPOLAIRE-005 | Minimal solutions need disambiguating observations: supported mechanism; additional case is a project deduction | meet the minimum variant of pose. | 3 recall criteria; 279 → 351 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed minimal solutions need disambiguating observations |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) — essential/fundamental constraints, recoverPose and triangulatePoints. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [OpenCV PnP](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html) — pose direction and P3P solver point requirements. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
