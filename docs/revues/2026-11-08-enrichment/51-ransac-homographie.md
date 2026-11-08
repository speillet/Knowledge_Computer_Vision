# Review — RANSAC for homography estimation — 2026-11-08

## Overview

7 cards reviewed in `approfondir` mode: 7 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 7 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HOMOGRAPHIE-001 | Plane height changes the valid transform: supported mechanism; additional case is a project deduction | Choose a geometric model. | 2 recall criteria; 327 → 402 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed plane height changes the valid transform |
| CV-HOMOGRAPHIE-002 | General position is more than a point count: supported mechanism; additional case is a project deduction | Connecting degrees of freedom and degeneration. | 2 recall criteria; 298 → 372 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed general position is more than a point count |
| CV-HOMOGRAPHIE-003 | Refinement should refresh acceptance evidence: supported mechanism; additional case is a project deduction | Rebuild a robust iteration. | 3 recall criteria; 333 → 405 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed refinement should refresh acceptance evidence |
| CV-HOMOGRAPHIE-004 | Nominal confidence is sensitive to the inlier estimate: supported mechanism; additional case is a project deduction | interpret the nominal budget of RANSAC. | 2 recall criteria; 346 → 429 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed nominal confidence is sensitive to the inlier estimate |
| CV-HOMOGRAPHIE-005 | Anisotropic resizing changes a circular gate: supported mechanism; additional case is a project deduction | interpret the unit of a threshold of residual. | 2 recall criteria; 337 → 413 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed anisotropic resizing changes a circular gate |
| CV-HOMOGRAPHIE-006 | Projective division amplifies extrapolation: supported mechanism; additional case is a project deduction | Diagnose an extrapolated model. | 3 recall criteria; 306 → 379 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed projective division amplifies extrapolation |
| CV-HOMOGRAPHIE-007 | Parallax has a predictable depth trend: supported mechanism; additional case is a project deduction | Explain a model incompatibility. | 2 recall criteria; 315 → 391 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed parallax has a predictable depth trend |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OpenCV projective geometry](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) — homography, findHomography residuals and robust estimation. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Zhang 1998](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) — §2.2 planar homography and Appendix A homogeneous estimation. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
