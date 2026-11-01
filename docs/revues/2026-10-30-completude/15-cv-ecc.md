# Review –  registration by intensities and ECC –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ECC-001 | Deduction/Assumption Cases; Documentary Context Below | Understanding the Standardized Criterion: Specifying the Existing Question | Finished core preserved; 184 → 293 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ECC-002 | Deduction/Assumption Cases; Documentary Context Below | Decouple score and plausibility: specifies the existing question | Finished core preserved; 192 → 304 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ECC-003 | Deduction/Assumption Cases; Documentary Context Below | Warp size and identifiability: specifies the existing question | Finished core preserved; 191 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-ECC](../../../vault/40-features-matching/references/45-recalage-ecc.md); [flashcards](../../../vault/40-features-matching/45-recalage-ecc.md). reference note modified before the flashcards.

- **CV-ECC-001 –  Understanding the Standardized Criterion**: on a fixed support, center the intensities $a_i$ and $b_i(\theta)$ gives $\bar a_i=a_i-\mu_a$ and $\bar b_i=b_i(\theta)-\mu_b$. The correlation is $\rho(\theta)=\sum_i\bar a_i\bar b_i/(\sqrt{\sum_i\bar a_i^2}\sqrt{\sum_i\bar b_i^2})$ if the norms are nonzero. Multiply an image by a positive gain and add a global offset retains this ideal value; a negative gain reverses its sign. Optimization modifies the warp, thus the interpolated intensities and their gradient with respect to the parameters. Valid media and hidden pixels must remain explicitly controlled: changing the overlap can change the compared criterion.

- **CV-ECC-002 –  Decouple score and plausibility**: A correlation close to 1 describes the standardized similarity of the actually compared content. It does not directly indicate the number of valid pixels, the uniqueness of the maximum, or the displacement error. A very small common area can therefore produce a high score with little geometric information. Report media size and error on reserved points, then test separate initializations of a period of the pattern. If several solutions keep scores close and physical constraints allowable, keep ambiguity in the decision. Turning the score into acceptance confidence requires calibration on representative cases, including false but visually plausible alignments.

- **CV-ECC-003 –  Dimension and identifiability of the warp**: translation: two parameters; plane Euclidean movement: rotation and two translations; affine: six parameters; homography: eight independent parameters after choice of scale. A homography acts by projective division: small changes in the denominator can strongly change the edges of the extrapolated region. With little overlap or texture, some parameters compensate and the local information matrix can become poorly conditioned. Compare models with reserved geometry rather than with the only optimized score. If a simpler model is sufficient, it can limit these compensations; if the capture violates its assumptions, this simplicity imposes on the contrary an irreducible bias.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, computeECC/findTransformECC](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html) –  criterion, motionType, initialization, and reverse warping. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
