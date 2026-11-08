# Review — Camera calibration with a target — Zhang’s method — 2026-11-08

## Overview

7 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 7 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ZHANG-001 | A known target scale fixes translation units: supported foundation; new case is a project deduction | There are three geometric objectives. | 3 recall criteria; 327 → 403 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a known target scale fixes translation units |
| CV-ZHANG-002 | Homogeneous scale is not another camera parameter: supported foundation; new case is a project deduction | interpret the projection conventions. | 3 recall criteria; 360 → 438 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed homogeneous scale is not another camera parameter |
| CV-ZHANG-003 | Different images can repeat the same constraint: supported foundation; new case is a project deduction | Explain the multi-view constraints. | 3 recall criteria; 329 → 403 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed different images can repeat the same constraint |
| CV-ZHANG-004 | Low pixel RMS can coexist with metric scale bias: supported foundation; new case is a project deduction | interpret a RMS without an abusive conclusion. | 2 recall criteria; 324 → 401 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed low pixel rms can coexist with metric scale bias |
| CV-ZHANG-005 | A transform chain avoids order mistakes: supported foundation; new case is a project deduction | Spreading a pixel transformation. | 2 recall criteria; 320 → 397 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a transform chain avoids order mistakes |
| CV-ZHANG-006 | Parameter stability needs withheld acquisition groups: supported foundation; new case is a project deduction | Diagnose observability. | 3 recall criteria; 310 → 388 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed parameter stability needs withheld acquisition groups |
| CV-ZHANG-007 | Measurement uncertainty includes the working plane: supported foundation; new case is a project deduction | Build consistent collection and validation. | 3 recall criteria; 316 → 394 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed measurement uncertainty includes the working plane |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [Zhang calibration](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) — §§2–4 intrinsic constraints, refinement and degeneracy. Consulted 2026-11-08.
- [OpenCV calibration](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) — pinhole and distortion conventions. Consulted 2026-11-08.

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
