---
id: CV-FISHEYE
type: methode
domaine: d05
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-ZHANG", "CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Fisheye calibration — angular projection and off-center validation

## Prerequisites and competencies

**Required prerequisites**: [CV-ZHANG](52-calibration-zhang.md), [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md). **Target competencies**: distinguish fisheye and pinhole projection; design wide-angle calibration views; locate a camera model defect; propagate the contract after rectification; interpret the rectified field parameter. Related notions remain alternatives, not implicit dependencies.

## Problem and data contract

Calibrate a wide-angle camera when the selected projection model must represent a strong peripheral deformation. Inputs: 3D/2D matches of calibration target, physical dimensions, resolution and optical model; outputs: intrinsics, distortion coefficients and poses. Keep the distinction between raw fisheye image and rectified image. A wide angle does not automatically impose a particular model: compare models on reserved observations.

## Mechanism and mathematics

In the model OpenCV fisheye 4.13, for a camera point $(X,Y,Z)$ with $Z>0$, pose $a=X/Z$, $b=Y/Z$, $r=\sqrt{a^2+b^2}$ and $\theta=\arctan r$. The distorted angle is $\theta_d=\theta(1+k_1\theta^2+k_2\theta^4+k_3\theta^6+k_4\theta^8)$. The normalized coordinates are $x_d=(\theta_d/r)a$, $y_d=(\theta_d/r)b$, with continuous limit in the center. The angles are in radians, the normalized coordinates and coefficients without unit; $u=f_x(x_d+\alpha y_d)+c_x$, $v=f_yy_d+c_y$, with focal lengths and center in pixels and skew $\alpha$ without unit. Even if the $k_i$ are zero, the projection remains angular: $r_d=\theta$, not $r_d=\tan\theta$.

## Acquisition, parameters and limitations

Calibrate by varying the inclination, distance and coverage of the field, especially the edges. Views close to the center do not constrain the peripheral distortion. Setting or estimating certain parameters is not trivial: a free coefficient can absorb a defect of calibration target, a blur or a pose little constraint. The four fisheye coefficients are not the first four Brown – Conrady coefficients of the pinhole model. Keep units of calibration target, direction of poses, resolution and mechanical stability.

## Cost and rectification

Optimization depends on views, points and parameters. For video, you can calculate a rectification map and then apply it to frames; it must be recalculated if the geometry or resolution changes. The `balance` parameter of the new OpenCV matrix exchanges conserved field and borders, without improving the already estimated physical parameters. Use the corrected image projection matrix for the calculations that follow, and take into account invalid pixels and interpolation. API checked with Context7; no real camera calibration executed.

## Evaluation and controlled variation

Proposed baseline: Pinhole model with distortion and even learning dataset. Variation: fisheye model, with comparable constraints. Evaluate residuals per radius and pose on out-of-the-way views; check a useful geometric measurement, not just a global RMS. Analytical example, without additional distortion: at $\theta=60°$, a focal length of 300 px gives an angular radius of 314,16 px against 519,62 px in pinhole. This calculation explains why undoing the coefficients does not convert to each other.

## Diagnosis and alternatives

A low medium RMS with large residuals edges calls for a spatial map of errors, inspection of corners and new peripheral views. A visually “straightened” image does not prove metric accuracy. For an omnidirectional or non-central device, compare another camera model rather than arbitrarily multiplying the coefficients. The projection contract and the observed region limit the conclusions.

## Guided reasoning and proposed checks

These constructed cases develop angular coverage and projection model compatibility. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-FISHEYE-001

**Question of work**: In OpenCV fisheye, does setting all four distortion coefficients to zero recover pinhole projection? Explain using an off-axis ray.

**Reference Response**: No: the normalized radius is then $r_d=\theta$, while the pinhole gives $r=\tan\theta$, with $\theta$ the angle at the optical center in radians. The projections coincide only approximately near the axis.

**Why the center is cheating**: near zero, $\tan\theta$ is close to $\theta$. The two models may therefore appear similar on a small central region. The deviation grows off-axis; zero coefficients do not mean "no difference with the pinhole", but no further correction to the chosen angular model.

**check**: project some known rays, including a sufficiently oblique one, with the two models in the same conventions and units. Then compare to the reserved observations of the real camera. A visually plausible image does not separate models on their peripheral accuracy. The coefficients and matrix of each model must remain associated with the image and projection function that interprets them.

### Case linked to CV-FISHEYE-005

**Question of work**: Changing OpenCV's balance parameter reveals more of the scene but adds borders. Is the camera better calibrated?

**Reference Response**: No: `balance` changes the choice of output projection and field compromise, not the physical parameters already estimated. Compare useful field, local resolution and valid pixels with the same calibration.

**Interpretation of Compromise**: An output projection may favor a framing that fills the rectangle or a wider field with invalid areas. These choices change the amount of information available and its local resolution, without changing the observations used to estimate the camera.

**Proposed evaluation**: Compare outputs on the same calibration by reporting valid mask, useful field and task error. For a measurement near a border, the interpolation and low density of observations can count more than the total number of pixels displayed. The output geometry must be propagated to the following algorithms. A change in presentation can therefore help a product without constituting an improvement in physical calibration.

**Documentary reference for this pass**: [OpenCV 4.13, Fisheye camera model](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html), equations in theta, coefficients and calibration functions. The other developments are in the [flashcards](../56-calibration-fisheye.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-FISHEYE-001

**Situation**: In OpenCV fisheye, does setting all four distortion coefficients to zero recover pinhole projection? Explain using an off-axis ray.

**Local development**: $\tan\theta=\theta+\theta^3/3+O(\theta^5)$. The apparent equality near the axis comes from the first common order; the relative deviation grows approximately as $\theta^2/3$ for small angles. This development is not a reliable approximation to use without check near 90°. To reverse a calibrated fisheye projection, you need to find the angle from the polynomial $\theta_d(\theta)$, then form a radius; we do not simply replace $r_d$ with a pinhole coordinate. Check that this function remains invertible in the exploited domain: parameters adjusted over a small region can produce undesirable behavior in extrapolation.

### CV-FISHEYE-002

**Situation**: Which acquisitions should be added when a wide-angle calibration uses many views concentrated near the image center?

**Sensitivity of coefficients**: in $\theta_d=\theta+\sum_{j=1}^4 k_j\theta^{2j+1}$, the derivative with respect to $k_j$ is $\theta^{2j+1}$. High-order terms therefore become very insensitive when all angles are small; thousands of center points can remain uninformative for $k_4$. This reading of the Jacobian explains the peripheral collection without prescribing a universal angle threshold. The high sensitivity at the edges is also not enough: the corners must be localizable and cover several directions and poses, in order to separate distortion, main center and orientation of the calibration target. The reserved residuals controls the generalization of the adjusted model.

### CV-FISHEYE-003

**Situation**: A fisheye calibration has low overall reprojection RMS, but measurements near the edges are wrong. What should be checked?

**Pixel Error and Angular Error**: breaking down the residual image $e$ in a unitary radial direction $n_r$ and a tangent $n_t$ gives $e_r=n_r^Te$ and $e_t=n_t^Te$. Analyzing these components by crown, with headcount and distributions, reveals biases that the average norm mixes. In a single radial cut, $\delta r\simeq f\,(d\theta_d/d\theta)\delta\theta$: a pixel does not represent everywhere the same angular error if the derivative varies. Metric conversion still depends on the scene and its depth. This analysis is a diagnosis, not a certain identification of the optical or localization cause.

### CV-FISHEYE-004

**Situation**: After remapping a fisheye image into a rectified image, which calibration should be used to reconstruct rays or estimate pose?

**Radius of exit**: for rectification to a pinhole model, a homogeneous pixel $\tilde u'$ gives a radius $q'=K_{\mathrm{new}}^{-1}\tilde u'$ in the rectified coordinate frame. If $R_{\mathrm{rect}}$ sends the raw camera rays to this coordinate frame, the corresponding raw ray is proportional to $R_{\mathrm{rect}}^Tq'$. The fisheye projection of this ray provides the position to be sampled in the source image: it is a reverse map construction. This transformation is usually unrefined. After an output crop, also adapt the main center; after a resize, adapt focal lengths and coordinates according to the pixel convention chosen. Pixels without a valid source do not create any geometric measurements.

### CV-FISHEYE-005

**Situation**: Changing OpenCV's balance parameter reveals more of the scene but adds borders. Is the camera better calibrated?

**Density of information**: Keeping more field in a set number of pixels can reduce sampling of certain directions. The map derivative, a Jacobian $2\times2$ between output and source coordinates, locally describes stretching and anisotropy. When many output pixels interpolate almost the same source samples, their number does not measure an optical resolution gain. To compare two values of `balance`, keep the same calibrated parameters and measure the task on the common valid region, and then separately report the additional field. This protocol prevents a change in pixel population from being taken for an improvement in accuracy.

**Passages consulted for these developments**: [OpenCV 4.13.0, fisheye](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html), Detailed Description, angular polynomial and rectification; sensitivities and protocols deduced by the project.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-FISHEYE-001 — Zero coefficients still leave an angular camera

At $\theta=60^\circ=\pi/3$, the zero-coefficient fisheye radius is approximately 1.047, while the pinhole radius is $\tan60^\circ\approx1.732$. With the same focal scaling, that is a substantial off-axis difference despite both coefficient arrays being zero. These constructed numbers compare model families, not two estimates of lens quality. A distortion vector only has meaning together with its projection model.

### CV-FISHEYE-002 — Peripheral views need usable corner localization

Wide radial coverage adds sensitivity to high-order angular coefficients, but extreme obliquity can also make target corners blurred, occluded or biased. Seek observations that are both informative and measurable, and inspect their localization rather than assuming that the farthest possible radius is always best. Hold out entire poses and peripheral sectors to distinguish genuine model support from fitting a small set of difficult edge observations.

### CV-FISHEYE-003 — An average weights regions by observation count

Constructed example: ninety central observations with 0.2 px error and ten peripheral ones with 2 px error give point RMS about 0.66 px. The average can conceal the region where the intended measurement fails. Report sample counts and residuals by radial bin and pose, then evaluate independent geometric quantities there. A uniform-looking global RMS does not imply uniform angular or metric accuracy across a wide field.

### CV-FISHEYE-004 — Rectification rotation changes the ray frame

If the remap uses $R_{rect}$ from raw camera coordinates to rectified camera coordinates, an output ray is proportional to $K_{new}^{-1}\tilde u\prime$ in the rectified frame. Returning it to the raw camera frame requires $R_{rect}^{-1}$ before applying the original camera pose. This derived chain separates output intrinsics from frame orientation. Using the new matrix with the old pose without that rotation can leave a systematic orientation error.

### CV-FISHEYE-005 — More visible field can mean fewer samples per angle

For a fixed output image size, a wider chosen field spreads the available pixels across more directions. The apparent addition of scene content does not create extra measurements from the original sensor. Compare valid-pixel masks and local angular resolution at the same physical directions when choosing balance. Newly exposed borders can be invalid because remapping requests source coordinates outside the acquired image, not because calibration has become less accurate.

Consulted foundations: [OpenCV fisheye](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html): angular projection, remap/rectification and balance definition; checked with Context7.

## Sources and flashcards

- [OpenCV 4.13, fisheye, Detailed Description and EstimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
- [OpenCV 4.13, calibration, pinhole model and distortion](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Related flashcards](../56-calibration-fisheye.md): CV-FISHEYE-001 to 005.

Editor: Agent Codex, 2026-10-24. Primary sources consulted and API OpenCV 4.13 verified with Context7. Analytical calculations and proposed protocols are distinguished from experiments; no actual export, video benchmark or independent scientific validation announced.
