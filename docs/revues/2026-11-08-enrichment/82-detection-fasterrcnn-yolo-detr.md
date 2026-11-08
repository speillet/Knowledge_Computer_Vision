# Review — Detection: Faster R-CNN, YOLO families and DETR — 2026-11-08

## Overview

13 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 2 important, 0 minor, 11 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-001 | Shared features do not make proposal count free: supported foundation; new case is a project deduction | Find the sharing of features. | 2 recall criteria; 291 → 366 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed shared features do not make proposal count free |
| CV-DETECTEURS-002 | A checkpoint name needs an export contract: supported foundation; new case is a project deduction | Do not generalize the whole YOLO family. | 2 recall criteria; 261 → 328 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a checkpoint name needs an export contract |
| CV-DETECTEURS-003 | Matching cost and optimized loss have different roles: supported foundation; new case is a project deduction | distinguish between the three assignments. | 2 recall criteria; 287 → 360 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed matching cost and optimized loss have different roles |
| CV-DETECTEURS-004 | The effective object can be only a few pixels: supported foundation; new case is a project deduction | analyze small objects after resize. | 3 recall criteria; 274 → 359 lexical words | Canonical explanation aligned; ID and front preserved | Important | Restore the missing before/after coverage condition in the small-object diagnosis; Developed the effective object can be only a few pixels |
| CV-DETECTEURS-005 | Throughput and single-image latency are different measurements: supported foundation; new case is a project deduction | compare detection pipelines. | 3 recall criteria; 274 → 351 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed throughput and single-image latency are different measurements |
| CV-DETECTEURS-006 | The training location is not an object center requirement: supported foundation; new case is a project deduction | rebuild site assignment in FCOS. | 3 recall criteria; 305 → 385 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed the training location is not an object center requirement |
| CV-DETECTEURS-007 | A site on the boundary has a zero distance: supported foundation; new case is a project deduction | Calculate the distance regression targets. | 2 recall criteria; 292 → 379 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a site on the boundary has a zero distance |
| CV-DETECTEURS-008 | The logit gradient includes a second term: supported foundation; new case is a project deduction | Explain the modulation of easy negatives by Focal Loss. | 2 recall criteria; 315 → 403 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed the logit gradient includes a second term |
| CV-DETECTEURS-009 | Enclosing geometry distinguishes some disjoint positions: supported foundation; new case is a project deduction | explain the signal of GIoU for disjointed boxes. | 2 recall criteria; 332 → 403 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed enclosing geometry distinguishes some disjoint positions |
| CV-DETECTEURS-010 | Upsampling adds locations, not recovered measurements: supported foundation; new case is a project deduction | explain the contribution of the lateral connections of FPN. | 2 recall criteria; 322 → 394 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed upsampling adds locations, not recovered measurements |
| CV-DETECTEURS-011 | An error category is not a causal diagnosis: supported foundation; new case is a project deduction | Distinguish between class, location, and duplicate errors. | 3 recall criteria; 310 → 386 lexical words | Canonical explanation aligned; ID and front preserved | Important | Use the TIDE duplicate-error category instead of a mistranslated label; Developed an error category is not a causal diagnosis |
| CV-DETECTEURS-012 | Annotation fixes must follow the declared policy: supported foundation; new case is a project deduction | Diagnose a false positive that may come from a missing annotation. | 2 recall criteria; 309 → 383 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed annotation fixes must follow the declared policy |
| CV-DETECTEURS-013 | Multiple instances and multiple valid labels are separate axes: supported foundation; new case is a project deduction | distinguish instances, classes, and labels by instance. | 3 recall criteria; 321 → 396 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed multiple instances and multiple valid labels are separate axes |

## Reference findings and applied corrections

Canonical revision 9 → 10; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

- CV-DETECTEURS-004: Restore the missing before/after coverage condition in the small-object diagnosis.
- CV-DETECTEURS-011: Use the TIDE duplicate-error category instead of a mistranslated label.

The attempted GIoU v12 HTML URL returned 404; the cited v2 HTML was accessible and used. New geometric numbers are constructed checks, not detector measurements.

## Sources

- [DETR](https://arxiv.org/html/2005.12872v3) — §3.1 bipartite assignment and set loss. Consulted 2026-11-08.
- [FCOS](https://arxiv.org/html/1904.01355v5) — §§3.1–3.3 target distances, level assignment and centerness. Consulted 2026-11-08.
- [Focal Loss](https://arxiv.org/html/1708.02002v2) — §3.2 modulating factor. Consulted 2026-11-08.
- [GIoU](https://arxiv.org/html/1902.09630v2) — §3 enclosing geometry. Consulted 2026-11-08.
- [FPN](https://arxiv.org/html/1612.03144v2) — §3 lateral/top-down fusion. Consulted 2026-11-08.
- [TIDE](https://arxiv.org/html/2008.08115v2) — §2.2 error taxonomy and annotation limitations. Consulted 2026-11-08.
- [Faster R-CNN](https://arxiv.org/html/1506.01497v3) — §3 shared convolutional features. Consulted 2026-11-08.

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
