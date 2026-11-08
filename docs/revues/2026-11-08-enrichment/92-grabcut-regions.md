# Review — GrabCut, regions and appearance models — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode: 0 enriched and 3
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-GRABCUT-001 | An exact subproblem does not give a global joint guarantee: retained explanation sufficient for this extension | Explain the GrabCut alternation. | 2 recall criteria; 283 → 283 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-GRABCUT-002 | Iterations cannot override a forbidden label: retained explanation sufficient for this extension | check is an initialization constraint. | 2 recall criteria; 286 → 286 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-GRABCUT-003 | Human effort belongs in the comparison budget: retained explanation sufficient for this extension | Choose an interaction. | 3 recall criteria; 288 → 288 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 4 retained; the original reference and cards
already contain the mechanisms proposed in the draft. No redundant expansion is retained.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV GrabCut](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html) — appearance mixtures, iterative graph cut and definite/probable label semantics; checked with Context7. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
