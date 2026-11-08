# Review — SLAM, VIO, IMU preintegration and loop closure — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 3 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VIO-001 | Bias correction has a local validity range: supported mechanism; additional case is a project deduction | situate the preintegration. | 2 recall criteria; 284 → 350 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed bias correction has a local validity range |
| CV-VIO-002 | A corrected map can move discontinuously: supported mechanism; additional case is a project deduction | distinguish odometry and loop. | 2 recall criteria; 294 → 372 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a corrected map can move discontinuously |
| CV-VIO-003 | Alignment can hide the error being diagnosed: retained explanation sufficient for this extension | Identify the VIO gauges. | 2 recall criteria; 299 → 299 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-VIO-004 | A recent timestamp is part of pose quality: retained explanation sufficient for this extension | design a VIO for augmented reality. | 3 recall criteria; 299 → 299 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-VIO-005 | Weak texture and weak excitation can coincide: supported mechanism; additional case is a project deduction | Diagnose a drift in the corridor. | 3 recall criteria; 296 → 369 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed weak texture and weak excitation can coincide |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [Forster et al. preintegration](https://dellaert.github.io/files/Forster16tro.pdf) — §§IV–VI relative inertial factors, bias correction and estimation. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Qin et al. VINS-Mono](https://arxiv.org/html/1708.03852v1) — §V-B initialization, §VI estimation and §VIII pose graph. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
