# Review — SORT — multi-object tracking with motion and association — 2026-11-08

## Overview

8 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 8 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SORT-001 | A confident correction can preserve a wrong identity: supported foundation; new case is a project deduction | Separate the responsibilities of the tracker. | 3 recall criteria; 311 → 384 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a confident correction can preserve a wrong identity |
| CV-SORT-002 | Area rate has a different unit from center rate: supported foundation; new case is a project deduction | interpret a state and its units. | 3 recall criteria; 333 → 414 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed area rate has a different unit from center rate |
| CV-SORT-003 | Posterior variance gives a second scalar check: supported foundation; new case is a project deduction | interpret the weight of a measure. | 2 recall criteria; 297 → 365 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed posterior variance gives a second scalar check |
| CV-SORT-004 | A kept track and a published track are different states: supported foundation; new case is a project deduction | Distinguish between memory and transmission. | 2 recall criteria; 316 → 390 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a kept track and a published track are different states |
| CV-SORT-005 | Admissibility can be a lexicographic objective: supported foundation; new case is a project deduction | Understanding rejection after assignment. | 2 recall criteria; 314 → 392 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed admissibility can be a lexicographic objective |
| CV-SORT-006 | Trace the first divergence, not only the final ID: supported foundation; new case is a project deduction | Make a discriminating diagnosis. | 3 recall criteria; 310 → 383 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed trace the first divergence, not only the final id |
| CV-SORT-007 | Per-frame geometry is invariant to ID renaming: supported foundation; new case is a project deduction | Distinguish between temporal tasks. | 3 recall criteria; 296 → 373 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed per-frame geometry is invariant to id renaming |
| CV-SORT-008 | Dropped frames change motion and lifecycle assumptions: supported foundation; new case is a project deduction | define a complete performance measure. | 3 recall criteria; 304 → 378 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed dropped frames change motion and lifecycle assumptions |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [SORT implementation](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py) — KalmanBoxTracker, associate_detections_to_trackers and Sort.update at pinned commit. Consulted 2026-11-08.
- [SORT paper](https://arxiv.org/html/1602.00763v2) — §3 model, association and lifecycle. Consulted 2026-11-08.

## Proposals

No new ID is created in this pass. See the [proposal register](../propositions.md)
and [overview](00-bilan.md) for pending complementary cards and decisions.

## Checks and limitations

Scope-wide executed checks and identity/field comparisons are recorded in the
[overview](00-bilan.md). The source assessment concerns the mechanisms and
boundary cases identified above; it is not a fresh passage-by-passage
certification of every retained historical paragraph or implementation claim.
No CV experiment, hardware benchmark, independent review, learner mastery or
AnkiDroid rendering is established. Export status: to republish with `paquet-anki`.
