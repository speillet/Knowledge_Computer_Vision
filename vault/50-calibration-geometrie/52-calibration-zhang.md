# Flashcards — Camera calibration with a target — Zhang’s method

reference note: [[50-calibration-geometrie/references/52-calibration-zhang|Calibration]]. Source: Agent.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-ZHANG-001

Objective: Distinguish three geometric objectives. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-001
Question: How do camera calibration, pose estimation and registration between two images differ?
Reponse: **Expected answer**: Calibration estimates image formation parameters, including intrinsic and distortion; pose describes a transformation of coordinate frames; registration aligns observations according to a chosen model.

**Further explanation**: A Zhang calibration procedure also estimates a pose of calibration target per view, but this does not make the objectives equivalent. PnP can estimate a pose with a camera already calibrated; a homography can register a plane without finding all the intrinsics. Calibrating the scores of a network is yet another problem.

**Example of a chain**: In a fixed cell, a calibration describes how rays are transformed into pixels. An estimate of pose places the camera or part in a coordinate frame. A registration can then align a reference image with the current observation. These operations combine, but their unknowns and reference data are not identical.

**Consequences for the diagnosis**: A good alignment of a calibration target plane can hide a bad extrapolation of parameters out of the views used. Conversely, a well-calibrated camera can give a bad registration if the matches are wrong. Naming the expected output makes it possible to choose the right protocol and avoids asking a single homography to certify the entire geometry of the system.

**Which data resolve which unknowns**: A calibration target plane of known geometry provides particular 3D coordinates, e.g. $(X,Y,0)$, and their 2D observations on several views. The calibration looks for common intrinsics and a pose per view; a new estimate of pose can then reuse these fixed intrinsics. A free homography between two images does not necessarily exploit the metric size of the squares and can align the plane without resolving the same unknowns. If the calibration target is printed at a bad uniform scale, the estimated translations follow this erroneous unit, while the pixel adjustment can remain almost identical. Metric validation therefore requires information independent of this alignment alone.

**Unknowns, counted**: For a planar target, $H\sim K[r_1\ r_2\ t]$ has 8 degrees of freedom, of which the pose takes 6, so one view yields only 2 constraints on the intrinsics [Zhang §2.3]. Five intrinsics therefore need at least three general views, or two with zero skew [§3.1], and $H$ contains no distortion term. Constructed count, recomputed in the check script of this pass: calibrating Zhang's model from 10 views of a $9\times6$-corner target estimates $5+2+6\times10=67$ parameters from $2\times10\times54=1080$ residuals; a pose with fixed intrinsics estimates 6 parameters from the 108 residuals of one view; a registering homography estimates 8 parameters from at least four correspondences and maps pixels to pixels without a metric unit. OpenCV 4.13 splits its outputs the same way: `calibrateCamera` returns $K$, the distortion vector, one rotation and translation per view and the RMS; `solvePnP` takes $K$ and the distortion and returns the rotation and translation that bring model points into the camera frame; `findHomography` returns a $3\times3$ matrix between two planes.

**Blocking errors**: Equating these three outputs, or believing that a homography is always a complete calibration.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, MSR-TR-98-71, §2.1 eq. 1 (extrinsic and intrinsic parameters), §2.3 (8 degrees of freedom, 2 constraints per view), §3.1 (intrinsics then one pose per view, number of views)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13.0, calib3d.hpp L782–L851 (`findHomography`), L1031–L1032 (`solvePnP` direction), L1606–L1743 (`calibrateCamera` outputs) and L1649–L1653: use solvePnP when the intrinsics are known](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp). Parameter count: project construction recomputed in the 2026-11-16 check script.
Tags: cv::pilote cv::d05 famille::comprehension cv_id::CV-ZHANG-001 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-002

Objective: interpret the projection conventions. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-002
Question: In $X_c=RX_w+t$ and $s\tilde x=K[R\mid t]\tilde X_w$, what are the coordinate frames, units and parameters of $K$?
Reponse: **Expected answer**: $R$ transforms the world (calibration target) frame into the camera frame; $t$ is expressed in the camera frame and in the unit of the world points. $K$ transforms normalized camera coordinates into pixels:
$$K=\begin{bmatrix}f_x&\gamma&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}.$$ The focal lengths and the principal point are in pixels; $s$ is a homogeneous factor.

**Further explanation**: $\gamma$ is the skew, often set to zero depending on the model. Distortion is not included in this ideal projective multiplication. A square size in millimeters gives translations in this unit, without changing the pixel dimensions of the intrinsics.

**Breakdown of the calculation**: the pose first gives the point in the camera axes. The division by its depth produces dimensionless normalized coordinates; the intrinsic matrix then expresses these coordinates in the image grid. The chosen distortion modifies this relationship and should be placed in the right place in the complete model.

**Check**: a point on the ideal optical axis is projected at the principal point; increasing its depth without changing its direction does not change its perspective projection. Checking these simple cases helps to detect an erroneous multiplication order or coordinate frame. A pixel transformation due to preprocessing still acts after these steps and must be propagated to the compared observations.

**Place distortion in the calculation**: after $X_c=RX_w+t$, set $x=X_c/Z_c$, $y=Y_c/Z_c$ and $r^2=x^2+y^2$. A simple polynomial radial model uses $x_d=x(1+k_1r^2+k_2r^4+\cdots)$ and the same for $y_d$; tangential terms are other contributions. The distorted coordinates are then converted into pixels by the intrinsics. The radial coefficients of this convention act on normalized coordinates, not directly on a distance in pixels. This separation explains why a crop changes the principal point but not mechanically these coefficients. The validity of the division by $Z_c$ and the visibility of the point must also be checked; a projected number does not imply that a point is in front of the camera.

**Homogeneous scale is not another camera parameter**: In the ideal pinhole model with the usual last row of $K$, the homogeneous projection scale can be chosen as camera depth $Z_c$. It changes from point to point and disappears after dividing the first two coordinates by the third. Translation retains the target coordinate unit; focal lengths remain in pixels. Adding a common metric scale to target points and translation does not require multiplying the intrinsic matrix by that scale.

**Blocking errors**: Reversing the direction of $R$ without changing the formula, confusing metres and pixels, or putting distortion into $K$ alone.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, §2.1, equation 1](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13.0, calib3d.hpp L56–L262: pinhole model, normalized coordinates and distortion](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-ZHANG-002 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-003

Objective: Explain the multi-view constraints. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-003
Question: How do homographies of a planar target constrain intrinsics in Zhang's method, and why is varying translation alone insufficient?
Reponse: **Expected answer**: $H\sim K[r_1\ r_2\ t]$. With $B=K^{-T}K^{-1}$, the columns $h_1,h_2$ give $h_1^TBh_2=0$ and $h_1^TBh_1=h_2^TBh_2$. These constraints are based on the orthogonal axes of rotation; repeated orientations do not provide the necessary diversity.

**Further explanation**: Each view brings two constraints. Three independent views are generally required for five free intrinsics; two may suffice with zero skew imposed. Algebraic minima do not guarantee accurate calibration on noisy images; the capture must also cover the useful area.

**Why orientation provides information**: A different rotation of the calibration target changes the directions of its axes in the camera. The same intrinsics must explain these new projections, which adds different constraints. Repeating almost the same orientation mainly provides noisy repetitions of similar constraints.

**Proposed acquisition**: Cover several inclinations and positions in the field with a sharp and rigid calibration target. Do not just try to multiply easy and frontal images to lower a RMS. Then compare the stability of the parameters when some views are removed, and the errors on held-out poses. The model explains the minimum of constraints; their effective independence and the quality of the corners determine the information available in practice.

**From constraints to poses**: The linear constraints on the symmetric matrix $B$ are stacked to estimate its six elements to within a scale. After recovering an admissible $K$, columns $K^{-1}h_1$ and $K^{-1}h_2$ give directions of rotation to be normalized with a common scale; the third direction is their cross product. Noise generally prevents the resulting matrix from being exactly orthonormal: it must be brought back to $SO(3)$ before the joint refinement. This step is an initialization, not a final estimate of all the distortion. Views repeating the same orientation can leave the constraints almost dependent even if their individual homographies are very well estimated.

**Different images can repeat the same constraint**: Pure translation of the planar target changes where it appears but preserves the orientation-based orthogonality constraints on intrinsics. Even an in-plane target rotation can leave its plane parallel and fail to add independent intrinsic information. Seek changes in plane normal, not merely a large image count or pixel displacement. Peripheral coverage still serves distortion estimation, so acquisition diversity has both orientation and image-position roles.

**Blocking errors**: Saying that any two pictures are always enough, or that simple translations make all intrinsics observable.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, §2.3 eqs. 3–4, §3.1 eqs. 8–9 and number of views, §4 Proposition 1](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-ZHANG-003 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-004

Objective: interpret a RMS without an abusive conclusion. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-004
Question: A calibration reports low reprojection RMS. What does it measure, and which additional validation should be proposed for industrial dimensional measurement?
Reponse: **Expected answer**: The RMS measures the adjustment of projections at observed corners, in a given convention and unit, usually pixels. It does not prove the absence of bias or metric accuracy. Validate on held-out captures and an independent measurement suited to the use.

**Further explanation**: record whether the average relates to points or coordinates, analyze the residuals by view and position. Project proposal: fix the intrinsics and distortion, estimate a pose with some of the held-out corners and test the others, then check a known dimension. Do not choose a universal threshold without business tolerance.

**Example of bias**: An erroneous square size can leave well-adjusted image projections while imposing a wrong translation unit. The pixel residual does not directly test this physical scale. Similarly, a poorly covered area of the image can be mismodeled without dominating the overall average.

**Constructed validation**: Measure a known dimension over several positions and operating distances, with parameters set before testing. Report systematic errors and dispersion, and then examine cases where tolerance is exceeded. A low average should not make difficult peripheral observations disappear. This protocol adds independent information adapted to the need, instead of reusing only the corners that were used to estimate the parameters.

**Defining the RMS**: with $N$ 2-D observations and residuals $e_i=(e_{xi},e_{yi})$, $RMS_{point}=\sqrt{\sum_i(e_{xi}^2+e_{yi}^2)/N}$. A mean per coordinate uses $2N$ at the denominator and is therefore $RMS_{point}/\sqrt2$. The average of the norms and the average of the RMS per view are still other statistics. A score announced without denominator can therefore be incomparable despite the same word RMS. Even within OpenCV 4.13, `calibrateCamera` divides by the number of points while `stereoCalibrate` divides by twice that number. Also present the residual maps and quantiles, then a validation on held-out views and points. When the pose of a held-out view must be estimated, separate the points used for that pose from those that evaluate the fixed parameters.

**Low pixel RMS can coexist with metric scale bias**: Constructed case: a target square is entered as 20 mm but is actually 19.8 mm. Under ideal uniform scaling, recovered metric translations are biased by about $20/19.8-1\approx1.01\%$, while the same image projections can still fit well. A held-out image from that same wrongly scaled target does not independently verify absolute dimensions. Use a separate traceable distance relevant to the measurement geometry.

**Blocking errors**: Inferring millimetre accuracy from the pixel RMS of the fit alone.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]] ; [Zhang, §3.2 eq. 10 and §5.2 Table 1 RMS](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) ; [OpenCV 4.13.0, calibration.cpp L546, L621 and L1155: RMS denominators](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration.cpp). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-ZHANG-004 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-005

Objective: Propagate a pixel transformation. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-005
Question: A calibrated image is resized uniformly by $a$, then cropped by $(b_x,b_y)$ pixels in this new frame. How should intrinsics be adapted without any physical change to the optics?
Reponse: **Expected answer**: multiply focal lengths and skew by $a$ and transform the principal point into $(ac_x-b_x,ac_y-b_y)$. More generally, $K'=AK$ with $A$ pixel transformation applied to the image.

**Further explanation**: $A$ here has diagonal $(a,a,1)$ and translation $(-b_x,-b_y)$. This derivation assumes exactly the described resize/crop and an unchanged optical model; check the convention of the pixel centers of the tool. A distortion expressed in normalized camera coordinates is not multiplied like a focal length in pixels. A modified focus or zoom requires a different diagnosis.

**Analytical example**: with $a=0.5$, $c_x=640$ px and a crop of 20 px in the reduced image, the new principal point is at 300 px. An observation and its projection must undergo the same transformation to keep a consistent residual. The grid change does not physically move the camera.

**Interface trap**: Two tools can use different conventions for pixel centers during resize. Test a few known points across the entire chain before applying a simplified formula. If the camera has changed focus, the optical relationship can really change: it is no longer a simple transformation of coordinates and the initial validation must be re-examined.

**Case of pixel centres**: If the tool sets the resize to $u'=a(u+1/2)-1/2$, the transformation also contains the translation $(a-1)/2$; the main point follows the same relationship before the crop. The $u'=au$ simple formula corresponds to another contract. These expressions are analytical cases: they do not describe all libraries. For a different scaling on both axes, multiply the relevant lines of $K$ respectively via the full pixel affine. The factor of the last homogeneous coordinate remains fixed at one per convention. Testing a round trip of multiple points is safer than inferring the affine from the final size of the array alone.

**A transform chain avoids order mistakes**: For resize matrix $S$ followed by crop matrix $C$, the pixel transform is $A=CS$, so $K^{\prime}=CSK$. Reversing the order applies crop offsets in a different pixel unit. A constructed example with half-size resizing and a 20 px crop moves a principal point at 320 px to 140 px, whereas cropping 20 original pixels first gives 150 px. Include the actual pixel-center convention when implementing the transformation.

**Blocking errors**: Keeping $K$ identical after a crop, or multiplying all distortion coefficients by $a$ indiscriminately.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [OpenCV 4.13.0, calib3d.hpp L316–L323: distortion coefficients independent of resolution, fx, fy, cx, cy scaled](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp); [Zhang, TR98-71, §2.1 eq. 1, intrinsic matrix](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-ZHANG-005 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-006

Objective: Diagnose observability. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-006
Question: Twenty nearly frontal views yield low RMS, but intrinsics change substantially when a few views are removed. What should be checked, and which new acquisition would be informative?
Reponse: **Expected answer**: Suspect an uninformative capture and a poorly constrained model, while checking the corners and the free parameters. Add diverse orientations and useful spatial coverage; the amount of almost identical views does not replace their diversity.

**Further explanation**: compare stability across subsets, residual maps and held-out validation; check flatness, sharpness and distortion pattern. Do not automatically conclude that the optimizer is defective. Setting a parameter is only justified by the model and the need, not to get a nicer score.

**Compensation mechanism**: Some parameters can move together while keeping close projections on a little diverse capture. The solver can therefore find several solutions that fit the same data almost equally well, without implementation errors. Subset stability reveals this sensitivity.

**Proposed test**: Add views with really different orientations and positions, then compare parameters and validation with the same model. Also inspect for possible deformation of calibration target or a systematic error in the location of corners. Freeing more coefficients can absorb these defects rather than explain them. The quality of a calibration is judged on the capture information and its future use, not on the raw number of images.

**Linking acquisition and information**: If two columns of the Jacobian of the residuals are almost dependent, a variation of one parameter can compensate that of another. Small singular values and covariance correlations signal this coupling in the local approximation. Adding views that excite new directions can separate them better than adding twenty copies of a front view. Covering the edge helps constrain terms that grow with distance to the center, but requires well-located corners in that area. A flexible calibration target or systematically biased corners can produce a consistent fit to the wrong model: numerical stability and physical adequacy are checked separately.

**Parameter stability needs withheld acquisition groups**: Leave out whole target poses rather than a few corners from every pose when testing acquisition diversity. Corners within one image share pose and image-formation effects, so randomly withholding them can make validation look more independent than it is. Compare parameter shifts, radial residual maps and metric predictions over the omitted poses. This is a proposed robustness check; a stable estimate can still share a systematic target or lens-model bias.

**Blocking errors**: Declaring the calibration correct only because twenty images have been used or the RMS is low.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, §4 degenerate configurations and §5.1 errors versus number and orientation of planes](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13.0, calibration.cpp L560–L572: standard deviations from J^T J](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration.cpp). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-ZHANG-006 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-007

Objective: Build consistent collection and validation. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-007
Question: For dimensional inspection with a fixed camera, which decisions make target-based calibration usable beyond a demonstration?
Reponse: **Expected answer**: define business tolerance, stable resolution/focus, optical model and units; capture a calibration target plane known under informative orientations and positions; check corners; retain independent observations and metric reference to validate.

**Further explanation**: log versions, flags, excluded captures and residuals; test the area and operating distances. Separate intrinsic calibration and pose from the camera in the cell. Provide for a new validation after modification of the optics or assembly. This scenario describes a proposed protocol, with no field test performed.

**Proposed operating criterion**: keep an independent check part or target and define the events that trigger a new check: focus modification, mechanical shock, resolution change or measurement drift. A calibration becomes a versioned artifact with its domain of validity.

**Validation loop**: relate measured errors to product decisions, then distinguish repeatability between captures and biases relative to the known dimension. Document the geometry of the plane or volume actually controlled. Proper projection on the calibration target does not guarantee that all 3D surfaces are measurable with a single view. This limit must remain visible in the path between calibration, estimation of pose and metrology.

**Moving from calibration to measurement on a plane**: with camera centre $C$ and ray direction $d$ in the world frame and known plane $n^TX=h$, the intersection is $X=C+\lambda d$, where $\lambda=(h-n^TC)/(n^Td)$ if the denominator is non-zero. This geometry shows that a metric measurement also requires the plane or depth of the surface: intrinsics alone are not enough. Near a ray parallel to the plane, the intersection becomes very sensitive to noise. Propagate calibration, edge-location and flatness errors into the product tolerance, and then compare with an independent reference. This calculation assumes a known flat surface and a properly undistorted projection, without certifying a relief measurement.

**Error budget against the tolerance** (constructed example, recomputed in the check script of this pass): a camera 1000 mm above a conveyor plane with $f=2000$ px sees 0.5 mm per pixel, and a 50 mm length must be measured to ±0.1 mm. Locating each edge to 0.1 px contributes 0.05 mm per edge, about 0.07 mm on the length if the two edge errors are independent: the resolution decision already consumes most of the tolerance. A target printed at 99.7% scale and used to locate the measurement plane scales every intersection by $1/0.997$, so the length reads 0.15 mm long. A top face 2 mm above the calibrated plane reads $50\times1000/998\approx50.10$ mm, and a point 200 mm off-axis moves by 0.4 mm. Adding views lowers none of these three terms; resolution, a measured target and the measured surface height do. Target flatness belongs to the same budget: in Zhang's simulations, systematic non-planarity degrades the estimates more than random errors on the model points, and the result "seems still usable in practice" below about 3% of the pattern size [§5.3.2], a criterion for the intrinsics, not for a 0.1 mm tolerance.

**Blocking errors**: Blindly reusing the parameters after changing focus, or ignoring the actual size of the calibration target.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, §3.4 procedure and §5.3 sensitivity to model imprecision, §5.3.2 systematic non-planarity](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13.0, calib3d.hpp L1606–L1743: calibrateCamera inputs, flags and outputs](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp). Error budget: project construction recomputed in the 2026-11-16 check script.
Tags: cv::pilote cv::d05 famille::conception cv_id::CV-ZHANG-007 provenance::agent pole::B pole::C pole::E
END
