# Review — Factor graphs and incremental optimization — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 2 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FACTEURS-001 | Independent factors require independent evidence: supported foundation; new case is a project deduction | separating representation and solver. | 3 recall criteria; 318 → 396 lexical words | Canonical explanation aligned; ID and front preserved | Important | Restore landmarks in the factor-graph variable definition; Developed independent factors require independent evidence |
| CV-FACTEURS-002 | A disconnected graph needs more than one anchor: supported foundation; new case is a project deduction | Explain a gauge. | 2 recall criteria; 294 → 375 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a disconnected graph needs more than one anchor |
| CV-FACTEURS-003 | A loop can win its own residual test: supported foundation; new case is a project deduction | Check for a loop closure. | 3 recall criteria; 313 → 395 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a loop can win its own residual test |
| CV-FACTEURS-004 | Convergence speed is a measured tradeoff: supported foundation; new case is a project deduction | Choose a robust back-end to fake loops. | 3 recall criteria; 300 → 390 lexical words | Canonical explanation aligned; ID and front preserved | Important | Restrict the empirical DCS speed comparison to its measured setting; Developed convergence speed is a measured tradeoff |
| CV-FACTEURS-005 | A small update can still be globally expensive: supported foundation; new case is a project deduction | explain the incremental update of iSAM2. | 3 recall criteria; 308 → 387 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a small update can still be globally expensive |

## Reference findings and applied corrections

Canonical revision 9 → 10; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

- CV-FACTEURS-001: Restore landmarks in the factor-graph variable definition.
- CV-FACTEURS-004: Restrict the empirical DCS speed comparison to its measured setting.



## Sources

- [Kaess et al., iSAM2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf) — §2 Gaussian model and §§3–4 elimination, relinearization and partial updates. Consulted 2026-11-08.
- [Agarwal et al., DCS](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf) — §IV dynamic covariance scaling; experimental convergence is dataset-specific. Consulted 2026-11-08.

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
