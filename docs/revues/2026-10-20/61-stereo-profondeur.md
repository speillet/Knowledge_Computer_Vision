# Review –  Corrected stereo, SGM and depth –  2026-10-20

## Overview

4 flashcards audited. 0 blocking; 2 important (conditions and kernel); 1 minor. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 1 large, 1 minor, 2 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-STEREO-001 | Confirmed by calculation: 10 m | Calculate a rectified depth. | 49 words at entry; core refocused on the issue | reference note and controlled format | Important | Conventions and optional detail |
| CV-STEREO-002 | Confirmed by derivation: sensitivity in 1/d² | Interpreting the uncertainty of depth. | 51 words at entry; a relationship, f/B set | reference note and controlled format | Minor | Attribution of calculation |
| CV-STEREO-003 | Confirmed: 16 factor and floating conversion | decode a fixed disparity. | 50 words at entry; storage contract | reference note and controlled format | None | Source versioned |
| CV-STEREO-004 | Confirmed: correcting does not resolve ambiguities | Separate rectification and matching. | 48 words at the entry; a geometric role | reference note and controlled format | None | Keep |

### reference note and flashcards claims

Simple model conditions specified; 1000×0,2/20=10 m, then 20 m for 10 px. The derivative is −fB/d²; the propagation is first order, for f and B fixed. SGBM is explicitly a variant, with documented penalties and format. The depth is not validated by a universal sign mask.

## Corrections applied

reference note revision 2; flashcard 001 clarified without changing its purpose; references 001 – 003 specified.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Explain the penalties SGM P1/P2 | Mechanism Named but Not Questioned | Algorithme | One flashcard, three criteria; duration to be measured | Hirschmüller, SGM; OpenCV for SGBM |

Absent families: algorithm, understanding, design, evaluation, practice. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [OpenCV 4.13.0, StereoSGBM, Detailed Description and create](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html)
- [OpenCV 4.13.0, stereoRectify and reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html): conversion /16 explicitly requested; minDisparity may change with rectification.

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
