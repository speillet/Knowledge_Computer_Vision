# Flashcards — Camera calibration with a target — Zhang’s method

reference note: [[50-calibration-geometrie/references/52-calibration-zhang|Calibration]]. Source: Agent.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-ZHANG-001

Objective: There are three geometric objectives. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-001
Question: How do camera calibration, pose estimation and registration between two images differ?
Reponse: **Expected answer**: Calibration estimates image formation parameters, including intrinsic and distortion; pose describes a transformation of coordinate frames; registration aligns observations according to a chosen model.

**Further explanation**: A Zhang calibration procedure also estimates a pose of calibration target per view, but this does not make the objectives equivalent. PnP can estimate a pose with a camera already calibrated; a homography can register a plane without finding all the intrinsics. Calibrating the scores of a network is yet another problem.

**Example of a string**: In a fixed cell, a calibration describes how rays are transformed into pixels. An estimate of pose places the camera or room in a coordinate frame. A registration can then align a reference image with the current observation. These operations combine, but their unknowns and reference data are not identical.

**Consequences for the diagnosis**: A good alignment of a calibration target plane can hide a bad extrapolation of parameters out of the views used. Conversely, a well-calibrated camera can give a bad registration if the matches are wrong. Naming the expected output makes it possible to choose the right protocol and avoids asking a single homograph to certify the entire geometry of the system.

**What data raises what unknowns**: A calibration target plane of known geometry provides particular 3D coordinates, e.g. $(X,Y,0)$, and their 2D observations on several views. The calibration looks for common intrinsics and a pose per view; a new estimate of pose can then reuse these fixed intrinsics. A free homography between two images does not necessarily exploit the metric size of the squares and can align the plane without lifting the same unknowns. If the calibration target is printed at a bad uniform scale, the estimated translations follow this erroneous unit, while the pixel adjustment can remain almost identical. Metric validation therefore requires information independent of this alignment alone.

**Blocking errors**: assimilate these three outputs or believe that a homography is always a complete calibration.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, §§2 – 3](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13, Camera Calibration, projection and distortion model; Context7 verification](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), see 2026-10-30.
Tags: cv::pilote cv::d05 famille::comprehension cv_id::CV-ZHANG-001 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-002

Objective: interpret the projection conventions. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-002
Question: In $X_c=RX_w+t$ and $s\tilde x=K[R\mid t]\tilde X_w$, what are the coordinate frames, units and parameters of $K$?
Reponse: **Expected answer**: $R$ transforms the coordinate frame world/calibration target to camera; $t$ is expressed in the coordinate frame camera and in the world points unit. $K$ transforms normalized camera coordinates into pixels:
$$K=\begin{bmatrix}f_x&\gamma&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}.$$ The focal lengths and the main dot are in pixels; $s$ is a homogeneous factor.

**Further explanation**: $\gamma$ is the skew, often set to zero depending on the model. Distortion is not included in this ideal projective multiplication. A square size in millimeters gives translations in this unit, without changing the pixel dimensions of the intrinsics.

**Breakdown of the calculation**: the pose first gives the point in the camera axes. The division by its depth produces normalized coordinates without unity; the intrinsic matrix then expresses these coordinates in the image grid. The chosen distortion modifies this relationship and should be placed in the right place in the complete model.

**check**: a point on the ideal optical axis is projected at the main point; increasing its depth without changing its direction does not change its perspective projection. Checking these simple cases helps to detect an erroneous multiplication order or coordinate frame. A pixel transformation due to preprocessing still acts after these steps and must be propagated to the compared observations.

**Place distortion in the calculation**: after $X_c=RX_w+t$, place $x=X_c/Z_c$, $y=Y_c/Z_c$ and $r^2=x^2+y^2$. A simple polynomial radial model uses $x_d=x(1+k_1r^2+k_2r^4+\cdots)$ and the same for $y_d$; tangential terms are other contributions. The distorted coordinates are then converted into pixels by the intrinsics. The radial coefficients of this convention act on normalized coordinates, not directly over a distance in pixels. This separation explains why a crop changes the main point but not mechanically these coefficients. The validity of the division by $Z_c$ and the visibility of the point must also be checked; a projected number does not imply that a point is in front of the camera.

**Blocking errors**: Reverse the meaning of $R$ without transforming the formula, confuse meters and pixels or include any distortion in $K$ alone.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, §2.1, equation 1](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13, Camera Calibration, projection and distortion model; Context7 verification](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), see 2026-10-30.
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

**Why guidance provides information**: A rotation different from the calibration target changes the directions of its axes in the camera. The same intrinsics must explain these new projections, which adds different constraints. Repeating almost the same orientation mainly provides noisy repetitions of similar stresses.

**Proposed acquisition**: Cover several inclinations and positions in the field with a sharp and rigid calibration target. Do not just try to multiply easy and frontal images to lower a RMS. Then compare the stability of the settings when some views are removed and errors on reserved poses. The model explains the minimum of constraints; their effective independence and the quality of the corners determine the information available in practice.

**Passing constraints to poses**: The linear constraints on the symmetric matrix $B$ are stacked to estimate its six elements to within a scale. After recovering an allowable $K$, columns $K^{-1}h_1$ and $K^{-1}h_2$ give directions of rotation to be normalized with a common scale; the third direction stems from their vector product. Noise generally prevents the resulting matrix from being exactly orthonormal: it must be brought back to $SO(3)$ before the joint refinement. This step is an initialization, not a final estimate of all the distortion. Views repeating the same orientation can leave the constraints almost dependent even if their individual homographies estimate themselves very well.

**Blocking errors**: say that any two pictures are always enough or that simple translations make all intrinsics observable.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, §§2.3, 3.1 and 4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13, Camera Calibration, projection and distortion model; Context7 verification](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), see 2026-10-30.
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-ZHANG-003 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-004

Objective: interpret a RMS without an abusive conclusion. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-004
Question: A calibration reports low reprojection RMS. What does it measure, and which additional validation should be proposed for industrial dimensional measurement?
Reponse: **Expected answer**: The RMS measures the adjustment of projections at observed corners, in a given convention and unit, usually pixels. It does not prove the absence of bias or metric accuracy. Validate on reserved catches and an independent measure suitable for use.

**Further explanation**: record whether the average relates to points or coordinates, analyze the residuals by view and position. Project proposal: fix intrinsic/distortion, estimate a pose with some of the reserved corners and test the others, then check a known dimension. Do not choose a universal threshold without business tolerance.

**Example of bias**: An erroneous square size can leave well-adjusted image projections while imposing a wrong translation unit. The residual pixel does not directly test this physical scale. Similarly, a poorly covered area of the image can be mismodeled without dominating the overall average.

**Validation construite**: Measure a known dimension over several positions and operating distances, with parameters set before testing. Report systematic errors and dispersion, and then examine cases where tolerance is exceeded. A low average should not make difficult peripheral observations disappear. This protocol adds independent information adapted to the need, instead of reusing only the corners that were used to estimate the parameters.

**Defining the RMS**: with $N$ observations 2D and residuals $e_i=(e_{xi},e_{yi})$, $RMS_{point}=\sqrt{\sum_i(e_{xi}^2+e_{yi}^2)/N}$. A mean per coordinate uses $2N$ at the denominator and is therefore $RMS_{point}/\sqrt2$. The average of the norms and the average of the RMS per view are still other statistics. A score announced without denominator can therefore be incomparable despite the same word RMS. Also present the maps of residuals and the quantiles, then a validation on views and reserved points. When the pose of a reserved view is to be estimated, separate the points that serve that pose from those that evaluate the set parameters.

**Blocking errors**: achieve accuracy in millimetres from the RMS adjustment pixel alone.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]] ; [Zhang, §3.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) ; [OpenCV calibrateCamera](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-ZHANG-004 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-005

Objective: Spreading a pixel transformation. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-005
Question: A calibrated image is resized uniformly by $a$, then cropped by $(b_x,b_y)$ pixels in this new frame. How should intrinsics be adapted without any physical change to the optics?
Reponse: **Expected answer**: multiply focal lengths and skew by $a$ and transform the main point into $(ac_x-b_x,ac_y-b_y)$. More generally, $K'=AK$ with $A$ pixel transformation applied to the image.

**Further explanation**: $A$ here has diagonal $(a,a,1)$ and translation $(-b_x,-b_y)$. This derivation assumes exactly the described resize/crop and an unchanged optical model; check the convention of the pixel centers of the tool. A distortion expressed in normalized camera coordinates is not multiplied like a focal length pixel. Modified focus/zooms require a different diagnosis.

**Analytical example**: with $a=0,5$, $c_x=640$ px and a crop of 20 px in the reduced image, the new center is worth 300 px. An observation and its projection must undergo the same transformation to keep a consistent residual. The grid change does not physically move the camera.

**Interface Trap**: Two tools can use different conventions for pixel centers during resize. Test a few known points across the entire chain before applying a simplified formula. If the camera has changed focus, the optical relationship can really change: it is no longer a simple transformation of coordinates and the initial validation must be re-examined.

**Case of pixel centers**: If the tool sets the resize to $u'=a(u+1/2)-1/2$, the transformation also contains the translation $(a-1)/2$; the main point follows the same relationship before the crop. The $u'=au$ simple formula corresponds to another contract. These expressions are analytical cases: they do not describe all libraries. For a different scaling on both axes, multiply the relevant lines of $K$ respectively via the full pixel affine. The factor of the last homogeneous coordinate remains fixed at one per convention. Testing a round trip of multiple points is safer than inferring the affine from the final size of the array alone.

**Blocking errors**: keep $K$ identical after crop or indiscriminately multiply all distortion coefficients by $a$.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [OpenCV, camera model](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html); [Zhang, TR98-71, §§2 – 4 and Annex C, Constraints, poses and Degenerations](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf), see 2026-10-30.
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-ZHANG-005 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-006

Objective: Diagnose observability. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-006
Question: Twenty nearly frontal views yield low RMS, but intrinsics change substantially when a few views are removed. What should be checked, and which new acquisition would be informative?
Reponse: **Expected answer**: Suspect an uninformative capture and a poorly constrained model, while checking free corners and parameters. Add diverse orientations and useful spatial coverage; the amount of almost identical views does not replace their diversity.

**Further explanation**: compare stability by sub-assemblies, maps by residuals and reserved validation; check flatness, sharpness and distortion pattern. Do not automatically conclude that the optimizer is defective. Setting a parameter is only justified by the model and the need, not to get a nicer score.

**Clearing mechanism**: Some parameters can move together while keeping close projections on a little diverse capture. The solver can therefore find several solutions that adjust almost as well the same data, without implementation errors. Subset stability reveals this sensitivity.

**Proposed test**: Add views with really different orientations and positions, then compare parameters and validation with the same model. Also inspect for possible deformation of calibration target or a systematic error in the location of corners. Unleashing more coefficients can absorb these defects rather than explain them. The quality of a calibration is judged on the capture information and its future use, not on the raw number of images.

**Linking acquisition and information**: If two columns of the Jacobian of the residuals are almost dependent, a variation of one parameter can compensate that of another. Small singular values and covariance correlations signal this coupling in the local approximation. Adding views that excite new directions can separate them better than adding twenty copies of a front view. Covering the edge helps constrain terms that grow with distance to the center, but requires well-located corners in that area. A flexible calibration target or systematically biased corners can produce a consistent fit to the wrong model: digital stability and physical adequacy are controlled separately.

**Blocking errors**: declare the calibration correct only because twenty images have been used or the RMS is weak.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, §4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13, Camera Calibration, projection and distortion model; Context7 verification](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), see 2026-10-30.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-ZHANG-006 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-007

Objective: Build consistent collection and validation. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-ZHANG-007
Question: For dimensional inspection with a fixed camera, which decisions make target-based calibration usable beyond a demonstration?
Reponse: **Expected answer**: define business tolerance, stable resolution/focus, optical model and units; capture a calibration target plane known under informative orientations and positions; check corners; retain independent observations and metric reference to validate.

**Further explanation**: log versions, flags, excluded catches and residuals; test the area and operating distances. Separate intrinsic calibration and pose from the camera in the cell. Provide for a new validation after modification of the optics or assembly. This scenario describes a proposed protocol, with no field test performed.

**Proposed operating criterion**: keep a part or target of check independent and define the events that trigger a new check: focus modification, mechanical shock, resolution change or measurement drift. A calibration becomes a versioned artifact with its domain of validity.

**Validation loop**: relate measured errors to product decisions, then distinguish repeatability between holds and biases relative to the known dimension. Document the geometry of the plane or volume actually controlled. Proper projection on the calibration target does not guarantee that all 3D surfaces are measurable with a single view. This limit must remain visible in the path between calibration, estimation of pose and metrology.

**Moving from calibration to measurement on a plan**: with center world camera $C$, radius world direction $d$ and known plane $n^TX=h$, the intersection is $X=C+\lambda d$, where $\lambda=(h-n^TC)/(n^Td)$ if the denominator is non-zero. This geometry shows that a metric measurement also requires the plane or depth of the surface: intrinsics alone are not enough. Near a radius parallel to the plane, the intersection becomes very sensitive to noise. Propagating calibration, edge location and flatness errors in product tolerance, and then comparing to an independent reference. This calculation assumes a known flat surface and a properly dedistorted projection, without certifying a relief measurement.

**Blocking errors**: blindly reuse the parameters after changing focus, or ignore the actual size of the calibration target.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|reference note calibration]]; [Zhang, §§2 – 4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13, Camera Calibration, projection and distortion model; Context7 verification](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), see 2026-10-30.
Tags: cv::pilote cv::d05 famille::conception cv_id::CV-ZHANG-007 provenance::agent pole::B pole::C pole::E
END
