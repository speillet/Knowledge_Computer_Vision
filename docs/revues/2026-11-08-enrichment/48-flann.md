# Review — FLANN — approximate nearest-neighbor search and distance conventions — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 4 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 1 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLANN-001 | Amortization has an explicit break-even point: supported mechanism; additional case is a project deduction | choose approximate or exhaustive search. | 2 recall criteria; 301 → 384 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed amortization has an explicit break-even point |
| CV-FLANN-002 | Metric compatibility survives no numeric cast: supported mechanism; additional case is a project deduction | preserve the metric of descriptors. | 2 recall criteria; 323 → 396 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed metric compatibility survives no numeric cast |
| CV-FLANN-003 | A rank-gap bound can certify a ratio decision: supported mechanism; additional case is a project deduction | Evaluate an approximation of neighbors. | 2 recall criteria; 310 → 398 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a rank-gap bound can certify a ratio decision |
| CV-FLANN-004 | Search effort should be selected on a frontier: supported mechanism; additional case is a project deduction | measure the recall time curve. | 3 recall criteria; 300 → 381 lexical words | ID/front preserved; canonical wording aligned | Important | Restore inliers as the final geometric matching measure; Developed search effort should be selected on a frontier |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.

- CV-FLANN-004: Restore inliers as the final geometric matching measure.



## Sources

- [Muja and Lowe 2014](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf) — §§2–3 approximate search, search budget and data-dependent index selection. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
