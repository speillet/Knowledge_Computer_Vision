# Review — NMS — suppressing redundant detections — 2026-11-08

## Overview

6 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-001 | A common geometric transform preserves IoU: supported foundation; new case is a project deduction | unroll hard NMS. | 2 recall criteria; 315 → 391 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a common geometric transform preserves iou |
| CV-NMS-002 | AP requires the score-ranking information retained: supported foundation; new case is a project deduction | There are three thresholds. | 3 recall criteria; 324 → 399 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed ap requires the score-ranking information retained |
| CV-NMS-003 | Cross-class scores may not have a shared meaning: supported foundation; new case is a project deduction | Choose the scope of a deletion. | 2 recall criteria; 322 → 397 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed cross-class scores may not have a shared meaning |
| CV-NMS-004 | The Gaussian parameter controls attenuation strength: supported foundation; new case is a project deduction | Explain the effect of Soft-NMS. | 2 recall criteria; 325 → 402 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed the gaussian parameter controls attenuation strength |
| CV-NMS-005 | Coverage loss needs a one-to-one object interpretation: supported foundation; new case is a project deduction | Find the cause of a disappearance. | 3 recall criteria; 342 → 418 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed coverage loss needs a one-to-one object interpretation |
| CV-NMS-006 | Containment and overlap use different denominators: supported foundation; new case is a project deduction | interpret the inclusion of boxes in a deletion by IoU. | 2 recall criteria; 307 → 382 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed containment and overlap use different denominators |

## Reference findings and applied corrections

Canonical revision 8 → 9; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [Soft-NMS](https://arxiv.org/html/1704.04503v2) — §4 greedy selection and score decay; §5 score filtering. Consulted 2026-11-08.

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
