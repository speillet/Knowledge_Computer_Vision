# Review — Harris and Shi–Tomasi — local structure and trackable points — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 4 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CORNERS-001 | The error ellipse gives a quantitative comparison: supported mechanism; additional case is a project deduction | Interpreting local values. | 2 recall criteria; 305 → 387 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the error ellipse gives a quantitative comparison |
| CV-CORNERS-002 | Contrast scaling changes the response power: supported mechanism; additional case is a project deduction | distinguish Harris and Shi – Tomasi scores. | 2 recall criteria; 295 → 372 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed contrast scaling changes the response power |
| CV-CORNERS-003 | A relative threshold can accept uniformly weak images: retained explanation sufficient for this extension | Set a selection of corners. | 3 recall criteria; 303 → 303 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-CORNERS-004 | Repeatability and identity need separate denominators: supported mechanism; additional case is a project deduction | distinguish detection and matching ambiguity. | 3 recall criteria; 311 → 385 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed repeatability and identity need separate denominators |
| CV-CORNERS-005 | Survivor-only error can reward excessive rejection: supported mechanism; additional case is a project deduction | Evaluate a selection for tracking. | 3 recall criteria; 294 → 372 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed survivor-only error can reward excessive rejection |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV Harris](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html) — structure tensor, eigenvalue interpretation and Harris response. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [OpenCV tracking](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html) — goodFeaturesToTrack quality and spacing contract. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
