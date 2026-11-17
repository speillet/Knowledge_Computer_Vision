# Review — Multisensor calibration, hand–eye calibration and timing — 2026-11-16

## Overview

1 card audited and deepened in `approfondir` mode (CV-MULTICALIB-002). Highest severity
before correction: 0 blocking, 0 important, 1 minor (the answer named the free translation
component but not the free rotation component, nor a check that tells the two kinds of
instability apart), 0 with no defect identified. No figure was assigned to this subject.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige. Reference revision 8 → 9.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MULTICALIB-002 | Existing claims confirmed: the translation equation $(R_A-I)t_X=R_Xt_B-t_A$ is the translation part of $AX=XB$ and is the system OpenCV solves (calibration_handeye.cpp L353–L376, "eq 15"); $(R_A-I)n=0$ recomputed; the minimum of two motions with non-parallel axes (calib3d.hpp L2352–L2353). The sentence "provided the rotation $R_X$ is itself correctly estimated" left implicit that a single-axis plan also leaves $R_X$ free about that axis | Diagnosis: separates pose count from pose diversity and names the components to inspect | 2 expected criteria, unchanged; 335 → 596 lexical words (the counter includes the Source line) | Consistent with the reference's Observability and Degenerate cases | Minor | Deepened: the rotation ambiguity from Horaud and Dornaika eq. 18, a discriminating check in a frame aligned with the motion axis, constructed singular values, OpenCV's missing rank check, the planar-vehicle analogue; Source line extended |

The addition does not repeat CV-HANDEYE-003 (another subject), which covers small
rotation angles and OpenCV's angle filter, not the free rotation component, the
singular values of a single-axis plan or the absence of a rank check.

## Applied corrections

- `vault/50-calibration-geometrie/55-calibration-multicapteurs.md`, card
  CV-MULTICALIB-002: new paragraphs **Which components drift** and **Constructed
  example**; Source line extended with Horaud and Dornaika §3 and
  `calibration_handeye.cpp` L334–L376.
- `vault/50-calibration-geometrie/references/55-calibration-multicapteurs.md`, revision
  8 → 9: the rotation ambiguity, the constructed singular values and OpenCV's missing rank
  check in the hand–eye observability bullet; the vertical lever arm in "Degenerate
  cases"; Horaud and Dornaika and `calibration_handeye.cpp` added to the source lists;
  closing provenance line extended.

Expected answer, question, objective, family, tags and ID are unchanged. No reference
claim was found false, so no correction-log entry is needed.

## Claims added and their passages

| Claim | Passage | Verdict |
| --- | --- | --- |
| The rotation equation gives $n_A=R_Xn_B$; eq. 19 is rank deficient for one motion; two independent motions are needed | Horaud and Dornaika 1995, arXiv 2311.12655, §3, eqs. 18–19 (lines 525–592 of the extraction) | Confirmed |
| With parallel axes, $\mathrm{Rot}(n_A,\varphi)R_X$ satisfies every rotation equation | Deduction from eq. 18; verified numerically for three angles | Recomputed |
| OpenCV's Tsai path errors only when fewer than two pairs pass its filter, then calls `solve(..., DECOMP_SVD)` for rotation and translation | calibration_handeye.cpp L334–L344, L376; the wrapper checks only the pose count (L743) | Confirmed |
| Singular values 2.31, 2.31, 0 and 2.31, 2.20, 0.73 | Constructed | Recomputed |
| The vertical lever arm of planar driving needs pitch and roll excitation or an independent measurement | Extends the reference's planar-vehicle degenerate case (project deduction) | Project deduction |

## Sources

Scientific sources:

- Horaud and Dornaika 1995, "Hand-Eye Calibration", IJRR 14(3), author copy
  [arXiv 2311.12655](https://arxiv.org/abs/2311.12655): text extracted during the
  2026-11-14 pass and copied to this pass's source folder; read §3 (eqs. 16–19 and the
  decoupling paragraph).

Implementation sources (official code at tag 4.13.0, fetched from
`raw.githubusercontent.com`):

- [`calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2234-L2356): L2234–L2250 (separable and simultaneous methods, eye-to-hand), L2318–L2347 (chains), L2352–L2353 (two non-parallel motions).
- [`calibration_handeye.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration_handeye.cpp#L275-L376): Tsai path L275–L376, wrapper checks L724–L790.

Failed accesses: none in this pass. Context7 is unavailable in this session.

## Checks and limitations

`python3 -I docs/revues/2026-11-16-card-depth/checks/55-calibration-multicapteurs.py`:
4 checks pass (singular values of a single-axis plan for 3, 20 and 200 motions; the mixed
plan; the rotation ambiguity; the translation null direction). No robot, sensor or solver
was run. AnkiDroid and Obsidian rendering are not verified. Export status: **to
republish with `paquet-anki`**.
