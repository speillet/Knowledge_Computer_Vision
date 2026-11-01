# Review –  Exposure, noise, colour and sampling –  2026-10-18

## Overview

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 3 large, 0 minor, 1 without detected defect. The observations relating only to the reference note are detailed separately below.

Self-review: Agent Codex (`revue-cartes`). The editorial status remains `redige`.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-001 | Confirmed by calculation: 4 then 8 px | Calculate a simplified blur. | Finished core; 48 words | reference note and format | Important (attribution) | Deduction reported |
| CV-ACQUISITION-002 | Confirmed: gain and photonic information | Distinguish between gain and exposure. | Finished core; 46 words | reference note and format | None | Keep the kernel |
| CV-ACQUISITION-003 | Confirmed: filtering before decimation | recognize aliasing and inconsistent preprocessing. | Finished core; 55 words | reference note and format | Important (source) | Source pyramide |
| CV-ACQUISITION-004 | Relevant checklist; sRGB transfer confirmed | check an image entry. | Finished core; 46 words | reference note and format | Important (source) | Photometric source |

### reference note and flashcards claims

Confirmed: photonic variance equal to the average in the ideal model; limits of gain; Nyquist under band hypothesis; pyramid filtering; nonlinearity sRGB. Calculations executed: 800×0,005=4 px; exposure doubled: 8 px. Controls of entry contracts and protocol on defects: project decisions.

## Corrections applied

reference note revision 2 and four corrected Source fields; responses and IDs retained.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Budget exposure – noise – flou | Choice of acquisition under pace and contrast imposed | Design; a flashcard | 3 compromise; duration to be measured | EMVA1288 §§2.4 – 2.7; explicit kinematic model |

## Sources

- [EMVA1288 Linear 4.0 (2021), §§2.1, 2.4, 2.6 – 2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf): Poisson variance Eq.13, SNR Eq.20 – 23, saturation §2.7.
- [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html): convolution and decimation.
- [sRGB, §§A.7 – A.8 and B.1, linear conversion and transfer function](https://www.w3.org/Graphics/Color/srgb): non-linear transfer.
- [Edmund, Resolution §2.2](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/resolution/): Nyquist limit; read via documentary browser, direct HTTP access 403.

## Checks and limitations

Reference checks: 52 reference notes, 224 flashcards, 34 passed tests. Controls after modification and retention of identifiers are recorded in the [bilan commun](../2026-10-20/00-bilan.md). Context7 unavailable: direct access to official documentation when necessary.

Real export Anki, rendering Obsidian/AnkiDroid, mastery of the learner and independent scientific validation not verified. Scenarios and diagnostic recommendations are reasonings of the project, unless explicitly assigned. Absent families alone do not justify new flashcards.
