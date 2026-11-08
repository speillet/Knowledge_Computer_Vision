---
id: CV-STEREO
type: methode
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d06]
---
# Rectified stereo, SGM and depth

## Problem, data and assumptions

Estimate the depth from two calibrated images. Inputs: synchronized left/right views, rectification and baseline; output: disparity and depth with validity mask. The texture, the occlusion and the accuracy of the matches limit the reconstruction.

## Prerequisites and competencies

**Required prerequisites**: [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Rectification organizes research along epipolar lines. A matching cost compares candidates; SGM aggregates paths with variation penalties. SGBM from OpenCV is a variant to document, not all the details of the original article.

## Mathematics, conventions and units

Ideal horizontal rectified case with main points of the same abscissa and $d=x_g-x_d>0$: $Z=fB/d$, f and d in pixels, baseline B in meters and Z in meters. For small uncertainty, $\sigma_Z\approx fB\sigma_d/d^2$. Use the Q matrix for general rectified geometry. A fixed integer disparity SGBM OpenCV can be stored multiplied by 16: convert according to the contract before reprojection.

## Parameters and properties

Disparities range, block, penalties, left/right consistency and mask invalids. In this simplified case, $d\le0$ does not give a valid finite depth before. In the general case, use Q and matcher mask: the sign of disparity alone does not define validity, especially if the rectification shifts the main points. Repeated texture and glossy surfaces can produce a minimum of false cost.

## Cost and implementation

Resolution × search range × aggregation dominate time/memory. No StereoSGBM executed; parameters and formats were confronted with OpenCV 4.13.

## Evaluation and controlled variation

Analytical example: f=1000 px, B=0,2 m, d=20 px gives 10 m; d=10 px gives 20 m. At the same disparity error, the far depth is more sensitive. Measure over known distances and invalid regions.

## Failure modes and diagnosis

Overall Depths ×16: inspect disparity format. Object edge errors: distinguish occlusion from non-rectification. Bad result far does not prove a lack of network capacity.

## Alternatives and applications

Learned stereo, active sensor or monocular depth depending on accuracy, cost and conditions; a monocular prediction does not automatically have a reliable metric scale.

## Guided reasoning and proposed checks

These constructed cases develop disparity, depth uncertainty and rectified geometry. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-STEREO-001

**Question of work**: For horizontally rectified stereo with equal principal-point x-coordinates, f=1000 px, a 0.2 m baseline and left-minus-right disparity of 20 px, what depth is obtained?

**Reference Response**: 10 m by $Z=fB/d$.

**derivation of units**: the quotient $f/d$ is without a unit if the two quantities use the pixels of the same rectified grid; the result therefore retains the unit of the baseline. The difference in coordinates reflects the separation of the two rays for a given point. A small disparity here corresponds to a great depth.

**Example of check**: check a known remote target, then artificially double the value of the baseline in the calculation: the calculated depth would also double. This helps locate a scale error without changing the matcher. The simplified formula assumes the main points aligned as advertised and a valid physical disparity. A hidden region or a bad match can produce a positive number without proper depth. In more general rectified geometry, use the reprojection transformation and its conventions rather than applying this formula to any output called disparity.

### Case linked to CV-STEREO-004

**Question of work**: Does rectification guarantee a correct correspondence at every pixel?

**Reference Response**: No: it simplifies search geometry; texture, repetition and occlusion can still make matching ambiguous.

**What the correction changes**: reorganizes images to simplify geometry-enabled search locations. It does not create texture and does not make visible a hidden surface in one of the cameras. The search along a line can therefore still contain several candidates or no real match.

**Constructed example**: a uniform surface offers close costs for many disparities; a periodic texture can favor the bad period; at the edge of an object, a point can only be seen on one side. A regularization may select a value in these regions, but this value is not a new observation. Maintain validity information and test available consistency, and then evaluate on an independent reference. Distinguishing the density of the produced map and the amount of really reliable depth avoids interpreting any filled pixel as a measurement.

**Documentary reference for this pass**: [OpenCV 4.13, Depth Map from Stereo Images](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html), relationship depth – disparity and correspondence. The other developments are in the [flashcards](../61-stereo-profondeur.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-STEREO-001

**Situation**: For horizontally rectified stereo with equal principal-point x-coordinates, f=1000 px, a 0.2 m baseline and left-minus-right disparity of 20 px, what depth is obtained?

**Construction of triangles**: With horizontally separated centers of $B$, even focal length and even main abscissa $c_x$, the ideal projections are $x_g=fX/Z+c_x$ and $x_d=f(X-B)/Z+c_x$. The subtraction eliminates $X$ and gives $d=fB/Z$. If the main abscissas differ, it is $d-(c_{x,g}-c_{x,d})$ that enters into this simplified geometry. This derivation explains why using the corresponding rectified image/reprojection matrix torque is essential. The result $Z$ is the depth along the rectified optical axis; the Euclidean distance to the camera center is $\sqrt{X^2+Y^2+Z^2}$ and can be greater for an off-axis point.

### CV-STEREO-002

**Situation**: Why does stereo depth accuracy often deteriorate at long range?

**Propagation of several uncertainties**: for $Z=fB/d$ and small disturbances, $\delta Z/Z\simeq\delta f/f+\delta B/B-\delta d/d$. If these errors are independent and centered, the relative variances add up; otherwise their covariances count. A baseline bias thus produces a relative error of scale, while a fixed disparity bias further penalizes long distances. Almost $d=0$, linearization becomes fragile and a symmetrical distribution in disparity gives a very asymmetrical distribution in depth. Also evaluate the intervals in depth or use a depth inverse representation according to the estimator, instead of assuming constant Gaussian metric uncertainty.

### CV-STEREO-003

**Situation**: An SGBM reconstruction has the wrong scale despite good calibration. Which numerical convention should be checked?

**Order of operations**: Conceptually, retain the mask provided by the matcher's contract, convert the fixed disparity to real, then apply $[X_h,Y_h,Z_h,W_h]^T=Q[x,y,d,1]^T$ and divide by $W_h$ when the projection is valid. These are homogeneous coordinates, not yet meters before this division and the interpretation of the units of $Q$. Do not build the mask only after filling the holes: an interpolation can replace a sentinel with a plausible value. Keep the original measurement, its validity and any depth completed separate. Testing a known pixel makes it possible to distinguish storage factor, disparity convention, and baseline unit.

### CV-STEREO-004

**Situation**: Does rectification guarantee a correct correspondence at every pixel?

**Bidirectional verification built**: Set $d_g(x)=x_g-x_d$ and a positive straight disparity $d_d(x_d)=x_g-x_d$ for the same point. A consistent pair must check $|d_g(x)-d_d(x-d_g(x))|<\tau$, subject to interpolation and visibility. If the right field uses the opposite sign, the equation changes in sum: the conventions must be explicit. This test rejects some inconsistencies, but two false matches on a repetitive texture can remain mutually compatible. Geometric validation, the distinction between holes and regularized values, and an independent reference remain necessary. The threshold $\tau$ is in pixels of disparity of the grid considered.

**Passages consulted for these developments**: [OpenCV 4.13.0, stereo](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html), Basics, triangles and disparity; built-in uncertainty derivations and bidirectional testing.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-STEREO-002 — Small disparities produce asymmetric depth errors

Constructed case: with $fB=200$ px·m, disparity $2\pm0.5$ px maps to depths from 80 to about 133.3 m around a nominal 100 m. The interval is asymmetric because inversion is nonlinear. Near zero disparity, a first-order standard deviation can be misleading and invalid disparities must remain invalid rather than being clamped into apparently finite obstacles. Report depth availability together with error over the relevant range.

### CV-STEREO-004 — Rectification does not resolve an occluded pixel

A foreground edge can reveal background in only one camera. The corresponding pixel then has no valid partner, regardless of how accurately epipolar lines are horizontal. A left/right consistency check can flag some failures, but repeated texture can produce consistent wrong pairs. Evaluate occlusion and low-texture masks separately, and distinguish raw matched depth from any later interpolation or completion used to fill unavailable regions.

Consulted foundations: [OpenCV stereo](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html): rectified disparity/depth relationship; [OpenCV calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html): stereoRectify Q matrix and reprojectImageTo3D disparity scaling.

## Sources and flashcards

- [OpenCV StereoSGBM, description and compute](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html).
- [OpenCV reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Related flashcards](../61-stereo-profondeur.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
