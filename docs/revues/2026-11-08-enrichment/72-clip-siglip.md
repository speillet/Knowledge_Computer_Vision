# Review — CLIP, SigLIP and text-based recognition — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 4 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CLIP-001 | The vocabulary defines the available decision: supported mechanism; additional case is a project deduction | interpret the zero-shot CLIP. | 3 recall criteria; 285 → 361 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the vocabulary defines the available decision |
| CV-CLIP-002 | Adding a candidate changes normalized confidence: supported mechanism; additional case is a project deduction | Reject a misleading probability. | 2 recall criteria; 295 → 367 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed adding a candidate changes normalized confidence |
| CV-CLIP-003 | Pairwise loss does not imply calibrated deployment probabilities: supported mechanism; additional case is a project deduction | distinguer objectifs contrastifs. | 2 recall criteria; 280 → 352 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed pairwise loss does not imply calibrated deployment probabilities |
| CV-CLIP-004 | Prompt selection is part of model selection: supported mechanism; additional case is a project deduction | test the sensitivity to the text. | 3 recall criteria; 287 → 363 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed prompt selection is part of model selection |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.


SigLIP HTML returned 404; its primary arXiv PDF was used. No assertion of calibrated SigLIP probabilities is added.

## Sources

- [CLIP](https://arxiv.org/html/2103.00020v1) — §2.3 contrastive training and §3.1 zero-shot classification. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [SigLIP](https://arxiv.org/pdf/2303.15343) — §3 pairwise sigmoid objective. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
