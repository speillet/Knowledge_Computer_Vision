# Review –  SORT –  multiobject tracking by movement and association –  2026-10-20

## Overview

8 flashcards audited. Two important inaccuracies and outdated returns corrected; confirmed mechanisms. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

8 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 2 large, 0 minor, 6 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SORT-001 | Confirmed; criterion clarified | Separate the responsibilities of the tracker. | 105 words at the entrance; A blocker now accurate | reference note and controlled format | important | Correct criteria |
| CV-SORT-002 | Confirmed | interpret a state and its units. | 119 words at entry; Single objective, finite kernel | reference note and controlled format | — | Keep |
| CV-SORT-003 | Confirmed | interpret the weight of a measure. | 99 words at entry; Single objective, finite kernel | reference note and controlled format | — | Keep |
| CV-SORT-004 | Confirmed; empty entry specified | Distinguish between memory and transmission. | 103 words at input; Finished case on two frames | reference note and controlled format | important | Specify table 2D |
| CV-SORT-005 | Confirmed | Understanding rejection after assignment. | 105 words at entry; Single objective, finite kernel | reference note and controlled format | — | Keep |
| CV-SORT-006 | Explicit Deduction of the Project | Make a discriminating diagnosis. | 106 words at entry; Cases and completed checks | reference note and controlled format | — | Keep |
| CV-SORT-007 | Confirmed | Distinguish between temporal tasks. | 100 words at entry; Single objective, finite kernel | reference note and controlled format | — | Keep |
| CV-SORT-008 | Explicit Deduction of the Project | define a complete performance measure. | 106 words at entry; Cases and completed checks | reference note and controlled format | — | Keep |

### reference note and flashcards claims

- Confirmed: SORT processes image-by-image detections, without appearance or future; center/area/ratio state and three speeds, transition F to unit pitch in the pinned code.
- Confirmed by reading the code: max_age=1, min_hits=3, threshold 0,3; deletion if age > maximum, issue only after update and hit_streak condition/start exception.
- Confirmed: combination by IoU, shortcut for unambiguous pairs, then assignment and rejection under threshold. The matrix counter-example is a calculation constructed: 0,90 > 0,62 then a single pair retained.
- Example Kalman recalculated with `examples/pilot_math.py`: 107,352941 px and variance 6,617647; R=100 gives 102 px. This is not an execution of SORT.
- Correctability: the 001 criterion on “independent output” was ambiguous; replaced by the net countersense of the tracker that would make the detection itself.
- API: The code documentation requires an empty array (0,5), not an empty Python list. Correction 004.
- 006/008 diagnostics are protocols to be performed; no video results are deduced from the paper.

## Corrections applied

reference note revised; correction criteria 001 and empty entry contract 004 specified; links to now existing topics.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: conception. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [SORT, §§3.1 – 3.4 and §4](https://arxiv.org/abs/1602.00763).
- [Official code commit 2236dff, convert_bbox_to_z, KalmanBoxTracker, association and Sort.update](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py), lu via raw.

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
