# Review — GrabCut, regions and appearance models — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-GRABCUT-001 | An exact subproblem does not give a global joint guarantee: supported foundation; new case is a project deduction | Explain the GrabCut alternation. | 2 recall criteria; 283 → 363 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed an exact subproblem does not give a global joint guarantee |
| CV-GRABCUT-002 | Iterations cannot override a forbidden label: supported foundation; new case is a project deduction | check is an initialization constraint. | 2 recall criteria; 286 → 362 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed iterations cannot override a forbidden label |
| CV-GRABCUT-003 | Human effort belongs in the comparison budget: supported foundation; new case is a project deduction | Choose an interaction. | 3 recall criteria; 288 → 365 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed human effort belongs in the comparison budget |

## Reference findings and applied corrections

Canonical revision 4 → 5; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [OpenCV GrabCut](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html) — appearance mixtures, iterative graph cut and definite/probable label semantics; checked with Context7. Consulted 2026-11-08.

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
