# Review –  Calibration fisheye –  Angular projection and off-centre validation –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FISHEYE-001 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Local development: specifies the existing issue | Finished core preserved; 208 → 313 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FISHEYE-002 | Deduction/Assumption Cases; Documentary Context Below | Sensitivity of coefficients: specifies the existing question | Finished core preserved; 218 → 326 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FISHEYE-003 | Deduction/Assumption Cases; Documentary Context Below | Pixel Error and Angular Error: Specify the Existing Question | Finished core preserved; 209 → 312 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FISHEYE-004 | Deduction/Assumption Cases; Documentary Context Below | Output radius: specifies the existing question | Finished core preserved; 206 → 319 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FISHEYE-005 | Deduction/Assumption Cases; Documentary Context Below | Density of information: specifies the existing question | Finished core preserved; 204 → 309 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-FISHEYE](../../../vault/50-calibration-geometrie/references/56-calibration-fisheye.md); [flashcards](../../../vault/50-calibration-geometrie/56-calibration-fisheye.md). reference note modified before the flashcards.

- **CV-FISHEYE-001 –  Local development**: $\tan\theta=\theta+\theta^3/3+O(\theta^5)$. The apparent equality near the axis comes from the first common order; the relative deviation grows approximately as $\theta^2/3$ for small angles. This development is not a reliable approximation to use without check near 90°. To reverse a calibrated fisheye projection, you need to find the angle from the polynomial $\theta_d(\theta)$, then form a radius; we do not simply replace $r_d$ with a pinhole coordinate. Check that this function remains invertible in the exploited domain: parameters adjusted over a small region can produce undesirable behavior in extrapolation.

- **CV-FISHEYE-002 –  Sensitivity of coefficients**: in $\theta_d=\theta+\sum_{j=1}^4 k_j\theta^{2j+1}$, the derivative with respect to $k_j$ is $\theta^{2j+1}$. High-order terms therefore become very insensitive when all angles are small; thousands of center points can remain uninformative for $k_4$. This reading of the Jacobian explains the peripheral collection without prescribing a universal angle threshold. The high sensitivity at the edges is also not enough: the corners must be localizable and cover several directions and poses, in order to separate distortion, main center and orientation of the calibration target. The reserved residuals controls the generalization of the adjusted model.

- **CV-FISHEYE-003 –  Pixel Error and Angular Error**: breaking down the residual image $e$ in a unitary radial direction $n_r$ and a tangent $n_t$ gives $e_r=n_r^Te$ and $e_t=n_t^Te$. Analyzing these components by crown, with headcount and distributions, reveals biases that the average norm mixes. In a single radial cut, $\delta r\simeq f\,(d\theta_d/d\theta)\delta\theta$: a pixel does not represent everywhere the same angular error if the derivative varies. Metric conversion still depends on the scene and its depth. This analysis is a diagnosis, not a certain identification of the optical or localization cause.

- **CV-FISHEYE-004 –  Output radius**: for rectification to a pinhole model, a homogeneous pixel $\tilde u'$ gives a radius $q'=K_{\mathrm{new}}^{-1}\tilde u'$ in the rectified coordinate frame. If $R_{\mathrm{rect}}$ sends the raw camera rays to this coordinate frame, the corresponding raw ray is proportional to $R_{\mathrm{rect}}^Tq'$. The fisheye projection of this ray provides the position to be sampled in the source image: it is a reverse map construction. This transformation is usually unrefined. After an output crop, also adapt the main center; after a resize, adapt focal lengths and coordinates according to the pixel convention chosen. Pixels without a valid source do not create any geometric measurements.

- **CV-FISHEYE-005 –  Density of information**: Keeping more field in a set number of pixels can reduce sampling of certain directions. The map derivative, a Jacobian $2\times2$ between output and source coordinates, locally describes stretching and anisotropy. When many output pixels interpolate almost the same source samples, their number does not measure an optical resolution gain. To compare two values of `balance`, keep the same calibrated parameters and measure the task on the common valid region, and then separately report the additional field. This protocol prevents a change in pixel population from being taken for an improvement in accuracy.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13.0, fisheye](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html) –  Detailed Description, angular polynomial and rectification; sensitivities and protocols deduced by the project. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
