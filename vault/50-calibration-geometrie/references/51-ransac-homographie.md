---
id: CV-HOMOGRAPHIE
type: methode
domaine: d05
poles: [B, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: []
revision: 7
tags: [cv/d05, geometrie, ransac, matching]
---
# RANSAC for homography estimation

## Problem, contract and prerequisites

Estimate a projective transformation between two image planes despite false matches. A homography describes in particular a plane observed from two positions, or a pure rotation of camera in the ideal perspective model. A translation in front of a scene with relief usually introduces parallax, incompatible with a single global homography. [OpenCV, geometry][tutorial]

Inputs: $n$ pairs of 2D dots in pixels in source and destination coordinate frames, with known units and preprocessing. Outputs: matrix $H$ and mask of inliers according to the residual retained. Highly distorted images may require correction before this projective model.

**Required prerequisites**: [Homogeneous points and residuals](../../01-Parcours/Pre-requis.md). **Connexions**: [SIFT](../../40-features-matching/references/41-sift.md), [ORB](../../40-features-matching/references/42-orb.md), [calibration](52-calibration-zhang.md). **Competences**: estimate, interpret consensus, diagnose degenerations.

## Intuition and procedure

The least squares on all matches can be dominated by the outliers. RANSAC proposes small hypotheses and looks for the one that explains a consensus. It is necessary to distinguish the robust algorithm from the chosen model: replacing the model with a fundamental or a pose changes the problem and the minimum size. [Fischler and Bolles, §II][ransac]

Pseudocode **not executed**, educational variant:

```text
repeat to budget or stop criterion: draw four pairs in general position estimate a candidate homography calculate the residual of each pair in the coordinate frame destination retain the consensus associated with the selected threshold and score re-estimate on the inliers of the best candidate recalculate and inspect the residuals and coverage
```

The implementation can use other scores, guided draws, and refinements. Do not assign to any `findHomography` call the properties of another variant.

## Model and residual

$$
\tilde x'_i\sim H\tilde x_i,\qquad
e_i=\|x'_i-\pi(H\tilde x_i)\|_2.
$$

$x_i,x'_i\in\mathbb R^2$ are Euclidean points; $\tilde x_i$ their homogeneous representation; $\pi$ divided by the third component. $H\in\mathbb R^{3\times3}$, invertible, is defined at a non-zero factor, i.e. eight degrees of freedom. $e_i$ is here a distance **in destination pixels**. A point is inlier if its residual meets the chosen threshold; specify the inequality of the implementation if the border value counts. [OpenCV `findHomography`][api]

Four pairs in the general position are sufficient for the minimum case: no collinear triplet in each minimum set. Points almost aligned or grouped on a small area can make the estimate ill-conditioned. Normalizing coordinates improves linear computation; this does not repair degeneration.

## Random sampling budget and parameters

$$
N=\left\lceil\frac{\log(1-p)}{\log(1-w^m)}\right\rceil.
$$

$p\in(0,1)$ is the nominal probability of having drawn at least one fully inlier sample, $w\in(0,1)$ the assumed proportion of inliers, and $m=4$ the minimum size for this model. With independent draws modeled as well, a sample is all-inlier with probability $w^m$. For $w=0,5$, $p=0,99$, the budget is 72; at $w=0,8$, it is 9. Results executed in `examples/pilot_math.py`.

This is not the probability that the final transformation is physically correct. Bad $w$, degenerate samples and repetitive structure can invalidate the simplified interpretation. [Fischler and Bolles, §II][ransac]

Too wide a threshold absorbs errors; too low, it excludes observations compatible with their noise. Changing the resolution requires reconsidering a threshold in pixels. Confidence, budget and score do not replace the check of the model and spatial distribution.

## Cost, implementation and evaluation

The naive evaluation of $N$ candidates on $n$ pairs has a cost of the order of $Nn$ residuals, to which are added estimation and refinement. Adaptive shutdowns change that cost. Upstream filtering and a better inlier proportion can help.

Extract **Illustrative not executed**, OpenCV 4.13:

```python
H, inliers = cv.findHomography(src_xy, dst_xy, cv.RANSAC, 3.0)
# Check that H/inliers exist, then inspect held-out points and the relevant image region.
```

`src_xy` and `dst_xy` contain the pairs in their respective coordinate frames; 3,0 is an illustrative threshold in destination pixels, not a recommendation. The call alone does not attest to geometric quality. [API][api]

**Proposed analytical baseline, not executed here**: Known transformation of points in a plane. Observe residual, proportion of inliers and error on unused points. **Proposed variation, not executed on images**: gradually add outliers and then a second depth under translation. Prediction: The first factor requires more draws; the second can make the model false. The rate of inliers does not alone distinguish these two situations.

## Diagnosis and industrial decision-making

| Symptom | Assumptions to distinguish | Validation |
| --- | --- | --- |
| Excellent consensus on a small logo, corners projected away | Extrapolation, misallocated points | inlier map, reserved points on the periphery, sensitivity to subsamples |
| residuals opposites between first and background | Parallax, several plans | Color the residuals by depth/zone; compare a suitable multiview model |
| Results change significantly between tests | Low proportion of inliers, degeneration, short budget | Log seed/variant, distribution of points and budgets |

To register a planar target, a homography is a reasonable hypothesis to test. To locate a camera in a known 3D scene, examine PnP; for two views of an unknown 3D scene, examine epipolar geometry and pose. Calibration, pose and registration meet distinct objectives.

## Guided reasoning and proposed checks

These built cases develop successful sampling, coverage and model validity. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-HOMOGRAPHIE-001

**Question of work**: When is a single global homography an appropriate model for relating two images, and which change usually causes it to fail?

**Reference Response**: suitable for points of the same plane, or pure camera rotation in the ideal perspective model. A translation in front of different depths usually creates a parallax incompatible with a single global model.

**Constructed example**: for a rigid flat label, its points can follow a same projective transformation between two shots, even if the bottom is at another depth. Accepting this homography for the label does not allow it to be extended to the bottom.

**check model**: Display vectors of residuals by region. If the errors are structured according to the depth under translation, adding robust draws does not create the missing 3D model. If they are rather random and located on a few pairs, outliers or a bad location remain plausible. The model decision therefore precedes the consensus threshold setting and refers to the area where the alignment will be used.

### Case linked to CV-HOMOGRAPHIE-007

**Question of work**: In a panorama captured with camera translation, nearby and distant points have systematically different residuals. What should be tested before making RANSAC more tolerant?

**Reference Response**: test a parallax due to the different depths, therefore the inadequacy of a global homography. Review the residuals by zone/depth and capture geometry before changing the threshold.

**Why does relief matter?**: Under camera translation, the apparent displacement depends in particular on the depth. Near and far points may require different deformations, while a global homography imposes a unique relationship. A consensus dominated by the background can thus leave a nearby object visibly split.

**Proposed ablation**: select separately matches on each plane, compare their models and check the crossed residuals. If two local models explain different groups, this supports the parallax hypothesis without proving that all associations are correct. Then choose a capture or a model adapted to the product. Expanding the threshold only mixes more groups in the same category of inliers and can hide the structure of the error.

**Documentary reference for this pass**: [Fischler and Bolles 1981](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf), §II, consensus and sampling. The other developments are in the [flashcards](../51-ransac-homographie.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-HOMOGRAPHIE-001

**Situation**: When is a single global homography an appropriate model for relating two images, and which change usually causes it to fail?

**Regaining dependence on the plan**: In the coordinate frame of the first camera, let's assume the $n^TX=d$ plan, with $d\ne0$, and the camera change $X'=RX+t$. As $X$ is located on this plane, we can write $X'=(R+tn^T/d)X$, hence $H\sim K'(R+tn^T/d)K^{-1}$ for the ideal pixels. The sign changes if the equation of the plan is defined otherwise: announce the convention. If $t=0$, the plan term disappears and $H\sim K'RK^{-1}$ no longer depends on depth. This derivation explains the case of pure rotation and why the same movement with translation does not give a common homography to all planes.

### CV-HOMOGRAPHIE-002

**Situation**: Why are four point pairs not always sufficient to estimate a homography despite its eight degrees of freedom?

**Link to DLT Rank**: Each pair brings two lines in a homogeneous system of nine coefficients. For four pairs, a $8\times9$ matrix must have rank eight in order to leave a single solution direction, corresponding to the projective scale. Dependent constraints enlarge the core: several homographs then satisfy the points provided. With more noise pairs, we are looking for a direction of small residual, but spectral separation and coverage remain important. An admissible homography must also be invertible; checking the behavior of the homogeneous division in the useful region avoids accepting a numerical matrix whose certain projections become infinite or extremely sensitive.

### CV-HOMOGRAPHIE-003

**Situation**: Describe one RANSAC iteration for homography estimation and the useful step after selecting the best consensus.

**Pedagogical pseudocode, not executed** :

```text
best_model = absent for each allowed test: choose four distinct pairs reject a minimal degenerate geometry estimate H and reject invalid projections measure all residuals and apply the advertised score retain H if the score improves the best refine on the inliers, then recalculate the mask validate cover and reserved observations, otherwise refuse
```

Absentee treatment is a normal exit if no permissible assumption satisfies the contract. The mask can change after refinement: keeping the original model without recalculation can mix two different states of the estimate. The order of the data, the possible seed and the budget are used to reproduce a result, without replacing its physical validation.

### CV-HOMOGRAPHIE-004

**Situation**: For homography estimation with an assumed inlier proportion $w=0,5$, why are 72 draws targeted for nominal confidence 0.99, and what does this confidence mean?

**Correcting the interpretation of a finished print**: If the set contains $I$ real inliers among $n$ pairs and if we draw four distinct indices uniformly, the exact all-inlier probability of a draw is $q=\binom I4/\binom n4$ when $I\ge4$. The term $w^4$ is a practical approximation, or the result of a model with replacement. If successive draws are independent, the confidence of at least one success is $1-(1-q)^N$. Repeating the same sample or using guided prints changes the analysis. Finally, “all-in” does not mean “sufficiently well conditioned”: an admissible and informative geometry remains necessary. These details are probability deductions, not a new warranty on RANSAC.

### CV-HOMOGRAPHIE-005

**Situation**: A three-pixel RANSAC threshold worked before downsampling. Why can retaining it without reconsideration change inlier selection?

**Local spread of uncertainty**: for $e=q-\pi(H\tilde p)$ and a $H$ considered fixed, independent noises of covariance $C_p,C_q$ give approximately $C_e=C_q+J_HC_pJ_H^T$, with $J_H$ the warp Jacobian at the source point. The reprojection noise can therefore vary depending on the position and deformation, even if the source noise is isotropic. A single threshold in pixels is a simplification to be validated; a whitened score uses a covariance consistent with the residual. If $H$ is estimated with these same points, this elementary covariance does not describe all the post-adjustment uncertainty. After an anisotropic resize, the two directions do not necessarily follow the same factor.

### CV-HOMOGRAPHIE-006

**Situation**: A homography has 90% inliers concentrated in one corner but projects the opposite edge poorly. Which checks distinguish consensus quality from registration quality?

**Observe the area of validity**: distinguish between interpolation error in the middle of constraints and extrapolation error outside. A small variation in projective coefficients can leave a concentrated area almost unchanged, but move a distant corner strongly, especially if the homogeneous denominator becomes small. Project a mesh of the useful region to inspect continuity, orientation and complete deformation, in addition to the four corners. This check is a proposal of the project: a visually plausible deformation is not a proof of precision. An independent reference near the future measurement zone brings a constraint that the number of inliers of the initial corner alone does not provide.

### CV-HOMOGRAPHIE-007

**Situation**: In a panorama captured with camera translation, nearby and distant points have systematically different residuals. What should be tested before making RANSAC more tolerant?

**Link to the disparity**: In a simple example of lateral translation between parallel cameras, the image displacement varies as $fB/Z$, with focal length $f$ in pixels, translation $B$ and depth $Z$ in the same unit. Two planes of depth $Z_1,Z_2$ therefore require displacements whose difference is $fB(1/Z_1-1/Z_2)$. This constructed case explains why the foreground can split up while the bottom aligns well. A local deformation or multi-plane assembly can reduce the visual artifact, but does not automatically provide a single metric reconstruction. Choose capture, model and success criterion according to the actual measurement or final image expected.

**Passages consulted for these developments**: [OpenCV 4.13, Homography](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html), Basic theory and Demo 3/5; plane and rotation models; [Fischler and Bolles 1981](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf), §II, consensus; combinatorial precisions deduced by the project.

## Sources and flashcards

- [Fischler and Bolles, 1981][ransac]: §II, consensus and nominal budget.
- [Tutoriel officiel homographie][tutorial]: geometry and conditions.
- [OpenCV 4.13 `findHomography`][api]: residual and implementation parameters.
- [flashcards](../51-ransac-homographie.md).

[ransac]: https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf
[tutorial]: https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html
[api]: https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html
