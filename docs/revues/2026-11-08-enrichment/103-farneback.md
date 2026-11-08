# Review — Farnebäck — dense optical flow through polynomial expansion — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 4 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FARNEBACK-001 | Constant terms provide a consistency check: supported mechanism; additional case is a project deduction | Explain the polynomial mechanism. | 3 recall criteria; 299 → 374 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed constant terms provide a consistency check |
| CV-FARNEBACK-002 | The equation is sensitive to coefficient scale and rank: supported mechanism; additional case is a project deduction | Solve an ideal local constraint. | 2 recall criteria; 302 → 380 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the equation is sensitive to coefficient scale and rank |
| CV-FARNEBACK-003 | Image array indices and vector components have different order: retained explanation sufficient for this extension | read the coordinate frame and the units of the stream. | 3 recall criteria; 299 → 299 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-FARNEBACK-004 | Composing flows requires transporting the lookup point: supported mechanism; additional case is a project deduction | interpret a round-trip inconsistency. | 2 recall criteria; 329 → 408 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed composing flows requires transporting the lookup point |
| CV-FARNEBACK-005 | Coarse scales can mix motions across a thin object: supported mechanism; additional case is a project deduction | Adjust the pyramid without masking the failures. | 2 recall criteria; 306 → 385 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed coarse scales can mix motions across a thin object |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.


The initial PDF extraction exposed the §2 quadratic model; a later detailed request timed out. This pass does not claim a fresh passage-level check of all §3 refinements. No flow implementation was executed.

## Sources

- [OpenCV dense flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) — Dense Optical Flow: polynomial neighborhood approximation; original Farnebäck equations are checked algebraically here. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Farnebäck 2003](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf) — §2 polynomial model visible in initial extraction; later detailed §3 request timed out; coefficient identities derived by the project. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
