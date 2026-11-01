# Review –  Visual representations, ViT, Swin, ConvNeXt and DINOv2 –  2026-10-20

## Overview

5 flashcards audited. 0 blocking; 1 important (missing source); 2 minor. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

5 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 1 large, 2 minor, 2 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-REPRESENTATIONS-001 | Confirmed: N×4 and term image×16 | Estimate the cost of tokens. | 39 words at entry; class token excluded | reference note and controlled format | Minor | Specified front |
| CV-REPRESENTATIONS-002 | Confirmed: offset windows vs convolution | Swin and ConvNeXt. | 43 words at entry; unique comparison | reference note and controlled format | None | Keep |
| CV-REPRESENTATIONS-003 | Transfer confirmed; product requirements deducted | Use self-supervised features. | 47 words at entry; evaluable outputs and decision | reference note and controlled format | None | Keep |
| CV-REPRESENTATIONS-004 | Not initially supported for LoRA/adapters; confirmed by dedicated sources | Choose an adaptation. | 52 words at input; parameters trained vs inference | reference note and controlled format | Important | Added sources |
| CV-REPRESENTATIONS-005 | Project Checklist | check preprocessing a backbone. | 43 words on entry; precise entry contract | reference note and controlled format | Minor | Attribution explicite |

### reference note and flashcards claims

ViT: patches and cost; Swin: hierarchical windows; ConvNeXt: ConvNet; DINOv2: self-supervised learning and transfer. LoRA/adapters verified at the principle level, without extrapolating their NLP performance to vision. MAE reconstructs hidden pixels. HOG primary summary available in index, INRIA download unavailable; no thorough derivation HOG is confirmed. The calculation excludes additional tokens and does not predict latency.

## Corrections applied

reference note revision 2 and sources 001/004/005; front 001 specified.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Interpret dense tokens and global tokens | Selecting Outputs for a Localized Task | Practice | One flashcard, two criteria; duration to be measured | DINOv2, dense tasks |

Absent families: algorithm, design, evaluation, practice. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [ViT, §3.1](https://arxiv.org/abs/2010.11929)
- [Swin, §3](https://arxiv.org/abs/2103.14030)
- [ConvNeXt, §2](https://arxiv.org/abs/2201.03545)
- [DINOv2, summary and valuation by transfer](https://arxiv.org/abs/2304.07193)
- [Hu et al., LoRA, summary and principle of frozen parameters](https://arxiv.org/abs/2106.09685)
- [Houlsby et al., adaptors, summary](https://arxiv.org/abs/1902.00751)
- [He et al., MAE, summary](https://arxiv.org/abs/2111.06377)
- [Dalal – Triggs, HOG, summary](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf)

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
