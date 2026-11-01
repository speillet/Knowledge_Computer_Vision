# Review –  Multisensor calibration, hand-eye and time –  2026-10-20

## Overview

3 flashcards audited. 0 blocking; 2 important (convention and source). Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

3 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 2 large, 0 minor, 1 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MULTICALIB-001 | Confirmed but reference note gave no complete convention | Interpreting hand-eye. | 51 words at the entrance; convention objective | reference note and controlled format | Important | Defined string |
| CV-MULTICALIB-002 | Confirmed: non-parallel axes; stability test deduced | Evaluate informative movements. | 44 words at the entrance; cause and action | reference note and controlled format | None | Targeted source |
| CV-MULTICALIB-003 | Not supported by hand-eye alone; LOAM confirms the deskew | separating intrinsic extrinsic and time. | 44 words at the entrance; three related responsibilities | reference note and controlled format | Important | Source LOAM |

### reference note and flashcards claims

Eye-in-hand chain and informative axes confronted with OpenCV; deformation of the scan confronted with LOAM. The choice of reserved trajectories and the diagnosis in motion are proposals of the project. No time calibration automatically produced by CalibrateHandEye is claimed.

## Corrections applied

reference note revision 2: coordinate frames explained; sources of the three targeted flashcards.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Diagnose offset and clock drift separately | A fixed offset does not model any desynchronization | Diagnostic | A flashcard; duration to be measured | Kalibr, calibration temporelle |

Absent families: algorithm, understanding, design, evaluation, practice. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [OpenCV 4.13.0, calibrateHandEye, eye-in-hand equations and note on axes](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)
- [Zhang – Singh 2014, LOAM, §§II, IV and V-B](https://www.roboticsproceedings.org/rss10/p07.pdf): Downloaded PDF, time interpolations of §V-B points.

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
