# Flashcards — Rectified stereo, SGM and depth

reference note: [[60-vision-3d/references/61-stereo-profondeur|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-STEREO-001

Objective: Calculate a rectified depth. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-STEREO-001
Question: For horizontally rectified stereo with equal principal-point x-coordinates, f=1000 px, a 0.2 m baseline and left-minus-right disparity of 20 px, what depth is obtained?
Reponse: **Expected answer**: 10 m by $Z=fB/d$.

**Further explanation**: At 10 px of disparity, one would obtain 20 m. The formula assumes a compatible rectified geometry and a valid disparity; f and d must be in the same pixel unit.

**derivation of units**: the quotient $f/d$ is without a unit if the two quantities use the pixels of the same rectified grid; the result therefore retains the unit of the baseline. The difference in coordinates reflects the separation of the two rays for a given point. A small disparity here corresponds to a great depth.

**Example of check**: check a known remote target, then artificially double the value of the baseline in the calculation: the calculated depth would also double. This helps locate a scale error without changing the matcher. The simplified formula assumes the main points aligned as advertised and a valid physical disparity. A hidden region or a bad match can produce a positive number without proper depth. In more general rectified geometry, use the reprojection transformation and its conventions rather than applying this formula to any output called disparity.

**Construction of triangles**: With horizontally separated centers of $B$, even focal length and even main abscissa $c_x$, the ideal projections are $x_g=fX/Z+c_x$ and $x_d=f(X-B)/Z+c_x$. The subtraction eliminates $X$ and gives $d=fB/Z$. If the main abscissas differ, it is $d-(c_{x,g}-c_{x,d})$ that enters into this simplified geometry. This derivation explains why using the corresponding rectified image/reprojection matrix torque is essential. The result $Z$ is the depth along the rectified optical axis; the Euclidean distance to the camera center is $\sqrt{X^2+Y^2+Z^2}$ and can be greater for an off-axis point.

**Principal-point offsets change effective disparity**: If rectified principal points differ, $d=x_L-x_R=fB/Z+(c_{xL}-c_{xR})$. Hence use $Z=fB/[d-(c_{xL}-c_{xR})]$ under the same parallel-axis model. The simplified front explicitly assumes equal principal-point abscissas. A reprojection matrix from the actual rectification can encode the offset; substituting the mnemonic formula without checking that assumption introduces a systematic depth error.

**Blocking errors**: Use a baseline in millimeters and announce directly meters.
Source: [[60-vision-3d/references/61-stereo-profondeur|Full reference]]; [OpenCV 4.13.0, stereoRectify and reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html); analytical calculation of the project; [OpenCV 4.13.0, Stereo, Basics, Triangles and Disparity; Uncertainty Diversions and Bidirectional Test Constructed](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-STEREO-001 provenance::agent pole::B pole::C
END

## CV-STEREO-002

Objective: Interpreting the uncertainty of depth. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-STEREO-002
Question: Why does stereo depth accuracy often deteriorate at long range?
Reponse: **Expected answer**: The sensitivity to disparity grows like $fB/d^2$; small d errors become large Z errors when d is low.

**Further explanation**: Compare a reprojection error and a metric error over known distances.

**Analytical Sensitivity**: drifting $Z=fB/d$ gives $\partial Z/\partial d=-fB/d^2$. With little error, the absolute value of this derivative converts the uncertainty of disparity into uncertainty of depth. When the distance doubles in this model, the disparity is halved and this sensitivity is multiplied by four.

**Constructed example**: with $fB=200$ px·m and a disparity error of 0,5 px, the approximation gives about 0,25 m at $d=20$ px and 1 m at $d=10$ px. These figures assume a small noise and correct matches; they do not describe the outliers of occlusion. Compare separately bias, scatter and invalid pixel rate. Increasing the baseline can help geometry, but can also make matching and overlaying more difficult: the decision connects precision, visibility and task.

**Propagation of several uncertainties**: for $Z=fB/d$ and small disturbances, $\delta Z/Z\simeq\delta f/f+\delta B/B-\delta d/d$. If these errors are independent and centered, the relative variances add up; otherwise their covariances count. A baseline bias thus produces a relative error of scale, while a fixed disparity bias further penalizes long distances. Almost $d=0$, linearization becomes fragile and a symmetrical distribution in disparity gives a very asymmetrical distribution in depth. Also evaluate the intervals in depth or use a depth inverse representation according to the estimator, instead of assuming constant Gaussian metric uncertainty.

**Small disparities produce asymmetric depth errors**: Constructed case: with $fB=200$ px·m, disparity $2\pm0.5$ px maps to depths from 80 to about 133.3 m around a nominal 100 m. The interval is asymmetric because inversion is nonlinear. Near zero disparity, a first-order standard deviation can be misleading and invalid disparities must remain invalid rather than being clamped into apparently finite obstacles. Report depth availability together with error over the relevant range.

**Blocking errors**: Assume constant depth noise for any distance.
Source: [[60-vision-3d/references/61-stereo-profondeur|Full reference]]; [OpenCV 4.13.0, stereoRectify and reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html); derivation of Z=fB/d, at f and B fixed; [OpenCV 4.13.0, Stereo, Basics, Triangles and Disparity; Uncertainty Diversions and Bidirectional Test Constructed](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-STEREO-002 provenance::agent pole::B pole::C
END

## CV-STEREO-003

Objective: decode a fixed disparity. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-STEREO-003
Question: An SGBM reconstruction has the wrong scale despite good calibration. Which numerical convention should be checked?
Reponse: **Expected answer**: The storage of the disparity and its scaling factor, including the four fractional bits of the concerned outputs; convert and mask invalid values.

**Further explanation**: Check also baseline and Q before arbitrarily correcting the final coordinates.

**Representation Trap**: An integer can encode a real value with fractional bits. If the relevant output stores sixteen times the disparity, a value 320 represents 20 pixels and not 320 pixels. Since depth is inversely proportional to disparity in the simple case, interpreting 320 as pixels would reduce depth by a factor of sixteen.

**Proposed investigation**: inspect type, valid values, invalid-value sentinel and exact function documentation. Then reproject a known point by checking the matrix associated with the rectification and the basic units. Do not simply multiply the final cloud to hide a contract defect: this could leave inconsistent masks and other downstream quantities. A good geometric calibration does not protect from a bad digital conversion of the matcher output.

**Order of operations**: Conceptually, retain the mask provided by the matcher's contract, convert the fixed disparity to real, then apply $[X_h,Y_h,Z_h,W_h]^T=Q[x,y,d,1]^T$ and divide by $W_h$ when the projection is valid. These are homogeneous coordinates, not yet meters before this division and the interpretation of the units of $Q$. Do not build the mask only after filling the holes: an interpolation can replace a sentinel with a plausible value. Keep the original measurement, its validity and any depth completed separate. Testing a known pixel makes it possible to distinguish storage factor, disparity convention, and baseline unit.

**A fixed-point mistake gives a predictable scale error**: If a stored disparity of 320 represents 20 px through a factor of 16, using 320 directly in $Z=fB/d$ produces one-sixteenth of the correct depth. Converting again after it has already been decoded produces the opposite error. Record representation at each interface and test one known plane at a measured distance. Invalid-value encoding and negative disparities depend on the matcher configuration and require its exact contract.

**Blocking errors**: Reproject fixed integers as ordinary pixels of disparity.
Source: [[60-vision-3d/references/61-stereo-profondeur|Full reference]]; [OpenCV 4.13.0, StereoSGBM, Detailed Description and create](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html); [OpenCV 4.13.0, stereoRectify and reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html); [OpenCV 4.13.0, Stereo, Basics, Triangles and Disparity; Uncertainty Diversions and Bidirectional Test Constructed](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-STEREO-003 provenance::agent pole::B pole::C
END

## CV-STEREO-004

Objective: Separate rectification and matching. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-STEREO-004
Question: Does rectification guarantee a correct correspondence at every pixel?
Reponse: **Expected answer**: No: it simplifies search geometry; texture, repetition and occlusion can still make matching ambiguous.

**Further explanation**: Confidence and invalid masks must be evaluated, not filled by a fictitious depth.

**What the correction changes**: reorganizes images to simplify geometry-enabled search locations. It does not create texture and does not make visible a hidden surface in one of the cameras. The search along a line can therefore still contain several candidates or no real match.

**Constructed example**: a uniform surface offers close costs for many disparities; a periodic texture can favor the bad period; at the edge of an object, a point can only be seen on one side. A regularization may select a value in these regions, but this value is not a new observation. Maintain validity information and test available consistency, and then evaluate on an independent reference. Distinguishing the density of the produced map and the amount of really reliable depth avoids interpreting any filled pixel as a measurement.

**Bidirectional verification built**: Set $d_g(x)=x_g-x_d$ and a positive straight disparity $d_d(x_d)=x_g-x_d$ for the same point. A consistent pair must check $|d_g(x)-d_d(x-d_g(x))|<\tau$, subject to interpolation and visibility. If the right field uses the opposite sign, the equation changes in sum: the conventions must be explicit. This test rejects some inconsistencies, but two false matches on a repetitive texture can remain mutually compatible. Geometric validation, the distinction between holes and regularized values, and an independent reference remain necessary. The threshold $\tau$ is in pixels of disparity of the grid considered.

**Rectification does not resolve an occluded pixel**: A foreground edge can reveal background in only one camera. The corresponding pixel then has no valid partner, regardless of how accurately epipolar lines are horizontal. A left/right consistency check can flag some failures, but repeated texture can produce consistent wrong pairs. Evaluate occlusion and low-texture masks separately, and distinguish raw matched depth from any later interpolation or completion used to fill unavailable regions.

**Blocking errors**: Deduct a reliable depth from the only horizontality of the epipolar lines.
Source: [[60-vision-3d/references/61-stereo-profondeur|Full reference]]; [OpenCV StereoSGBM, description and compute](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html); [OpenCV reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html); [OpenCV 4.13.0, Stereo, Basics, Triangles and Disparity; Uncertainty Diversions and Bidirectional Test Constructed](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-STEREO-004 provenance::agent pole::B pole::C
END
