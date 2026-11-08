# Review — Point clouds, BEV and occupancy representations — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BEV-001 | A pillar can encode height without retaining height cells: supported foundation; new case is a project deduction | distinguish voxel pillar and BEV. | 2 recall criteria; 286 → 370 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a pillar can encode height without retaining height cells |
| CV-BEV-002 | Repeated absence needs a visibility model: supported foundation; new case is a project deduction | Preserving the unknown. | 2 recall criteria; 277 → 350 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed repeated absence needs a visibility model |
| CV-BEV-003 | An inside probability is not a signed distance: supported foundation; new case is a project deduction | Separate the sense of occupation. | 2 recall criteria; 277 → 354 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed an inside probability is not a signed distance |
| CV-BEV-004 | Ego compensation does not make moving objects static: supported foundation; new case is a project deduction | check a BEV merge. | 2 recall criteria; 294 → 370 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed ego compensation does not make moving objects static |
| CV-BEV-005 | The output needs age and unknown-state semantics: supported foundation; new case is a project deduction | Designing a warehouse perception. | 3 recall criteria; 318 → 395 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed the output needs age and unknown-state semantics |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

The PointPillars CVF HTML page returned HTTP 403; the primary arXiv PDF was accessible. The Occupancy Networks CVF PDF also returned 403; its arXiv HTML was accessible and used. No new learned occupancy calibration or safety certification is asserted.

## Sources

- [OctoMap](https://octomap.github.io/) — explicit distinction between occupied, free and unknown space. Consulted 2026-11-08.
- [PointPillars](https://arxiv.org/pdf/1812.05784) — §2 learned pillar encoding and pseudo-image representation. Consulted 2026-11-08.
- [Occupancy Networks](https://arxiv.org/html/1812.03828v1) — §3 continuous inside/outside occupancy function. Consulted 2026-11-08.

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
