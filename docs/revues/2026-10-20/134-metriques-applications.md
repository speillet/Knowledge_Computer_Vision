# Review –  Segmentation, inspection and application metrics –  2026-10-20

## Overview

4 flashcards audited. Targeted sources and alternative primary link added; responses retained. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 4 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-APPLIQUEES-001 | Confirmed; targeted source | Distinguish between border and border. | 51 words at the entrance; finite and autonomous goal | reference note and controlled format | Minor | Specify the source |
| CV-METRIQUES-APPLIQUEES-002 | Confirmed; targeted source | Measure the small flaws. | 53 words at the entrance; finite and autonomous goal | reference note and controlled format | Minor | Specify the source |
| CV-METRIQUES-APPLIQUEES-003 | Confirmed; targeted source | separate calibration and metrology. | 44 words at the entrance; finite and autonomous goal | reference note and controlled format | Minor | Specify the source |
| CV-METRIQUES-APPLIQUEES-004 | Confirmed; targeted source | Treat the empty masks. | 48 words at the entrance; finite and autonomous goal | reference note and controlled format | Minor | Specify the source |

### reference note and flashcards claims

- Confirmed: Dice is an overlap; HD95 characterizes the border distances with conventions to be defined. Reinke fig. 4a shows that the same Dice can hide different borders; fig. 5c explains the robust percentile HD95.
- Confirmed: MVTec AD2 v1, fig. 4, weights each region in PRO, unlike an aggregation dominated by large defects. The integration FPR domain must remain explicit; no unique value is imposed on the flashcards.
- Confirmed: NIST separates repeatability, reproducibility, stability, and bias; the RMS of a camera fit does not summarize these physical components.
- Confirmed: Empty cases can make metrics undefined and change an average; Reinke P2.3/P2.4/P3.2 requests to process these properties.
- Examples of small defects and metrology are constructed reasonings. The detailed biometric/OCR definitions remain in their reference notes 75/74; no equivalence of all these rates is asserted.

## Corrections applied

reference note revised, AD2 link replaced by the same primary version v1; four sources of flashcards targeted.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: algorithm, understanding, design, reasoning. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [Metrics Reloaded, Semantic segmentation and complementary metrics](https://doi.org/10.1038/s41592-023-02151-z).
- [Reinke et al., fig. 4a/5c and P2.3/P2.4/P3.2](https://www.nature.com/articles/s41592-023-02150-0).
- [MVTec AD2 v1, fig. 4 and PRO protocol](https://arxiv.org/abs/2503.21622v1); PDF initial provider inaccessible.
- [NIST, repeatability](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc441.htm), [Reproducibility](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc442.htm), [Stability](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc443.htm), [Bias](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc45.htm).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
