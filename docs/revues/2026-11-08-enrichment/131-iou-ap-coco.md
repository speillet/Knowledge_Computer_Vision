# Review — IoU and AP — the COCO detection protocol — 2026-11-08

## Overview

7 cards reviewed in `approfondir` mode: 5 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 1 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IOU-AP-001 | Normalization must precede a shared geometric comparison: supported mechanism; additional case is a project deduction | calculate a overlap in the right contract. | 3 recall criteria; 309 → 388 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed normalization must precede a shared geometric comparison |
| CV-IOU-AP-002 | AP aggregation omits undefined categories according to protocol: supported mechanism; additional case is a project deduction | Distinguish between local measurement and aggregated protocol. | 3 recall criteria; 317 → 395 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed ap aggregation omits undefined categories according to protocol |
| CV-IOU-AP-003 | A late false positive need not reduce interpolated AP: retained explanation sufficient for this extension | Explain the penalty for a duplicate. | 2 recall criteria; 306 → 306 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-IOU-AP-004 | The recall-grid endpoint changes the arithmetic: supported mechanism; additional case is a project deduction | rebuild a simple interpolated AP. | 3 recall criteria; 324 → 403 lexical words | ID/front preserved; canonical wording aligned | Important | Restore recall and precision as the quantities used in AP101; Developed the recall-grid endpoint changes the arithmetic |
| CV-IOU-AP-005 | Identical boxes are insufficient without identical filtering: supported mechanism; additional case is a project deduction | Compare evaluators with caution. | 3 recall criteria; 310 → 385 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed identical boxes are insufficient without identical filtering |
| CV-IOU-AP-006 | Small objects have a smaller pixel-shift allowance: supported mechanism; additional case is a project deduction | diagnose a deviation according to the location requirement. | 2 recall criteria; 290 → 365 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed small objects have a smaller pixel-shift allowance |
| CV-IOU-AP-007 | Operational burden depends on prevalence and throughput: retained explanation sufficient for this extension | link average benchmark and business decision. | 3 recall criteria; 319 → 319 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.

- CV-IOU-AP-004: Restore recall and precision as the quantities used in AP101.



## Sources

- [COCO evaluator](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py) — evaluateImg, accumulate and Params at pinned commit. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
