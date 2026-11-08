# Review — 3D detection, object pose and articulated pose — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-POSE3D-001 | Pose alignment changes the meaning of an error: supported foundation; new case is a project deduction | name the output of pose. | 2 recall criteria; 287 → 365 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed pose alignment changes the meaning of an error |
| CV-POSE3D-002 | Dimension swaps can pass a center-only check: supported foundation; new case is a project deduction | check a box 3D. | 2 recall criteria; 301 → 381 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed dimension swaps can pass a center-only check |
| CV-POSE3D-003 | Localization matching leaves other box errors to other metrics: supported foundation; new case is a project deduction | distinguish nuScenes and COCO. | 2 recall criteria; 274 → 351 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed localization matching leaves other box errors to other metrics |
| CV-POSE3D-004 | Symmetry can be broken by observable texture: supported foundation; new case is a project deduction | respect the symmetries of pose. | 2 recall criteria; 289 → 366 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed symmetry can be broken by observable texture |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [BOP tasks](https://bop.felk.cvut.cz/tasks/) — 6D localization and symmetry-aware VSD/MSSD/MSPD task definitions. Consulted 2026-11-08.
- [nuScenes evaluation](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md) — center-distance matching and separate true-positive error terms. Consulted 2026-11-08.

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
