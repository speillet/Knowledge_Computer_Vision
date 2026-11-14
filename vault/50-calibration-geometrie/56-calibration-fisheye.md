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

**Why the centre misleads**: Near zero, $\tan\theta$ is close to $\theta$. The two models may therefore appear similar on a small central region. The deviation grows off-axis; zero coefficients do not mean "no difference from the pinhole", but no correction beyond the chosen angular model.

**Discriminating check**: Project some known rays, including a sufficiently oblique one, with the two models in the same conventions and units. Then compare with held-out observations of the real camera. A visually plausible image does not separate models on their peripheral accuracy. The coefficients and matrix of each model must remain associated with the image and projection function that interprets them.

**Series expansion**: $\tan\theta=\theta+\theta^3/3+O(\theta^5)$. The apparent equality near the axis comes from the first common order; the relative deviation grows approximately as $\theta^2/3$ for small angles. This expansion is not a reliable approximation near 90°. To invert a calibrated fisheye projection, solve the polynomial $\theta_d(\theta)$ for the angle and then form the ray; one cannot simply replace $r_d$ with a pinhole coordinate. Check that this function remains invertible over the field actually used: parameters fitted over a small region can behave badly in extrapolation.

**Zero coefficients still leave an angular camera**: At $\theta=60^\circ=\pi/3$, the zero-coefficient fisheye radius is approximately 1.047, while the pinhole radius is $\tan60^\circ\approx1.732$. With the same focal scaling, that is a substantial off-axis difference despite both coefficient arrays being zero. These constructed numbers compare model families, not two estimates of lens quality. A distortion vector only has meaning together with its projection model.

**Blocking errors**: Equating the fisheye coefficients with the first pinhole coefficients; concluding that the projection is identical everywhere.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L509–L536, fisheye model](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L509-L536); [Kannala and Brandt 2006, §II-A and §III](https://users.aalto.fi/~kannalj1/calibration/Kannala_Brandt_calibration.pdf). Numerical comparison: project calculation.
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-FISHEYE-001 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-002

Objective: design wide angle calibration views. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-FISHEYE-002
Question: Which acquisitions should be added when a wide-angle calibration uses many views concentrated near the image center?
Reponse: **Expected answer**: Add views covering the periphery and diversify orientations and distances of the calibration target. Hold out poses and regions for validation. The number of photos does not replace the geometric information they provide.

**Further explanation**: Rays close to the axis barely constrain the peripheral parameters. Check sharpness, corner detection, the rigidity of the calibration target and the stability of the mounting. The proposed protocol aims at conditioning, without guaranteeing the calibration of any device.

**Reading the observations**: Points close to the axis explore a small range of angles. Several models or parameters can then produce similar projections in this range while diverging at the edges. Adding nearly identical central images does not test this extrapolation.

**Constructed acquisition**: Spread the corners over the useful field, vary the tilts and keep some sharp peripheral views out of the fit. Examine the residuals by radius and the stability on subsets. Difficult corner detection at the edge can itself introduce bias; inspect the observations rather than just asking for more coefficients. The protocol aims for more complete geometric information and must remain compatible with the optical model and rigidity of the calibration target.

**Sensitivity of coefficients**: In $\theta_d=\theta+\sum_{j=1}^4 k_j\theta^{2j+1}$, the derivative with respect to $k_j$ is $\theta^{2j+1}$. High-order terms therefore become very insensitive when all angles are small; thousands of center points can remain uninformative for $k_4$. This reading of the Jacobian explains the peripheral collection without prescribing a universal angle threshold. The high sensitivity at the edges is also not enough: the corners must be localizable and cover several directions and poses, in order to separate distortion, principal point and target orientation. Held-out residuals test the generalization of the fitted model.

**Peripheral views need usable corner localization**: Wide radial coverage adds sensitivity to high-order angular coefficients, but extreme obliquity can also make target corners blurred, occluded or biased. Seek observations that are both informative and measurable, and inspect their localization rather than assuming that the farthest possible radius is always best. Hold out entire poses and peripheral sectors to distinguish genuine model support from fitting a small set of difficult edge observations.

**Blocking errors**: Adding only frontal central views; validating only on the fitting images.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]]; [Kannala and Brandt 2006, §II-B and §V-B](https://users.aalto.fi/~kannalj1/calibration/Kannala_Brandt_calibration.pdf); [OpenCV 4.13.0, `calib3d.hpp` L4208–L4245, `fisheye::calibrate`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L4208-L4245). Sensitivity and acquisition protocol: project deductions.
Tags: cv::pilote cv::d05 famille::conception cv_id::CV-FISHEYE-002 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-003

Objective: Locate a camera model defect. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FISHEYE-003
Question: A fisheye calibration has low overall reprojection RMS, but measurements near the edges are wrong. What should be checked?
Reponse: **Expected answer**: Map the residuals by radius, position and pose on held-out observations; inspect the calibration-target points at the edges and check the projection model. Then compare the metric errors for the intended use.

**Further explanation**: An average is dominated by the most sampled areas. Systematic biases at the periphery can come from the model, the calibration target, blurring or lack of views. A visually straightened image does not separate them.

**Why the average hides the defect**: If most of the corners are near the center, their small error dominates the RMS, while the useful peripheral region is little evaluated. A global average must therefore be accompanied by a spatial map and comparable error groups.

**Constructed diagnosis**: Freeze the calibration and project held-out points at several radii, then observe the direction and amplitude of the errors. A systematic pattern suggests a structured cause, but does not by itself distinguish an optical-model error from a corner-localization bias. Inspect the points and repeat with new poses. Validate also a quantity related to the use: the precision of a projection at the edges is not summarized by the corrected appearance.

**Pixel error and angular error**: Decomposing the image residual $e$ along a unit radial direction $n_r$ and a tangential direction $n_t$ gives $e_r=n_r^Te$ and $e_t=n_t^Te$. Analyzing these components by radial ring, with sample counts and distributions, reveals biases that the mean norm mixes. Along one radial line, $\delta r\simeq f\,(d\theta_d/d\theta)\delta\theta$: one pixel does not represent the same angular error everywhere if the derivative varies. Metric conversion still depends on the scene and its depth. This analysis is a diagnosis, not a definitive identification of the optical or localization cause.

**An average weights regions by observation count**: Constructed example: ninety central observations with 0.2 px error and ten peripheral ones with 2 px error give point RMS about 0.66 px. The average can conceal the region where the intended measurement fails. Report sample counts and residuals by radial bin and pose, then evaluate independent geometric quantities there. A uniform-looking global RMS does not imply uniform angular or metric accuracy across a wide field.

**Blocking errors**: Concluding that the calibration is correct from a single training RMS.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]]; [Kannala and Brandt 2006, §V-B, Table III](https://users.aalto.fi/~kannalj1/calibration/Kannala_Brandt_calibration.pdf); [OpenCV 4.13.0, `calib3d.hpp` L509–L536](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L509-L536). Residual decomposition and weighting example: project deductions.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-FISHEYE-003 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-004

Objective: Propagate the contract after rectification. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FISHEYE-004
Question: After remapping a fisheye image into a rectified image, which calibration should be used to reconstruct rays or estimate pose?
Reponse: **Expected answer**: Use the model and the new matrix associated with the corrected image, with its dimensions and its valid region. The intrinsics and coefficients of the raw image describe another geometry of pixels.

**Further explanation**: The map defines a correspondence between output and source pixels. Changing the resolution, crop or output projection requires propagating this transformation. Check a known 3D point through the complete chain.

**Data chain**: The remap defines which source position contributes to each output pixel. The new grid therefore describes another projection, even if it comes from the same sensor. To back-project a pixel to a ray, use the contract of this grid, not that of the raw file.

**Constructed test**: Project a known 3D point into the raw image, follow the transformation to the output, and then check the ray or the computed pose in the rectified model. Include crop, padding and areas without data. Applying the raw distortion a second time would transform already corrected coordinates. A general visual coherence can let this error pass, especially near the center where the models look more alike.

**Output ray**: For rectification to a pinhole model, a homogeneous pixel $\tilde u'$ gives a ray $q'=K_{\mathrm{new}}^{-1}\tilde u'$ in the rectified coordinate frame. If $R_{\mathrm{rect}}$ sends the raw camera rays to this coordinate frame, the corresponding raw ray is proportional to $R_{\mathrm{rect}}^Tq'$. The fisheye projection of this ray provides the position to be sampled in the source image: this is how the inverse map is built. This construction does not re-estimate the calibration. After an output crop, also adapt the principal point; after a resize, adapt the focal lengths and coordinates according to the chosen pixel convention. Pixels without a valid source do not create any geometric measurements.

**Blocking errors**: Reuse the raw distortion on an already rectified image without adaptation.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]]; [OpenCV 4.13.0, `fisheye.cpp` L560–L615, `initUndistortRectifyMap`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fisheye.cpp#L560-L615); [OpenCV 4.13.0, `calib3d.hpp` L4144–L4160](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L4144-L4160).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-FISHEYE-004 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-005

Objective: interpret the rectified field parameter. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FISHEYE-005
Question: Changing OpenCV's balance parameter reveals more of the scene but adds borders. Is the camera better calibrated?
Reponse: **Expected answer**: No: `balance` changes the choice of output projection and field compromise, not the physical parameters already estimated. Compare useful field, local resolution and valid pixels with the same calibration.

**Further explanation**: A large output area can contain pixels without original observation or very interpolated. The quality criterion must come from the task: coverage, metric accuracy or geometry, not just the size of the image.

**Interpreting the trade-off**: An output projection may favor a framing that fills the rectangle or a wider field with invalid areas. These choices change the amount of information available and its local resolution, without changing the observations used to estimate the camera.

**Proposed evaluation**: Compare outputs on the same calibration by reporting valid mask, useful field and task error. For a measurement near a border, the interpolation and low density of observations can count more than the total number of pixels displayed. The output geometry must be propagated to the following algorithms. A change in presentation can therefore help a product without constituting an improvement in physical calibration.

**Information density**: Keeping more field in a fixed number of pixels can reduce the sampling of certain directions. The derivative of the map, a $2\times2$ Jacobian between output and source coordinates, locally describes stretching and anisotropy. When many output pixels interpolate almost the same source samples, their number does not measure an optical resolution gain. To compare two values of `balance`, keep the same calibrated parameters and measure the task on the common valid region, and then separately report the additional field. This protocol prevents a change in pixel population from being taken for an improvement in accuracy.

**More visible field can mean fewer samples per angle**: For a fixed output image size, a wider chosen field spreads the available pixels across more directions. The apparent addition of scene content does not create extra measurements from the original sensor. Compare valid-pixel masks and local angular resolution at the same physical directions when choosing balance. Newly exposed borders can be invalid because remapping requests source coordinates outside the acquired image, not because calibration has become less accurate.

**What `balance` computes**: In OpenCV 4.13, `estimateNewCameraMatrixForUndistortRectify` undistorts the four edge midpoints, computes for each the focal length that would place it on the output border, and interpolates linearly between the largest value (`balance` = 0) and the smallest (`balance` = 1); `fov_scale` divides the result. $K$ and $D$ are inputs and are never modified.

**Blocking errors**: Equating an increase of the displayed field with a decrease of the calibration error.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Full reference]]; [OpenCV 4.13.0, `fisheye.cpp` L655–L724, `estimateNewCameraMatrixForUndistortRectify`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fisheye.cpp#L655-L724); [OpenCV 4.13.0, `calib3d.hpp` L4192–L4206](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L4192-L4206). Evaluation protocol: project deduction.
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-FISHEYE-005 provenance::agent pole::B pole::C pole::E
END
