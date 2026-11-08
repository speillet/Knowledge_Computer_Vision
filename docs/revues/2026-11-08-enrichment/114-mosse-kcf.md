# Review — MOSSE and KCF — tracking with correlation filters — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 4 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CORRELATION-001 | A search crop defines the capture region: supported mechanism; additional case is a project deduction | Explain the loop of a tracking filter. | 3 recall criteria; 296 → 372 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a search crop defines the capture region |
| CV-CORRELATION-002 | Cyclic training creates artificial boundary examples: supported mechanism; additional case is a project deduction | distinguish MOSSE and KCF. | 3 recall criteria; 302 → 378 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed cyclic training creates artificial boundary examples |
| CV-CORRELATION-003 | PSR is invariant to some response rescalings: supported mechanism; additional case is a project deduction | interpret a PSR. | 2 recall criteria; 323 → 400 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed psr is invariant to some response rescalings |
| CV-CORRELATION-004 | A learned distractor can make confidence self-reinforcing: supported mechanism; additional case is a project deduction | Look for contamination of the model. | 3 recall criteria; 279 → 351 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a learned distractor can make confidence self-reinforcing |
| CV-CORRELATION-005 | Resets inject new localization information: retained explanation sufficient for this extension | Define an honest comparison of trackers. | 3 recall criteria; 285 → 285 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 4 → 5; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.


The initial MOSSE author-site URL returned HTTP 403; the draper-hosted primary copy was accessible and used.

## Sources

- [KCF](https://arxiv.org/html/1404.7584v1) — §IV circulant ridge regression and Appendix F MOSSE. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf) — §§3.2–3.5 filter adaptation and PSR. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
