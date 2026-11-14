# Flashcards — RANSAC for homography estimation

reference note: [[50-calibration-geometrie/references/51-ransac-homographie|RANSAC/homographie]]. Source: Agent.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-HOMOGRAPHIE-001

Objective: Choose a geometric model. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-001
Question: When is a single global homography an appropriate model for relating two images, and which change usually causes it to fail?
Reponse: **Expected answer**: suitable for points of the same plane, or pure camera rotation in the ideal perspective model. A translation in front of different depths usually creates a parallax incompatible with a single global model.

**Further explanation**: The sensor, the distortion and the preprocessing must be consistent with this model. A homography of a particular plane can remain valid in a 3D scene without describing the other points. Depending on the need, examine epipolar model, pose or several planes.

**Constructed example**: for a rigid flat label, its points can follow the same projective transformation between two shots, even if the background is at another depth. Accepting this homography for the label does not allow it to be extended to the background.

**Model check**: Display residual vectors by region. If the errors are structured according to depth under translation, adding robust draws does not create the missing 3D model. If they are rather random and located on a few pairs, outliers or a poor localization remain plausible. The model decision therefore precedes the setting of the consensus threshold and refers to the area where the alignment will be used.

**Recovering the dependence on the plane**: In the coordinate frame of the first camera, assume the plane $n^TX=d$, with $d\ne0$, and the camera change $X'=RX+t$. As $X$ lies on this plane, we can write $X'=(R+tn^T/d)X$, hence $H\sim K'(R+tn^T/d)K^{-1}$ for ideal (distortion-free) pixels. The sign changes if the plane equation is defined otherwise: state the convention. If $t=0$, the plane term disappears and $H\sim K'RK^{-1}$ no longer depends on depth. This derivation explains the case of pure rotation and why the same motion with translation does not give a homography common to all planes.

**Plane height changes the valid transform**: Constructed inspection case: a homography is calibrated on a conveyor plane while a raised component is imaged from a translated viewpoint. Its top surface need not follow the conveyor homography because it lies on a different plane. Residuals grouped by object height can distinguish this model mismatch from random matching noise. The correct intervention depends on whether the product needs planar position, top-surface measurement or full 3D geometry.

**Blocking errors**: Saying that a homography always links any two photos, or that more RANSAC draws remove the parallax.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|reference note]] ; [OpenCV 4.13.0 homography tutorial source, Basic theory (plane, two views, rotating camera), Demo 3 (homography from camera displacement)](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/features2d/homography/homography.markdown). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-HOMOGRAPHIE-001 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-002

Objective: Relate degrees of freedom and degeneracy. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-002
Question: Why are four point pairs not always sufficient to estimate a homography despite its eight degrees of freedom?
Reponse: **Expected answer**: Four pairs provide the minimum number of constraints only in general position. A collinear or otherwise degenerate configuration does not determine the model; almost degenerate, it can make it unstable.

**Further explanation**: $H$ is a $3\times3$ matrix with one factor. In a minimal set, avoid collinear triplets in each image. Coordinate normalization improves numerical conditioning without recreating absent constraints. Also examine the coverage to avoid a fragile extrapolation.

**Why counting is not enough**: Constraints must be independent. Several points on the same line inform this line, but do not freely fix the behavior of the plane in the other directions. Almost collinear points can give a numerical solution that is very sensitive to noise.

**Proposed verification**: visualize the points before the solver, examine the rank after normalization and check the projection on held-out observations away from the minimal set. Adding more concentrated points to the same area can keep a poor extrapolation. The algebraic minimum explains when a solution is possible; the capture protocol must still make this solution informative and stable for use.

**Link to the DLT rank**: Each pair contributes two rows to a homogeneous system in nine coefficients. For four pairs, the $8\times9$ matrix must have rank eight to leave a single solution direction, corresponding to the projective scale. Dependent constraints enlarge the null space: several homographies then satisfy the given points. With more, noisy pairs, one looks for a direction of small residual, but spectral separation and coverage remain important. An admissible homography must also be invertible; checking the behavior of the homogeneous division in the useful region avoids accepting a numerical matrix some of whose projections become infinite or extremely sensitive.

**General position is more than a point count**: Four distinct source points can still be collinear, leaving transformations away from that line unconstrained. Nearly collinear points can yield a numerical solution whose extrapolation is highly unstable. Check independence in both images and inspect normalized system rank. A proposed perturbation check moves observations by a small plausible localization error and examines transferred points across the useful region; point count alone does not predict the effect.

**Blocking errors**: Counting nine independent degrees of freedom, or claiming that any four matches guarantee a usable estimate.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|reference note]]; [OpenCV 4.13.0, fundam.cpp L74–L188: rejection of collinear minimal samples and normalized DLT](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fundam.cpp); [OpenCV 4.13.0, calib3d.hpp L782–L853, findHomography: four-pair subsets, collinear subsets discarded](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-HOMOGRAPHIE-002 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-003

Objective: Rebuild a robust iteration. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-003
Question: Describe one RANSAC iteration for homography estimation and the useful step after selecting the best consensus.
Reponse: **Expected answer**: draw a non-degenerate minimal set, estimate a candidate, calculate a residual on all pairs, count or score the inliers according to an explicit threshold. After selection, re-estimate on the inliers and check the residuals.

**Further explanation**: Small samples keep outliers out of a candidate estimate instead of including all of them in an initial fit. The score, the residual, the sampling and the refinement vary between variants. Check the result on the useful area and on unused points; a consensus step does not prove the validity of the physical model.

**Role of each operation**: The small sample avoids having all outliers enter the solver immediately; the global score compares how well the candidates explain the data; the refit uses more compatible measurements to reduce dependence on the initial sample alone.

**Example of a limit**: Regular repetition can provide a large set of false but consistent pairs. The best consensus according to the score can then be the wrong physical alignment. After refinement, check coverage, direction of the warp and independent points. Also record the variant, threshold and budget to reproduce a failure. This decomposition distinguishes too few draws, bad geometry and scene ambiguity, instead of attributing any error to the randomness of the draws.

**Pedagogical pseudocode, not executed**:

```text
best_model = none
for each allowed trial:
    choose four distinct pairs; reject a degenerate minimal geometry
    estimate H; reject invalid projections
    measure all residuals and apply the declared score
    keep H if the score improves on the best
refine on the inliers, then recompute the mask
validate coverage and held-out observations, otherwise refuse
```

Returning no model is a normal outcome when no admissible hypothesis satisfies the contract. The mask can change after refinement: keeping the original mask without recomputation mixes two different states of the estimate. The order of the data, the possible seed and the budget serve to reproduce a result, without replacing its physical validation.

**Refinement should refresh acceptance evidence**: After refitting on an initial consensus, recompute every residual with the refined model and the same declared threshold. The inlier mask can change because the fitted transformation changed. Preserve the model used to generate each mask so diagnostics remain reproducible. A larger consensus is useful evidence only when it retains spatial support and independent geometric accuracy; a coherent wrong periodic alignment can also increase its inlier count.

**Blocking errors**: Evaluating the candidate only on the four points drawn, or treating any consensus as ground truth.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|reference note]] ; [Fischler and Bolles 1981, §II paradigm and §II.C final consensus](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf); [OpenCV 4.13.0, fundam.cpp L415–L452: refit, Levenberg–Marquardt and recomputed mask](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fundam.cpp). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d05 famille::algorithme cv_id::CV-HOMOGRAPHIE-003 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-004

Objective: interpret the nominal budget of RANSAC. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-004
Question: For homography estimation with an assumed inlier proportion $w=0.5$, why are 72 draws targeted for nominal confidence 0.99, and what does this confidence mean?
Reponse: **Expected answer**: A four-point draw is all-inlier with probability $w^4$. Under the independent model, requiring $1-(1-w^4)^N\ge0.99$ gives
$$N=\left\lceil\frac{\log(1-0.99)}{\log(1-0.5^4)}\right\rceil=72.$$ Confidence concerns the existence of at least one all-inlier draw, not the physical truth of the final result.

**Further explanation**: an all-inlier sample may remain degenerate; $w$ may be misestimated and draw hypotheses imperfect. The budget is nominal. A better proportion of inliers can greatly reduce the cost: with 0.8 in the same calculation, nine draws are enough.

**Probabilistic reading**: The opposite event is not to draw any all-inlier samples, with nominal probability $(1-w^4)^N$. The logarithm reflects the decline of this event with the budget. A drop in the inlier proportion can therefore cause the number of attempts to explode. Implementations differ in details: OpenCV 4.13 rounds the same ratio (71 draws here), recomputes it from the best inlier ratio seen so far and never exceeds `maxIters` (2000 by default).

**Proposed practical decision**: Improving upstream matches can reduce this cost, but too strict filtering can also degrade their coverage. Both effects must be measured. A consistent repetitive structure or degenerated sample is not part of the simplified promise of the calculation: even a large budget does not guarantee to distinguish a bad physical hypothesis. The stopping confidence and the validation of the registration are two different pieces of information.

**Exact probability for a finite set**: If the set contains $I$ true inliers among $n$ pairs and four distinct indices are drawn uniformly, the exact all-inlier probability of a draw is $q=\binom I4/\binom n4$ when $I\ge4$. The term $w^4$ is a practical approximation, or the result of a model with replacement. If successive draws are independent, the confidence of at least one success is $1-(1-q)^N$. Repeating the same sample or using guided sampling changes the analysis. Finally, “all-inlier” does not mean “sufficiently well conditioned”: an admissible and informative geometry remains necessary. These details are probability deductions, not a new guarantee on RANSAC.

**Nominal confidence is sensitive to the inlier estimate**: For four-point samples and confidence 0.99, an assumed inlier rate of 0.5 gives 72 draws, whereas 0.3 requires about 567. The budget can therefore be badly understated when the inlier fraction is guessed optimistically. Correlated matches and degenerate all-inlier samples further break the simple success model. Record a maximum iteration budget and a failure outcome rather than presenting the requested confidence as a probability that the returned homography is correct.

**Blocking errors**: Announcing a 99% probability that the estimated homography is correct, without the assumptions of the calculation.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|reference note]] ; [Fischler and Bolles 1981, §II.B number of trials, k = log(1 − z)/log(1 − b)](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf); [OpenCV 4.13.0, ptsetreg.cpp L55–L76: adaptive iteration count](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/ptsetreg.cpp). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-HOMOGRAPHIE-004 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-005

Objective: Interpret the unit of a residual threshold. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-005
Question: A three-pixel RANSAC threshold worked before downsampling. Why can retaining it without reconsideration change inlier selection?
Reponse: **Expected answer**: The direct residual is measured in the destination coordinate frame: $e=\|x'-\pi(H\tilde x)\|_2$. A reduction in resolution changes the scale of coordinates, errors and possibly location noise; three pixels no longer have the same meaning.

**Further explanation**: keep the transformation between coordinate frames, review the threshold in relation to the actual uncertainty and verify residuals and success rate. In the ideal uniform resize of factor $a$, the same geometric errors are multiplied by $a$, but re-extracting the features can also change their noise. A broader threshold may mask an erroneous model.

**Example of scale**: After a uniform resize by one half, a geometric deviation of four pixels in the initial image ideally becomes two pixels in the new one. Keeping three pixels becomes more permissive for this physical gap. But an extraction redone at a lower resolution can modify the location of the features; the simple multiplication of the threshold is therefore only a reasoned starting point.

**Proposed validation**: carry some known matches through the coordinate frame transformation and compare their residuals before re-running the detection. This isolates the coordinate transformation from the quality of the new features. Then review the threshold and measure of success on the useful area, clearly announcing the units.

**Local propagation of uncertainty**: for $e=q-\pi(H\tilde p)$ and a $H$ considered fixed, independent noises of covariance $C_p,C_q$ give approximately $C_e=C_q+J_HC_pJ_H^T$, with $J_H$ the warp Jacobian at the source point. The reprojection noise can therefore vary with position and deformation, even if the source noise is isotropic. A single threshold in pixels is a simplification to be validated; a whitened score uses a covariance consistent with the residual. If $H$ is estimated from these same points, this elementary covariance does not describe all the post-adjustment uncertainty. After an anisotropic resize, the two directions do not necessarily follow the same factor.

**Anisotropic resizing changes a circular gate**: Under pixel scaling $D=\operatorname{diag}(a_x,a_y)$, a residual vector becomes $e^{\prime}=De$. If $a_x\ne a_y$, an old circular Euclidean threshold maps to an ellipse, not another circle obtained by one scalar factor. Propagating the residual covariance gives $C^{\prime}=DC D^T$ and preserves a correctly transformed Mahalanobis gate. This constructed relation explains why merely multiplying a pixel threshold by an average resize factor changes selection.

**Blocking errors**: Treating the threshold as a unitless quantity, or assuming that changing the threshold repairs any parallax.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|reference note]]; [OpenCV 4.13.0, calib3d.hpp L794–L797: ransacReprojThreshold in pixels of the destination, outlier if the transfer error exceeds it](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp); [OpenCV 4.13.0, ptsetreg.cpp L86–L100: inlier test on the squared error](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/ptsetreg.cpp). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-HOMOGRAPHIE-005 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-006

Objective: Diagnose an extrapolated model. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-006
Question: A homography has 90% inliers concentrated in one corner but projects the opposite edge poorly. Which checks distinguish consensus quality from registration quality?
Reponse: **Expected answer**: Examine spatial coverage, conditioning, and error on held-out points spread across the useful area. Consensus can be good locally while constraining extrapolation poorly.

**Further explanation**: compare estimates on subsets, check that points are not nearly collinear and that they lie on the model plane, and then look for informative observations elsewhere. Report the region in which the accuracy is established. Increasing the threshold or number of draws does not provide the missing spatial constraints.

**Intuition of extrapolation**: Several close transformations can almost coincide on a small neighborhood and diverge away from it. The points of consensus therefore establish a local precision; the percentage of inliers does not describe the extent in which the parameters are well constrained.

**Constructed experiment**: re-estimate with different subsets of the concentrated area, and then project the same peripheral corners. If these corners vary greatly despite weak local residuals, look for constraints elsewhere or limit the use to the validated region. Better normalization improves computation, without creating additional spatial support. The report should specify region of confidence and observed errors, rather than announcing an overall quality over the entire image.

**Observe the area of validity**: distinguish between interpolation error within the constrained region and extrapolation error outside it. A small variation in projective coefficients can leave a concentrated area almost unchanged, but move a distant corner strongly, especially if the homogeneous denominator becomes small. Project a mesh of the useful region to inspect continuity, orientation and complete deformation, in addition to the four corners. This check is a proposal of the project: a visually plausible deformation is not a proof of precision. An independent reference near the future measurement zone brings a constraint that the number of inliers of the initial corner alone does not provide.

**Projective division amplifies extrapolation**: For $u=(h_1^T\tilde x)/(h_3^T\tilde x)$, small denominator values amplify changes in both coordinates and fitted coefficients. A homography may therefore be stable on the observed patch yet predict extreme positions farther away. Check denominator behavior and held-out transfer throughout the intended ROI. This is especially important when a small corner of a label supplies most matches but the measurement concerns the opposite edge.

**Blocking errors**: Declaring the registration validated on the inlier percentage alone, or automatically concluding a descriptor bug.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|reference note]]; [OpenCV 4.13.0, calib3d.hpp L782–L853: findHomography model and transfer error](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp); coverage scenario, extrapolation calculation and diagnostic protocol proposed by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-HOMOGRAPHIE-006 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-007

Objective: Explain a model incompatibility. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-007
Question: In a panorama captured with camera translation, nearby and distant points have systematically different residuals. What should be tested before making RANSAC more tolerant?
Reponse: **Expected answer**: test a parallax due to the different depths, therefore the inadequacy of a global homography. Review the residuals by zone/depth and capture geometry before changing the threshold.

**Further explanation**: A single dominant plane can explain part of the image and leave the rest incompatible. Depending on the product, change the capture to a rotation around the optical center, limit the area to the useful plane or choose a suitable reconstruction/modeling. A large threshold can only label poorly explained points as "inliers".

**Why does relief matter?**: Under camera translation, the apparent displacement depends in particular on the depth. Near and far points may require different deformations, while a global homography imposes a unique relationship. A consensus dominated by the background can thus leave a nearby object visibly split.

**Proposed ablation**: select separately matches on each plane, compare their models and check the crossed residuals. If two local models explain different groups, this supports the parallax hypothesis without proving that all associations are correct. Then choose a capture or a model adapted to the product. Expanding the threshold only mixes more groups in the same category of inliers and can hide the structure of the error.

**Link to the disparity**: In a simple example of lateral translation between parallel cameras, the image displacement varies as $fB/Z$, with focal length $f$ in pixels, translation $B$ and depth $Z$ in the same unit. Two planes of depth $Z_1,Z_2$ therefore require displacements whose difference is $fB(1/Z_1-1/Z_2)$. This constructed case explains why the foreground can split up while the background aligns well. A local deformation or a multi-plane composition can reduce the visual artifact, but does not automatically provide a single metric reconstruction. Choose capture, model and success criterion according to the actual measurement or final image expected.

**Parallax has a predictable depth trend**: Constructed case: with $f=800$ px and a 0.1 m lateral baseline, ideal disparity is 40 px at 2 m and 8 px at 10 m. A single depth-independent translation cannot align both. A homography fitting one plane leaves structured residuals elsewhere. Plotting residual direction and magnitude against scene regions or independent depth supports testing parallax before raising the threshold and absorbing a systematic model error as noise.

**Blocking errors**: Promising that a sufficient RANSAC budget will remove relief effects under translation.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|reference note]] ; [OpenCV 4.13.0 homography tutorial source, Basic theory and Demo 5 (rotating camera)](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/features2d/homography/homography.markdown). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-HOMOGRAPHIE-007 provenance::agent pole::B pole::E
END
