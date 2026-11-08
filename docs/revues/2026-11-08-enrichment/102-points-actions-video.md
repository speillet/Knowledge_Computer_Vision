# Review — Point tracking, actions and video understanding — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 3 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VIDEO-001 | Point identity is additional information across time: supported mechanism; additional case is a project deduction | Choose the right video output. | 3 recall criteria; 271 → 345 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed point identity is additional information across time |
| CV-VIDEO-002 | Sampling phase creates a measurable miss probability: retained explanation sufficient for this extension | Test the loss of short events. | 2 recall criteria; 280 → 280 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-VIDEO-003 | Future context imposes a latency floor: supported mechanism; additional case is a project deduction | check causation and delay. | 2 recall criteria; 282 → 358 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed future context imposes a latency floor |
| CV-VIDEO-004 | Order sensitivity should match the task labels: supported mechanism; additional case is a project deduction | check the use of the time order. | 2 recall criteria; 287 → 367 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed order sensitivity should match the task labels |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [CoTracker3](https://arxiv.org/html/2410.11831v1) — point-track/visibility outputs, online and offline protocols. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
