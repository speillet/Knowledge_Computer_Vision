# Review — 3D detection, object pose and articulated pose — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 3 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-POSE3D-001 | Pose alignment changes the meaning of an error: supported mechanism; additional case is a project deduction | name the output of pose. | 2 recall criteria; 287 → 365 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed pose alignment changes the meaning of an error |
| CV-POSE3D-002 | Dimension swaps can pass a center-only check: supported mechanism; additional case is a project deduction | check a box 3D. | 2 recall criteria; 301 → 381 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed dimension swaps can pass a center-only check |
| CV-POSE3D-003 | Localization matching leaves other box errors to other metrics: supported mechanism; additional case is a project deduction | distinguish nuScenes and COCO. | 2 recall criteria; 274 → 351 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed localization matching leaves other box errors to other metrics |
| CV-POSE3D-004 | Symmetry can be broken by observable texture: retained explanation sufficient for this extension | respect the symmetries of pose. | 2 recall criteria; 289 → 289 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [BOP tasks](https://bop.felk.cvut.cz/tasks/) — 6D localization and symmetry-aware VSD/MSSD/MSPD task definitions. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [nuScenes evaluation](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md) — center-distance matching and separate true-positive error terms. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
