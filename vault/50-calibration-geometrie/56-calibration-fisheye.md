# Flashcards — Fisheye calibration — angular projection and off-center validation

reference note: [[50-calibration-geometrie/references/56-calibration-fisheye|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-FISHEYE-001

Objective: distinguish projection fisheye and pinhole. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FISHEYE-001
Question: In OpenCV fisheye, does setting all four distortion coefficients to zero recover pinhole projection? Explain using an off-axis ray.
Reponse: **Expected answer**: No: the normalized radius is then $r_d=\theta$, while the pinhole gives $r=\tan\theta$, with $\theta$ the angle at the optical center in radians. The projections coincide only approximately near the axis.

**Further explanation**: Analytical case: at 60° and with a focal length of 300 px, the radius is about 314 px against 520 px in pinhole. Compare the models on the rays actually observed, not just on their names or the number of coefficients.

**Why the center is cheating**: near zero, $\tan\theta$ is close to $\theta$. The two models may therefore appear similar on a small central region. The deviation grows off-axis; zero coefficients do not mean "no difference with the pinhole", but no further correction to the chosen angular model.

**check**: project some known rays, including a sufficiently oblique one, with the two models in the same conventions and units. Then compare to the reserved observations of the real camera. A visually plausible image does not separate models on their peripheral accuracy. The coefficients and matrix of each model must remain associated with the image and projection function that interprets them.

**Local development**: $\tan\theta=\theta+\theta^3/3+O(\theta^5)$. The apparent equality near the axis comes from the first common order; the relative deviation grows approximately as $\theta^2/3$ for small angles. This development is not a reliable approximation to use without check near 90°. To reverse a calibrated fisheye projection, you need to find the angle from the polynomial $\theta_d(\theta)$, then form a radius; we do not simply replace $r_d$ with a pinhole coordinate. Check that this function remains invertible in the exploited domain: parameters adjusted over a small region can produce undesirable behavior in extrapolation.

**Blocking errors**: Assimilate the fisheye coefficients to the first pinhole coefficients; conclude with an identical projection everywhere.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]] ; [OpenCV 4.13, fisheye, Detailed Description and EstimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-FISHEYE-001 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-002

Objective: design wide angle calibration views. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-FISHEYE-002
Question: Which acquisitions should be added when a wide-angle calibration uses many views concentrated near the image center?
Reponse: **Expected answer**: Add views covering the periphery and diversify orientations and distances of the calibration target. Reserve poses and regions for validation. The number of photos does not replace the geometric information they provide.

**Further explanation**: The peripheral parameters are little constrained by rays close to the axis. check sharpness, spot detection, rigidity of the calibration target and stability of the mounting. The proposed protocol aims at packaging, without guaranteeing the calibration of any device.

**Reading of observations**: points close to the axis explore a small range of angles. Several models or parameters can then produce similar projections in this range while diverging at the edges. Adding nearly identical central images does not test this extrapolation.

**Acquisition construite**: Spread the corners over the useful field, vary the inclinations and keep sharp peripheral views away from the adjustment. Examine the residuals by radius and stability on subsets. A difficulty in detecting corners at the edge can itself introduce bias; inspecting observations rather than just asking for more coefficients. The protocol aims for more complete geometric information and must remain compatible with the optical model and rigidity of the calibration target.

**Sensitivity of coefficients**: in $\theta_d=\theta+\sum_{j=1}^4 k_j\theta^{2j+1}$, the derivative with respect to $k_j$ is $\theta^{2j+1}$. High-order terms therefore become very insensitive when all angles are small; thousands of center points can remain uninformative for $k_4$. This reading of the Jacobian explains the peripheral collection without prescribing a universal angle threshold. The high sensitivity at the edges is also not enough: the corners must be localizable and cover several directions and poses, in order to separate distortion, main center and orientation of the calibration target. The reserved residuals controls the generalization of the adjusted model.

**Blocking errors**: Multiply only center front views; validate on adjustment images only.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]] ; [OpenCV 4.13, fisheye, Detailed Description and EstimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::conception cv_id::CV-FISHEYE-002 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-003

Objective: Locate a camera model defect. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FISHEYE-003
Question: A fisheye calibration has low overall reprojection RMS, but measurements near the edges are wrong. What should be checked?
Reponse: **Expected answer**: Map the residuals according to radius, position and pose on reserved observations; inspect the points of calibration target at the edges and check the projection model. Then compare the metric errors of the target use.

**Further explanation**: An average is dominated by the most sampled areas. Systematic biases at the periphery can come from the model, the calibration target, blurring or lack of views. A straightened visual aspect does not separate them.

**Why the average hides the defect**: If most of the corners are near the center, their small error dominates the RMS, while the useful peripheral region is little evaluated. A global average must therefore be accompanied by a spatial map and comparable error groups.

**Diagnostic construit**: fix the calibration and project points reserved for several radii, then observe direction and amplitude of errors. A systematic pattern suggests a structured cause, but does not single-handedly differentiate between optical model and location bias. Inspect the points and repeat with new poses. Validate also a quantity related to the use: the precision of a projection at the edges is not summarized by the corrected appearance.

**Pixel Error and Angular Error**: breaking down the residual image $e$ in a unitary radial direction $n_r$ and a tangent $n_t$ gives $e_r=n_r^Te$ and $e_t=n_t^Te$. Analyzing these components by crown, with headcount and distributions, reveals biases that the average norm mixes. In a single radial cut, $\delta r\simeq f\,(d\theta_d/d\theta)\delta\theta$: a pixel does not represent everywhere the same angular error if the derivative varies. Metric conversion still depends on the scene and its depth. This analysis is a diagnosis, not a certain identification of the optical or localization cause.

**Blocking errors**: Conclude a correct calibration from a single RMS of learning.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]] ; [OpenCV 4.13, fisheye, Detailed Description and EstimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-FISHEYE-003 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-004

Objective: Propagating the contract after rectification. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FISHEYE-004
Question: After remapping a fisheye image into a rectified image, which calibration should be used to reconstruct rays or estimate pose?
Reponse: **Expected answer**: Use the model and the new matrix associated with the corrected image, with its dimensions and its valid region. The intrinsics and coefficients of the raw image describe another geometry of pixels.

**Further explanation**: The map sets a match between output and source pixels. Changing the resolution, crop, or output projection requires propagating this transformation. Check a known 3D point through the complete string.

**Data Chain**: The remap defines which source position contributes to each output pixel. The new grid therefore describes another projection, even if it comes from the same sensor. To reassemble a pixel to a radius, use the contract of this grid, not that of the raw file.

**Test construit**: From a known 3D point, project it into the raw image, follow the transformation to the output, and then check the radius or calculated pose in the rectified model. Include crop, padding and data-free areas. Then applying the raw distortion a second time is like transforming already corrected coordinates. A general visual coherence can let this error pass, especially near the center where the models look more alike.

**Radius of exit**: for rectification to a pinhole model, a homogeneous pixel $\tilde u'$ gives a radius $q'=K_{\mathrm{new}}^{-1}\tilde u'$ in the rectified coordinate frame. If $R_{\mathrm{rect}}$ sends the raw camera rays to this coordinate frame, the corresponding raw ray is proportional to $R_{\mathrm{rect}}^Tq'$. The fisheye projection of this ray provides the position to be sampled in the source image: it is a reverse map construction. This transformation is usually unrefined. After an output crop, also adapt the main center; after a resize, adapt focal lengths and coordinates according to the pixel convention chosen. Pixels without a valid source do not create any geometric measurements.

**Blocking errors**: Reuse the raw distortion on an already rectified image without adaptation.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]] ; [OpenCV 4.13, fisheye, Detailed Description and EstimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-FISHEYE-004 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-005

Objective: interpret the rectified field parameter. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FISHEYE-005
Question: Changing OpenCV's balance parameter reveals more of the scene but adds borders. Is the camera better calibrated?
Reponse: **Expected answer**: No: `balance` changes the choice of output projection and field compromise, not the physical parameters already estimated. Compare useful field, local resolution and valid pixels with the same calibration.

**Further explanation**: A large output area can contain pixels without original observation or very interpolated. The quality criterion must come from the task: cover, metric or geometry, not just the size of the image.

**Interpretation of Compromise**: An output projection may favor a framing that fills the rectangle or a wider field with invalid areas. These choices change the amount of information available and its local resolution, without changing the observations used to estimate the camera.

**Proposed evaluation**: Compare outputs on the same calibration by reporting valid mask, useful field and task error. For a measurement near a border, the interpolation and low density of observations can count more than the total number of pixels displayed. The output geometry must be propagated to the following algorithms. A change in presentation can therefore help a product without constituting an improvement in physical calibration.

**Density of information**: Keeping more field in a set number of pixels can reduce sampling of certain directions. The map derivative, a Jacobian $2\times2$ between output and source coordinates, locally describes stretching and anisotropy. When many output pixels interpolate almost the same source samples, their number does not measure an optical resolution gain. To compare two values of `balance`, keep the same calibrated parameters and measure the task on the common valid region, and then separately report the additional field. This protocol prevents a change in pixel population from being taken for an improvement in accuracy.

**Blocking errors**: Assimilate increase of the displayed field and decrease of the calibration error.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]] ; [OpenCV 4.13, fisheye, Detailed Description and EstimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-FISHEYE-005 provenance::agent pole::B pole::C pole::E
END
