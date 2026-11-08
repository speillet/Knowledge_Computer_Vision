# Review — Visual representations, ViT, Swin, ConvNeXt and DINOv2 — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 5 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-REPRESENTATIONS-001 | Quadratic attention is only one runtime term: supported mechanism; additional case is a project deduction | Estimate the cost of tokens. | 2 recall criteria; 266 → 345 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed quadratic attention is only one runtime term |
| CV-REPRESENTATIONS-002 | Local windows exchange information across layers: supported mechanism; additional case is a project deduction | Swin and ConvNeXt. | 2 recall criteria; 274 → 345 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed local windows exchange information across layers |
| CV-REPRESENTATIONS-003 | Upsampling cannot recreate missing defect evidence: supported mechanism; additional case is a project deduction | Use self-supervised features. | 2 recall criteria; 284 → 357 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed upsampling cannot recreate missing defect evidence |
| CV-REPRESENTATIONS-004 | Trainable-parameter count is not total training memory: supported mechanism; additional case is a project deduction | Choose an adaptation. | 3 recall criteria; 287 → 364 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed trainable-parameter count is not total training memory |
| CV-REPRESENTATIONS-005 | Compare tensors before comparing predictions: supported mechanism; additional case is a project deduction | check preprocessing a backbone. | 2 recall criteria; 267 → 343 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed compare tensors before comparing predictions |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [ViT](https://arxiv.org/html/2010.11929v2) — §3.1 image patches and token sequence. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Swin](https://arxiv.org/html/2103.14030v2) — §3.2 local windows and shifted connections. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [DINOv2](https://arxiv.org/html/2304.07193v2) — §7 downstream dense evaluation and representation use. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
