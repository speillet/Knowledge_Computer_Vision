# Review — Rectified stereo, SGM and depth — 2026-11-08

## Overview

4 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 4 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-STEREO-001 | Principal-point offsets change effective disparity: supported foundation; new case is a project deduction | Calculate a rectified depth. | 2 recall criteria; 305 → 373 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed principal-point offsets change effective disparity |
| CV-STEREO-002 | Small disparities produce asymmetric depth errors: supported foundation; new case is a project deduction | Interpreting the uncertainty of depth. | 2 recall criteria; 275 → 351 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed small disparities produce asymmetric depth errors |
| CV-STEREO-003 | A fixed-point mistake gives a predictable scale error: supported foundation; new case is a project deduction | decode a fixed disparity. | 2 recall criteria; 275 → 354 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a fixed-point mistake gives a predictable scale error |
| CV-STEREO-004 | Rectification does not resolve an occluded pixel: supported foundation; new case is a project deduction | Separate rectification and matching. | 2 recall criteria; 277 → 350 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed rectification does not resolve an occluded pixel |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [OpenCV stereo](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html) — rectified disparity/depth relationship. Consulted 2026-11-08.
- [OpenCV calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) — stereoRectify Q matrix and reprojectImageTo3D disparity scaling. Consulted 2026-11-08.

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
