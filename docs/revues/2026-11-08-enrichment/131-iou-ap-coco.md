# Review — IoU and AP — the COCO detection protocol — 2026-11-08

## Overview

7 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 1 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IOU-AP-001 | Normalization must precede a shared geometric comparison: supported foundation; new case is a project deduction | calculate a overlap in the right contract. | 3 recall criteria; 309 → 388 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed normalization must precede a shared geometric comparison |
| CV-IOU-AP-002 | AP aggregation omits undefined categories according to protocol: supported foundation; new case is a project deduction | Distinguish between local measurement and aggregated protocol. | 3 recall criteria; 317 → 395 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed ap aggregation omits undefined categories according to protocol |
| CV-IOU-AP-003 | A late false positive need not reduce interpolated AP: supported foundation; new case is a project deduction | Explain the penalty for a duplicate. | 2 recall criteria; 306 → 381 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a late false positive need not reduce interpolated ap |
| CV-IOU-AP-004 | The recall-grid endpoint changes the arithmetic: supported foundation; new case is a project deduction | rebuild a simple interpolated AP. | 3 recall criteria; 324 → 403 lexical words | Canonical explanation aligned; ID and front preserved | Important | Restore recall and precision as the quantities used in AP101; Developed the recall-grid endpoint changes the arithmetic |
| CV-IOU-AP-005 | Identical boxes are insufficient without identical filtering: supported foundation; new case is a project deduction | Compare evaluators with caution. | 3 recall criteria; 310 → 385 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed identical boxes are insufficient without identical filtering |
| CV-IOU-AP-006 | Small objects have a smaller pixel-shift allowance: supported foundation; new case is a project deduction | diagnose a deviation according to the location requirement. | 2 recall criteria; 290 → 365 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed small objects have a smaller pixel-shift allowance |
| CV-IOU-AP-007 | Operational burden depends on prevalence and throughput: supported foundation; new case is a project deduction | link average benchmark and business decision. | 3 recall criteria; 319 → 394 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed operational burden depends on prevalence and throughput |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

- CV-IOU-AP-004: Restore recall and precision as the quantities used in AP101.



## Sources

- [COCO evaluator](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py) — evaluateImg, accumulate and Params at pinned commit. Consulted 2026-11-08.

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
