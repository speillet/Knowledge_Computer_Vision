# Review –  NeRF, 3D Gaussian Splatting and Reconstruction –  2026-10-20

## Overview

3 flashcards audited. An important ambiguity of the reference note on the lifted NeRF density; sources specified. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

3 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 3 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-RENDU3D-001 | Confirmed, targeted source | Implicit and primitive representation. | 51 words at the entrance; Unique purpose retained | reference note and controlled format | Minor | Specify source |
| CV-RENDU3D-002 | Deduction from the explicit project | separating rendering and geometry. | 49 words at entry; finished protocol, no promise of result | reference note and controlled format | Minor | Assign the case |
| CV-RENDU3D-003 | Deduction from the explicit project | Check out a little-observed scene. | 40 words at entry; finished protocol, no promise of result | reference note and controlled format | Minor | Assign the case |

### reference note and flashcards claims

- Confirmed and then specified: in NeRF original, positional density and directional color, with integration along the spokes. The phrase of the reference note might have led one to believe that the density was directional.
- Confirmed: 3DGS optimizes Gaussians with anisotropic covariance and check density, then renders by splatting.
- Deduction: PSNR compares images, does not measure a physical length. The scale and a geometric reference are necessary for a metrological assertion.
- Coverage checks/poses are proposed diagnostics, not an evaluation based on project data.
- DUSt3R/MASt3R, MVS and TSDF are only references to other contracts; no detailed comparison of these methods is validated here.

## Corrections applied

reference note revised and direct references added; objectives of the three flashcards unchanged.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: algorithm, understanding, design, practice, reasoning. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [NeRF, author's page](https://www.matthewtancik.com/nerf) and [§§3 – 4, protocol §6](https://arxiv.org/abs/2003.08934).
- [3DGS, summary and presentation of the authors](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) ; [Paper](https://arxiv.org/abs/2308.04079).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
