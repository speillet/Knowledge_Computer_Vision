# Review –  OCR and documentary understanding –  2026-10-20

## Overview

3 flashcards audited. 0 blocking; 1 important (variant of the cited protocol). Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

3 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 1 large, 0 minor, 2 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OCR-001 | Confirmed: distinct outputs; business choice deducted | Separate recognition and structure. | 49 words at the entrance; a need for evaluation | reference note and controlled format | None | Targeted source |
| CV-OCR-002 | Confirmed for CER classic; OCR-D divergence explained | Interpreting CER. | 51 words at entry; conditions of the score | reference note and controlled format | Important | Convention specified |
| CV-OCR-003 | Diagnosis deduced from the treatment chain | locate a reading order defect. | 44 words at the input; localization of a component | reference note and controlled format | None | Keep |

### reference note and flashcards claims

CRNN: extraction/sequence/CTC; TrOCR: encoder-decoder transform; LayoutLM: text and positions; Donut: structured generation without separate OCR, confirmed at the level of identification by the primary texts. OCR-D distinguishes several CER; own example: reference “a”, prediction “abc” gives 2/1=200% with the classical convention. On the other hand, its normalized CER remains limited. Characters and words must be defined by protocol.

## Corrections applied

reference note revision 2; classic/standardized distinction and sources of the three flashcards.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Aggregate CER per medium mic/macro | Avoid comparing documents of different lengths without protocol | Evaluation | A flashcard, an example; duration to be measured | OCR-D CER Granularity |

Absent families: algorithm, understanding, design, evaluation, practice. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [OCR-D, Text Evaluation, CER and WER, Viewed on 2026-10-20](https://ocr-d.de/en/spec/ocrd_eval.html) : sections Characters, Levenshtein, CER and WER lues.
- [CRNN §2](https://arxiv.org/abs/1507.05717), [TrOCR summary](https://arxiv.org/abs/2109.10282), [LayoutLM summary/§2](https://arxiv.org/abs/1912.13318), [Donut summary and figure 1](https://arxiv.org/abs/2111.15664): Extracted PDFs.

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
