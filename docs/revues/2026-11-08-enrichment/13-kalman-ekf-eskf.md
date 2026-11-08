# Review — Kalman, EKF, UKF and ESKF for sensor fusion — 2026-11-08

## Overview

6 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FUSION-001 | Curvature can change the propagated mean: supported foundation; new case is a project deduction | distinguish filter variants. | 3 recall criteria; 290 → 377 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed curvature can change the propagated mean |
| CV-FUSION-002 | Whitened innovation direction matters: supported foundation; new case is a project deduction | interpret a standardized innovation. | 3 recall criteria; 324 → 397 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed whitened innovation direction matters |
| CV-FUSION-003 | A zero correction gives a reset identity test: supported foundation; new case is a project deduction | preserve the covariance ESKF. | 2 recall criteria; 322 → 403 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a zero correction gives a reset identity test |
| CV-FUSION-004 | Latency can dominate the nominal observation rate: supported foundation; new case is a project deduction | Processing time and missing data. | 3 recall criteria; 330 → 413 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed latency can dominate the nominal observation rate |
| CV-FUSION-005 | Small errors are a maintained condition: supported foundation; new case is a project deduction | justify the formulation at the state of error. | 3 recall criteria; 351 → 425 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed small errors are a maintained condition |
| CV-FUSION-006 | Symmetry repair is not positivity repair: supported foundation; new case is a project deduction | stabilizing the covariance update. | 3 recall criteria; 329 → 404 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed symmetry repair is not positivity repair |

## Reference findings and applied corrections

Canonical revision 8 → 9; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [Solà, quaternion kinematics](https://arxiv.org/html/1711.02508v1) — §5 error-state formulation, §6.3 reset, Appendix E noise integration. Consulted 2026-11-08.

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
