# Review –  optical flow: Lucas – Kanade, Farnebäck and RAFT –  2026-10-20

## Overview

4 flashcards audited. No defects requiring correction in the four flashcards. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 0 minor, 4 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLOT-001 | Confirmed | interpret the constraint of the flow. | 47 words at entry; Single objective, finite kernel | reference note and controlled format | — | Keep |
| CV-FLOT-002 | Confirmed | respect the temporal unity. | 51 words at entry; Single objective, finite kernel | reference note and controlled format | — | Keep |
| CV-FLOT-003 | Confirmed | situer RAFT. | 51 words at entry; Single objective, finite kernel | reference note and controlled format | — | Keep |
| CV-FLOT-004 | Explicit Deduction of the Project | process a occlusion. | 46 words at entry; Cases and completed checks | reference note and controlled format | — | Keep |

### reference note and flashcards claims

- Confirmed: photometric constancy and coherent local movement lead to scalar stress; the Lucas-Kanade system requires good spatial conditioning. The pyramid deals with larger displacements without inventing gradients.
- Confirmed: The tutorial defines the returned flow as moving between images and also derives the continuous speed dx/dt. The reference note explicitly conditions the units at the step of derivation. Calculation 4/0,020 = 200 px/s checked.
- Confirmed: RAFT §3.2 builds correlations between all feature pairs; §3.3 refines the stream repeatedly. The recurrence is about refinement, not a ReID of object.
- `status=1` indicates a point found by the algorithm, not physical evidence; the diagnosis of occlusion and the baseline are deductions from the project. No check round trip alone guarantees a good connection.

## Corrections applied

No correction needed.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Distinguish EPE and validity under occlusion | Explicitly choose the pixels evaluated | evaluation | 1 flashcard; norm and mask | RAFT §4 and selected dataset protocol |

Absent families: algorithm, understanding, design, evaluation. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [OpenCV 4.13.0, Optical Flow and Lucas – Kanade, definition, derivation and status](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html).
- [RAFT, §§3.1 – 3.3](https://arxiv.org/abs/2003.12039).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
