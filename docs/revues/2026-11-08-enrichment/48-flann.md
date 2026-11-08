# Review — FLANN — approximate nearest-neighbor search and distance conventions — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 1 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLANN-001 | Amortization has an explicit break-even point: supported foundation; new case is a project deduction | choose approximate or exhaustive search. | 2 recall criteria; 301 → 384 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed amortization has an explicit break-even point |
| CV-FLANN-002 | Metric compatibility survives no numeric cast: supported foundation; new case is a project deduction | preserve the metric of descriptors. | 2 recall criteria; 323 → 396 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed metric compatibility survives no numeric cast |
| CV-FLANN-003 | A rank-gap bound can certify a ratio decision: supported foundation; new case is a project deduction | Evaluate an approximation of neighbors. | 2 recall criteria; 310 → 398 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a rank-gap bound can certify a ratio decision |
| CV-FLANN-004 | Search effort should be selected on a frontier: supported foundation; new case is a project deduction | measure the recall time curve. | 3 recall criteria; 300 → 381 lexical words | Canonical explanation aligned; ID and front preserved | Important | Restore inliers as the final geometric matching measure; Developed search effort should be selected on a frontier |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

- CV-FLANN-004: Restore inliers as the final geometric matching measure.



## Sources

- [Muja and Lowe 2014](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf) — §§2–3 approximate search, search budget and data-dependent index selection. Consulted 2026-11-08.

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
