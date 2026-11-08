# Review — SAM, SAM 2 and prompted video segmentation — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode: 1 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SAM-001 | A correct mask can still be the wrong requested object: retained explanation sufficient for this extension | Set the output to SAM. | 2 recall criteria; 292 → 292 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-SAM-002 | History is part of the state being evaluated: retained explanation sufficient for this extension | Find SAM 2 on video. | 2 recall criteria; 274 → 274 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-SAM-003 | Causal inputs can still have delayed outputs: supported mechanism; additional case is a project deduction | check the future in evaluation. | 2 recall criteria; 272 → 357 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed causal inputs can still have delayed outputs |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [SAM](https://arxiv.org/html/2304.02643v1) — §§2–3 promptable masks, ambiguity and mask-quality prediction. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [SAM 2](https://arxiv.org/html/2408.00714v2) — §§3–4 promptable video segmentation and memory. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
