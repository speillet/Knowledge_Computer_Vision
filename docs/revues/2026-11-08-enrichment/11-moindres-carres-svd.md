# Review — Least squares, SVD and conditioning — 2026-11-08

## Overview

9 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 1 important, 0 minor, 8 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SVD-001 | A fit with arbitrarily unstable parameters: supported foundation; new case is a project deduction | distinguish residual and identifiability. | 2 recall criteria; 288 → 368 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a fit with arbitrarily unstable parameters |
| CV-SVD-002 | Choosing a solver by error budget: supported foundation; new case is a project deduction | choose QR or normal equations. | 3 recall criteria; 310 → 391 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed choosing a solver by error budget |
| CV-SVD-003 | Correlated measurements do not count twice: supported foundation; new case is a project deduction | weighting heterogeneous residuals. | 2 recall criteria; 317 → 400 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed correlated measurements do not count twice |
| CV-SVD-004 | A diagnostic requires competing explanations: supported foundation; new case is a project deduction | distinguish outliers and deficient rank. | 3 recall criteria; 327 → 405 lexical words | Canonical explanation aligned; ID and front preserved | Important | Qualify outlier residual signatures and stabilization; contamination can be coherent and filtering can worsen coverage; Developed a diagnostic requires competing explanations |
| CV-SVD-005 | An invertible homography can have a zero last coefficient: supported foundation; new case is a project deduction | Make a DLT estimate. | 3 recall criteria; 329 → 422 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed an invertible homography can have a zero last coefficient |
| CV-SVD-006 | Normalization is not geometric evidence: supported foundation; new case is a project deduction | linking standardization and conditioning of the DLT. | 3 recall criteria; 320 → 397 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed normalization is not geometric evidence |
| CV-SVD-007 | Accepted steps need model agreement: supported foundation; new case is a project deduction | Gauss-Newton and Levenberg-Marquardt. | 3 recall criteria; 295 → 375 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed accepted steps need model agreement |
| CV-SVD-008 | A robust scale changes influence, not the residual unit: supported foundation; new case is a project deduction | Adjust the scale of a robust loss. | 2 recall criteria; 288 → 367 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a robust scale changes influence, not the residual unit |
| CV-SVD-009 | More repeated data do not remove a gauge: supported foundation; new case is a project deduction | interpret an estimation covariance. | 3 recall criteria; 312 → 393 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed more repeated data do not remove a gauge |

## Reference findings and applied corrections

Canonical revision 8 → 9; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

- CV-SVD-004: Qualify outlier residual signatures and stabilization; contamination can be coherent and filtering can worsen coverage.



## Sources

- [Ceres covariance](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) — Introduction, Gauge Invariance and Rank of the Jacobian; Context7 checked. Consulted 2026-11-08.
- [Ceres solving](https://ceres-solver.readthedocs.io/latest/nnls_solving.html) — Trust Region Methods and Linear Solvers. Consulted 2026-11-08.
- [Ceres modeling](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html) — LossFunction and scaling. Consulted 2026-11-08.

## Proposals

No new ID is created in this pass. See the [proposal register](../propositions.md)
and [overview](00-bilan.md) for pending complementary cards and decisions.

## Checks and limitations

Scope-wide executed checks and identity/field comparisons are recorded in the
[overview](00-bilan.md). The source assessment concerns the mechanisms and
boundary cases identified above; it is not a fresh passage-by-passage
certification of every retained historical paragraph or implementation claim.
No CV experiment, hardware benchmark, independent review, learner mastery or
AnkiDroid rendering is established. Export status: to republish with `paquet-anki`.
