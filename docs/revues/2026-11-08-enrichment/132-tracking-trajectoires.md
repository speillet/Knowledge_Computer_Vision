# Review — Evaluating identities, trajectories and 3D localization — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-TEMPS-001 | Track IDs must be evaluated over time: supported foundation; new case is a project deduction | Separate detection and identity. | 2 recall criteria; 268 → 343 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed track ids must be evaluated over time |
| CV-METRIQUES-TEMPS-002 | A counterexample exposes averaging order: supported foundation; new case is a project deduction | Comply with the HOTA aggregation. | 2 recall criteria; 279 → 357 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a counterexample exposes averaging order |
| CV-METRIQUES-TEMPS-003 | A scale-two trajectory can vanish under similarity alignment: supported foundation; new case is a project deduction | choose a trajectory alignment. | 2 recall criteria; 285 → 359 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a scale-two trajectory can vanish under similarity alignment |
| CV-METRIQUES-TEMPS-004 | Relative error depends on the interval: supported foundation; new case is a project deduction | distinguish ATE and RPE. | 2 recall criteria; 253 → 327 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed relative error depends on the interval |
| CV-METRIQUES-TEMPS-005 | Missing poses should not disappear from the denominator: supported foundation; new case is a project deduction | Comparing temporal evaluators. | 3 recall criteria; 269 → 344 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed missing poses should not disappear from the denominator |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [HOTA](https://arxiv.org/html/2009.07736v2) — §5 DetA/AssA and threshold aggregation. Consulted 2026-11-08.
- [Sturm et al. trajectory evaluation](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf) — §VII-A/B RPE and ATE definitions. Consulted 2026-11-08.

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
