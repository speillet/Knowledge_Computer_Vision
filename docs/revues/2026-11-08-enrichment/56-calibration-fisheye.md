# Review — Fisheye calibration — angular projection and off-center validation — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FISHEYE-001 | Zero coefficients still leave an angular camera: supported foundation; new case is a project deduction | distinguish projection fisheye and pinhole. | 2 recall criteria; 306 → 378 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed zero coefficients still leave an angular camera |
| CV-FISHEYE-002 | Peripheral views need usable corner localization: supported foundation; new case is a project deduction | design wide angle calibration views. | 3 recall criteria; 305 → 377 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed peripheral views need usable corner localization |
| CV-FISHEYE-003 | An average weights regions by observation count: supported foundation; new case is a project deduction | Locate a camera model defect. | 3 recall criteria; 298 → 374 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed an average weights regions by observation count |
| CV-FISHEYE-004 | Rectification rotation changes the ray frame: supported foundation; new case is a project deduction | Propagating the contract after rectification. | 2 recall criteria; 311 → 390 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed rectification rotation changes the ray frame |
| CV-FISHEYE-005 | More visible field can mean fewer samples per angle: supported foundation; new case is a project deduction | interpret the rectified field parameter. | 2 recall criteria; 284 → 363 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed more visible field can mean fewer samples per angle |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [OpenCV fisheye](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html) — angular projection, remap/rectification and balance definition; checked with Context7. Consulted 2026-11-08.

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
