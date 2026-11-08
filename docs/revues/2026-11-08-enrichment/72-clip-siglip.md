# Review — CLIP, SigLIP and text-based recognition — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CLIP-001 | The vocabulary defines the available decision: supported foundation; new case is a project deduction | interpret the zero-shot CLIP. | 3 recall criteria; 285 → 361 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed the vocabulary defines the available decision |
| CV-CLIP-002 | Adding a candidate changes normalized confidence: supported foundation; new case is a project deduction | Reject a misleading probability. | 2 recall criteria; 295 → 367 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed adding a candidate changes normalized confidence |
| CV-CLIP-003 | Pairwise loss does not imply calibrated deployment probabilities: supported foundation; new case is a project deduction | distinguer objectifs contrastifs. | 2 recall criteria; 280 → 352 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed pairwise loss does not imply calibrated deployment probabilities |
| CV-CLIP-004 | Prompt selection is part of model selection: supported foundation; new case is a project deduction | test the sensitivity to the text. | 3 recall criteria; 287 → 363 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed prompt selection is part of model selection |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

SigLIP HTML returned 404; its primary arXiv PDF was used. No assertion of calibrated SigLIP probabilities is added.

## Sources

- [CLIP](https://arxiv.org/html/2103.00020v1) — §2.3 contrastive training and §3.1 zero-shot classification. Consulted 2026-11-08.
- [SigLIP](https://arxiv.org/pdf/2303.15343) — §3 pairwise sigmoid objective. Consulted 2026-11-08.

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
