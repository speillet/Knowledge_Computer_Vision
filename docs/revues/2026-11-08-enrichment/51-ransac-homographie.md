# Review — RANSAC for homography estimation — 2026-11-08

## Overview

7 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 7 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HOMOGRAPHIE-001 | Plane height changes the valid transform: supported foundation; new case is a project deduction | Choose a geometric model. | 2 recall criteria; 327 → 402 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed plane height changes the valid transform |
| CV-HOMOGRAPHIE-002 | General position is more than a point count: supported foundation; new case is a project deduction | Connecting degrees of freedom and degeneration. | 2 recall criteria; 298 → 372 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed general position is more than a point count |
| CV-HOMOGRAPHIE-003 | Refinement should refresh acceptance evidence: supported foundation; new case is a project deduction | Rebuild a robust iteration. | 3 recall criteria; 333 → 405 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed refinement should refresh acceptance evidence |
| CV-HOMOGRAPHIE-004 | Nominal confidence is sensitive to the inlier estimate: supported foundation; new case is a project deduction | interpret the nominal budget of RANSAC. | 2 recall criteria; 346 → 429 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed nominal confidence is sensitive to the inlier estimate |
| CV-HOMOGRAPHIE-005 | Anisotropic resizing changes a circular gate: supported foundation; new case is a project deduction | interpret the unit of a threshold of residual. | 2 recall criteria; 337 → 413 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed anisotropic resizing changes a circular gate |
| CV-HOMOGRAPHIE-006 | Projective division amplifies extrapolation: supported foundation; new case is a project deduction | Diagnose an extrapolated model. | 3 recall criteria; 306 → 379 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed projective division amplifies extrapolation |
| CV-HOMOGRAPHIE-007 | Parallax has a predictable depth trend: supported foundation; new case is a project deduction | Explain a model incompatibility. | 2 recall criteria; 315 → 391 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed parallax has a predictable depth trend |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [OpenCV projective geometry](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) — homography, findHomography residuals and robust estimation. Consulted 2026-11-08.
- [Zhang 1998](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) — §2.2 planar homography and Appendix A homogeneous estimation. Consulted 2026-11-08.

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
