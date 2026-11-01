# Review –  Camera calibration on calibration target –  Zhang's method –  2026-10-20

## Overview

7 flashcards audited. 0 blocking; 1 important (error source passage); 1 minor (bibliographical coordinate frame). Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

7 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 1 large, 1 minor, 5 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ZHANG-001 | Confirmed: separate exits | There are three geometric objectives. | 104 words at entry; unique comparison | reference note and controlled format | None | Keep |
| CV-ZHANG-002 | Confirmed at §2.1; old inaccurate reference | interpret the projection conventions. | 124 words at entry; evaluable conventions; explicit optional skew | reference note and controlled format | Important | Corrected passage |
| CV-ZHANG-003 | Confirmed: two constraints and independent views | Explain the multi-view constraints. | 109 words at entry; mechanism and bounds | reference note and controlled format | Minor | §2.3 added |
| CV-ZHANG-004 | Confirmed: pixel adjustment; proposed validation | interpret a RMS without an abusive conclusion. | 111 words at the entrance; no universal threshold | reference note and controlled format | None | Keep |
| CV-ZHANG-005 | Confirmed by composition K′=AK | Spreading a pixel transformation. | 105 words at the input; pixel convention of the tool to be checked | reference note and controlled format | None | Keep |
| CV-ZHANG-006 | Confirmed: degenerate orientations; diagnosis deduced | Diagnose observability. | 107 words at entry; consistent hypothesis and test | reference note and controlled format | None | Keep |
| CV-ZHANG-007 | Project protocol consistent with Zhang capture | Build consistent collection and validation. | 102 words at input; flashcard design; load to measure | reference note and controlled format | None | Keep |

### reference note and flashcards claims

Confirmed: projection world→camera, K, orthogonality of columns, three views for five parameters, two sub zero skew, degeneration by identical orientations, radial model and minimization of reprojection. The §4 mentions an exception under known translation (Appendix D): it does not contradict the case without known metric movement of the vault. The resize/crop is a derivation of coordinate frame and not a recalibration. Industrial recommendations are already distinguished from paper results.

## Corrections applied

reference note revision 3; sources of 002 – 003 corrected.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Identify the known metric translation case | Avoid generalizing degeneration to any calibration | further explanation from reference note | No priority flashcard | Zhang, annexe D |

Absent families: algorithm, comparison. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [Zhang, report TR98-71, §§2.1 – 2.3, 3.1 – 3.3, 4 and Annex D](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf), full text downloaded.
- [OpenCV 4.13, camera model and calibrateCamera](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), parameters, RMS and resolution change.

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
