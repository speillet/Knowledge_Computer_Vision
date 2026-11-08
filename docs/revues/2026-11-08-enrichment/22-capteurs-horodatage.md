# Review — Sensors, rolling shutter and synchronization — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 4 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CAPTEURS-001 | Short exposure can coexist with large skew: supported mechanism; additional case is a project deduction | separate exhibition and reading rolling shutter. | 2 recall criteria; 281 → 368 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed short exposure can coexist with large skew |
| CV-CAPTEURS-002 | Offset and drift need different corrections: supported mechanism; additional case is a project deduction | estimate a spatial time lag. | 2 recall criteria; 298 → 373 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed offset and drift need different corrections |
| CV-CAPTEURS-003 | Turning exposes a lever-arm timing error: supported mechanism; additional case is a project deduction | Calibration and time. | 3 recall criteria; 330 → 415 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed turning exposes a lever-arm timing error |
| CV-CAPTEURS-004 | Radial speed depends on relative motion: supported mechanism; additional case is a project deduction | interpret the output of sensors. | 2 recall criteria; 304 → 387 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed radial speed depends on relative motion |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [Basler shutter types](https://docs.baslerweb.com/electronic-shutter-types) — Global Shutter and Rolling Shutter exposure timing. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Zhang and Singh, LOAM](https://www.roboticsproceedings.org/rss10/p07.pdf) — §§II/V time-varying acquisition and motion compensation. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
