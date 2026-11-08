# Review — Exposure, noise, color and sampling — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 4 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-001 | Exposure chosen from a blur budget: supported mechanism; additional case is a project deduction | Calculate a simplified blur. | 2 recall criteria; 299 → 378 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed exposure chosen from a blur budget |
| CV-ACQUISITION-002 | Read noise changes the value of additional light: supported mechanism; additional case is a project deduction | Distinguish between gain and exposure. | 3 recall criteria; 406 → 490 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed read noise changes the value of additional light |
| CV-ACQUISITION-003 | Aliasing can survive apparently smooth output: supported mechanism; additional case is a project deduction | recognize aliasing and inconsistent preprocessing. | 2 recall criteria; 346 → 423 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed aliasing can survive apparently smooth output |
| CV-ACQUISITION-004 | An interface check needs a known stimulus: supported mechanism; additional case is a project deduction | check an image entry. | 2 recall criteria; 285 → 368 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed an interface check needs a known stimulus |

## Reference findings and applied corrections

Canonical revision 9 → 10; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [EMVA 1288 Linear 4.0](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) — §§2.4–2.7 noise, SNR and saturation. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Parmar et al., aliased resizing](https://arxiv.org/abs/2104.11222) — §§2–3 sampling and resize implementation dependence. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
