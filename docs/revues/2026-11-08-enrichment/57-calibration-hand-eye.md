# Review — Hand–eye calibration — solving AX = XB with consistent coordinate frames — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HANDEYE-001 | Pose pairing creates correlated relative motions: supported foundation; new case is a project deduction | drift the relative movements. | 3 recall criteria; 280 → 354 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed pose pairing creates correlated relative motions |
| CV-HANDEYE-002 | A valid rigid matrix can still have wrong units: supported foundation; new case is a project deduction | respect the meaning of the poses API. | 3 recall criteria; 319 → 397 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a valid rigid matrix can still have wrong units |
| CV-HANDEYE-003 | Tiny rotations provide weak translation leverage: supported foundation; new case is a project deduction | Exciting the observable directions. | 2 recall criteria; 284 → 357 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed tiny rotations provide weak translation leverage |
| CV-HANDEYE-004 | Closure residuals need separate position and angle scales: supported foundation; new case is a project deduction | Test the closing of the chain. | 3 recall criteria; 320 → 398 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed closure residuals need separate position and angle scales |
| CV-HANDEYE-005 | Write the new invariant before reusing a solver: supported foundation; new case is a project deduction | Distinguish between eye-in-hand and eye-to-hand. | 2 recall criteria; 323 → 406 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed write the new invariant before reusing a solver |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [OpenCV calibrateHandEye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) — input/output frame directions, eye-in-hand/eye-to-hand equations and minimum motions; checked with Context7. Consulted 2026-11-08.

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
