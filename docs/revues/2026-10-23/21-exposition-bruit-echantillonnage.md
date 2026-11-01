# Review –  Exposure, noise, colour and sampling –  2026-10-23

## Overview

Four flashcards audited, plus their reference note. No false claims. An important observation of source: CV-ACQUISITION-003 attributed the aliasing to the tutorial OpenCV of the pyramids, which does not treat it. Two minor observations. Correction applied: reference note in revision 3, IDs and objectives unchanged. On the proposed enrichments, the learner has retained only the encrypted rewriting of CV-ACQUISITION-002, written in revision 4; the number of flashcards does not change.

Self-review: Agent Claude Code (`revue-cartes`). Editorial status `redige`.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-001 | Calculation redone: 800 × 0,005 = 4 px | Useful for designing a test | Net Core | Agreement reference note | None | — |
| CV-ACQUISITION-002 | Confirmed by EMVA 1288, §2.6, eq. 21: excluding quantification, $K$ cancels itself in the SNR | Forte | Front in "why" that guides; family comparison without numerical comparison | Agreement reference note | Minor | Proposed Enrichment |
| CV-ACQUISITION-003 | Not supported by the source cited, then confirmed (Parmar et al. 2022, §§2, 3.2) | Forte | Net Core | Agreement reference note | Important | Dedicated source; Resize conventions by library |
| CV-ACQUISITION-004 | Project checklist, plausible | Forte | Six-point verifiable core | Agreement reference note | None | — |

reference note: The Edmund Optics page cited refuses automated access; it could not be rechecked (minor, reported in reference note).

## Corrections applied

- reference note `vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md`, revision 3: prefilter, folding and resize conventions according to Parmar et al.; scope of tutorial OpenCV specified; Edmund Optics reported unverified.
- CV-ACQUISITION-003: source and further explanation.
- Journal: A line.

## Enrichments: decision of the learner

Holding the 2026-10-23: CV-ACQUISITION-002, rewritten in numerical comparison without changing the objective, and the corresponding part of reference note (EMVA model, SNR regimes, saturation). Not retained: photon transfer and sizing. Their sources are checked for later addition.

Table of proposals as submitted:

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| CV-ACQUISITION-002: quantified comparison "double the gain or double the exposure" with the SNR EMVA model. Example: $\sigma_d=5$ e⁻, 100 e⁻ gives SNR 8,9; 200 e⁻ gives 13,3; doubling $K$ leaves 8,9. Effects on blur and saturation | The flashcard is qualitative while the standard enciphers the effect | comparison, rewriting without changing the objective | No new reminders | EMVA 1288 Linear 4.0, §2.4, eq. 13 – 15, and §2.6, eq. 21 – 22 |
| CV-ACQUISITION-005: estimate system gain and camera playback noise by the photon transfer method, with one pair of images per level | Characterizing a camera before accusing a model; machine vision engineer gesture absent from the vault | practice | 1 flashcard; core at 3 points | EMVA 1288, §2.4, eq. 15, and §2.5, eq. 16 – 18 |
| CV-ACQUISITION-006: size the acquisition of a check in line (strip of 0,2 mm, field of 150 mm, scroll to 0,5 m/s): 15 px/mm, approximately 2 500 px, exposure ≤ 133 µs, lighting accordingly | Family conception absent from the subject | design | 1 flashcard; core at 4 points | The Imaging Source, Field of View (empirical rule from 2 to 3 px); EMVA 1288, §2.6; project calculations |
| reference note: EMVA noise model, SNR regimes, photon transfer, sizing | Mathematics and Thin Assessment | reference note | without flashcard | The same sources |

## Sources

- [EMVA 1288 Linear, Release 4.0, 16 juin 2021](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf), full text:
  - §2.1, eq. 5 – 6;
  - §2.4, eq. 13 – 15 and photon transfer method;
  - §2.5, eq. 16 – 19;
  - §2.6, eq. 20 – 23;
  - §2.7, eq. 24 – 25.
- [Parmar, Zhang and Zhu 2022](https://arxiv.org/abs/2104.11222), read in HTML on ar5iv: §§1, 2, 3.2 – 3.3, 4.1, 4.3 and 6.3.
- [The Imaging Source, Field of View in Machine Vision](https://www.theimagingsource.com/en-us/resource/glossary/field-of-view-in-machine-vision/), manufacturer glossary without date: empirical rule from 2 to 3 pixels and pixel/mm formulas.
- Project calculations (Python 3.10.13): SNR according to $K$ and $\mu_e$; dimensioning 15 px/mm, 2 475 px with 10% margin, 7 500 px/s, 133 µs.
- Unverifiable: Edmund Optics, Resolution, which returns an anti-robot verification page.

## Checks and limitations

`check_vault.py` OK (244 flashcards) after correction. Context7 is not available in this session. Not verified: export Anki, rendering Obsidian and AnkiDroid, control, independent validation, any measurement on real camera.
