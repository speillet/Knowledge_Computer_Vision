# Flashcards — Epipolar geometry, PnP and triangulation

reference note: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-EPIPOLAIRE-001

Objective: distinguish E and F. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-001
Question: Which coordinate conventions distinguish the essential and fundamental matrices?
Reponse: **Expected answer**: E acts on ideal normalized camera coordinates; F on ideal pixels with absorbed intrinsics.

**Further explanation**: Correct or model distortion; use the correct matrices and direction of pose announced.

**Consistent writing**: for $X_2=RX_1+t$, the essential is $E=[t]_\times R$. The $x_2^TEx_1=0$ constraint is written with ideal normalized coordinates; in ideal pixels, $F=K_2^{-T}EK_1^{-1}$ absorbs both intrinsic matrices. The homogeneous symbol also implies a standardization convention.

**Example of check**: If the dots have been undistorted to normalized coordinates, re-inject them into a fundamental associated with other pixel matrices mixes two contracts. Check a known point and its epipolar location before interpreting the score. An algebraic scalar product close to zero is not directly a Euclidean error in pixels: the choice of the residual and its threshold must be explained. The chosen matrix describes the relationship between views; it does not implicitly correct all distortions or preprocessing transformations applied afterwards.

**Constraint at a distance**: A point $\tilde p_1$ defines a line $l_2=F\tilde p_1$ in the 2 image. If $l_2=(a,b,c)$, the distance of $(u,v)$ to this line is $|au+bv+c|/\sqrt{a^2+b^2}$ when the denominator is non-zero. This normalization removes the arbitrary scale from the right, unlike the only product $\tilde p_2^TF\tilde p_1$. A Sampson residual or a symmetric error responds to other approximations and conventions. In the presence of distortion not removed, the corresponding places are generally no longer the lines of this ideal model; applying a pixel threshold to the wrong geometry can reject physically correct matches.

**Blocking errors**: Apply E directly to raw pixels as a universal rule.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Full reference]] ; [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; [OpenCV solvePnP, conventions and variants](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-EPIPOLAIRE-001 provenance::agent pole::B pole::C
END

## CV-EPIPOLAIRE-002

Objective: Interpret the translation scale. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-002
Question: Does a pose recovered from a monocular essential matrix directly provide the distance between cameras in meters?
Reponse: **Expected answer**: No: the two views alone give a direction and a reconstruction to a scale in the general case.

**Further explanation**: An additional metric measurement, a known baseline or a sensor can fix the scale under its assumptions.

**Ambiguity of scale**: multiplying all the distances of the reconstruction and the translation between cameras by the same positive constant can leave the projections identical. Monocular images therefore do not distinguish these scenes solely by this geometry. A normalization of the translation vector chooses a convenient representation of its direction.

**Constructed example**: Two reconstructions separated by a factor of ten can explain the same pixels. Arbitrary interpretation of the unit norm as a meter gives arbitrary speed and dimensions. A known baseline, an object of known dimension or a sufficiently informative inertial fusion can provide an additional constraint, depending on its model. Also check parallax, pose ambiguities and quality of matches: setting a scale does not automatically improve the other components of the estimate. The metric validation must cite the actual source of this information.

**pose and cheirality**: The decomposition of an allowable essential provides several combinations of rotation and translation sign. Triangulating and then imposing positive depths in both cameras helps to choose a compatible solution, when noise levels and scene geometry permit. This selects a meaning, without measuring the norm of translation. In pure rotation, $t=0$ and $E=[t]_\times R$ cancels: the translation and the depths do not become observable by normalizing a vector from the noise. A very low parallax can produce a similar difficulty in practice. Always connect the scale to the measure that sets it and separate this problem from the selection of a pose among the candidates.

**Blocking errors**: Present the unit norm of t as one meter.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Full reference]] ; [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; [OpenCV solvePnP, conventions and variants](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
Tags: cv::pilote cv::d05 famille::comprehension cv_id::CV-EPIPOLAIRE-002 provenance::agent pole::B pole::C
END

## CV-EPIPOLAIRE-003

Objective: choose PnP or triangulation. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-003
Question: Do PnP and triangulation solve for the same unknown?
Reponse: **Expected answer**: PnP estimates the pose from 3D points and 2D observations; triangulation estimates the points from several poses/views.

**Further explanation**: Both can be linked in SfM and refined by BA; gauges and units must remain consistent.

**Mental picture of the unknowns**: PnP uses a map of 3D points already expressed in a coordinate frame, and then looks at how to project them into the camera. Triangulation assumes views and their known poses, and then looks for a point that is compatible with the observed rays. The bundle adjustment can then adjust these two types of variables together.

**Constructed example**: Locate a camera in front of a CAD part with identified points is a 3D – 2D problem. Rebuilding the corner of a room from two calibrated cameras is a triangulation problem. In both cases, a bad association can produce a digital solution with no physical value. Keep units of known points, direction of poses and visibility checks. An SfM string can alternate operations, but that doesn’t make their inputs or ambiguities interchangeable.

**Write Linear Triangulation**: for a projection matrix $P$ whose rows are $P_1,P_2,P_3$ and an observation $(u,v)$, equations $(uP_3-P_1)X_h=0$ and $(vP_3-P_2)X_h=0$ constrain the homogeneous point $X_h\in\mathbb R^4$. Stacking them on multiple views produces a linear estimate, to be divided by its fourth component when it is valid. Observations and $P$ must both use ideal pixels, or both have compatible normalized coordinates. A nearly zero homogeneous component can indicate a point at a very great distance. A refinement of reprojection and controls of depth, parallax and visibility remain necessary; the linear solution does not certify the correspondence.

**Blocking errors**: Reverse entries and unknowns without reporting it.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Full reference]] ; [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; [OpenCV solvePnP, conventions and variants](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-EPIPOLAIRE-003 provenance::agent pole::B pole::C
END

## CV-EPIPOLAIRE-004

Objective: detect a low parallax. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-004
Question: Why can a triangulated point have low reprojection error but highly uncertain depth?
Reponse: **Expected answer**: With almost parallel rays, several large depths produce close projections.

**Further explanation**: Measure parallax angle, sensitivity and reference 3D; a better baseline can add missing information.

**Intuition of conditioning**: Two rays that intersect at a very small angle define their intersection in depth in a fragile way. A small angular variation, coming from the noise of localization, moves the point a lot while modifying little its projections. This mechanism is analogous to a direction of parameters with little stress in a linear system.

**Protocol built**: preserve image noise and compare several known distances or baselines. Measure depth error, angle between radii and residuals separately. Reject or report points almost without parallax rather than consider them reliable because their reprojection is good. A larger baseline can provide information, but also make matches more difficult or cause occlusionss, so its choice is a system compromise. Also check that the dots are in front of the cameras and that the scale used is actually metric.

**Why reverse depth helps**: for a depth of $Z>0$, posing $\rho=1/Z$ places the far points near zero instead of an immense value. In an ideal stereo, $\rho=d/(fB)$ depends linearly on the disparity $d$, while $Z=fB/d$ becomes very sensitive near zero. A small uncertainty of $\rho$ can therefore correspond to a huge uncertainty of $Z$. This reparameterization facilitates certain representations without creating parallax or making the distance known. It should not be used to present a point almost infinitely as a precise metric depth. If the errors are large, the linear propagation and a symmetrical interval on $Z$ may themselves become inadequate.

**Blocking errors**: Deduct the 3D accuracy from the single residual pixel.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Full reference]]; [OpenCV 4.13.0, decomposeEssentialMat, recoverPose, solveP3P and triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html); low parallax sensitivity: geometric deduction of the project; [OpenCV 4.13, PnP, pose computation methods and P3P; verified contract with Context7](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html), consult the 2026-10-30.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-EPIPOLAIRE-004 provenance::agent pole::B pole::C
END

## CV-EPIPOLAIRE-005

Objective: meet the minimum variant of pose. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-005
Question: Why is the slogan “P3P means calling solvePnP with any three points” misleading?
Reponse: **Expected answer**: The problem may have several solutions, configurations may be degenerated, and the selected API may request a fourth point.

**Further explanation**: Name the variant, check its contract and then refine and test the cheirality.

**Difference Between Problem and Function**: A minimal formulation indicates how many matches can be sufficient under geometric assumptions. A function can add an observation to select a solution, return multiple assumptions, or impose other data constraints. Its name therefore does not replace the reading of the contract of the variant used.

**Proposed Protocol**: Record method and version, check number and configuration of points, and then review the poses candidates with additional observations. check residuals, visibility and plausibility of the movement in the announced coordinate frames. Degenerate or nearly degenerate points may remain uninformative even if the requested number is satisfied. In a critical application for accuracy, also use reserved points and appropriate refinement. This reasoning avoids confusing algebraic minimum, successful API call and pose actually validated in the real scene.

**Origin of multiple solutions**: With three known 3D points and three unit sighting directions, P3P looks for their positive $\lambda_i$ distances to the camera. The cosine law imposes $\|X_i-X_j\|^2=\lambda_i^2+\lambda_j^2-2\lambda_i\lambda_j\cos\alpha_{ij}$, where $\alpha_{ij}$ is the angle between the rays. This nonlinear system can admit several triangles of compatible rays. An additional observation then serves to separate them, according to the function chosen. This geometric derivation explains why “minimum three” and “pose unique” are not equivalent. Almost collinear points, their uncertainties and the solutions behind the camera must be controlled before refinement on more matches.

**Blocking errors**: Confounding theoretical minimum and API contract.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Full reference]] ; [OpenCV 4.13.0, solvePnP, pose computation methods and P3P](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html) ; [OpenCV 4.13.0, decomposeEssentialMat, recoverPose, solveP3P and triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-EPIPOLAIRE-005 provenance::agent pole::B pole::C
END
