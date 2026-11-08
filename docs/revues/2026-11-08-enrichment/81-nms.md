# Review — NMS — suppressing redundant detections — 2026-11-08

## Overview

6 cards reviewed in `approfondir` mode: 5 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-001 | A common geometric transform preserves IoU: supported mechanism; additional case is a project deduction | unroll hard NMS. | 2 recall criteria; 315 → 391 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a common geometric transform preserves iou |
| CV-NMS-002 | AP requires the score-ranking information retained: supported mechanism; additional case is a project deduction | There are three thresholds. | 3 recall criteria; 324 → 399 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed ap requires the score-ranking information retained |
| CV-NMS-003 | Cross-class scores may not have a shared meaning: supported mechanism; additional case is a project deduction | Choose the scope of a deletion. | 2 recall criteria; 322 → 397 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed cross-class scores may not have a shared meaning |
| CV-NMS-004 | The Gaussian parameter controls attenuation strength: supported mechanism; additional case is a project deduction | Explain the effect of Soft-NMS. | 2 recall criteria; 325 → 402 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the gaussian parameter controls attenuation strength |
| CV-NMS-005 | Coverage loss needs a one-to-one object interpretation: supported mechanism; additional case is a project deduction | Find the cause of a disappearance. | 3 recall criteria; 342 → 418 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed coverage loss needs a one-to-one object interpretation |
| CV-NMS-006 | Containment and overlap use different denominators: retained explanation sufficient for this extension | interpret the inclusion of boxes in a deletion by IoU. | 2 recall criteria; 307 → 307 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 8 → 9; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [Soft-NMS](https://arxiv.org/html/1704.04503v2) — §4 greedy selection and score decay; §5 score filtering. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
