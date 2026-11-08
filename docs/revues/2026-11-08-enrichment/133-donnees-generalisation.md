# Review — Data splits, annotations, score calibration and drift — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 3 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FIABILITE-001 | Derived samples inherit their source group: supported mechanism; additional case is a project deduction | Choose a split unit. | 2 recall criteria; 277 → 350 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed derived samples inherit their source group |
| CV-FIABILITE-002 | Calibration needs a defined correctness event: retained explanation sufficient for this extension | distinguish between two calibrations. | 2 recall criteria; 271 → 271 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-FIABILITE-003 | An untouched test is consumed by repeated selection: supported mechanism; additional case is a project deduction | Keep a non-adaptive test. | 2 recall criteria; 307 → 384 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed an untouched test is consumed by repeated selection |
| CV-FIABILITE-004 | Season and sensor can be confounded: supported mechanism; additional case is a project deduction | Diagnose a seasonal drift. | 3 recall criteria; 308 → 381 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed season and sensor can be confounded |
| CV-FIABILITE-005 | Selective prediction needs both risk and coverage: retained explanation sufficient for this extension | Avoiding certainty outside the field. | 2 recall criteria; 278 → 278 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [Guo et al. calibration](https://proceedings.mlr.press/v70/guo17a.html) — §2 confidence/calibration and reliability diagrams. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Cawley and Talbot](https://www.jmlr.org/papers/v11/cawley10a.html) — model-selection overfitting and evaluation bias. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
