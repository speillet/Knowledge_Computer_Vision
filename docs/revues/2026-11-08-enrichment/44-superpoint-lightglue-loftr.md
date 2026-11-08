# Review — SuperPoint, LightGlue and LoFTR — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 5 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCH-APPRIS-001 | Unmatched points are a necessary output: supported mechanism; additional case is a project deduction | Assign the role of components. | 2 recall criteria; 271 → 345 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed unmatched points are a necessary output |
| CV-MATCH-APPRIS-002 | Detector-free does not mean confidence-free: supported mechanism; additional case is a project deduction | Distinguish between detector-free and dense flow. | 2 recall criteria; 278 → 353 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed detector-free does not mean confidence-free |
| CV-MATCH-APPRIS-003 | Coordinate metadata is part of feature compatibility: supported mechanism; additional case is a project deduction | Keep the features compatible. | 2 recall criteria; 283 → 360 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed coordinate metadata is part of feature compatibility |
| CV-MATCH-APPRIS-004 | Adaptive computation needs latency distributions: supported mechanism; additional case is a project deduction | Build a comparable baseline. | 3 recall criteria; 286 → 360 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed adaptive computation needs latency distributions |
| CV-MATCH-APPRIS-005 | One landmark gives a preprocessing round trip: supported mechanism; additional case is a project deduction | check the coordinates of the matching. | 2 recall criteria; 294 → 366 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed one landmark gives a preprocessing round trip |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.


The LoFTR HTML endpoint returned 404; its arXiv PDF was accessible and used instead. No new checkpoint API or runtime result is asserted.

## Sources

- [LightGlue](https://arxiv.org/html/2306.13643v1) — §3 contextual matching, matchability, adaptive depth/width. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [SuperPoint](https://arxiv.org/html/1712.07629v4) — §3 joint detection/description and §5 homographic adaptation. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [LoFTR](https://arxiv.org/pdf/2104.00680) — §3 coarse-to-fine correspondence pipeline. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
