# Review — Bundle adjustment and the Schur complement — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BA-001 | Observation connectivity determines recoverable structure: supported foundation; new case is a project deduction | Identify the unknowns of a BA. | 3 recall criteria; 288 → 361 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed observation connectivity determines recoverable structure |
| CV-BA-002 | Elimination creates camera-to-camera coupling: supported foundation; new case is a project deduction | Explain the elimination of Schur. | 2 recall criteria; 313 → 389 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed elimination creates camera-to-camera coupling |
| CV-BA-003 | A baseline prior adds evidence only if it is measured: supported foundation; new case is a project deduction | Do not hide a gauge. | 2 recall criteria; 295 → 375 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a baseline prior adds evidence only if it is measured |
| CV-BA-004 | A flexible lens can absorb another model error: supported foundation; new case is a project deduction | check a model too free. | 2 recall criteria; 268 → 342 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a flexible lens can absorb another model error |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [Ceres Schur solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html#the-schur-complement-trick) — block normal equations, point elimination and camera coupling; Context7 solver sources consulted. Consulted 2026-11-08.
- [Ceres covariance](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) — gauge invariance and Jacobian rank. Consulted 2026-11-08.

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
