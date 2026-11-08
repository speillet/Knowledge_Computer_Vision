# Review — Data splits, annotations, score calibration and drift — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FIABILITE-001 | Derived samples inherit their source group: supported foundation; new case is a project deduction | Choose a split unit. | 2 recall criteria; 277 → 350 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed derived samples inherit their source group |
| CV-FIABILITE-002 | Calibration needs a defined correctness event: supported foundation; new case is a project deduction | distinguish between two calibrations. | 2 recall criteria; 271 → 344 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed calibration needs a defined correctness event |
| CV-FIABILITE-003 | An untouched test is consumed by repeated selection: supported foundation; new case is a project deduction | Keep a non-adaptive test. | 2 recall criteria; 307 → 384 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed an untouched test is consumed by repeated selection |
| CV-FIABILITE-004 | Season and sensor can be confounded: supported foundation; new case is a project deduction | Diagnose a seasonal drift. | 3 recall criteria; 308 → 381 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed season and sensor can be confounded |
| CV-FIABILITE-005 | Selective prediction needs both risk and coverage: supported foundation; new case is a project deduction | Avoiding certainty outside the field. | 2 recall criteria; 278 → 349 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed selective prediction needs both risk and coverage |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [Guo et al. calibration](https://proceedings.mlr.press/v70/guo17a.html) — §2 confidence/calibration and reliability diagrams. Consulted 2026-11-08.
- [Cawley and Talbot](https://www.jmlr.org/papers/v11/cawley10a.html) — model-selection overfitting and evaluation bias. Consulted 2026-11-08.

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
