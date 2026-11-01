# Review –  RANSAC applied to a homography –  2026-10-30

## Overview

7 enriched flashcards; reference note scope of revision 4 to 5, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HOMOGRAPHIE-001 | Deduction/Assumption Cases; Documentary Context Below | Finding Dependence on the Plan: Specifying the Existing Question | Finished core preserved; 218 → 336 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HOMOGRAPHIE-002 | Deduction/Assumption Cases; Documentary Context Below | Link to DLT rank: clarifies existing question | Finished core preserved; 207 → 315 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HOMOGRAPHIE-003 | Deduction/Assumption Cases; Documentary Context Below | Pedagogical pseudocode, not executed: specifies the existing question | Finished core preserved; 229 → 344 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HOMOGRAPHIE-004 | Deduction/Assumption Cases; Documentary Context Below | Correcting the interpretation of a finished print run: specifies the existing question | Finished core preserved; 239 → 357 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HOMOGRAPHIE-005 | Deduction/Assumption Cases; Documentary Context Below | Local spread of uncertainty: specifies the existing question | Finished core preserved; 232 → 344 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HOMOGRAPHIE-006 | Deduction/Assumption Cases; Documentary Context Below | Observe the area of validity: specifies the existing question | Finished core preserved; 210 → 318 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HOMOGRAPHIE-007 | Deduction/Assumption Cases; Documentary Context Below | Link to disparity: specifies the existing question | Finished core preserved; 221 → 331 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-HOMOGRAPHIE](../../../vault/50-calibration-geometrie/references/51-ransac-homographie.md); [flashcards](../../../vault/50-calibration-geometrie/51-ransac-homographie.md). reference note modified before the flashcards.

- **CV-HOMOGRAPHIE-001 –  Finding Dependence on the Plan**: In the coordinate frame of the first camera, let's assume the $n^TX=d$ plan, with $d\ne0$, and the camera change $X'=RX+t$. As $X$ is located on this plane, we can write $X'=(R+tn^T/d)X$, hence $H\sim K'(R+tn^T/d)K^{-1}$ for the ideal pixels. The sign changes if the equation of the plan is defined otherwise: announce the convention. If $t=0$, the plan term disappears and $H\sim K'RK^{-1}$ no longer depends on depth. This derivation explains the case of pure rotation and why the same movement with translation does not give a common homography to all planes.

- **CV-HOMOGRAPHIE-002 –  Link to DLT rank**: Each pair brings two lines in a homogeneous system of nine coefficients. For four pairs, a $8\times9$ matrix must have rank eight in order to leave a single solution direction, corresponding to the projective scale. Dependent constraints enlarge the core: several homographs then satisfy the points provided. With more noise pairs, we are looking for a direction of small residual, but spectral separation and coverage remain important. An admissible homography must also be invertible; checking the behavior of the homogeneous division in the useful region avoids accepting a numerical matrix whose certain projections become infinite or extremely sensitive.

- **CV-HOMOGRAPHIE-003 –  Educational pseudocode, not executed** : **Pedagogical pseudocode, not executed** :

```text
best_model = absent for each allowed test: choose four distinct pairs reject a minimal degenerate geometry estimate H and reject invalid projections measure all residuals and apply the advertised score retain H if the score improves the best refine on the inliers, then recalculate the mask validate cover and reserved observations, otherwise refuse
```

Absentee treatment is a normal exit if no permissible assumption satisfies the contract. The mask can change after refinement: keeping the original model without recalculation can mix two different states of the estimate. The order of the data, the possible seed and the budget are used to reproduce a result, without replacing its physical validation.

- **CV-HOMOGRAPHIE-004 –  Correct the interpretation of a finished print**: If the set contains $I$ real inliers among $n$ pairs and if we draw four distinct indices uniformly, the exact all-inlier probability of a draw is $q=\binom I4/\binom n4$ when $I\ge4$. The term $w^4$ is a practical approximation, or the result of a model with replacement. If successive draws are independent, the confidence of at least one success is $1-(1-q)^N$. Repeating the same sample or using guided prints changes the analysis. Finally, “all-in” does not mean “sufficiently well conditioned”: an admissible and informative geometry remains necessary. These details are probability deductions, not a new warranty on RANSAC.

- **CV-HOMOGRAPHIE-005 –  Local spread of uncertainty**: for $e=q-\pi(H\tilde p)$ and a $H$ considered fixed, independent noises of covariance $C_p,C_q$ give approximately $C_e=C_q+J_HC_pJ_H^T$, with $J_H$ the warp Jacobian at the source point. The reprojection noise can therefore vary depending on the position and deformation, even if the source noise is isotropic. A single threshold in pixels is a simplification to be validated; a whitened score uses a covariance consistent with the residual. If $H$ is estimated with these same points, this elementary covariance does not describe all the post-adjustment uncertainty. After an anisotropic resize, the two directions do not necessarily follow the same factor.

- **CV-HOMOGRAPHIE-006 –  Observe the area of validity**: distinguish between interpolation error in the middle of constraints and extrapolation error outside. A small variation in projective coefficients can leave a concentrated area almost unchanged, but move a distant corner strongly, especially if the homogeneous denominator becomes small. Project a mesh of the useful region to inspect continuity, orientation and complete deformation, in addition to the four corners. This check is a proposal of the project: a visually plausible deformation is not a proof of precision. An independent reference near the future measurement zone brings a constraint that the number of inliers of the initial corner alone does not provide.

- **CV-HOMOGRAPHIE-007 –  Link to disparity**: In a simple example of lateral translation between parallel cameras, the image displacement varies as $fB/Z$, with focal length $f$ in pixels, translation $B$ and depth $Z$ in the same unit. Two planes of depth $Z_1,Z_2$ therefore require displacements whose difference is $fB(1/Z_1-1/Z_2)$. This constructed case explains why the foreground can split up while the bottom aligns well. A local deformation or multi-plane assembly can reduce the visual artifact, but does not automatically provide a single metric reconstruction. Choose capture, model and success criterion according to the actual measurement or final image expected.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, Homography](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html) –  Basic theory and Demo 3/5; plan and rotation models. View on 2026-10-30.
- [Fischler and Bolles 1981](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf) –  §II, consensus; combinatorial precisions deduced by the project. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
