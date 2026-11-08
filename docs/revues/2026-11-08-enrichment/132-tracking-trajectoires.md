# Review — Evaluating identities, trajectories and 3D localization — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 3 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-TEMPS-001 | Track IDs must be evaluated over time: retained explanation sufficient for this extension | Separate detection and identity. | 2 recall criteria; 268 → 268 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-METRIQUES-TEMPS-002 | The aggregation gap has an angle interpretation: supported mechanism; additional case is a project deduction | Comply with the HOTA aggregation. | 2 recall criteria; 279 → 364 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the aggregation gap has an angle interpretation |
| CV-METRIQUES-TEMPS-003 | A scale-two trajectory can vanish under similarity alignment: retained explanation sufficient for this extension | choose a trajectory alignment. | 2 recall criteria; 285 → 285 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-METRIQUES-TEMPS-004 | Relative error depends on the interval: supported mechanism; additional case is a project deduction | distinguish ATE and RPE. | 2 recall criteria; 253 → 327 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed relative error depends on the interval |
| CV-METRIQUES-TEMPS-005 | Missing poses should not disappear from the denominator: supported mechanism; additional case is a project deduction | Comparing temporal evaluators. | 3 recall criteria; 269 → 344 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed missing poses should not disappear from the denominator |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [HOTA](https://arxiv.org/html/2009.07736v2) — §5 DetA/AssA and threshold aggregation. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Sturm et al. trajectory evaluation](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf) — §VII-A/B RPE and ATE definitions. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
