# Review — Canny and Hough: edges, lines and segments — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode: 4 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 1 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CANNY-HOUGH-001 | Weak chains need a surviving strong seed: supported mechanism; additional case is a project deduction | Explain the hysteresis. | 2 recall criteria; 295 → 374 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed weak chains need a surviving strong seed |
| CV-CANNY-HOUGH-002 | Moving a Hough line from ROI to full-image coordinates: supported mechanism; additional case is a project deduction | interpret a Hough vote. | 2 recall criteria; 318 → 417 lexical words | ID/front preserved; canonical wording aligned | Important | Restore the geometric meaning of Hough voting after mistranslation; Specify the origin and sign of the Hough distance; Developed moving a hough line from roi to full-image coordinates |
| CV-CANNY-HOUGH-003 | Disconnected support should not become one segment: supported mechanism; additional case is a project deduction | Distinguish between right and segment. | 2 recall criteria; 300 → 370 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed disconnected support should not become one segment |
| CV-CANNY-HOUGH-004 | Normal consistency can reject texture support: supported mechanism; additional case is a project deduction | Differentiate texture and structure. | 2 recall criteria; 295 → 371 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed normal consistency can reject texture support |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.

- CV-CANNY-HOUGH-002: Restore the geometric meaning of Hough voting after mistranslation.
- CV-CANNY-HOUGH-002: Specify the origin and sign of the Hough distance.



## Sources

- [OpenCV Canny](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html) — nonmaximum suppression and hysteresis. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [OpenCV Hough](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html) — normal parameterization; standard versus probabilistic line outputs. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
