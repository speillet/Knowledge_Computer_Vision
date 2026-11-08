# Review — Filters, gradients and pyramids — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 4 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FILTRES-001 | Robustness to impulses has a geometric price: supported mechanism; additional case is a project deduction | Choose a filter based on the noise. | 2 recall criteria; 305 → 384 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed robustness to impulses has a geometric price |
| CV-FILTRES-002 | Only affine intensity scaling preserves this ratio: supported mechanism; additional case is a project deduction | settle a bilateral in the right units. | 2 recall criteria; 311 → 385 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed only affine intensity scaling preserves this ratio |
| CV-FILTRES-003 | A task metric needs the same operating point: supported mechanism; additional case is a project deduction | Protect a business detail. | 2 recall criteria; 289 → 363 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a task metric needs the same operating point |
| CV-FILTRES-004 | A coarse-level displacement changes its unit: supported mechanism; additional case is a project deduction | Explain a pyramid. | 2 recall criteria; 288 → 369 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a coarse-level displacement changes its unit |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV smoothing](https://docs.opencv.org/4.13.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html) — median/Gaussian/bilateral definitions; checked with Context7. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Tomasi and Manduchi](https://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf) — §§2–3 spatial and range weighting. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
