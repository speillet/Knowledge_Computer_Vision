# Review — VLMs, grounding and the vision–action boundary — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 3 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VLM-001 | An action interface needs a state and timing contract: supported mechanism; additional case is a project deduction | locate encoder VLM and VLA. | 3 recall criteria; 280 → 359 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed an action interface needs a state and timing contract |
| CV-VLM-002 | Learned queries are a representation bottleneck: retained explanation sufficient for this extension | Locate a visual connector. | 2 recall criteria; 291 → 291 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-VLM-003 | Retrieval needs both event coverage and verification: supported mechanism; additional case is a project deduction | Create a video index. | 3 recall criteria; 316 → 389 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed retrieval needs both event coverage and verification |
| CV-VLM-004 | A counterfactual image pair can test visual dependence: supported mechanism; additional case is a project deduction | Distinct hallucination and insufficient observation. | 3 recall criteria; 304 → 377 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a counterfactual image pair can test visual dependence |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [BLIP-2](https://arxiv.org/html/2301.12597v2) — §3 Q-Former learned queries and frozen encoder/language-model bridge. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [LLaVA](https://arxiv.org/html/2304.08485v2) — §4 visual instruction tuning and limitations. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
