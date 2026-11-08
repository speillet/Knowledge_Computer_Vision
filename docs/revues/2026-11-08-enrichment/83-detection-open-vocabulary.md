# Review — Open-vocabulary detection and grounding — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OPENVOC-001 | Region grounding needs a localization evaluation: supported foundation; new case is a project deduction | separate the multimodal outputs. | 2 recall criteria; 299 → 371 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed region grounding needs a localization evaluation |
| CV-OPENVOC-002 | Vocabulary updates need backward-compatibility evidence: supported foundation; new case is a project deduction | choose a system with a scalable catalog. | 3 recall criteria; 308 → 383 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed vocabulary updates need backward-compatibility evidence |
| CV-OPENVOC-003 | A broad phrase can be semantically correct but operationally wrong: supported foundation; new case is a project deduction | Check the specificity of the text. | 2 recall criteria; 278 → 353 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a broad phrase can be semantically correct but operationally wrong |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [OWL-ViT](https://arxiv.org/html/2205.06230v2) — §3 localized image-text matching. Consulted 2026-11-08.
- [Grounding DINO](https://arxiv.org/html/2303.05499v4) — §§3.2–3.3 language-guided queries and cross-modal decoding. Consulted 2026-11-08.

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
