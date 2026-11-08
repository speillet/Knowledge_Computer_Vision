# Review — SORT — multi-object tracking with motion and association — 2026-11-08

## Overview

8 cards reviewed in `approfondir` mode: 8 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 8 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SORT-001 | A confident correction can preserve a wrong identity: supported mechanism; additional case is a project deduction | Separate the responsibilities of the tracker. | 3 recall criteria; 311 → 384 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a confident correction can preserve a wrong identity |
| CV-SORT-002 | Area rate has a different unit from center rate: supported mechanism; additional case is a project deduction | interpret a state and its units. | 3 recall criteria; 333 → 414 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed area rate has a different unit from center rate |
| CV-SORT-003 | Posterior variance gives a second scalar check: supported mechanism; additional case is a project deduction | interpret the weight of a measure. | 2 recall criteria; 297 → 365 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed posterior variance gives a second scalar check |
| CV-SORT-004 | A kept track and a published track are different states: supported mechanism; additional case is a project deduction | Distinguish between memory and transmission. | 2 recall criteria; 316 → 390 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a kept track and a published track are different states |
| CV-SORT-005 | Admissibility can be a lexicographic objective: supported mechanism; additional case is a project deduction | Understanding rejection after assignment. | 2 recall criteria; 314 → 392 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed admissibility can be a lexicographic objective |
| CV-SORT-006 | Trace the first divergence, not only the final ID: supported mechanism; additional case is a project deduction | Make a discriminating diagnosis. | 3 recall criteria; 310 → 383 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed trace the first divergence, not only the final id |
| CV-SORT-007 | Per-frame geometry is invariant to ID renaming: supported mechanism; additional case is a project deduction | Distinguish between temporal tasks. | 3 recall criteria; 296 → 373 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed per-frame geometry is invariant to id renaming |
| CV-SORT-008 | Dropped frames change motion and lifecycle assumptions: supported mechanism; additional case is a project deduction | define a complete performance measure. | 3 recall criteria; 304 → 378 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed dropped frames change motion and lifecycle assumptions |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [SORT implementation](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py) — KalmanBoxTracker, associate_detections_to_trackers and Sort.update at pinned commit. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [SORT paper](https://arxiv.org/html/1602.00763v2) — §3 model, association and lifecycle. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
