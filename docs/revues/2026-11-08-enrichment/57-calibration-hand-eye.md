# Review — Hand–eye calibration — solving AX = XB with consistent coordinate frames — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 4 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HANDEYE-001 | Pose pairing creates correlated relative motions: supported mechanism; additional case is a project deduction | drift the relative movements. | 3 recall criteria; 280 → 354 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed pose pairing creates correlated relative motions |
| CV-HANDEYE-002 | A valid rigid matrix can still have wrong units: supported mechanism; additional case is a project deduction | respect the meaning of the poses API. | 3 recall criteria; 319 → 397 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a valid rigid matrix can still have wrong units |
| CV-HANDEYE-003 | Tiny rotations provide weak translation leverage: supported mechanism; additional case is a project deduction | Exciting the observable directions. | 2 recall criteria; 284 → 357 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed tiny rotations provide weak translation leverage |
| CV-HANDEYE-004 | Closure residuals need separate position and angle scales: supported mechanism; additional case is a project deduction | Test the closing of the chain. | 3 recall criteria; 320 → 398 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed closure residuals need separate position and angle scales |
| CV-HANDEYE-005 | Write the new invariant before reusing a solver: retained explanation sufficient for this extension | Distinguish between eye-in-hand and eye-to-hand. | 2 recall criteria; 323 → 323 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV calibrateHandEye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) — input/output frame directions, eye-in-hand/eye-to-hand equations and minimum motions; checked with Context7. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
