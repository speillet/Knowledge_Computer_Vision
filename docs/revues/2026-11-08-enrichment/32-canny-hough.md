# Review — Canny and Hough: edges, lines and segments — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 1 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CANNY-HOUGH-001 | Weak chains need a surviving strong seed: supported foundation; new case is a project deduction | Explain the hysteresis. | 2 recall criteria; 295 → 374 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed weak chains need a surviving strong seed |
| CV-CANNY-HOUGH-002 | The angle belongs to the normal: supported foundation; new case is a project deduction | interpret a Hough vote. | 2 recall criteria; 318 → 397 lexical words | Canonical explanation aligned; ID and front preserved | Important | Restore the geometric meaning of Hough voting after mistranslation; Specify the origin and sign of the Hough distance; Developed the angle belongs to the normal |
| CV-CANNY-HOUGH-003 | Disconnected support should not become one segment: supported foundation; new case is a project deduction | Distinguish between right and segment. | 2 recall criteria; 300 → 370 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed disconnected support should not become one segment |
| CV-CANNY-HOUGH-004 | Normal consistency can reject texture support: supported foundation; new case is a project deduction | Differentiate texture and structure. | 2 recall criteria; 295 → 371 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed normal consistency can reject texture support |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

- CV-CANNY-HOUGH-002: Restore the geometric meaning of Hough voting after mistranslation.
- CV-CANNY-HOUGH-002: Specify the origin and sign of the Hough distance.



## Sources

- [OpenCV Canny](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html) — nonmaximum suppression and hysteresis. Consulted 2026-11-08.
- [OpenCV Hough](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html) — normal parameterization; standard versus probabilistic line outputs. Consulted 2026-11-08.

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
