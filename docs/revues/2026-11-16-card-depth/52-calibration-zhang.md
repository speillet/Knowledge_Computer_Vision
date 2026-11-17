# Review — Camera calibration with a target — Zhang’s method — 2026-11-16

## Overview

2 cards audited and deepened in `approfondir` mode (CV-ZHANG-007 and CV-ZHANG-001), the
two shortest of the subject. Highest severity per card before correction: 0 blocking,
0 important, 2 minor (both answers lacked a worked number for their objective), 0 with
no defect identified. No figure was assigned to this subject.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige. Reference revision 9 → 10.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ZHANG-007 | Existing claims confirmed: Zhang's procedure (§3.4, lines 418–427 of the extraction); `calibrateCamera` inputs and outputs (calib3d.hpp L1606–L1743); the ray–plane intersection and its 0.4 mm off-plane case match the reference's worked example D. The answer listed design decisions without showing which of them dominates a tolerance | Design: turns a calibration into a measurement instrument | 3 expected criteria, unchanged; 319 → 530 lexical words (the counter includes the Source line) | Aligned with worked example D and the Assumptions section | Minor | Deepened: constructed error budget (pixel footprint and edge localization, printed-target scale, surface height), Zhang's non-planarity result (§5.3.2); Source line extended |
| CV-ZHANG-001 | Existing claims confirmed: one pose per view and intrinsics shared (§2.1 eq. 1, §3.1); "use solvePnP" when intrinsics are known (calib3d.hpp L1649–L1653); the homography argument is supported by §2.3, which the Source line did not cite. Missing: why a homography cannot be a calibration, in numbers | Understanding: separates calibration, pose and registration by their unknowns | 3 expected criteria, unchanged; 327 → 509 lexical words | Aligned with the reference's Problem, Constraints and Cost sections | Minor | Deepened: Zhang's counting argument (8 − 6 = 2 constraints per view), parameter and residual counts for the three problems, the OpenCV 4.13 outputs of each; Source line given §2.3 and header lines |

The two additions do not repeat other cards of the subject. CV-ZHANG-003 states the
two constraints per view but not their origin in the degrees of freedom of $H$;
CV-ZHANG-004 uses a 20 mm against 19.8 mm square for an RMS argument, so CV-ZHANG-007
uses a different scale error (a target printed at 99.7%) inside a length budget.

## Applied corrections

- `vault/50-calibration-geometrie/52-calibration-zhang.md`, card CV-ZHANG-001: new
  paragraph **Unknowns, counted**; Source line extended with Zhang §2.3 and the
  `findHomography`, `solvePnP` and `calibrateCamera` header lines.
- Same file, card CV-ZHANG-007: new paragraph **Error budget against the tolerance**;
  Source line extended with §5.3.2.
- `vault/50-calibration-geometrie/references/52-calibration-zhang.md`, revision 9 → 10:
  the unknown counts in "Problem and data contract"; Zhang's counting sentence under the
  constraints; the non-planarity results of §5.3.2 in "Assumptions"; an error budget
  after worked example D; closing provenance line extended.

Expected answers, questions, objectives, families, tags and IDs are unchanged. No
reference claim was found false, so no correction-log entry is needed.

## Claims added and their passages

| Claim | Passage | Verdict |
| --- | --- | --- |
| A homography has 8 degrees of freedom, the pose 6, hence 2 constraints on the intrinsics per view | Zhang MSR-TR-98-71 §2.3, lines 214–217 of the `pdftotext` extraction | Confirmed |
| $n\ge3$ general views, or $n=2$ with zero skew | §3.1, lines 321–323 | Confirmed |
| Systematic non-planarity has more effect than random model-point errors; cylindrical worse than spherical; "seems still usable in practice" below about 3%; 10% is 2.5 cm | §5.3.2, lines 806–864 | Confirmed |
| `findHomography` maps between two planes and its robust methods draw subsets of four pairs | calib3d.hpp L782–L841, L818 | Confirmed |
| `solvePnP` returns the transform from model to camera | calib3d.hpp L1031–L1032 | Confirmed |
| 67 parameters and 1080 residuals; 6 and 108; 8 from four correspondences | Constructed from the reference's $5+2+6n$ and $2nm$ | Recomputed |
| 0.5 mm per pixel, 0.07 mm on a length, 0.15 mm for a 99.7% target, 50.10 mm and 0.4 mm for a 2 mm height | Constructed with the reference's ray–plane model | Recomputed |

## Sources

Scientific sources:

- Zhang, "A Flexible New Technique for Camera Calibration", MSR-TR-98-71 (last updated
  2008): the PDF downloaded during the 2026-11-14 pass was copied and extracted with
  `pdftotext -layout`; read §2.3, §3.1, §3.4 and §5.1–§5.3.2.

Implementation sources (official code at tag 4.13.0, fetched from
`raw.githubusercontent.com`):

- [`modules/calib3d/include/opencv2/calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L782-L851): L782–L851 (`findHomography`), L1020–L1040 (`solvePnP` parameters), L1606–L1656 and L1726–L1743 (`calibrateCamera`).

Failed accesses: docs.opencv.org was not tried (HTTP 403 in earlier passes). Context7 is
unavailable in this session.

## Checks and limitations

`python3 -I docs/revues/2026-11-16-card-depth/checks/52-calibration-zhang.py`: 7 checks
pass (counting argument, parameter and residual counts, views needed, edge budget,
target-scale scaling of a ray–plane intersection, off-plane length and position, Zhang's
non-planarity scale). The error budget is a constructed example, not a measurement; no
calibration or OpenCV call was executed. AnkiDroid and Obsidian rendering are not
verified. Export status: **to republish with `paquet-anki`**.
