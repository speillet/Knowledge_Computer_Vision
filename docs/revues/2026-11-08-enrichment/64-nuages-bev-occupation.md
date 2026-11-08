# Review — Point clouds, BEV and occupancy representations — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 3 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BEV-001 | A pillar can encode height without retaining height cells: supported mechanism; additional case is a project deduction | distinguish voxel pillar and BEV. | 2 recall criteria; 286 → 370 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a pillar can encode height without retaining height cells |
| CV-BEV-002 | Repeated absence needs a visibility model: supported mechanism; additional case is a project deduction | Preserving the unknown. | 2 recall criteria; 277 → 350 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed repeated absence needs a visibility model |
| CV-BEV-003 | An inside probability is not a signed distance: retained explanation sufficient for this extension | Separate the sense of occupation. | 2 recall criteria; 277 → 277 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-BEV-004 | Ego compensation does not make moving objects static: retained explanation sufficient for this extension | check a BEV merge. | 2 recall criteria; 294 → 294 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-BEV-005 | The output needs age and unknown-state semantics: supported mechanism; additional case is a project deduction | Designing a warehouse perception. | 3 recall criteria; 318 → 395 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the output needs age and unknown-state semantics |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.


The CVF PointPillars and Occupancy Networks endpoints returned HTTP 403. The primary PointPillars arXiv PDF and Occupancy Networks arXiv HTML were accessible and used.

## Sources

- [OctoMap](https://octomap.github.io/) — explicit distinction between occupied, free and unknown space. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [PointPillars](https://arxiv.org/pdf/1812.05784) — §2 learned pillar encoding and pseudo-image representation. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Occupancy Networks](https://arxiv.org/html/1812.03828v1) — §3 continuous inside/outside occupancy function. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
