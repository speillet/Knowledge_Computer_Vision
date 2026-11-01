# Review –  Hand-eye calibration –  solve AX = XB without mixing the coordinate frames –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HANDEYE-001 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Consistent case generator: specifies the existing question | Finished core preserved; 194 → 301 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HANDEYE-002 | Deduction/Assumption Cases; Documentary Context Below | Verification of matrices: specifies the existing question | Finished core preserved; 214 → 325 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HANDEYE-003 | Deduction/Assumption Cases; Documentary Context Below | Stacked system diagnostics: specifies the existing question | Finished core preserved; 202 → 307 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HANDEYE-004 | Deduction/Assumption Cases; Documentary Context Below | residual of measurable closure: specifies the existing question | Finished core preserved; 220 → 332 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-HANDEYE-005 | Deduction/Assumption Cases; Documentary Context Below | Explicit eye-to-hand chain: specifies the existing question | Finished core preserved; 217 → 325 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-HANDEYE](../../../vault/50-calibration-geometrie/references/57-calibration-hand-eye.md); [flashcards](../../../vault/50-calibration-geometrie/57-calibration-hand-eye.md). reference note modified before the flashcards.

- **CV-HANDEYE-001 –  Consistent Case Generator**: choose rigid transformations $X$ and $Y$, then several poses robot $G_i$. Define synthetic observations by $C_i=X^{-1}G_i^{-1}Y$. We then have exactly $G_iXC_i=Y$ and the derived relative movements satisfy $AX-XB=0$ to the nearest numerical rounding. Then introducing noise on the observations makes it possible to study the sensitivity, but this test first verifies the algebra and conventions. It does not prove that the chosen movements make $X$ identifiable. Use rotations around distinct axes and non-zero translations to avoid a test that would mask product inversions or non-commutativity.

- **CV-HANDEYE-002 –  Verification of matrices**: a rotation block must satisfy $R^TR\simeq I$ and $\det R\simeq1$; the last homogeneous line is $(0,0,0,1)$. These conditions control a rigid transformation, not its physical meaning. To reverse it, use $T^{-1}=[R^T,-R^Tt;0,1]$, never the only negation of $t$ when $R$ is non-trivial. Convert all the translations in the same unit before the estimation: mixing meters and millimeters does not correct by a rotation convention. Finally, to distinguish a rotation represented in matrix, axis-angle vector or quaternion; the order of the components and the angle units belong to the interface contract.

- **CV-HANDEYE-003 –  Diagnostic by stacked system**: after estimating $R_X$, stack the $R_{A_k}-I$ blocks to solve the translation. A small singular value of this matrix signals a direction where large variations in translation little change the equations. Its interpretation depends on the noise, the angles actually traveled and the units of the complete system; a simple number of conditions is not a physical certification. The rotation must also be observable, because its errors pass into the second member $R_Xt_{B_k}-t_{A_k}$. To estimate stability by resampling, select whole acquisitions or sequences rather than treating all their pairs as independent samples.

- **CV-HANDEYE-004 –  residual measurable closure**: between two reserved poses, form $E_{ij}=Y_j^{-1}Y_i$. The ideal is identity. Report the norm of its translation in the assembly unit and its angle of rotation, for example $\phi=\arccos(\operatorname{clip}((\operatorname{tr}R_E-1)/2,-1,1))$, in radians. Near digitally sensitive cases, a robust logarithmic representation is preferable. Do not add centimeters and degrees directly: a combined score requires scaling or explicit covariance. Compare these residuals according to speed and amplitude of rotation, then an error on the useful points, because the closure alone does not give the accuracy of the entire measuring chain.

- **CV-HANDEYE-005 –  Explicit eye-to-hand chain**: If the camera is fixed in the base and the calibration target is attached to the gripper, note $G_i={}^bT_{g_i}$, $C_i={}^cT_{t_i}$, $X={}^bT_c$ and $Y={}^gT_t$. We have $G_iY=XC_i$, so $G_i^{-1}XC_i=Y$ constant. The shape becomes that of a hand-eye chain using the inverted robot poses, under these precise conventions, and the unknown now corresponds to camera→base. The equation justifies adaptation; reversing only an old exit does not justify it. If the calibration target is not attached to the gripper, this constancy of $Y$ disappears and observations and unknowns must be reformulated before any resolution.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13.0, calibration hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) –  calibrateHandEye, coordinate frames, eye-in-hand and eye-to-hand strings and non-parallel axes; algebraic complements of the project. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
