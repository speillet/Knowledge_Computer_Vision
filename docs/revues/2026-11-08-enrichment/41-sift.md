# Review — SIFT — local features and multiscale descriptors — 2026-11-08

## Overview

7 cards reviewed in `approfondir` mode: 7 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 1 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SIFT-001 | Match count does not establish spatial support: supported mechanism; additional case is a project deduction | Explain the components of a correspondence pipeline. | 3 recall criteria; 329 → 410 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed match count does not establish spatial support |
| CV-SIFT-002 | Scale sampling and octave boundaries: supported mechanism; additional case is a project deduction | Explain the search for a characteristic scale. | 2 recall criteria; 338 → 421 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed scale sampling and octave boundaries |
| CV-SIFT-003 | Orientation ambiguity can create multiple descriptors: supported mechanism; additional case is a project deduction | justify the construction of the descriptor. | 3 recall criteria; 310 → 383 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed orientation ambiguity can create multiple descriptors |
| CV-SIFT-004 | The second neighbor depends on the search population: supported mechanism; additional case is a project deduction | interpret the ratio test. | 2 recall criteria; 323 → 400 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the second neighbor depends on the search population |
| CV-SIFT-005 | Viewpoint normalization cannot recover occlusion: supported mechanism; additional case is a project deduction | Distinguish between the limits of invariances. | 2 recall criteria; 336 → 411 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed viewpoint normalization cannot recover occlusion |
| CV-SIFT-006 | A geometric consensus can support the wrong period: supported mechanism; additional case is a project deduction | Diagnose a misleading consensus. | 2 recall criteria; 312 → 387 lexical words | ID/front preserved; canonical wording aligned | Important | Restore the geometric meaning of inlier count; Developed a geometric consensus can support the wrong period |
| CV-SIFT-007 | Compare refusal as well as successful localization: supported mechanism; additional case is a project deduction | Build a comparison under constraint. | 3 recall criteria; 312 → 386 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed compare refusal as well as successful localization |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.

- CV-SIFT-006: Restore the geometric meaning of inlier count.



## Sources

- [Lowe 2004](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf) — §§3–7 scale-space, localization, orientation, descriptor and matching. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
