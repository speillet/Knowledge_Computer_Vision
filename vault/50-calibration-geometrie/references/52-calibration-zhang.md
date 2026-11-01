---
id: CV-ZHANG
type: methode
domaine: d05
poles: [B, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: ["CV-HOMOGRAPHIE"]
revision: 6
tags: [cv/d05, calibration, zhang]
---
# Camera calibration with a target — Zhang’s method

## Problem and contract

Calibration estimates the parameters of image formation from known and observed calibration target points. It differs from the pose of an already calibrated camera and a registration between images. It does not calibrate the probabilistic scores of a detector. [Zhang, §§2 – 3][zhang]

Inputs: 3D coordinates of the corners of a calibration target plane, associated 2D coordinates in multiple views, resolution and optical model selected. The size of the square fixes the unit of translations: millimeters if the points are in millimeters. Outputs: intrinsic $K$, distortion and one pose of calibration target per frame. Keep corner identifiers, checkerboard dimensions and order of matches.

**Required prerequisites**: [Projection and coordinate frames](../../01-Parcours/Pre-requis.md), [homographie](51-ransac-homographie.md) for initialization. **Competences**: explain identifiability, design capture and validate.

## Intuition and equations

The same known plan is observed under different orientations. Each view gives a homography; the orthogonality of the axes of the calibration target constrains the same intrinsics through the views. An optimization then refines the parameters.

$$
X_c=RX_w+t,\qquad
s\tilde x=K[R\mid t]\tilde X_w,\qquad
K=\begin{bmatrix}f_x&\gamma&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}.
$$

$X_w,X_c\in\mathbb R^3$ are the dot in the coordinate frames calibration target and camera; $R\in SO(3)$ transforms world to camera; $t\in\mathbb R^3$ is in units of calibration target; $\tilde X_w$ is homogeneous. $f_x,f_y$ and the main point $(c_x,c_y)$ are in pixels; $\gamma$ is the skew in pixel units. $s$ is the homogeneous factor. The written projection is ideal, before distortion.

On $Z_w=0$, $H\sim K[r_1\ r_2\ t]$, where $r_1,r_2$ are the first two columns of $R$. By noting $B=K^{-T}K^{-1}$ and $h_i$ the columns of $H$:

$$
h_1^TBh_2=0,\qquad h_1^TBh_1=h_2^TBh_2.
$$

These two constraints per view come from the orthogonality and the equality of norms of the axes of rotation. With five free intrinsics, three independent views are usually required for linear initialization; two may suffice by imposing a zero skew. This algebraic minimum does not give a guarantee of accuracy. Translations alone do not bring new orientation constraints. [Zhang, §§2.3, 3.1 and 4][zhang]

## Procedure, distortion and acquisition

1. Define the model, the actual square size and the order of the corners.
2. Capture sharp, oriented and distributed views in the image.
3. Detect and refine corners, inspect associations.
4. Initialize homographs, intrinsics and poses; estimate distortion.
5. Refine the parameters with a nonlinear reprojection error.
6. Validate on other observations and with a measure related to use.

The radial paper model and the OpenCV models with additional coefficients are not interchangeable without specifying it. For example, in normalized coordinates without unit $(x_n,y_n)$, $r^2=x_n^2+y_n^2$ and $x_d=x_n(1+k_1r^2+k_2r^4)$ describe the single radial component; the analogous relationship applies to $y_n$. Tangential parameters, fisheye or rational models require their own definition. [Zhang, §3.3][zhang]

Assumptions: calibration target sufficiently flat and rigid, stable optical parameters, projection adapted to the sensor, usable observations. Focus/zoom variables, rolling shutter with motion and distorted calibration target can violate these assumptions. Their presence requires diagnosis, not just more coefficients.

## Residual, parameters and cost

For $M$ valid observations, a geometric RMS convention is

$$
E=\sqrt{\frac1M\sum_{j,i}\|x_{ij}-\hat x(K,d,R_j,t_j,X_i)\|_2^2}.
$$

$x_{ij}$ is the observed corner, $\hat x$ its predicted projection in pixels, $d$ the distortion coefficients and $j$ the view. $M$ counts points, not twice coordinates; other conventions can use $2M$. The RMS is here in pixels. It measures adjustment to observations, not directly metric accuracy or no bias. [OpenCV calibration][opencv]

Parameters to record: distortion model, intrinsic constraints, resolution, corner estimation, convergence criteria and excluded views. Too many parameters can over-adjust an uninformative capture. The cost increases with the number of views/coins and iterations; this is often an offline step, separate from the cost of a production undistortion.

Pseudocode **not executed**: detect → check → calibrate → analyze the residuals by view and position → validate on reserved catches. No actual calibration results are announced in this batch.

## Validation and controlled variation

**Protocol proposed by the project**, not a paper prescription: keep $K,d$ fixed on reserved catches; estimate the pose with one part of the corners and measure the others. Add an independent measurement adapted to the product, for example a known dimension at different positions and distances. Acceptance thresholds come from business need, not a universal RMS value.

**Variation not executed**: Compare an almost front-end game to a game with various orientations, with comparable views and corner quality. Prediction: Diversity improves observability; the drive RMS can remain low in both cases. Examine external stability and validation.

| Symptom | Possible causes | Discriminant verification |
| --- | --- | --- |
| Low RMS, false metric results | Square size, calibration target bias, misidentified model | Independent measurement and verification of units |
| Forts residuals on the outskirts | Insufficient coverage, inadequate distortion | vector residual map, new peripheral views |
| Unstable intrinsics according to the subset | poses redundant, blurry, excessive free settings | Subsamples, angular diversity and constrained model justified |

After resize by $a_x,a_y$ factors, apply pixel transformation to intrinsics; crop/padding also move the main point. If the physical model remains valid, this coordinate frame transformation does not necessarily require a new calibration. A change of focus or zoom is another situation.

## Guided reasoning and proposed checks

These constructed cases develop view constraints, resize and check out of learning. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-ZHANG-001

**Question of work**: How do camera calibration, pose estimation and registration between two images differ?

**Reference Response**: Calibration estimates image formation parameters, including intrinsic and distortion; pose describes a transformation of coordinate frames; registration aligns observations according to a chosen model.

**Example of a string**: In a fixed cell, a calibration describes how rays are transformed into pixels. An estimate of pose places the camera or room in a coordinate frame. A registration can then align a reference image with the current observation. These operations combine, but their unknowns and reference data are not identical.

**Consequences for the diagnosis**: A good alignment of a calibration target plane can hide a bad extrapolation of parameters out of the views used. Conversely, a well-calibrated camera can give a bad registration if the matches are wrong. Naming the expected output makes it possible to choose the right protocol and avoids asking a single homograph to certify the entire geometry of the system.

### Case linked to CV-ZHANG-007

**Question of work**: For dimensional inspection with a fixed camera, which decisions make target-based calibration usable beyond a demonstration?

**Reference Response**: define business tolerance, stable resolution/focus, optical model and units; capture a calibration target plane known under informative orientations and positions; check corners; retain independent observations and metric reference to validate.

**Proposed operating criterion**: keep a part or target of check independent and define the events that trigger a new check: focus modification, mechanical shock, resolution change or measurement drift. A calibration becomes a versioned artifact with its domain of validity.

**Validation loop**: relate measured errors to product decisions, then distinguish repeatability between holds and biases relative to the known dimension. Document the geometry of the plane or volume actually controlled. Proper projection on the calibration target does not guarantee that all 3D surfaces are measurable with a single view. This limit must remain visible in the path between calibration, estimation of pose and metrology.

**Documentary reference for this pass**: [Zhang, rapport TR98-71](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf), §§2 – 4, projection, estimation and refinement. The other developments are in the [flashcards](../52-calibration-zhang.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-ZHANG-001

**Situation**: How do camera calibration, pose estimation and registration between two images differ?

**What data raises what unknowns**: A calibration target plane of known geometry provides particular 3D coordinates, e.g. $(X,Y,0)$, and their 2D observations on several views. The calibration looks for common intrinsics and a pose per view; a new estimate of pose can then reuse these fixed intrinsics. A free homography between two images does not necessarily exploit the metric size of the squares and can align the plane without lifting the same unknowns. If the calibration target is printed at a bad uniform scale, the estimated translations follow this erroneous unit, while the pixel adjustment can remain almost identical. Metric validation therefore requires information independent of this alignment alone.

### CV-ZHANG-002

**Situation**: In $X_c=RX_w+t$ and $s\tilde x=K[R\mid t]\tilde X_w$, what are the coordinate frames, units and parameters of $K$?

**Place distortion in the calculation**: after $X_c=RX_w+t$, place $x=X_c/Z_c$, $y=Y_c/Z_c$ and $r^2=x^2+y^2$. A simple polynomial radial model uses $x_d=x(1+k_1r^2+k_2r^4+\cdots)$ and the same for $y_d$; tangential terms are other contributions. The distorted coordinates are then converted into pixels by the intrinsics. The radial coefficients of this convention act on normalized coordinates, not directly over a distance in pixels. This separation explains why a crop changes the main point but not mechanically these coefficients. The validity of the division by $Z_c$ and the visibility of the point must also be checked; a projected number does not imply that a point is in front of the camera.

### CV-ZHANG-003

**Situation**: How do homographies of a planar target constrain intrinsics in Zhang's method, and why is varying translation alone insufficient?

**Passing constraints to poses**: The linear constraints on the symmetric matrix $B$ are stacked to estimate its six elements to within a scale. After recovering an allowable $K$, columns $K^{-1}h_1$ and $K^{-1}h_2$ give directions of rotation to be normalized with a common scale; the third direction stems from their vector product. Noise generally prevents the resulting matrix from being exactly orthonormal: it must be brought back to $SO(3)$ before the joint refinement. This step is an initialization, not a final estimate of all the distortion. Views repeating the same orientation can leave the constraints almost dependent even if their individual homographies estimate themselves very well.

### CV-ZHANG-004

**Situation**: A calibration reports low reprojection RMS. What does it measure, and which additional validation should be proposed for industrial dimensional measurement?

**Defining the RMS**: with $N$ observations 2D and residuals $e_i=(e_{xi},e_{yi})$, $RMS_{point}=\sqrt{\sum_i(e_{xi}^2+e_{yi}^2)/N}$. A mean per coordinate uses $2N$ at the denominator and is therefore $RMS_{point}/\sqrt2$. The average of the norms and the average of the RMS per view are still other statistics. A score announced without denominator can therefore be incomparable despite the same word RMS. Also present the maps of residuals and the quantiles, then a validation on views and reserved points. When the pose of a reserved view is to be estimated, separate the points that serve that pose from those that evaluate the set parameters.

### CV-ZHANG-005

**Situation**: A calibrated image is resized uniformly by $a$, then cropped by $(b_x,b_y)$ pixels in this new frame. How should intrinsics be adapted without any physical change to the optics?

**Case of pixel centers**: If the tool sets the resize to $u'=a(u+1/2)-1/2$, the transformation also contains the translation $(a-1)/2$; the main point follows the same relationship before the crop. The $u'=au$ simple formula corresponds to another contract. These expressions are analytical cases: they do not describe all libraries. For a different scaling on both axes, multiply the relevant lines of $K$ respectively via the full pixel affine. The factor of the last homogeneous coordinate remains fixed at one per convention. Testing a round trip of multiple points is safer than inferring the affine from the final size of the array alone.

### CV-ZHANG-006

**Situation**: Twenty nearly frontal views yield low RMS, but intrinsics change substantially when a few views are removed. What should be checked, and which new acquisition would be informative?

**Linking acquisition and information**: If two columns of the Jacobian of the residuals are almost dependent, a variation of one parameter can compensate that of another. Small singular values and covariance correlations signal this coupling in the local approximation. Adding views that excite new directions can separate them better than adding twenty copies of a front view. Covering the edge helps constrain terms that grow with distance to the center, but requires well-located corners in that area. A flexible calibration target or systematically biased corners can produce a consistent fit to the wrong model: digital stability and physical adequacy are controlled separately.

### CV-ZHANG-007

**Situation**: For dimensional inspection with a fixed camera, which decisions make target-based calibration usable beyond a demonstration?

**Moving from calibration to measurement on a plan**: with center world camera $C$, radius world direction $d$ and known plane $n^TX=h$, the intersection is $X=C+\lambda d$, where $\lambda=(h-n^TC)/(n^Td)$ if the denominator is non-zero. This geometry shows that a metric measurement also requires the plane or depth of the surface: intrinsics alone are not enough. Near a radius parallel to the plane, the intersection becomes very sensitive to noise. Propagating calibration, edge location and flatness errors in product tolerance, and then comparing to an independent reference. This calculation assumes a known flat surface and a properly dedistorted projection, without certifying a relief measurement.

**Passages consulted for these developments**: [Zhang, TR98-71](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf), §§2 – 4 and Annex C, stresses, poses and degenerations; [OpenCV 4.13, Camera Calibration](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), projection and distortion model; Context7 verification.

## Alternatives, sources and flashcards

For wide angle, evaluate a fisheye model; for several sensors, distinguish intrinsic individual and extrinsic between sensors; for a pose alone, starting from a calibration already known with PnP.

- [Zhang, full report associated with TPAMI 2000][zhang] : §§2 – 4.
- [OpenCV 4.13 `calibrateCamera`][opencv]: Flags, models and expected data.
- [flashcards calibration](../52-calibration-zhang.md).

[zhang]: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf
[opencv]: https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html
