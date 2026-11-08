# Review — MeanShift and CamShift — tracking an appearance distribution — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 3 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MEANSHIFT-001 | Total mass and centroid convey different evidence: supported mechanism; additional case is a project deduction | Explain a MeanShift iteration. | 2 recall criteria; 313 → 385 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed total mass and centroid convey different evidence |
| CV-MEANSHIFT-002 | Moment orientation becomes ambiguous for a round distribution: supported mechanism; additional case is a project deduction | distinguish MeanShift and CamShift. | 2 recall criteria; 316 → 388 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed moment orientation becomes ambiguous for a round distribution |
| CV-MEANSHIFT-003 | Convergence can strengthen a semantically wrong mode: supported mechanism; additional case is a project deduction | Diagnose a color distractor. | 2 recall criteria; 305 → 378 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed convergence can strengthen a semantically wrong mode |
| CV-MEANSHIFT-004 | Factorial comparison reveals interactions: retained explanation sufficient for this extension | Evaluate color and adaptation separately. | 3 recall criteria; 299 → 299 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV MeanShift/CamShift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html) — backprojection centroid iteration and moment-based adaptive window. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
