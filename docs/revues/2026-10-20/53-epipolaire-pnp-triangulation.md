# Review –  Epipolar, PnP and triangulation –  2026-10-20

## Overview

5 flashcards audited. 0 blocking; 1 important in the reference note; 1 minor attribution. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

5 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 1 large, 1 minor, 3 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-EPIPOLAIRE-001 | Confirmed: normalized coordinates/ideal pixels | distinguish E and F. | 45 words at input; single lens and finite core | reference note and controlled format | None | Keep |
| CV-EPIPOLAIRE-002 | Confirmed: translation to scale | Interpret the translation scale. | 50 words at input; single lens and finite core | reference note and controlled format | None | Keep |
| CV-EPIPOLAIRE-003 | Confirmed: unknown different | choose PnP or triangulation. | 56 words at input; single lens and finite core | reference note and controlled format | None | Keep |
| CV-EPIPOLAIRE-004 | Checked Geometric Deduction | detect a low parallax. | 41 words at input; single lens and finite core | reference note and controlled format | Minor | Attribution |
| CV-EPIPOLAIRE-005 | flashcard prudent correct; reference note mistakenly generalized | meet the minimum variant of pose. | 44 words at input; single lens and finite core | reference note and controlled format | Important | Distinguish between solvePnP and solveP3P |

### reference note and flashcards claims

E=[t]×R and F=K2⁻TEK1⁻1 match the camera direction 1→2; the camera center is inverted. The docs confirm the arbitrary scale, chirality and unknowns PnP/triangulation. Important correction of contract P3P of the reference note. Weak parallax reasoning is not an executed experiment.

## Corrections applied

reference note revision 2; sources 004 – 005 targeted.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Degeneration in pure rotation | E then does not provide an observable direction of translation | Diagnostic | One flashcard, two criteria; duration to be measured | Epipolar geometry, degenerate cases |

Absent families: algorithm, design, evaluation. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [OpenCV 4.13.0, solvePnP, pose computation methods and P3P](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html)
- [OpenCV 4.13.0, decomposeEssentialMat, recoverPose, solveP3P and triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
