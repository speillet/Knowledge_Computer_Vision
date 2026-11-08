# Review — Local detectors, descriptors and matchers — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 4 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCHING-001 | Local uncertainty follows the weakest direction: supported mechanism; additional case is a project deduction | interpret the structure matrix. | 2 recall criteria; 281 → 355 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed local uncertainty follows the weakest direction |
| CV-MATCHING-002 | Descriptor support can invalidate a detected point: supported mechanism; additional case is a project deduction | separate detector and descriptor. | 2 recall criteria; 276 → 350 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed descriptor support can invalidate a detected point |
| CV-MATCHING-003 | Approximation can change the robust solver budget: supported mechanism; additional case is a project deduction | Measure an approximate search. | 3 recall criteria; 287 → 361 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed approximation can change the robust solver budget |
| CV-MATCHING-004 | Model compatibility is weaker than unique identity: supported mechanism; additional case is a project deduction | choose a geometric check. | 2 recall criteria; 275 → 349 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed model compatibility is weaker than unique identity |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV Harris](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html) — local displacement quadratic and structure tensor. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [OpenCV matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html) — distance norms, mutual matching and two-neighbor matching; checked with Context7. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
