# Review — Kalman, EKF, UKF and ESKF for sensor fusion — 2026-11-08

## Overview

6 cards reviewed in `approfondir` mode: 6 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FUSION-001 | Curvature can change the propagated mean: supported mechanism; additional case is a project deduction | distinguish filter variants. | 3 recall criteria; 290 → 377 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed curvature can change the propagated mean |
| CV-FUSION-002 | Whitened innovation direction matters: supported mechanism; additional case is a project deduction | interpret a standardized innovation. | 3 recall criteria; 324 → 397 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed whitened innovation direction matters |
| CV-FUSION-003 | A zero correction gives a reset identity test: supported mechanism; additional case is a project deduction | preserve the covariance ESKF. | 2 recall criteria; 322 → 403 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a zero correction gives a reset identity test |
| CV-FUSION-004 | Latency can dominate the nominal observation rate: supported mechanism; additional case is a project deduction | Processing time and missing data. | 3 recall criteria; 330 → 413 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed latency can dominate the nominal observation rate |
| CV-FUSION-005 | Small errors are a maintained condition: supported mechanism; additional case is a project deduction | justify the formulation at the state of error. | 3 recall criteria; 351 → 425 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed small errors are a maintained condition |
| CV-FUSION-006 | Symmetry repair is not positivity repair: supported mechanism; additional case is a project deduction | stabilizing the covariance update. | 3 recall criteria; 329 → 404 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed symmetry repair is not positivity repair |

## Reference findings and applied corrections

Canonical revision 8 → 9; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [Solà, quaternion kinematics](https://arxiv.org/html/1711.02508v1) — §5 error-state formulation, §6.3 reset, Appendix E noise integration. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
