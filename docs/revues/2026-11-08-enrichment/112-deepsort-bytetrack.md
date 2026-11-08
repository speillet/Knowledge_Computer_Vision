# Review — DeepSORT, ByteTrack and multi-object association — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 4 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ASSOCIATION-001 | An older covariance can make motion distance smaller: supported mechanism; additional case is a project deduction | Identify the addition of DeepSORT. | 3 recall criteria; 274 → 346 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed an older covariance can make motion distance smaller |
| CV-ASSOCIATION-002 | Birth and continuation use different evidence: supported mechanism; additional case is a project deduction | understand the use of low scores ByteTrack. | 2 recall criteria; 298 → 377 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed birth and continuation use different evidence |
| CV-ASSOCIATION-003 | Some identities are visually unobservable: supported mechanism; additional case is a project deduction | check the transfer ReID. | 2 recall criteria; 267 → 343 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed some identities are visually unobservable |
| CV-ASSOCIATION-004 | Association changes can interact with score calibration: supported mechanism; additional case is a project deduction | separate detector and association. | 3 recall criteria; 275 → 347 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed association changes can interact with score calibration |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [DeepSORT](https://arxiv.org/html/1703.07402v1) — §§2.2–2.4 motion/appearance gates, cascade and descriptor. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [ByteTrack](https://arxiv.org/html/2110.06864v3) — §3 two-stage association and new-track creation. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
