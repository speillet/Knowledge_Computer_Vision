# Review — Fisheye calibration — angular projection and off-center validation — 2026-11-16

## Overview

1 card audited and deepened in `approfondir` mode (CV-FISHEYE-004). Highest severity
before correction: 0 blocking, 0 important, 1 minor (the answer built the inverse map but
did not say in which frame a pose estimated on the rectified image lives, nor show the
size of the error when the raw calibration is reused), 0 with no defect identified. One
minor reference defect was corrected on the way: a dangling "worked example E" label. No
figure was assigned to this subject.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige. Reference revision 7 → 8.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FISHEYE-004 | Existing claims confirmed: the inverse map through $(PR)^{-1}$, the raw ray $R^\top K_{\mathrm{new}}^{-1}\tilde u'$ and the infinite coordinates for $w\le0$ (fisheye.cpp L560–L615); scaling of focal length and centre with the output size (fisheye.cpp L705–L713). Missing: the frame of a pose estimated on the rectified image, the matching sparse path, and a number for the error of reusing the raw calibration | Practice: carries the rectified contract into pose estimation | 2 expected criteria, unchanged; 314 → 585 lexical words (the counter includes the Source line) | Consistent with the Rectification paragraph and worked example C of the reference | Minor | Deepened: zero distortion and $K_{\mathrm{new}}$ for `solvePnP`, the rectified frame and $R^\top$, the `undistortPoints` cross-check, three readings of one rectified pixel; Source line extended |

The addition does not repeat CV-FISHEYE-005, which uses the same edge-midpoint rule to
discuss field and sampling density, not the reading of a rectified pixel or a pose frame.

## Reference correction

| Error | Source | Correction |
| --- | --- | --- |
| "A fitted polynomial may violate this outside the calibrated field (worked example E)": the reference has no worked example E; the 2026-11-14 check script computes the monotonicity case as its example D | `docs/revues/2026-11-14-reference-depth/checks/56-calibration-fisheye.py`, example D (check 10) | The sentence now states the case: with $k_1=-0.1$ alone, $\mathrm d\theta_d/\mathrm d\theta$ vanishes at 1.83 rad, citing example D of that script |

Minor, low risk; no fisheye card uses the label (`rg "worked example E" vault` finds it in
other subjects only, which were not checked in this pass).

## Applied corrections

- `vault/50-calibration-geometrie/56-calibration-fisheye.md`, card CV-FISHEYE-004: new
  paragraphs **Pose and frame after rectification** and **Constructed example**; Source
  line extended with `undistortPoints`, `estimateNewCameraMatrixForUndistortRectify`, the
  `solvePnP` distortion default and the `stereoRectify` change of basis.
- `vault/50-calibration-geometrie/references/56-calibration-fisheye.md`, revision 7 → 8:
  two consequences of rectification for points and poses, a worked example of three
  readings of one rectified pixel, the monotonicity label fixed; closing provenance line
  extended.

Expected answer, question, objective, family, tags and ID are unchanged.

## Claims added and their passages

| Claim | Passage | Verdict |
| --- | --- | --- |
| `fisheye::undistortPoints` multiplies $R$ by the left $3\times3$ block of $P$ and applies it to the undistorted point | fisheye.cpp L394–L409, L500–L505 | Confirmed |
| `fisheye::initUndistortRectifyMap` inverts $PR$ | fisheye.cpp L565–L579 | Confirmed |
| An empty distortion vector means zero coefficients for `solvePnP` | calib3d.hpp L1029–L1030 | Confirmed |
| The rectification rotation is a change of basis from the unrectified to the rectified camera frame | calib3d.hpp L2016–L2019 (`stereoRectify`, $R_1$); the fisheye maps use $R$ the same way | Confirmed |
| `balance` = 0 gives $f_{\max}$; with the lens of worked example C, 336.1 px | fisheye.cpp L655–L724; reference worked example C | Recomputed |
| 300 and 229.9 px; readings 34.4°, 26.3° and 39.2°; 0.105 m for a 4° rotation at 1.5 m | Constructed | Recomputed |

## Sources

Scientific sources: none newly consulted; the card's mechanism is an implementation
contract, and the model it relies on was checked against Kannala and Brandt in the
2026-11-14 pass.

Implementation sources (official code at tag 4.13.0, fetched from
`raw.githubusercontent.com`):

- [`calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L4120-L4160): L1029–L1030, L2016–L2019, L4128–L4160 (fisheye `undistortPoints`, `initUndistortRectifyMap`), L4250–L4279 (fisheye `stereoRectify`).
- [`fisheye.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fisheye.cpp#L363-L724): L363–L520 (`undistortPoints`), L532–L615 (`initUndistortRectifyMap`), L655–L724 (`estimateNewCameraMatrixForUndistortRectify`).

Failed accesses: none in this pass. Context7 is unavailable in this session.

## Checks and limitations

`python3 -I docs/revues/2026-11-16-card-depth/checks/56-calibration-fisheye.py`: 6 checks
pass ($f_{\min}$ and $f_{\max}$; raw and rectified offsets; the three readings; agreement
of the `undistortPoints` path with the map path under a 4° rectification rotation; the
frame shift; the 1.83 rad monotonicity limit). No OpenCV call was executed: the paths are
reimplemented from the code in the check script. AnkiDroid and Obsidian rendering are not
verified. Export status: **to republish with `paquet-anki`**.
