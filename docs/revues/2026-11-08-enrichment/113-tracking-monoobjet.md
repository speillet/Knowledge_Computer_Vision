# Review — Single-object tracking: correlation, Siamese networks and MeanShift — 2026-11-08

## Overview

2 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 2 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SOT-001 | Independent target searches can collapse to one distractor: supported foundation; new case is a project deduction | distinguish SOT and MOT. | 2 recall criteria; 264 → 340 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed independent target searches can collapse to one distractor |
| CV-SOT-002 | Freezing adaptation preserves the model, not visibility: supported foundation; new case is a project deduction | understand a template drift. | 2 recall criteria; 280 → 357 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed freezing adaptation preserves the model, not visibility |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [SiamFC](https://arxiv.org/html/1606.09549v2) — §4 initialized target matching and tracking protocol. Consulted 2026-11-08.
- [KCF](https://arxiv.org/html/1404.7584v1) — tracking pipeline and online model interpolation. Consulted 2026-11-08.

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
