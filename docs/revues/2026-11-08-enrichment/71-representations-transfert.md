# Review — Visual representations, ViT, Swin, ConvNeXt and DINOv2 — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-REPRESENTATIONS-001 | Quadratic attention is only one runtime term: supported foundation; new case is a project deduction | Estimate the cost of tokens. | 2 recall criteria; 266 → 345 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed quadratic attention is only one runtime term |
| CV-REPRESENTATIONS-002 | Local windows exchange information across layers: supported foundation; new case is a project deduction | Swin and ConvNeXt. | 2 recall criteria; 274 → 345 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed local windows exchange information across layers |
| CV-REPRESENTATIONS-003 | Upsampling cannot recreate missing defect evidence: supported foundation; new case is a project deduction | Use self-supervised features. | 2 recall criteria; 284 → 357 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed upsampling cannot recreate missing defect evidence |
| CV-REPRESENTATIONS-004 | Trainable-parameter count is not total training memory: supported foundation; new case is a project deduction | Choose an adaptation. | 3 recall criteria; 287 → 364 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed trainable-parameter count is not total training memory |
| CV-REPRESENTATIONS-005 | Compare tensors before comparing predictions: supported foundation; new case is a project deduction | check preprocessing a backbone. | 2 recall criteria; 267 → 343 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed compare tensors before comparing predictions |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [ViT](https://arxiv.org/html/2010.11929v2) — §3.1 image patches and token sequence. Consulted 2026-11-08.
- [Swin](https://arxiv.org/html/2103.14030v2) — §3.2 local windows and shifted connections. Consulted 2026-11-08.
- [DINOv2](https://arxiv.org/html/2304.07193v2) — §7 downstream dense evaluation and representation use. Consulted 2026-11-08.

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
