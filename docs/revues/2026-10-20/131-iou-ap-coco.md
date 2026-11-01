# Review –  IoU and AP –  COCO detection protocol –  2026-10-20

## Overview

7 flashcards audited. No new scientific defects; a corrected reference note shell. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

7 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 0 minor, 7 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IOU-AP-001 | Confirmed | calculate a overlap in the right contract. | 98 words at the entrance; Finished core, context and explicit conventions | reference note and controlled format | — | Keep |
| CV-IOU-AP-002 | Confirmed | Distinguish between local measurement and aggregated protocol. | 124 words at the entrance; Finished core, context and explicit conventions | reference note and controlled format | — | Keep |
| CV-IOU-AP-003 | Confirmed | Explain the penalty for a duplicate. | 94 words at the entrance; Finished core, context and explicit conventions | reference note and controlled format | — | Keep |
| CV-IOU-AP-004 | Confirmed | rebuild a simple interpolated AP. | 110 words at the entrance; Finished core, context and explicit conventions | reference note and controlled format | — | Keep |
| CV-IOU-AP-005 | Confirmed | Compare evaluators with caution. | 113 words at the entrance; Finished core, context and explicit conventions | reference note and controlled format | — | Keep |
| CV-IOU-AP-006 | Deduction from protocol | diagnose a deviation according to the location requirement. | 103 words at the entrance; Diagnosis finished; no cause asserted without proof | reference note and controlled format | — | Keep |
| CV-IOU-AP-007 | Deduction from protocol | link average benchmark and business decision. | 103 words at the entrance; Diagnosis finished; no cause asserted without proof | reference note and controlled format | — | Keep |

### reference note and flashcards claims

- Confirmed: official bbox format [x,y,width,height], floating coordinates; `maskApi.c` calculates continuous areas without +1. The pilot's IoU is without a unit.
- Confirmed by `evaluateImg`: Sorting detections by score, ordinary GT associated at most once, reusable crowd, ignored cases and separate area filters.
- Confirmed by `accumulate`/`Params`: precision envelope, 101 reminders, ten thresholds IoU; categories without valid GT left to −1 then excluded, category valid without zero detection.
- Difference really noted: the official page says top-100 all classes; the code pinned cut by image/category when useCats=1 before truncate maxDet. The existing nuance is preserved.
- Recalculation executed: TP/FP/TP gives 0,834983; only one GT detected out of two gives 0,504950. The change in rank is a deduction from the envelope, with no conclusion on the business cost of a FP.
- The flashcards 006/007 are proposed diagnostic/evaluation protocols, not project measures.

## Corrections applied

Grammatical chord in reference note; seven flashcards preserved.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: comparison, conception. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [COCO, page actually loaded: detection-eval.htm](https://cocodataset.org/dataset/detection-eval.htm), metric and point 6.
- [COCO, format-results.htm](https://cocodataset.org/dataset/format-results.htm), Object Detection.
- [cocoeval.py, commit 8c9bcc3, evaluateImg/accumulate/Params](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), lu via raw.
- [maskApi.c, same commit, bbIou/rleIou](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/common/maskApi.c).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation. The pinned code uses np.float in particular: it was read, not executed with a current NumPy environment. No current software operation of this old commit is claimed.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
