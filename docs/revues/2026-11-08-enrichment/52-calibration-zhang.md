# Review — Camera calibration with a target — Zhang’s method — 2026-11-08

## Overview

7 cards reviewed in `approfondir` mode: 5 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 7 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ZHANG-001 | A known target scale fixes translation units: retained explanation sufficient for this extension | There are three geometric objectives. | 3 recall criteria; 327 → 327 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-ZHANG-002 | Homogeneous scale is not another camera parameter: supported mechanism; additional case is a project deduction | interpret the projection conventions. | 3 recall criteria; 360 → 438 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed homogeneous scale is not another camera parameter |
| CV-ZHANG-003 | Different images can repeat the same constraint: supported mechanism; additional case is a project deduction | Explain the multi-view constraints. | 3 recall criteria; 329 → 403 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed different images can repeat the same constraint |
| CV-ZHANG-004 | Low pixel RMS can coexist with metric scale bias: supported mechanism; additional case is a project deduction | interpret a RMS without an abusive conclusion. | 2 recall criteria; 324 → 401 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed low pixel rms can coexist with metric scale bias |
| CV-ZHANG-005 | A transform chain avoids order mistakes: supported mechanism; additional case is a project deduction | Spreading a pixel transformation. | 2 recall criteria; 320 → 397 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a transform chain avoids order mistakes |
| CV-ZHANG-006 | Parameter stability needs withheld acquisition groups: supported mechanism; additional case is a project deduction | Diagnose observability. | 3 recall criteria; 310 → 388 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed parameter stability needs withheld acquisition groups |
| CV-ZHANG-007 | Measurement uncertainty includes the working plane: retained explanation sufficient for this extension | Build consistent collection and validation. | 3 recall criteria; 316 → 316 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [Zhang calibration](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) — §§2–4 intrinsic constraints, refinement and degeneracy. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [OpenCV calibration](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) — pinhole and distortion conventions. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
