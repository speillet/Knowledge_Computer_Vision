# Review — SLAM, VIO, IMU preintegration and loop closure — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VIO-001 | Bias correction has a local validity range: supported foundation; new case is a project deduction | situate the preintegration. | 2 recall criteria; 284 → 350 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed bias correction has a local validity range |
| CV-VIO-002 | A corrected map can move discontinuously: supported foundation; new case is a project deduction | distinguish odometry and loop. | 2 recall criteria; 294 → 372 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a corrected map can move discontinuously |
| CV-VIO-003 | Alignment can hide the error being diagnosed: supported foundation; new case is a project deduction | Identify the VIO gauges. | 2 recall criteria; 299 → 373 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed alignment can hide the error being diagnosed |
| CV-VIO-004 | A recent timestamp is part of pose quality: supported foundation; new case is a project deduction | design a VIO for augmented reality. | 3 recall criteria; 299 → 376 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a recent timestamp is part of pose quality |
| CV-VIO-005 | Weak texture and weak excitation can coincide: supported foundation; new case is a project deduction | Diagnose a drift in the corridor. | 3 recall criteria; 296 → 369 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed weak texture and weak excitation can coincide |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [Forster et al. preintegration](https://dellaert.github.io/files/Forster16tro.pdf) — §§IV–VI relative inertial factors, bias correction and estimation. Consulted 2026-11-08.
- [Qin et al. VINS-Mono](https://arxiv.org/html/1708.03852v1) — §V-B initialization, §VI estimation and §VIII pose graph. Consulted 2026-11-08.

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
