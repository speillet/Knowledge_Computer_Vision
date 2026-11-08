# Review — SAM, SAM 2 and prompted video segmentation — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SAM-001 | A correct mask can still be the wrong requested object: supported foundation; new case is a project deduction | Set the output to SAM. | 2 recall criteria; 292 → 371 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a correct mask can still be the wrong requested object |
| CV-SAM-002 | History is part of the state being evaluated: supported foundation; new case is a project deduction | Find SAM 2 on video. | 2 recall criteria; 274 → 349 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed history is part of the state being evaluated |
| CV-SAM-003 | Causal inputs can still have delayed outputs: supported foundation; new case is a project deduction | check the future in evaluation. | 2 recall criteria; 272 → 357 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed causal inputs can still have delayed outputs |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [SAM](https://arxiv.org/html/2304.02643v1) — §§2–3 promptable masks, ambiguity and mask-quality prediction. Consulted 2026-11-08.
- [SAM 2](https://arxiv.org/html/2408.00714v2) — §§3–4 promptable video segmentation and memory. Consulted 2026-11-08.

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
