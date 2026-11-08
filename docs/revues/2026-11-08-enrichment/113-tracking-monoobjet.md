# Review — Single-object tracking: correlation, Siamese networks and MeanShift — 2026-11-08

## Overview

2 cards reviewed in `approfondir` mode: 0 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 2 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SOT-001 | Independent target searches can collapse to one distractor: retained explanation sufficient for this extension | distinguish SOT and MOT. | 2 recall criteria; 264 → 264 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-SOT-002 | Freezing adaptation preserves the model, not visibility: retained explanation sufficient for this extension | understand a template drift. | 2 recall criteria; 280 → 280 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 5 retained; the original reference and cards
already contain the mechanisms proposed in the draft. No redundant expansion is retained.
The review does not establish exhaustive subject coverage.




## Sources

- [SiamFC](https://arxiv.org/html/1606.09549v2) — §4 initialized target matching and tracking protocol. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [KCF](https://arxiv.org/html/1404.7584v1) — tracking pipeline and online model interpolation. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
