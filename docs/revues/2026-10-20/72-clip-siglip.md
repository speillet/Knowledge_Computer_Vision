# Review –  CLIP, SigLIP and text recognition –  2026-10-20

## Overview

4 flashcards audited. 0 blocking; 1 important shared (bad passage cited); 2 minors. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 2 minor, 2 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CLIP-001 | Confirmed: Encoders and Text Classes | interpret the zero-shot CLIP. | 51 words at entry; ambiguous sentence clarified | reference note and controlled format | Minor | Reformuler |
| CV-CLIP-002 | Deducted from standardization on candidates | Reject a misleading probability. | 45 words at the entrance; counter-example finished | reference note and controlled format | None | Keep |
| CV-CLIP-003 | Confirmed: bidirectional softmax vs sigmoid per pair | distinguer objectifs contrastifs. | 51 words at the entrance; central distinction | reference note and controlled format | None | Keep |
| CV-CLIP-004 | Project Protocol | test the sensitivity to the text. | 55 words at input; validation/test separation | reference note and controlled format | Minor | Attribution |

### reference note and flashcards claims

Standardized form of embeddings and temperature, zero-shot classification, sensitivity to prompts, sigmoid lens with temperature and bias confirmed by the passages consulted. The general limits are at §6 of CLIP, the §7 deals with impacts. Automatic non-calibration is a logical limit; no threshold or target performance attributed to authors.

## Corrections applied

reference note revision 2; §6 everywhere; further explanation 001 clarified.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Effect of an additional candidate on softmax | Numerical example of the reasoning of 002 | Further explanation | No new reminders needed | Definition of softmax; CLIP §2.3 |

Absent families: algorithm, design, diagnosis, practice. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [Radford et al., CLIP, §§2.3, 3.1 and limits §6](https://arxiv.org/abs/2103.00020): PDF, pseudocode §2.3, §3.1.4 and §6.
- [Zhai et al., SigLIP, §3 and algorithm 1](https://arxiv.org/abs/2303.15343): PDF, algorithm 1 and §3.

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
