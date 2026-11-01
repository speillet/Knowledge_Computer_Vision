# Journal –  Semantic segmentation, instances and panoptic segmentation –  2026-10-20

## Overview

4 flashcards audited. Panopticon definition and justification of specified metrics. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 1 large, 3 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SEGMENTATION-001 | Confirmed after precision | Select the segmentation output. | 44 words at the entrance; Three separate exits | reference note and controlled format | important | Specify partition |
| CV-SEGMENTATION-002 | Confirmed, reference specified | Detecting a bad job definition. | 47 words at the entrance; Goal retained | reference note and controlled format | Minor | Cibler source |
| CV-SEGMENTATION-003 | Deduction of discrete labels | Propagating a dense increase. | 54 words at entry; One consistency goal | reference note and controlled format | Minor | Attributing Reasoning |
| CV-SEGMENTATION-004 | Confirmed, reference specified | Evaluate medical segmentation. | 51 words at the entrance; Goal retained | reference note and controlled format | Minor | Cibler source |

### reference note and flashcards claims

- Confirmed: U-Net encoder/decoder with concatenations (§2), DeepLabv3+ atrous context (summary), Mask R-CNN mask branch and detection (summary), nnU-Net configuration of an entire pipeline (Nature summary).
- Imprecise and then corrected: the panoptic kernel omitted the lack of overlap; §3 sets an assignment per pixel.
- Confirmed: PQ separates segmentation quality and recognition (§4). Formulas IoU/Dice consistent non-zero denominator; the reference note requires a vacuum convention.
- Label Discretion: Deduction, not API prescription. Interpolating class numbers as intensities can create a meaningless class.
- Completed sources: Reinke P1/P2/P3 justifies the limits of overlap, boundaries, small structures and aggregations. External validation remains a project proposal.

## Corrections applied

reference note and 001 kernel specify partition; sources 002 – 004 suitable.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Calculate PQ on a mini-matching | The reference note cites PQ without an operating recall | evaluation | 1 flashcard; TP/FP/FN and IoU medium | Panoptic Segmentation §4 |

Absent families: algorithm, understanding, design, reasoning. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [U-Net, §2 and overlap-tile](https://arxiv.org/abs/1505.04597).
- [DeepLabv3+, summary](https://arxiv.org/abs/1802.02611) ; [Mask R-CNN, summary and introduction](https://arxiv.org/abs/1703.06870).
- [Panoptic Segmentation, §§3 – 4](https://arxiv.org/abs/1801.00868).
- [nnU-Net, summary](https://doi.org/10.1038/s41592-020-01008-z).
- [Reinke et al., P1, P2.1 – P2.4, P3.2 and discussion](https://www.nature.com/articles/s41592-023-02150-0).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
