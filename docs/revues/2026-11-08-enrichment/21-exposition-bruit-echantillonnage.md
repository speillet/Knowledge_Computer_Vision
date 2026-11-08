# Review — Exposure, noise, color and sampling — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-001 | Exposure chosen from a blur budget: supported foundation; new case is a project deduction | Calculate a simplified blur. | 2 recall criteria; 299 → 378 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed exposure chosen from a blur budget |
| CV-ACQUISITION-002 | Read noise changes the value of additional light: supported foundation; new case is a project deduction | Distinguish between gain and exposure. | 3 recall criteria; 406 → 486 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed read noise changes the value of additional light |
| CV-ACQUISITION-003 | Aliasing can survive apparently smooth output: supported foundation; new case is a project deduction | recognize aliasing and inconsistent preprocessing. | 2 recall criteria; 346 → 423 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed aliasing can survive apparently smooth output |
| CV-ACQUISITION-004 | An interface check needs a known stimulus: supported foundation; new case is a project deduction | check an image entry. | 2 recall criteria; 285 → 368 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed an interface check needs a known stimulus |

## Reference findings and applied corrections

Canonical revision 9 → 10; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [EMVA 1288 Linear 4.0](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) — §§2.4–2.7 noise, SNR and saturation. Consulted 2026-11-08.
- [Parmar et al., aliased resizing](https://arxiv.org/abs/2104.11222) — §§2–3 sampling and resize implementation dependence. Consulted 2026-11-08.

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
