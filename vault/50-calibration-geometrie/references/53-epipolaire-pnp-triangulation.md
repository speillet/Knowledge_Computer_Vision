---
id: CV-EPIPOLAIRE
type: methode
domaine: d05
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 5
prerequis: ["CV-SE3", "CV-ZHANG"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Epipolar geometry, PnP and triangulation

## Problem, data and assumptions

Distinguish constraints between two views, pose from known points 3D and reconstruction of points. Coordinates must be distortion corrected or processed by a consistent model; specify coordinate frame and point scale.

## Prerequisites and competencies

**Required prerequisites**: [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md); [CV-ZHANG](52-calibration-zhang.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

The fundamental connects pixel points; the essential exploits the intrinsics. PnP estimates the pose object→camera from 3D – 2D. Triangulation looks for a point 3D explaining several rays; low parallax and noise can make its depth very uncertain.

## Mathematics, conventions and units

For $X_2=RX_1+t$, $E=[t]_\times R$ and $x_2^TEx_1=0$ in normalized coordinates. In ideal pixels $F=K_2^{-T}EK_1^{-1}$. The direction t from two monocular views does not have a metric scale. PnP returns t in the unit of points 3D; the camera has center $-R^Tt$.

## Parameters and properties

Minimum, ambiguities and refinement depend on the variant. P3P can give several solutions; in OpenCV 4.13.0, `solvePnP(..., SOLVEPNP_P3P)` requires four points, while `solveP3P` accepts three matches and returns the candidate solutions. Check cheirality, parallax and residuals, not the only number of points.

## Cost and implementation

RANSAC, solver and downstream optimization have different costs. No OpenCV calls executed; `solvePnP` conventions have been verified in the 4.13 documentation.

## Evaluation and controlled variation

Analytical case: two almost parallel rays give a sensitive depth to a small angular error. Proposed variation: modify baseline or distance while retaining image noise; report uncertainty and error 3D on reference.

## Failure modes and diagnosis

Huge depth with small residual: examine parallax, scale, cheirality and bad association. pose reversed: check world→camera and axes.

## Alternatives and applications

Homography for a shot; PnP if a 3D map is known; two views then reconstruction if the map is unknown. Do not interpret any translation as metric.

## Guided reasoning and proposed checks

These constructed cases develop epipolarity, pose and depth distinguished by their contract. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-EPIPOLAIRE-001

**Question of work**: Which coordinate conventions distinguish the essential and fundamental matrices?

**Reference Response**: E acts on ideal normalized camera coordinates; F on ideal pixels with absorbed intrinsics.

**Consistent writing**: for $X_2=RX_1+t$, the essential is $E=[t]_\times R$. The $x_2^TEx_1=0$ constraint is written with ideal normalized coordinates; in ideal pixels, $F=K_2^{-T}EK_1^{-1}$ absorbs both intrinsic matrices. The homogeneous symbol also implies a standardization convention.

**Example of check**: If the dots have been undistorted to normalized coordinates, re-inject them into a fundamental associated with other pixel matrices mixes two contracts. Check a known point and its epipolar location before interpreting the score. An algebraic scalar product close to zero is not directly a Euclidean error in pixels: the choice of the residual and its threshold must be explained. The chosen matrix describes the relationship between views; it does not implicitly correct all distortions or preprocessing transformations applied afterwards.

### Case linked to CV-EPIPOLAIRE-005

**Question of work**: Why is the slogan “P3P means calling solvePnP with any three points” misleading?

**Reference Response**: The problem may have several solutions, configurations may be degenerated, and the selected API may request a fourth point.

**Difference Between Problem and Function**: A minimal formulation indicates how many matches can be sufficient under geometric assumptions. A function can add an observation to select a solution, return multiple assumptions, or impose other data constraints. Its name therefore does not replace the reading of the contract of the variant used.

**Proposed Protocol**: Record method and version, check number and configuration of points, and then review the poses candidates with additional observations. check residuals, visibility and plausibility of the movement in the announced coordinate frames. Degenerate or nearly degenerate points may remain uninformative even if the requested number is satisfied. In a critical application for accuracy, also use reserved points and appropriate refinement. This reasoning avoids confusing algebraic minimum, successful API call and pose actually validated in the real scene.

**Documentary reference for this pass**: [OpenCV 4.13, Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), pinhole model, essential matrices, solvePnP and triangulation. The other developments are in the [flashcards](../53-epipolaire-pnp-triangulation.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-EPIPOLAIRE-001

**Situation**: Which coordinate conventions distinguish the essential and fundamental matrices?

**Constraint at a distance**: A point $\tilde p_1$ defines a line $l_2=F\tilde p_1$ in the 2 image. If $l_2=(a,b,c)$, the distance of $(u,v)$ to this line is $|au+bv+c|/\sqrt{a^2+b^2}$ when the denominator is non-zero. This normalization removes the arbitrary scale from the right, unlike the only product $\tilde p_2^TF\tilde p_1$. A Sampson residual or a symmetric error responds to other approximations and conventions. In the presence of distortion not removed, the corresponding places are generally no longer the lines of this ideal model; applying a pixel threshold to the wrong geometry can reject physically correct matches.

### CV-EPIPOLAIRE-002

**Situation**: Does a pose recovered from a monocular essential matrix directly provide the distance between cameras in meters?

**pose and cheirality**: The decomposition of an allowable essential provides several combinations of rotation and translation sign. Triangulating and then imposing positive depths in both cameras helps to choose a compatible solution, when noise levels and scene geometry permit. This selects a meaning, without measuring the norm of translation. In pure rotation, $t=0$ and $E=[t]_\times R$ cancels: the translation and the depths do not become observable by normalizing a vector from the noise. A very low parallax can produce a similar difficulty in practice. Always connect the scale to the measure that sets it and separate this problem from the selection of a pose among the candidates.

### CV-EPIPOLAIRE-003

**Situation**: Do PnP and triangulation solve for the same unknown?

**Write Linear Triangulation**: for a projection matrix $P$ whose rows are $P_1,P_2,P_3$ and an observation $(u,v)$, equations $(uP_3-P_1)X_h=0$ and $(vP_3-P_2)X_h=0$ constrain the homogeneous point $X_h\in\mathbb R^4$. Stacking them on multiple views produces a linear estimate, to be divided by its fourth component when it is valid. Observations and $P$ must both use ideal pixels, or both have compatible normalized coordinates. A nearly zero homogeneous component can indicate a point at a very great distance. A refinement of reprojection and controls of depth, parallax and visibility remain necessary; the linear solution does not certify the correspondence.

### CV-EPIPOLAIRE-004

**Situation**: Why can a triangulated point have low reprojection error but highly uncertain depth?

**Why reverse depth helps**: for a depth of $Z>0$, posing $\rho=1/Z$ places the far points near zero instead of an immense value. In an ideal stereo, $\rho=d/(fB)$ depends linearly on the disparity $d$, while $Z=fB/d$ becomes very sensitive near zero. A small uncertainty of $\rho$ can therefore correspond to a huge uncertainty of $Z$. This reparameterization facilitates certain representations without creating parallax or making the distance known. It should not be used to present a point almost infinitely as a precise metric depth. If the errors are large, the linear propagation and a symmetrical interval on $Z$ may themselves become inadequate.

### CV-EPIPOLAIRE-005

**Situation**: Why is the slogan “P3P means calling solvePnP with any three points” misleading?

**Origin of multiple solutions**: With three known 3D points and three unit sighting directions, P3P looks for their positive $\lambda_i$ distances to the camera. The cosine law imposes $\|X_i-X_j\|^2=\lambda_i^2+\lambda_j^2-2\lambda_i\lambda_j\cos\alpha_{ij}$, where $\alpha_{ij}$ is the angle between the rays. This nonlinear system can admit several triangles of compatible rays. An additional observation then serves to separate them, according to the function chosen. This geometric derivation explains why “minimum three” and “pose unique” are not equivalent. Almost collinear points, their uncertainties and the solutions behind the camera must be controlled before refinement on more matches.

**Passages consulted for these developments**: [OpenCV 4.13, calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), E/F, recoverPose and triangulatePoints; linear geometry deduced; [OpenCV 4.13, PnP](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html), pose computation methods and P3P; verified contract with Context7.

## Sources and flashcards

- [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [OpenCV solvePnP, conventions and variants](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
- [Related flashcards](../53-epipolaire-pnp-triangulation.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
