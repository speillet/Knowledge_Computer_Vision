# Review –  RANSAC applied to a homography –  2026-10-20

## Overview

7 flashcards audited. 0 blocking, 0 important; 1 minor shared (case status). Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

7 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 1 minor, 6 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HOMOGRAPHIE-001 | Confirmed: pure plan/rotation, parallax | Choose a geometric model. | 103 words at the input; distinct core of the further explanation | reference note and controlled format | None | Keep |
| CV-HOMOGRAPHIE-002 | Confirmed: 8 degrees and minimum rank | Connecting degrees of freedom and degeneration. | 93 words at the input; distinct core of the further explanation | reference note and controlled format | None | Keep |
| CV-HOMOGRAPHIE-003 | Confirmed: hypothesis, consensus, re-evaluation | Rebuild a robust iteration. | 111 words at the input; distinct core of the further explanation | reference note and controlled format | None | Keep |
| CV-HOMOGRAPHIE-004 | Confirmed by §II and calculation: 72/9 | interpret the nominal budget of RANSAC. | 122 words at the input; distinct core of the further explanation | reference note and controlled format | None | Keep the requested justification |
| CV-HOMOGRAPHIE-005 | Confirmed: residual destination; resize deducted | interpret the unit of a threshold of residual. | 117 words at the input; distinct core of the further explanation | reference note and controlled format | None | Keep |
| CV-HOMOGRAPHIE-006 | Algebraic diagnosis of the project | Diagnose an extrapolated model. | 95 words at the input; distinct core of the further explanation | reference note and controlled format | Minor | Attribution explicite |
| CV-HOMOGRAPHIE-007 | Confirmed: model incompatibility | Explain a model incompatibility. | 100 words at the input; distinct core of the further explanation | reference note and controlled format | None | Keep |

### reference note and flashcards claims

Confirmed: homogeneous model, plan/rotation case, calculation of residual, four non-degenerate correspondences, budget under independent assumption. Normalization does not restore an absent rank: algebraic deduction. Spatial diagnostics are not the result of experience. The two diagnoses 006/007 have different causes (packaging and model). The flashcard 004 gives the numerical result but asks for its derivation and its interpretation: no answer revealed.

## Corrections applied

reference note revision 3 and source of 006. Calculations of examples/pilot_math.py executed: 72 and 9.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| residual symmetric and uncertainty in both images | Limit of the only transfer to destination | Reasoning | One flashcard, three criteria; duration to be measured | Hartley – Zisserman, Optimal Homography Estimation |

Absent families: understanding, design, evaluation. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [Fischler – Bolles 1981, §II, procedure and probability p.383](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf), PDF extract; formula and interpretation consulted.
- [OpenCV 4.13, homography, Basic theory and Demo 5](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html).
- [OpenCV 4.13, findHomography, parameters and algorithm](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
