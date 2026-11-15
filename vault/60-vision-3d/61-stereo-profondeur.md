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

**Units in the derivation**: The quotient $f/d$ is unitless if both quantities use pixels of the same rectified grid; the result therefore keeps the unit of the baseline. The difference in coordinates reflects the separation of the two rays for a given point. A small disparity here corresponds to a large depth.

**Example check**: Check a known distant target, then artificially double the baseline in the calculation: the computed depth also doubles. This helps locate a scale error without changing the matcher. The simplified formula assumes that the principal points are aligned as stated and that the disparity is physically valid. An occluded region or a wrong match can produce a positive number without a correct depth. In more general rectified geometry, use the reprojection transformation and its conventions rather than applying this formula to any output called disparity.

**Similar-triangle construction**: With camera centres separated horizontally by $B$, the same focal length and the same principal-point abscissa $c_x$, the ideal projections are $x_g=fX/Z+c_x$ and $x_d=f(X-B)/Z+c_x$ ($g$ for left, $d$ for right). The subtraction eliminates $X$ and gives $d=fB/Z$. If the principal-point abscissas differ, it is $d-(c_{x,g}-c_{x,d})$ that enters this simplified geometry. This derivation explains why each rectified image must be used with its own reprojection matrix. The result $Z$ is the depth along the rectified optical axis; the Euclidean distance to the camera centre is $\sqrt{X^2+Y^2+Z^2}$ and can be greater for an off-axis point.

**Blocking errors**: Using a baseline in millimetres and reporting the result directly in metres.
Source: [[60-vision-3d/references/61-stereo-profondeur|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L2058–L2085, `stereoRectify` P1, P2 and Q](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2058-L2085). Numerical case and derivation: project calculations.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-STEREO-001 provenance::agent pole::B pole::C
END

## CV-STEREO-002

Objective: Interpret depth uncertainty. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-STEREO-002
Question: Why does stereo depth accuracy often deteriorate at long range?
Reponse: **Expected answer**: The sensitivity to disparity grows like $fB/d^2$; small d errors become large Z errors when d is low.

**Further explanation**: Compare a reprojection error and a metric error over known distances.

**Analytical sensitivity**: Differentiating $Z=fB/d$ gives $\partial Z/\partial d=-fB/d^2$. For small errors, the absolute value of this derivative converts the uncertainty of disparity into uncertainty of depth. When the distance doubles in this model, the disparity is halved and this sensitivity is multiplied by four.

**Constructed example**: With $fB=200$ px·m and a disparity error of 0.5 px, the approximation gives about 0.25 m at $d=20$ px and 1 m at $d=10$ px. These figures assume a small noise and correct matches; they do not describe the outliers of occlusion. Compare separately bias, scatter and invalid pixel rate. Increasing the baseline can help the geometry, but also makes matching harder and reduces the overlap: the decision links precision, visibility and task.

**Propagation of several uncertainties**: For $Z=fB/d$ and small perturbations, $\delta Z/Z\simeq\delta f/f+\delta B/B-\delta d/d$. If these errors are independent and centred, the relative variances add up; otherwise their covariances count. A baseline bias thus produces a relative scale error, while a fixed disparity bias penalizes long distances more. Near $d=0$, linearization becomes fragile and a symmetric distribution in disparity gives a very asymmetric distribution in depth. Also evaluate intervals in depth, or use an inverse-depth representation depending on the estimator, instead of assuming a constant Gaussian metric uncertainty.

**Small disparities produce asymmetric depth errors**: Constructed case: with $fB=200$ px·m, disparity $2\pm0.5$ px maps to depths from 80 to about 133.3 m around a nominal 100 m. The interval is asymmetric because inversion is nonlinear. Near zero disparity, a first-order standard deviation can be misleading and invalid disparities must remain invalid rather than being clamped into apparently finite obstacles. Report depth availability together with error over the relevant range.

**Blocking errors**: Assuming constant depth noise at every distance.
Source: [[60-vision-3d/references/61-stereo-profondeur|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L2058–L2085, Q for horizontal stereo](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2058-L2085); [Scharstein and Szeliski 2002, §5.1](https://vision.middlebury.edu/stereo/taxonomy-IJCV.pdf). Sensitivity derivation and constructed cases: project calculations.
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

**Representation trap**: An integer can encode a real value with fractional bits. If the relevant output stores sixteen times the disparity, a value 320 represents 20 pixels and not 320 pixels. Since depth is inversely proportional to disparity in the simple case, interpreting 320 as pixels would reduce depth by a factor of sixteen.

**Proposed investigation**: Inspect the type, valid values, invalid-value sentinel and the documentation of the exact function. Then reproject a known point while checking the matrix associated with the rectification and the baseline units. Do not simply multiply the final cloud to hide a contract defect: this could leave inconsistent masks and other downstream quantities. A good geometric calibration does not protect against a wrong numerical conversion of the matcher output.

**Order of operations**: Conceptually, keep the mask defined by the matcher's contract, convert the fixed-point disparity to a real value, then apply $[X_h,Y_h,Z_h,W_h]^T=Q[x,y,d,1]^T$ and divide by $W_h$ when the projection is valid. These are homogeneous coordinates, not yet meters before this division and the interpretation of the units of $Q$. Do not build the mask only after filling the holes: an interpolation can replace a sentinel with a plausible value. Keep the original measurement, its validity and any completed depth separate. Testing a known pixel makes it possible to distinguish storage factor, disparity convention and baseline unit.

**Blocking errors**: Reprojecting fixed-point integers as ordinary disparity pixels.
Source: [[60-vision-3d/references/61-stereo-profondeur|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L3502–L3512, `DISP_SHIFT` and fixed-point output](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L3502-L3512); [OpenCV 4.13.0, `calib3d.hpp` L3060–L3064, `reprojectImageTo3D` input scaling](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L3060-L3064); [OpenCV 4.13.0, `stereosgbm.cpp` L507, invalid value](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/stereosgbm.cpp#L507).
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

**What rectification changes**: It resamples the images so that the geometrically possible matches lie on one row. It does not create texture and does not make visible a surface hidden from one of the cameras. The search along a row can therefore still contain several candidates or no real match.

**Constructed example**: A uniform surface offers close costs for many disparities; a periodic texture can favour the wrong period; at the edge of an object, a point can be visible on one side only. A regularization may select a value in these regions, but this value is not a new observation. Keep the validity information, test the available consistency, and then evaluate on an independent reference. Distinguishing the density of the produced map from the amount of truly reliable depth avoids interpreting every filled pixel as a measurement.

**Constructed left–right check**: Let $d_g(x)=x_g-x_d$ be the left disparity and $d_d(x_d)=x_g-x_d$ the right disparity, positive with the same convention, for the same point ($g$ for left, $d$ for right). A consistent pair must satisfy $|d_g(x)-d_d(x-d_g(x))|<\tau$, subject to interpolation and visibility. If the right map uses the opposite sign, the difference becomes a sum: the conventions must be explicit. This test rejects some inconsistencies, but two false matches on a repetitive texture can remain mutually compatible. Geometric validation, the distinction between holes and regularized values, and an independent reference remain necessary. The threshold $\tau$ is in disparity pixels of the grid considered.

**Rectification does not resolve an occluded pixel**: A foreground edge can reveal background in only one camera. The corresponding pixel then has no valid partner, regardless of how accurately epipolar lines are horizontal. A left/right consistency check can flag some failures, but repeated texture can produce consistent wrong pairs. Evaluate occlusion and low-texture masks separately, and distinguish raw matched depth from any later interpolation or completion used to fill unavailable regions.

**Blocking errors**: Inferring a reliable depth from the horizontality of the epipolar lines alone.
Source: [[60-vision-3d/references/61-stereo-profondeur|Full reference]]; [Hirschmüller 2008, §2.2 and §2.3, eq. 15](https://www.cvlibs.net/projects/autonomous_vision_survey/literature/Hirschmueller2008PAMI.pdf); [OpenCV 4.13.0, `stereosgbm.cpp` L945–L960, left–right check](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/stereosgbm.cpp#L945-L960). Constructed cases: project deductions.
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-STEREO-004 provenance::agent pole::B pole::C
END

## CV-STEREO-005

Objective: explain the SGM smoothness penalties P1 and P2. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-STEREO-005
Question: OpenCV 4.13 `StereoSGBM` runs on grayscale images with `blockSize=5`, and the header's suggested penalties give `P1=200` and `P2=800`. Between two neighbouring pixels on an aggregation path, what does each penalty charge for, and which scene geometry is each meant to accommodate? Why must `P2` not be smaller than `P1`? In a warehouse scene with small speckle blobs and 6 px wide shelving uprights, what changes in the disparity map as `P2` is swept over 250, 800 and 3200 with `P1=200`?
Reponse: **Expected answer**: (1) `P1` is added when the disparity changes by exactly one pixel between neighbours; `P2` when it changes by more than one pixel, whatever the size of the jump. `P1` lets slanted or curved surfaces, whose disparity drifts one pixel at a time, pass at low cost; `P2` charges a depth discontinuity once, independently of its height, so object boundaries survive instead of being penalized in proportion to the jump. (2) The penalty must not decrease with the size of the change. In the path recursion, the term $\min_iL_r(p-r,i)+P_2$ also covers $d\pm1$; if $P_2<P_1$, `P1` never acts and every change, even of one pixel, costs `P2`, so slopes are priced like discontinuities. (3) Raising `P2` makes every jump dearer: small speckle blobs are absorbed into their surroundings, but narrow structures whose matching evidence cannot pay for entering and leaving them are erased into the background. In the constructed toy, blobs survive at 250 and vanish at 800; the uprights survive at 800 and vanish at 3200.

**Further explanation**: Hirschmüller's energy adds, for each neighbour $q$ of $p$, $P_1$ if $|D_p-D_q|=1$ and $P_2$ if $|D_p-D_q|>1$. Each path cost follows $L_r(p,d)=C(p,d)+\min(L_r(p-r,d),L_r(p-r,d\pm1)+P_1,\min_iL_r(p-r,i)+P_2)-\min_kL_r(p-r,k)$, and the path costs are summed over at least eight directions in the paper, five in OpenCV's default mode. He adapts $P_2=P_2'/|I_{bp}-I_{bq}|$ to place jumps at intensity edges, yet requires $P_2\ge P_1$ in every case. OpenCV states that the algorithm requires $P_2>P_1$ and, in every mode, silently replaces $P_2$ by $\max(P_2,P_1+1)$: `P2=150` with `P1=200` becomes 201, without an error. Its aggregation loops use a constant $P_2$.

**Units**: the penalties are in the units of the matching cost. OpenCV sums Birchfield–Tomasi pixel costs over the block, hence the suggestions $8cb^2$ and $32cb^2$ for $c$ channels and block size $b$. Changing `blockSize` or the number of channels without rescaling the penalties changes the smoothing.

**Single-path arithmetic**: on one horizontal path, a structure $w$ pixels wide with a per-pixel cost advantage $\Delta$ is kept only if $w\Delta>2P_2$. With $w=6$ and $\Delta=400$: $2400>1600$ at $P_2=800$, but $2400<6400$ at 3200. Paths running along the upright pay no jump, so the summed cost keeps it longer than one path predicts: in the toy, horizontal paths alone already lose it at 1600, while the eight-direction sum keeps it there.

**Blocking errors**: Describing `P2` as growing with the size of the jump. Assigning discontinuities to `P1` and slopes to `P2`. Expecting a larger `P2` only to remove noise. Keeping the same penalties after changing `blockSize` or the number of channels.
Source: [[60-vision-3d/references/61-stereo-profondeur|Full reference]]; [Hirschmüller 2008, §2.2, eqs. 11–14: penalties, path recursion, P2 adapted to the intensity gradient and the requirement on P1 and P2](https://www.cvlibs.net/projects/autonomous_vision_survey/literature/Hirschmueller2008PAMI.pdf); [OpenCV 4.13.0, `calib3d.hpp` L3723–L3729, P1 and P2 and their suggested values](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L3723-L3729); [OpenCV 4.13.0, `stereosgbm.cpp` L500, correction of P2, and L676–L811, aggregation with constant P2](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/stereosgbm.cpp#L500). Toy scene, single-path arithmetic and blob and upright results: project constructions recomputed in the check script of this pass.
Tags: cv::pilote cv::d06 famille::algorithme cv_id::CV-STEREO-005 provenance::agent pole::B pole::C
END
