# Review — Semantic, instance and panoptic segmentation — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 3 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SEGMENTATION-001 | Instance IDs are local identities unless stated otherwise: supported mechanism; additional case is a project deduction | Select the segmentation output. | 3 recall criteria; 283 → 357 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed instance ids are local identities unless stated otherwise |
| CV-SEGMENTATION-002 | Semantic supervision cannot choose an instance partition: retained explanation sufficient for this extension | Detecting a bad job definition. | 2 recall criteria; 270 → 270 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-SEGMENTATION-003 | Padding requires an explicit ignored-label policy: supported mechanism; additional case is a project deduction | Propagating a dense increase. | 2 recall criteria; 293 → 371 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed padding requires an explicit ignored-label policy |
| CV-SEGMENTATION-004 | A small structure can vanish inside a favorable average: supported mechanism; additional case is a project deduction | Evaluate medical segmentation. | 3 recall criteria; 290 → 374 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a small structure can vanish inside a favorable average |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [Panoptic Segmentation](https://arxiv.org/html/1801.00868v3) — §3 task format and §4 segment matching/PQ. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
