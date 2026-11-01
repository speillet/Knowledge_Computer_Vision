# Review –  NMS –  remove redundant detections –  2026-10-20

## Overview

5 flashcards audited. No new defects in the perimeter of the five flashcards; the distinctions of conventions already present are confirmed. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

5 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 0 minor, 5 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-001 | Confirmed | unroll hard NMS. | 100 words at the entrance; Finished core, autonomous question | reference note and controlled format | — | Keep |
| CV-NMS-002 | Confirmed | There are three thresholds. | 117 words at the entrance; Finished core, autonomous question | reference note and controlled format | — | Keep |
| CV-NMS-003 | Confirmed | Choose the scope of a deletion. | 101 words at the entrance; Finished core, autonomous question | reference note and controlled format | — | Keep |
| CV-NMS-004 | Confirmed | Explain the effect of Soft-NMS. | 125 words at the entrance; Finished core, autonomous question | reference note and controlled format | — | Keep |
| CV-NMS-005 | Confirmed | Find the cause of a disappearance. | 110 words at the entrance; Finished core, autonomous question | reference note and controlled format | — | Keep |

### reference note and flashcards claims

- Confirmed: deletion strictly above the threshold in Torchvision and the original code; the paper also presents the convention ≥. Index splitting is a driver decision, not a CPU/GPU promise.
- Confirmed: The Gaussian penalty applies to all candidates; new maximum sought and elimination under threshold in the original code.
- Confirmed by calculation executed: IoU 2/3, outputs A,C to 0,5 and A,B,C to 0,7 (`examples/pilot_math.py`).
- Confirmed: `batched_nms` does not delete between categories; the business choice and diagnosis 005 are reasonings of the project.
- Complexities: deduction for naive pseudocode; no API benchmark announced. The roles NMS/evaluation are distinct, also verified with COCO in the journal 131.

## Corrections applied

No correction needed.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: design, evaluation, practice. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [Soft-NMS, §4 equations and §5 score threshold](https://arxiv.org/abs/1704.04503).
- [Original code b8e69bd, maximum loop, penalties and threshold](https://github.com/bharatsingh430/soft-nms/blob/b8e69bdf8df2ad53025c9d198ded909b50471d4f/lib/nms/cpu_nms.pyx).
- [Torchvision nms, convention and equality](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html); [batched_nms](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.batched_nms.html), accessed October 20 2026.
- [DETR, summary and §3.1](https://arxiv.org/abs/2005.12872).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
