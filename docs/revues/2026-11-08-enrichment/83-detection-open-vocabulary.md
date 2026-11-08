# Review — Open-vocabulary detection and grounding — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode: 3 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OPENVOC-001 | Region grounding needs a localization evaluation: supported mechanism; additional case is a project deduction | separate the multimodal outputs. | 2 recall criteria; 299 → 371 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed region grounding needs a localization evaluation |
| CV-OPENVOC-002 | Vocabulary updates need backward-compatibility evidence: supported mechanism; additional case is a project deduction | choose a system with a scalable catalog. | 3 recall criteria; 308 → 383 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed vocabulary updates need backward-compatibility evidence |
| CV-OPENVOC-003 | A broad phrase can be semantically correct but operationally wrong: supported mechanism; additional case is a project deduction | Check the specificity of the text. | 2 recall criteria; 278 → 353 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a broad phrase can be semantically correct but operationally wrong |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OWL-ViT](https://arxiv.org/html/2205.06230v2) — §3 localized image-text matching. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Grounding DINO](https://arxiv.org/html/2303.05499v4) — §§3.2–3.3 language-guided queries and cross-modal decoding. Accessed or attempted 2026-11-08, with failures qualified explicitly.

## Proposals

No new ID is created. See the [proposal register](../propositions.md) and
[overview](00-bilan.md) for the four existing pending decisions.

## Checks and limitations

Scope-wide checks and protected-field comparisons appear in the [overview](00-bilan.md).
The evidence concerns the named mechanisms and corrections, not every retained
historical sentence or implementation claim. [Pre-merge review](65-pre-merge-review.md)
removed redundant draft additions and corrected two new wording inaccuracies.
This is agent self-review, without independent scientific validation, learner
mastery, a new CV experiment or AnkiDroid rendering. Export status:
**to republish with `paquet-anki`**.
