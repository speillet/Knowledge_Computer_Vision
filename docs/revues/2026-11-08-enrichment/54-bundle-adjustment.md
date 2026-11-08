# Review — Bundle adjustment and the Schur complement — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 4 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BA-001 | Observation connectivity determines recoverable structure: supported mechanism; additional case is a project deduction | Identify the unknowns of a BA. | 3 recall criteria; 288 → 361 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed observation connectivity determines recoverable structure |
| CV-BA-002 | A shared landmark can create a camera clique: supported mechanism; additional case is a project deduction | Explain the elimination of Schur. | 2 recall criteria; 313 → 403 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a shared landmark can create a camera clique |
| CV-BA-003 | A baseline prior adds evidence only if it is measured: supported mechanism; additional case is a project deduction | Do not hide a gauge. | 2 recall criteria; 295 → 375 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a baseline prior adds evidence only if it is measured |
| CV-BA-004 | A flexible lens can absorb another model error: supported mechanism; additional case is a project deduction | check a model too free. | 2 recall criteria; 268 → 342 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a flexible lens can absorb another model error |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [Ceres Schur solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html#the-schur-complement-trick) — block normal equations, point elimination and camera coupling; Context7 solver sources consulted. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Ceres covariance](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) — gauge invariance and Jacobian rank. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
