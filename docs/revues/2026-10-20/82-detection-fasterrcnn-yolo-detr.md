# Review –  Detection: Faster R-CNN, families YOLO and DETR –  2026-10-20

## Overview

5 flashcards audited. A significant lack of justification for YOLO diversity corrected; sources of other specified flashcards. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

5 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 1 large, 4 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-001 | Confirmed after source accuracy | Find the sharing of features. | 50 words at the entrance; Finished core, objective retained | reference note and controlled format | Minor | Targeting the source |
| CV-DETECTEURS-002 | Confirmed with additional sources | Do not generalize the whole YOLO family. | 40 words at the entrance; Single goal | reference note and controlled format | important | Add proof of variants |
| CV-DETECTEURS-003 | Confirmed after source accuracy | distinguish between the three assignments. | 57 words at the entrance; Finished core, objective retained | reference note and controlled format | Minor | Targeting the source |
| CV-DETECTEURS-004 | Detailed Project Reasoning | analyze small objects after resize. | 82 words at entry; Criteria finished; case not executed | reference note and controlled format | Minor | Specify attribution |
| CV-DETECTEURS-005 | Detailed Project Reasoning | compare detection pipelines. | 48 words at entry; Criteria finished; case not executed | reference note and controlled format | Minor | Specify attribution |

### reference note and flashcards claims

- Confirmed: RPN and detection head share the convolutions of the image (Faster R-CNN §3).
- The YOLO diversity was not supported by the only original article: YOLOv3 §2.1 describes its anchors; YOLOX §2.1 explicitly describes the anchor-free passage, the head and SimOTA. Added sources, without extending the flashcards program.
- Confirmed: DETR §3.1 assigns bipartite matching predictions to a set of targets completed by no-object; supervision and NMS have distinct functions.
- Resize controls, split selection, and timing conditions are protocol proposals, not empirical results of these papers.

## Corrections applied

reference note revised and then sources of the five targeted flashcards; responses and IDs retained.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: conception, practice, reasoning. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [Faster R-CNN, §3 and introduction](https://arxiv.org/abs/1506.01497).
- [DETR, §3.1, fig. 1 and equations 1 – 2](https://arxiv.org/abs/2005.12872).
- [YOLov3, §2.1](https://arxiv.org/abs/1804.02767) ; [YOLOX, §2.1, paragraphes Anchor-free/Decoupled head](https://arxiv.org/abs/2107.08430).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
