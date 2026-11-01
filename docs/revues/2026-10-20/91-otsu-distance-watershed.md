# Review –  Otsu, distance transform and watershed –  2026-10-20

## Overview

5 flashcards audited. No defects requiring correction in the five flashcards. Diagnostics are still built cases. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

5 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 0 minor, 5 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-WATERSHED-001 | Explicit Reasoning of the Project | interpret the Otsu objective. | 55 words at input; Verifications finished, no promise of result | reference note and controlled format | — | Keep |
| CV-WATERSHED-002 | Confirmed | Rebuild the marker pipeline. | 46 words at the entrance; finite and autonomous core | reference note and controlled format | — | Keep |
| CV-WATERSHED-003 | Confirmed | distinguish background and unknown. | 48 words at the entrance; finite and autonomous core | reference note and controlled format | — | Keep |
| CV-WATERSHED-004 | Explicit Reasoning of the Project | Locate a sub-segmentation. | 58 words at input; Verifications finished, no promise of result | reference note and controlled format | — | Keep |
| CV-WATERSHED-005 | Explicit Reasoning of the Project | Choose a classic instance metric. | 48 words at input; Verifications finished, no promise of result | reference note and controlled format | — | Keep |

### reference note and flashcards claims

- Confirmed: minimization of weighted intra-class variance in OpenCV, equivalence to inter-class variance by decomposition of total variance.
- Confirmed: `distanceTransform` measures the distance to the nearest null pixel; metric and mask matter. A maximum is not a semantic class.
- Confirmed: int32 markers of the same size, positive labels, unknown 0, borders −1 and table modification; the tutorial explicitly distinguishes known and unknown background.
- Diagnostics and Instance Protocol: Project Deductions. A union of two objects can keep the same binary mask after merging, so the binary IoU does not test the count.
- The Otsu example of the repository is a histogram calculation; no OpenCV execution or claimed image validation.

## Corrections applied

No correction needed.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: comparison, understanding, conception. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [OpenCV 4.13.0, Otsu’s Binarization and How does... work](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html).
- [OpenCV 4.13.0, watershed, Theory and Code: distance and markers](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
