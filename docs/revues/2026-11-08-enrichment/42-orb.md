# Review — ORB — detection and oriented binary descriptors — 2026-11-08

## Overview

6 cards reviewed in `approfondir` mode: 4 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ORB-001 | Orientation quality can limit binary matching: supported mechanism; additional case is a project deduction | rebuild the ORB mechanism. | 3 recall criteria; 306 → 382 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed orientation quality can limit binary matching |
| CV-ORB-002 | A byte example exposes the wrong metric: supported mechanism; additional case is a project deduction | Linking representation and distance. | 2 recall criteria; 314 → 388 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a byte example exposes the wrong metric |
| CV-ORB-003 | One symbol mismatch can contain two flipped bits: retained explanation sufficient for this extension | select the norm after changing the variant. | 2 recall criteria; 306 → 306 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-ORB-004 | Tie handling belongs to the acceptance rule: supported mechanism; additional case is a project deduction | distinguish between two matching filters. | 3 recall criteria; 314 → 393 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed tie handling belongs to the acceptance rule |
| CV-ORB-005 | A finer pyramid cannot undo the input sampling: retained explanation sufficient for this extension | Diagnose a loss of repeatability. | 3 recall criteria; 325 → 325 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-ORB-006 | A memory estimate needs database lifetime: supported mechanism; additional case is a project deduction | articulating computational constraint and task success. | 3 recall criteria; 302 → 380 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a memory estimate needs database lifetime |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.


The original Willow Garage ORB PDF was inaccessible. The algorithm and norm contract were checked using the official OpenCV 4.13 documentation; historical paper-specific empirical claims are not re-certified.

## Sources

- [OpenCV ORB](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html) — oriented intensity-centroid descriptor and WTA_K norm contract; checked with Context7. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
