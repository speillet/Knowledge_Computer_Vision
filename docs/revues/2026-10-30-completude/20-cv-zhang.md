# Review –  Camera calibration on calibration target –  Zhang's method –  2026-10-30

## Overview

7 enriched flashcards; reference note scope of revision 4 to 5, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ZHANG-001 | Deduction/Assumption Cases; Documentary Context Below | Which data raises which unknowns: specifies the existing question | Finished core preserved; 225 → 338 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ZHANG-002 | Deduction/Assumption Cases; Documentary Context Below | Place distortion in the calculation: specifies the existing question | Finished core preserved; 241 → 363 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ZHANG-003 | Deduction/Assumption Cases; Documentary Context Below | Switching constraints to poses: specifies the existing question | Finished core preserved; 229 → 343 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ZHANG-004 | Deduction/Assumption Cases; Documentary Context Below | Precisely define the RMS: specifies the existing question | Finished core preserved; 230 → 343 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ZHANG-005 | Deduction/Assumption Cases; Documentary Context Below | Pixel centers case: specifies the existing question | Finished core preserved; 217 → 335 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ZHANG-006 | Deduction/Assumption Cases; Documentary Context Below | Linking acquisition and information: specifies the existing question | Finished core preserved; 227 → 337 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ZHANG-007 | Deduction/Assumption Cases; Documentary Context Below | Moving from calibration to measurement on a plan: specifies the existing question | Finished core preserved; 216 → 337 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-ZHANG](../../../vault/50-calibration-geometrie/references/52-calibration-zhang.md); [flashcards](../../../vault/50-calibration-geometrie/52-calibration-zhang.md). reference note modified before the flashcards.

- **CV-ZHANG-001 –  What data raises what unknowns**: A calibration target plane of known geometry provides particular 3D coordinates, e.g. $(X,Y,0)$, and their 2D observations on several views. The calibration looks for common intrinsics and a pose per view; a new estimate of pose can then reuse these fixed intrinsics. A free homography between two images does not necessarily exploit the metric size of the squares and can align the plane without lifting the same unknowns. If the calibration target is printed at a bad uniform scale, the estimated translations follow this erroneous unit, while the pixel adjustment can remain almost identical. Metric validation therefore requires information independent of this alignment alone.

- **CV-ZHANG-002 –  Place distortion in calculation**: after $X_c=RX_w+t$, place $x=X_c/Z_c$, $y=Y_c/Z_c$ and $r^2=x^2+y^2$. A simple polynomial radial model uses $x_d=x(1+k_1r^2+k_2r^4+\cdots)$ and the same for $y_d$; tangential terms are other contributions. The distorted coordinates are then converted into pixels by the intrinsics. The radial coefficients of this convention act on normalized coordinates, not directly over a distance in pixels. This separation explains why a crop changes the main point but not mechanically these coefficients. The validity of the division by $Z_c$ and the visibility of the point must also be checked; a projected number does not imply that a point is in front of the camera.

- **CV-ZHANG-003 –  Switch from constraints to poses**: The linear constraints on the symmetric matrix $B$ are stacked to estimate its six elements to within a scale. After recovering an allowable $K$, columns $K^{-1}h_1$ and $K^{-1}h_2$ give directions of rotation to be normalized with a common scale; the third direction stems from their vector product. Noise generally prevents the resulting matrix from being exactly orthonormal: it must be brought back to $SO(3)$ before the joint refinement. This step is an initialization, not a final estimate of all the distortion. Views repeating the same orientation can leave the constraints almost dependent even if their individual homographies estimate themselves very well.

- **CV-ZHANG-004 –  Precisely define the RMS**: with $N$ observations 2D and residuals $e_i=(e_{xi},e_{yi})$, $RMS_{point}=\sqrt{\sum_i(e_{xi}^2+e_{yi}^2)/N}$. A mean per coordinate uses $2N$ at the denominator and is therefore $RMS_{point}/\sqrt2$. The average of the norms and the average of the RMS per view are still other statistics. A score announced without denominator can therefore be incomparable despite the same word RMS. Also present the residual maps and the quantiles, then a validation on views and reserved points. When the pose of a reserved view is to be estimated, separate the points that serve that pose from those that evaluate the set parameters.

- **CV-ZHANG-005 –  Case of pixel centers**: If the tool sets the resize to $u'=a(u+1/2)-1/2$, the transformation also contains the translation $(a-1)/2$; the main point follows the same relationship before the crop. The $u'=au$ simple formula corresponds to another contract. These expressions are analytical cases: they do not describe all libraries. For a different scaling on both axes, multiply the relevant lines of $K$ respectively via the full pixel affine. The factor of the last homogeneous coordinate remains fixed at one per convention. Testing a round trip of multiple points is safer than inferring the affine from the final size of the array alone.

- **CV-ZHANG-006 –  Link acquisition and information**: If two columns of the Jacobian of the residuals are almost dependent, a variation of one parameter can compensate that of another. Small singular values and covariance correlations signal this coupling in the local approximation. Adding views that excite new directions can separate them better than adding twenty copies of a front view. Covering the edge helps constrain terms that grow with distance to the center, but requires well-located corners in that area. A flexible calibration target or systematically biased corners can produce a consistent fit to the wrong model: digital stability and physical adequacy are controlled separately.

- **CV-ZHANG-007 –  Pass calibration on a plan**: with center world camera $C$, radius world direction $d$ and known plane $n^TX=h$, the intersection is $X=C+\lambda d$, where $\lambda=(h-n^TC)/(n^Td)$ if the denominator is non-zero. This geometry shows that a metric measurement also requires the plane or depth of the surface: intrinsics alone are not enough. Near a radius parallel to the plane, the intersection becomes very sensitive to noise. Propagating calibration, edge location and flatness errors in product tolerance, and then comparing to an independent reference. This calculation assumes a known flat surface and a properly dedistorted projection, without certifying a relief measurement.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Zhang, TR98-71](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) –  §§2 – 4 and Annex C, stresses, poses and degenerations. View on 2026-10-30.
- [OpenCV 4.13, Camera Calibration](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) –  projection and distortion model; Context7 verification. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
