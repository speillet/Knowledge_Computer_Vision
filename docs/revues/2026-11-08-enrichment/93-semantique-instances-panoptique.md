# Review — Semantic, instance and panoptic segmentation — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SEGMENTATION-001 | Instance IDs are local identities unless stated otherwise: supported foundation; new case is a project deduction | Select the segmentation output. | 3 recall criteria; 283 → 357 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed instance ids are local identities unless stated otherwise |
| CV-SEGMENTATION-002 | Semantic supervision cannot choose an instance partition: supported foundation; new case is a project deduction | Detecting a bad job definition. | 2 recall criteria; 270 → 346 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed semantic supervision cannot choose an instance partition |
| CV-SEGMENTATION-003 | Padding requires an explicit ignored-label policy: supported foundation; new case is a project deduction | Propagating a dense increase. | 2 recall criteria; 293 → 371 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed padding requires an explicit ignored-label policy |
| CV-SEGMENTATION-004 | A small structure can vanish inside a favorable average: supported foundation; new case is a project deduction | Evaluate medical segmentation. | 3 recall criteria; 290 → 374 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a small structure can vanish inside a favorable average |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [Panoptic Segmentation](https://arxiv.org/html/1801.00868v3) — §3 task format and §4 segment matching/PQ. Consulted 2026-11-08.

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
