# Review –  Epipolar, PnP and triangulation –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-EPIPOLAIRE-001 | Deduction/Assumption Cases; Documentary Context Below | Constraint at a distance: specifies the existing question | Finished core preserved; 183 → 299 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-EPIPOLAIRE-002 | Deduction/Assumption Cases; Documentary Context Below | pose and chirality: specifies the existing question | Finished core preserved; 187 → 301 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-EPIPOLAIRE-003 | Deduction/Assumption Cases; Documentary Context Below | Writing Linear Triangulation: Specifying the Existing Question | Finished core preserved; 194 → 308 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-EPIPOLAIRE-004 | Deduction/Assumption Cases; Documentary Context Below | Why reverse depth helps: clarifies the existing question | Finished core preserved; 183 → 299 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-EPIPOLAIRE-005 | Deduction/Assumption Cases; Documentary Context Below | Origin of multiple solutions: specifies the existing question | Finished core preserved; 180 → 290 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-EPIPOLAIRE](../../../vault/50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md); [flashcards](../../../vault/50-calibration-geometrie/53-epipolaire-pnp-triangulation.md). reference note modified before the flashcards.

- **CV-EPIPOLAIRE-001 –  Constraint at a distance**: A point $\tilde p_1$ defines a line $l_2=F\tilde p_1$ in the 2 image. If $l_2=(a,b,c)$, the distance of $(u,v)$ to this line is $|au+bv+c|/\sqrt{a^2+b^2}$ when the denominator is non-zero. This normalization removes the arbitrary scale from the right, unlike the only product $\tilde p_2^TF\tilde p_1$. A Sampson residual or a symmetric error responds to other approximations and conventions. In the presence of distortion not removed, the corresponding places are generally no longer the lines of this ideal model; applying a pixel threshold to the wrong geometry can reject physically correct matches.

- **CV-EPIPOLAIRE-002 –  pose and chirality**: The decomposition of an allowable essential provides several combinations of rotation and translation sign. Triangulating and then imposing positive depths in both cameras helps to choose a compatible solution, under sufficient noise and geometry. This selects a meaning, without measuring the norm of translation. In pure rotation, $t=0$ and $E=[t]_\times R$ cancels: the translation and the depths do not become observable by normalizing a vector from the noise. A very low parallax can produce a similar difficulty in practice. Always connect the scale to the measure that sets it and separate this problem from the selection of a pose among the candidates.

- **CV-EPIPOLAIRE-003 –  Write linear triangulation**: for a projection matrix $P$ whose rows are $P_1,P_2,P_3$ and an observation $(u,v)$, equations $(uP_3-P_1)X_h=0$ and $(vP_3-P_2)X_h=0$ constrain the homogeneous point $X_h\in\mathbb R^4$. Stacking them on multiple views produces a linear estimate, to be divided by its fourth component when it is valid. Observations and $P$ must both use ideal pixels, or both have compatible normalized coordinates. A nearly zero homogeneous component can indicate a point at a very great distance. A refinement of reprojection and controls of depth, parallax and visibility remain necessary; the linear solution does not certify the correspondence.

- **CV-EPIPOLAIRE-004 –  Why reverse depth helps**: for a depth of $Z>0$, posing $\rho=1/Z$ places the far points near zero instead of an immense value. In an ideal stereo, $\rho=d/(fB)$ depends linearly on the disparity $d$, while $Z=fB/d$ becomes very sensitive near zero. A small uncertainty of $\rho$ can therefore correspond to a huge uncertainty of $Z$. This reparameterization facilitates certain representations without creating parallax or making the distance known. It should not be used to present a point almost infinitely as a precise metric depth. If the errors are large, the linear propagation and a symmetrical interval on $Z$ may themselves become inadequate.

- **CV-EPIPOLAIRE-005 –  Origin of multiple solutions**: With three known 3D points and three unit sighting directions, P3P looks for their positive $\lambda_i$ distances to the camera. The cosine law imposes $\|X_i-X_j\|^2=\lambda_i^2+\lambda_j^2-2\lambda_i\lambda_j\cos\alpha_{ij}$, where $\alpha_{ij}$ is the angle between the rays. This nonlinear system can admit several triangles of compatible rays. An additional observation then serves to separate them, according to the function chosen. This geometric derivation explains why “minimum three” and “pose unique” are not equivalent. Almost collinear points, their uncertainties and the solutions behind the camera must be controlled before refinement on more matches.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) –  E/F, recoverPose and triangulatePoints; linear geometry deduced. View on 2026-10-30.
- [OpenCV 4.13, PnP](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html) –  pose computation methods and P3P; verified contract with Context7. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
