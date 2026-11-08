# Review — Sensors, rolling shutter and synchronization — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CAPTEURS-001 | Short exposure can coexist with large skew: supported foundation; new case is a project deduction | separate exhibition and reading rolling shutter. | 2 recall criteria; 281 → 368 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed short exposure can coexist with large skew |
| CV-CAPTEURS-002 | Offset and drift need different corrections: supported foundation; new case is a project deduction | estimate a spatial time lag. | 2 recall criteria; 298 → 373 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed offset and drift need different corrections |
| CV-CAPTEURS-003 | Turning exposes a lever-arm timing error: supported foundation; new case is a project deduction | Calibration and time. | 3 recall criteria; 330 → 415 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed turning exposes a lever-arm timing error |
| CV-CAPTEURS-004 | Radial speed depends on relative motion: supported foundation; new case is a project deduction | interpret the output of sensors. | 2 recall criteria; 304 → 387 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed radial speed depends on relative motion |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [Basler shutter types](https://docs.baslerweb.com/electronic-shutter-types) — Global Shutter and Rolling Shutter exposure timing. Consulted 2026-11-08.
- [Zhang and Singh, LOAM](https://www.roboticsproceedings.org/rss10/p07.pdf) — §§II/V time-varying acquisition and motion compensation. Consulted 2026-11-08.

## Proposals

No new ID is created in this pass. See the [proposal register](../propositions.md)
and [overview](00-bilan.md) for pending complementary cards and decisions.

## Checks and limitations

Scope-wide executed checks and identity/field comparisons are recorded in the
[overview](00-bilan.md). The source assessment concerns the mechanisms and
boundary cases identified above; it is not a fresh passage-by-passage
certification of every retained historical paragraph or implementation claim.
No CV experiment, hardware benchmark, independent review, learner mastery or
AnkiDroid rendering is established. Export status: to republish with `paquet-anki`.
