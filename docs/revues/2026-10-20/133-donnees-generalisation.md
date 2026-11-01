# Review –  Splits, annotations, score calibration and drift –  2026-10-20

## Overview

5 flashcards audited. Direct sources on selection and offset added; cores retained. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

5 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 2 large, 3 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FIABILITE-001 | Confirmed; targeted source | Choose a split unit. | 42 words at the entrance; finite and autonomous goal | reference note and controlled format | Minor | Specify the source |
| CV-FIABILITE-002 | Confirmed; targeted source | distinguish between two calibrations. | 50 words at the entrance; finite and autonomous goal | reference note and controlled format | Minor | Specify the source |
| CV-FIABILITE-003 | Confirmed with source added | Keep a non-adaptive test. | 55 words at entry; clear separation rule | reference note and controlled format | important | Ajouter Cawley–Talbot |
| CV-FIABILITE-004 | Deduction of explicit protocol | Diagnose a seasonal drift. | 82 words at the entrance; Business case finished | reference note and controlled format | Minor | Assign the diagnosis |
| CV-FIABILITE-005 | Confirmed with source added | Avoiding certainty outside the field. | 43 words at entry; Conclusion limited to evidence | reference note and controlled format | important | Ajouter Ovadia |

### reference note and flashcards claims

- Confirmed: Roberts explains the underestimation of the error by some random splits of structured data; the blocking depends on the targeted scenario and is not automatically better for any target. The flashcard retains this condition.
- Confirmed: Guo §2 defines the confidence/correction frequency agreement; this is not Zhang's intrinsic/extrinsic estimate. Threshold accuracy also depends on prevalence (Bayes identity).
- Source added: Cawley – Talbot deals with the optimistic bias due to selection; applying to a suitable test during active learning is a deduction from the project.
- Source added: Ovadia shows the limits of post-hoc calibration under offset; no high softmax becomes an out-of-domain warranty.
- Seasonal drift, collection criteria and monitoring: proposed protocols, with no results in the field.

## Corrections applied

Bibliography of the completed reference note; sources of the five targeted flashcards.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Link prevalence, recall and threshold accuracy | Avoid transferring the accuracy of an enriched test to production | reasoning | 1 flashcard; Bayes calculation on two prevalences | Guo and explicit probabilistic protocol |

Absent families: algorithm, understanding, design, reasoning. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [Roberts et al., summary and discussion of blocking](https://doi.org/10.1111/ecog.02881), PDF lu via [Author's deposit](https://www.biom.uni-freiburg.de/mitarbeiter/dormann/roberts-et-al-2017-ecography.pdf/at_download/file).
- [Guo et al., §2 equation 1](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf).
- [Cawley – Talbot, summary and introduction](https://www.jmlr.org/papers/volume11/cawley10a/cawley10a.pdf).
- [Ovadia et al., summary and introduction](https://arxiv.org/abs/1906.02530).
- [The ML Test Score, official summary](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/), only for the role of testing/monitoring; no audit of 28 tests.
- Zhang, controlled passages in the journal 52.

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
