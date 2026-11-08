# Review — Least squares, SVD and conditioning — 2026-11-08

## Overview

9 cards reviewed in `approfondir` mode: 9 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 1 important, 0 minor, 8 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SVD-001 | A fit with arbitrarily unstable parameters: supported mechanism; additional case is a project deduction | distinguish residual and identifiability. | 2 recall criteria; 288 → 368 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a fit with arbitrarily unstable parameters |
| CV-SVD-002 | Choosing a solver by error budget: supported mechanism; additional case is a project deduction | choose QR or normal equations. | 3 recall criteria; 310 → 391 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed choosing a solver by error budget |
| CV-SVD-003 | Correlated measurements do not count twice: supported mechanism; additional case is a project deduction | weighting heterogeneous residuals. | 2 recall criteria; 317 → 400 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed correlated measurements do not count twice |
| CV-SVD-004 | A diagnostic requires competing explanations: supported mechanism; additional case is a project deduction | distinguish outliers and deficient rank. | 3 recall criteria; 327 → 405 lexical words | ID/front preserved; canonical wording aligned | Important | Qualify outlier residual signatures and stabilization; contamination can be coherent and filtering can worsen coverage; Developed a diagnostic requires competing explanations |
| CV-SVD-005 | An invertible homography can have a zero last coefficient: supported mechanism; additional case is a project deduction | Make a DLT estimate. | 3 recall criteria; 329 → 422 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed an invertible homography can have a zero last coefficient |
| CV-SVD-006 | Normalization is not geometric evidence: supported mechanism; additional case is a project deduction | linking standardization and conditioning of the DLT. | 3 recall criteria; 320 → 397 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed normalization is not geometric evidence |
| CV-SVD-007 | Accepted steps need model agreement: supported mechanism; additional case is a project deduction | Gauss-Newton and Levenberg-Marquardt. | 3 recall criteria; 295 → 375 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed accepted steps need model agreement |
| CV-SVD-008 | A robust scale changes influence, not the residual unit: supported mechanism; additional case is a project deduction | Adjust the scale of a robust loss. | 2 recall criteria; 288 → 371 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a robust scale changes influence, not the residual unit |
| CV-SVD-009 | More repeated data do not remove a gauge: supported mechanism; additional case is a project deduction | interpret an estimation covariance. | 3 recall criteria; 312 → 393 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed more repeated data do not remove a gauge |

## Reference findings and applied corrections

Canonical revision 8 → 9; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.

- CV-SVD-004: Qualify outlier residual signatures and stabilization; contamination can be coherent and filtering can worsen coverage.



## Sources

- [Ceres covariance](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) — Introduction, Gauge Invariance and Rank of the Jacobian; Context7 checked. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Ceres solving](https://ceres-solver.readthedocs.io/latest/nnls_solving.html) — Trust Region Methods and Linear Solvers. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Ceres modeling](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html) — LossFunction and scaling. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
