# Review — Optical flow: Lucas–Kanade, Farnebäck and RAFT — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 3 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLOT-001 | Brightness constancy is a model assumption: supported mechanism; additional case is a project deduction | interpret the constraint of the flow. | 2 recall criteria; 275 → 345 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed brightness constancy is a model assumption |
| CV-FLOT-002 | The timestamp interval belongs to each pair: supported mechanism; additional case is a project deduction | respect the temporal unity. | 2 recall criteria; 280 → 360 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the timestamp interval belongs to each pair |
| CV-FLOT-003 | A correlation maximum is not yet the flow field: supported mechanism; additional case is a project deduction | situer RAFT. | 2 recall criteria; 270 → 349 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a correlation maximum is not yet the flow field |
| CV-FLOT-004 | Consistency can fail or succeed for different reasons: retained explanation sufficient for this extension | process a occlusion. | 2 recall criteria; 278 → 278 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 4 → 5; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV optical flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) — brightness constancy, Lucas–Kanade local system and pyramids. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [RAFT](https://arxiv.org/html/2003.12039v3) — §3 all-pairs correlation, lookup and recurrent updates. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
