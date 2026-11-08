# Review — VLMs, grounding and the vision–action boundary — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VLM-001 | An action interface needs a state and timing contract: supported foundation; new case is a project deduction | locate encoder VLM and VLA. | 3 recall criteria; 280 → 359 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed an action interface needs a state and timing contract |
| CV-VLM-002 | Learned queries are a representation bottleneck: supported foundation; new case is a project deduction | Locate a visual connector. | 2 recall criteria; 291 → 368 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed learned queries are a representation bottleneck |
| CV-VLM-003 | Retrieval needs both event coverage and verification: supported foundation; new case is a project deduction | Create a video index. | 3 recall criteria; 316 → 389 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed retrieval needs both event coverage and verification |
| CV-VLM-004 | A counterfactual image pair can test visual dependence: supported foundation; new case is a project deduction | Distinct hallucination and insufficient observation. | 3 recall criteria; 304 → 377 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a counterfactual image pair can test visual dependence |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [BLIP-2](https://arxiv.org/html/2301.12597v2) — §3 Q-Former learned queries and frozen encoder/language-model bridge. Consulted 2026-11-08.
- [LLaVA](https://arxiv.org/html/2304.08485v2) — §4 visual instruction tuning and limitations. Consulted 2026-11-08.

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
