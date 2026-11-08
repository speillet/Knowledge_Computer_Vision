# Review — FAST and BRIEF — detecting corners and describing their neighborhoods — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FAST-BRIEF-001 | The segment must wrap around the circle: supported foundation; new case is a project deduction | Explain the FAST test. | 2 recall criteria; 313 → 388 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed the segment must wrap around the circle |
| CV-FAST-BRIEF-002 | Hamming distance is invariant to a shared bit permutation: supported foundation; new case is a project deduction | Calculate a binary distance. | 2 recall criteria; 293 → 362 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed hamming distance is invariant to a shared bit permutation |
| CV-FAST-BRIEF-003 | An oriented pattern has its own failure source: supported foundation; new case is a project deduction | separate FAST BRIEF and ORB. | 3 recall criteria; 294 → 369 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed an oriented pattern has its own failure source |
| CV-FAST-BRIEF-004 | Rotation near a boundary changes valid support: supported foundation; new case is a project deduction | Isolate a failure under rotation. | 2 recall criteria; 313 → 383 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed rotation near a boundary changes valid support |
| CV-FAST-BRIEF-005 | A faster front end can make geometry slower: supported foundation; new case is a project deduction | measure the compromis calculation repeatability. | 3 recall criteria; 296 → 371 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a faster front end can make geometry slower |

## Reference findings and applied corrections

Canonical revision 4 → 5; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [Rosten and Drummond](https://www.edwardrosten.com/work/rosten_2006_machine.pdf) — segment test, learned decision tree and repeatability evaluation. Consulted 2026-11-08.
- [Calonder et al., BRIEF](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf) — §3 smoothed intensity tests and Hamming matching. Consulted 2026-11-08.

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
