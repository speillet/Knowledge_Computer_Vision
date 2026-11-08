# Review — Optical flow: Lucas–Kanade, Farnebäck and RAFT — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLOT-001 | Brightness constancy is a model assumption: supported foundation; new case is a project deduction | interpret the constraint of the flow. | 2 recall criteria; 275 → 345 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed brightness constancy is a model assumption |
| CV-FLOT-002 | The timestamp interval belongs to each pair: supported foundation; new case is a project deduction | respect the temporal unity. | 2 recall criteria; 280 → 360 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed the timestamp interval belongs to each pair |
| CV-FLOT-003 | A correlation maximum is not yet the flow field: supported foundation; new case is a project deduction | situer RAFT. | 2 recall criteria; 270 → 349 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a correlation maximum is not yet the flow field |
| CV-FLOT-004 | Consistency can fail or succeed for different reasons: supported foundation; new case is a project deduction | process a occlusion. | 2 recall criteria; 278 → 348 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed consistency can fail or succeed for different reasons |

## Reference findings and applied corrections

Canonical revision 4 → 5; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [OpenCV optical flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) — brightness constancy, Lucas–Kanade local system and pyramids. Consulted 2026-11-08.
- [RAFT](https://arxiv.org/html/2003.12039v3) — §3 all-pairs correlation, lookup and recurrent updates. Consulted 2026-11-08.

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
