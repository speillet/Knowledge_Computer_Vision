# Review –  Local detectors, descriptors and matchers –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCHING-001 | Deduction/Assumption Cases; Documentary Context Below | Link to the aperture problem: specifies the existing question | Finished core preserved; 184 → 296 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MATCHING-002 | Deduction/Assumption Cases; Documentary Context Below | Expected equivariance and invariance: specifies the existing question | Finished core preserved; 182 → 293 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MATCHING-003 | Deduction/Assumption Cases; Documentary Context Below | Measuring the cascade effect: specifies the existing question | Finished core preserved; 194 → 305 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MATCHING-004 | Deduction/Assumption Cases; Documentary Context Below | Choosing the right residual: specifies the existing question | Finished core preserved; 185 → 290 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-MATCHING](../../../vault/40-features-matching/references/43-detecteurs-matchers.md); [flashcards](../../../vault/40-features-matching/43-detecteurs-matchers.md). reference note modified before the flashcards.

- **CV-MATCHING-001 –  Link to aperture problem**: The linearized luminance constant gives $I_xu+I_yv+I_t=0$, an equation for two displacement components. On an edge, the neighboring gradients are almost parallel, so stacking their equations does not add a second independent direction. A corner brings different gradient orientations and can make the local system invertible. This reasoning assumes a movement common to the patch and small variations between images. A window through two objects can have a well-conditioned tensor but no longer respect the single movement. The corner score should be read with this model, and not as a universal utility score for all estimators.

- **CV-MATCHING-002 –  Expected equivariance and invariance**: If an image is geometrically transformed by $T$, a repeatable detector should find the transformed positions $T(p)$; it should therefore not produce the same numerical coordinates. On the contrary, the descriptor aims at a comparable representation of the corresponding neighborhoods after the planned standardizations. Confusing these two properties misconstrues a rotation test: the coordinates should change, while the description should stay close enough. Too much invariance can also remove distinctive information and make several patches similar. The aim is not to make all descriptors identical under any transformation, but to keep discrimination in the field of variations useful.

- **CV-MATCHING-003 –  Measuring the cascade effect**: on the same requests, keep successively the identity of the two neighbors, the decision of the ratio filter, the insider status and the reserved geometric error. This track allows you to locate where a search difference becomes a product error. If the index finds the exact neighbors but the registration changes, consider order of matches, separation of the ex æquo and randomness of the robust estimate. If neighbors differ, only increasing the budget or redoing the exact distances on additional candidates is a more targeted ablation. An identical recall average may still mask the loss of rare distinguishing points that are decisive for lifting a symmetry.

- **CV-MATCHING-004 –  Choose the right residual**: for a $H$ homography sending the image A to B, $e_i=\|\pi(H\tilde p_i)-q_i\|_2$ is a transfer error in B pixels, with $\pi$ the homogeneous division. An epipolar geometry imposes another constraint, and PnP combines points 3D and calibrated projection. Reusing a threshold without announcing the residual changes what “inlier” means. The geometric test checks for compatibility conditional to the model; one symmetry can provide another set equally compatible. Adding an independent constraint is then a change in available information, while tightening the threshold only changes the tolerance of the same test.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, Feature Matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html) –  BF/FLANN, metrics and filters; Context7 verification. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
