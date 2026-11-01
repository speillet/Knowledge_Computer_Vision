# Review –  Single-object tracking: correlation, Siamese and MeanShift –  2026-10-20

## Overview

2 flashcards audited. An important justification corrected: SiamFC does not update the 002 case template. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

2 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 1 large, 1 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SOT-001 | Confirmed; source specified | distinguish SOT and MOT. | 49 words at the entrance; Goal retained | reference note and controlled format | Minor | Cibler source |
| CV-SOT-002 | Not supported by SiamFC; corrected | understand a template drift. | 47 words at the entrance; Conditional case, drift objective retained | reference note and controlled format | important | Cite KCF and specify scope |

### reference note and flashcards claims

- Confirmed: MeanShift moves a window to a distribution mode, with histogram projected in the tutorial; CamShift adapts the window. This is not an automatic MOT.
- Confirmed: SiamFC compares initial target and search with a Siamese network; it explicitly says do not refresh the appearance model. It could therefore not serve as an example of drift due to this update.
- Correction: the reference note distinguishes the adaptive variants of SiamFC. KCF describes drive at the new position and interpolation of the model; contamination by a distractor is a deduction from the project on this mechanism.
- The search region limits the captureable movement in these local pipelines; the reference note does not announce a universal limit for any tracker.
- The freeze, loss and reset policies are proposals to be tested.

## Corrections applied

reference note revised to limit the update to the variants concerned; KCF added and sources of the corrected flashcards.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: algorithm, understanding, design, evaluation, practice, reasoning. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [OpenCV 4.13.0, Meanshift/Camshift, template introduction and loop](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
- [SiamFC, introduction and §4: fixed template](https://arxiv.org/abs/1606.09549).
- [KCF, model tracking and interpolation pipeline](https://arxiv.org/abs/1404.7584).
- [SORT, §3](https://arxiv.org/abs/1602.00763).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
