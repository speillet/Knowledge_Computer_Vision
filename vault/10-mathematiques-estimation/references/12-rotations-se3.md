---
id: CV-SE3
type: methode
domaine: d01
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 8
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# SO(3), SE(3) and transformation conventions

## Problem, data and assumptions

Compose poses without mixing transformations, axes or units. Inputs: rotations and translations with coordinate frames named; output: transformed coordinates or compound pose. A homogeneous matrix does not indicate its meaning without an explicit convention.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

A rotation preserves norms and orientation of the base (determinant +1), but generally changes the direction of a vector; a rigid pose adds a translation. Compose in order of coordinate frames, invert algebraically and test a known point. An optimization uses a small three-parameter perturbation for rotation.

## Mathematics, conventions and units

Define $p_a=R_{ab}p_b+t_{ab}$ and $T_{ac}=T_{ab}T_{bc}$, i.e. $(R_{ab}R_{bc},\;t_{ab}+R_{ab}t_{bc})$: $t_{bc}$, expressed in $b$, is rotated in $a$ before addition (Solà et al., equation 171). $R^TR=I$, $\det R=1$; $T^{-1}=(R^T,-R^Tt)$ (equation 170). For a relative pose between two data cameras in the world, $T_{c_1c_2}=T_{wc_1}^{-1}T_{wc_2}$. Translations have a unit of length; small rotations are in radians.

$R'=R\operatorname{Exp}(\delta\theta)$ and $R'=\operatorname{Exp}(\delta\theta)R$ are different local (right) and global (left) perturbations (§II-E, equations 25 – 28). The assistant connects them: $\operatorname{Exp}(\mathrm{Ad}_R\,\delta\theta_L)R=R\operatorname{Exp}(\delta\theta_L)$, with $\mathrm{Ad}_R=R$ for SO(3) (§II-F, equations 29 – 32; appendix B-C, equation 139). A Jacobian compared to the local increment is therefore $J_L=J_GR$. `Exp` takes a vector of $\mathbb R^3$; `exp` takes the antisymmetric matrix $[\delta\theta]_\times$.

## Parameters and properties

Specify the order of the components of the quaternion, active/passive convention and standardization. Solà (Quaternion kinematics, §3.1, equations 140 – 143) distinguishes four binary choices: order of components, algebra $ij=k$ or $ij=-k$, active or passive function, local sense →global or inverse. His 2 table pitted Hamilton against JPL; his §3.1.1 classed Eigen as Hamilton despite its scalar storage last. On the implementation side, the manufacturer `Quaternion(w,x,y,z)` Eigen 's 5.0.1-dev takes the scalar first but stores `[x,y,z,w]` ; `Rotation.from_quat` SciPy 1.18.0 Suppose the scalar is last except `scalar_first=True`. A quaternion has four components and three degrees of freedom; $q$ and $-q$ represent the same rotation (micro Lie theory, Appendix B). Euler angles have parameterization singularities.

## Cost and implementation

Basic operations cost little; convention errors have an effect on all sensors. Illustrative pseudocode: name the coordinate frames → dial → verify identity/inverse → test a point; no group library is executed.

## Evaluation and controlled variation

Analytical variation: reverse the order of two non-parallel rotations. Predict a different pose; check on a known axis. Then test that a transformation followed by its inverse returns the point, to numerical tolerance.

Measure a rotation error by the residual rotation angle: $\theta=\arccos\frac{\operatorname{tr}(R^T\hat R)-1}{2}$, the angle of $\operatorname{Log}(R^T\hat R)$ (micro Lie theory, appendix B-A, equation 135). Since unit quaternions, $\theta=2\arccos|\langle q_1,q_2\rangle|$; the absolute value absorbs the double coverage, formula derived by the project. Bound the arccos argument in $[-1,1]$; near $\theta=0$, the arccos of the trace loses precision, and the log or quaternion formula are preferred.

Controlled variation, calculated the 2026-10-23 excluding deposit (NumPy 2.2.6, SciPy 1.13.1). Baseline: Euler ZYX angle component-by-component deviation. Varied factor: the measure, with identical rotations. Prediction: divergence near the pitch of 90°. Result: $(30°;89{,}9°;0°)$ and $(0°;89{,}9°;-30°)$ differ from 30° on two angles, against 0,052° in geodesic angle; $q$ and $-q$ are at Euclidean distance 2 for a zero angle. Constructed cases, not system measures.

## Failure modes and diagnosis

Objects rotating in the wrong direction: check axes, degrees/radians and inversion. A visually plausible pose is not enough; check points coordinate frames and extrinsic composition.

Camera axis conventions. OpenCV projects $x'=X_c/Z_c$, $y'=Y_c/Z_c$ (`calib3d.hpp` 4.13.0, l. 94 – 118): Visible points have $Z_c>0$, and with $v=f_yy'+c_y$ and lines growing downwards, $Y_c$ points downwards, project deduction. ROS (REP 103) fixes the body in $x$ front, $y$ left, $z$ top; its coordinate frame `_optical` place $z$ front, $x$ right, $y$ bottom, as OpenCV. In OpenGL, `gluLookAt` sends the target point on the axis $-z$ and the direction "high" on $+y$. Switching from OpenCV to OpenGL is therefore equivalent to applying $M=\mathrm{diag}(1,-1,-1)$, rotation of 180° around $x$ and determinant $+1$. For homogeneous poses $4\times4$, use $M_h=\mathrm{diag}(1,-1,-1,1)$: $T^{gl}_{wc}=T^{cv}_{wc}M_h$ and $V^{gl}=M_h\,T^{cv}_{cw}$. $M$ acts on vectors 3D; $M_h$ acts on homogeneous coordinates. Symptoms: Scene behind the camera or image flipped. A single axis inversion, of determinant $-1$, is a reflection. Test: A known point in front of the camera must remain so after conversion.

## Alternatives and applications

Matrices for composition, quaternions for storage/interpolation, tangential coordinates for optimization; do not mix their Jacobians without transformation.

## Guided reasoning and proposed checks

These constructed cases develop coordinate frames composition and left/right disturbances. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-SE3-001

**Question of work**: For two images, a SLAM system provides poses $T_{wc_1}$ and $T_{wc_2}$ that map camera coordinates into the world frame: $p_w=T_{wc_i}\,p_{c_i}$. Which transformation expresses a point known in camera 2 coordinates in camera 1 coordinates?

**Reference Response**: $T_{c_1c_2}=T_{wc_1}^{-1}T_{wc_2}=T_{c_1w}T_{wc_2}$: go back from $c_2$ to the world, then from the world to $c_1$. The adjacent indices must coincide ($c_1w$ then $wc_2$); the composition is not commutative.

**Constructed example**: with two identical orientations and centers offset on a world axis, the origin point of the second camera must appear at the same offset in the first. Turning only the first camera then makes it necessary to express this shift in its axes. This simple test reveals a translation added in the wrong coordinate frame, which a seemingly valid multiplication of matrices can pass.

### Case linked to CV-SE3-005

**Question of work**: To evaluate an estimated orientation $\hat R$ against ground truth $R$, one report compares Euler angles component by component and another compares quaternions. Which measure should be used instead, and why can both direct comparisons mislead?

**Reference Response**: measure the angle of the residual rotation $R^T\hat R$: $\theta=\arccos\frac{\operatorname{tr}(R^T\hat R)-1}{2}$, independent of parameterization. Euler angles depend on convention and are singular: near a pitch of 90°, large yaw and roll gaps compensate. $q$ and $-q$ represent the same rotation: their components may differ from 2 for a zero error; since unit quaternions, use $\theta=2\arccos|\langle q_1,q_2\rangle|$.

**Reading the score**: The angular error measures the relative rotation required to align the orientations, not their distance to a particular angle origin. Keep radians and degrees explicit in the calculation and report, and then examine the distribution of errors instead of a single average.

**Documentary reference for this pass**: [Solà et al., micro Lie theory](https://arxiv.org/html/1812.01537v9), §II, disturbances and uncertainties; Annex D, SE(3). The other developments are in the [flashcards](../12-rotations-se3.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-SE3-001

**Situation**: For two images, a SLAM system provides poses $T_{wc_1}$ and $T_{wc_2}$ that map camera coordinates into the world frame: $p_w=T_{wc_i}\,p_{c_i}$. Which transformation expresses a point known in camera 2 coordinates in camera 1 coordinates?

**Calculation by blocks**: a homogeneous pose is written $T=\begin{bmatrix}R&t\\0&1\end{bmatrix}$, with $R\in SO(3)$, $t\in\mathbb R^3$ and homogeneous points $[p^T,1]^T$. Its reverse uses $R^T$ and $-R^Tt$. For the two poses on the front, the relative rotation is $R_{wc_1}^TR_{wc_2}$ and the translation is $R_{wc_1}^T(t_{wc_2}-t_{wc_1})$. The latter is the movement between centers re-expressed in the 1 camera, not just a difference in world coordinates. A homogeneous direction vector has a last zero coordinate and must not receive this translation. This check distinguishes the application of a pose at a point of its application to a direction.

### CV-SE3-002

**Situation**: Given $p_c=Rp_w+t$, how do you recover the camera center in world coordinates?

**From Pixel to World Ray**: After removing the distortion, a homogeneous pixel $\tilde u$ defines a camera direction proportional to $K^{-1}\tilde u$, where $K$ is the intrinsic matrix. Worldwide, the radius is written as $p_w(\lambda)=C_w+\lambda R^TK^{-1}\tilde u$, with a scale convention for $\lambda$. The center is its origin, the inverse rotation orients its direction and the depth remains unknown on a single view. This calculation shows the distinct role of the three elements: $t$ participates in the localization of the camera, $R$ in the change of axes and $K$ in the geometry in pixels. None of these elements alone provide the depth of a point.

### CV-SE3-003

**Situation**: Two implementations of the same cost parameterize rotation increments with a small vector $\delta\theta$ and obtain different Jacobians, both verified by finite differences. Which convention can explain this, how are the two related, and which should you choose?

**Complete extension to poses**: by ordering increment $\xi=(\rho,\phi)$, translation then rotation, the assistant of $T=(R,t)$ is $\operatorname{Ad}_T=\begin{bmatrix}R&[t]_\times R\\0&R\end{bmatrix}$, where $[t]_\times a=t\times a$. Switching from a right disturbance to the equivalent left disturbance uses $\xi_G=\operatorname{Ad}_T\xi_L$. A covariance follows $P_G=\operatorname{Ad}_TP_L\operatorname{Ad}_T^T$ in this local approximation. The cross block reflects the fact that a small rotation around another origin also induces a displacement. A simple block-by-block rotation would forget this lever arm effect. The translation/rotation conventions must accompany the matrix to avoid swapping its blocks.

### CV-SE3-004

**Situation**: A camera–IMU extrinsic calibration is passed between libraries as a unit quaternion and translation. Reprojection becomes incorrect even though the quaternion norm is 1. Which conventions should be checked, and which test distinguishes them?

**check of representation**: A unit quaternion describes a rotation, but its multiplication is noncommutative. In Hamilton convention, an angle $\theta$ around a unit axis $a$ is represented, scalar first, by $(\cos(\theta/2),a\sin(\theta/2))$. This writing makes it possible to build a verifiable quarter turn without converting ambiguous Euler angles. A convention conversion must address the order, signs and meaning of application in a consistent way: swapping the four numbers is not always enough. Test successively the three axes of the base and a translated point makes it possible to verify the entire transformation; normalization does not repair either an inversion of pose or an incompatible product convention.

### CV-SE3-005

**Situation**: To evaluate an estimated orientation $\hat R$ against ground truth $R$, one report compares Euler angles component by component and another compares quaternions. Which measure should be used instead, and why can both direct comparisons mislead?

**More robust near-zero calculation**: From a unitary relative quaternion in convention announced, $q_{rel}=(w,v)$, the main angle can be written as $\theta=2\operatorname{atan2}(\|v\|_2,|w|)\in[0,\pi]$. This shape exploits the vector part when the arccos becomes sensitive to rounding near 1. The absolute value processes double coverage, without erasing a true rotation error. Check that the two orientations express the same coordinate frame and the same direction before forming the relative rotation. For aggregations, report also quantiles and extreme cases: a low average error can hide some completely reversed orientations. These expressions give radians; explicitly convert only for display to degrees.

### CV-SE3-006

**Situation**: A camera pose estimated with OpenCV is passed to an OpenGL renderer and a ROS node. The rendered scene appears upside down or behind the camera. Which axis conventions should be compared, and which transformation relates OpenCV and OpenGL?

**Change of bases on both sides**: if $p'_c=B_c p_c$ and $p'_w=B_w p_w$, then a world matrix→camera becomes $T'_{cw}=B_cT_{cw}B_w^{-1}$, using homogeneous matrices $4\times4$. The kernel example changes only the camera base: $B_w=I$, hence the multiplication on the left. Changing the coordinate frame world also requires the second factor. This general rule avoids applying an "OpenGL conversion" without specifying which base changes. Camera coordinate conventions alone do not define clip space projection, depth buffer direction, or the origin of the framebuffer pixels: these additional contracts must be checked separately in the render.

**Passages consulted for these developments**: [Solà et al., micro Lie theory](https://arxiv.org/html/1812.01537v9), §II-F, deputy; §II-H, covariances; appendices B and D; [Solà, Quaternion kinematics](https://arxiv.org/html/1711.02508v1), §§2.4 and 3.1, quaternion and conventions.

## Sources and flashcards

- [Solà et al., A micro Lie theory, appendix D-A, equations 170 – 171](https://arxiv.org/html/1812.01537v9#A4.SS1).
- [Solà et al., A micro Lie theory, §II-E, equations 25 – 28, §II-F, equations 29 – 32, appendix B and equation 139](https://arxiv.org/html/1812.01537v9#S2.SS5).

- [Solà, Quaternion kinematics, §3.1, equations 140 – 143 and table 2](https://arxiv.org/abs/1711.02508).
- [Eigen 5.0.1-dev, Quaternion (accessed on 2026-10-23)](https://libeigen.gitlab.io/eigen/docs-nightly/classEigen_1_1Quaternion.html): constructor and storage order.
- [SciPy 1.18.0, Rotation.from_quat (accessed on 2026-10-23)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_quat.html): Last scalar order by default.
- [OpenCV 4.13.0, `calib3d.hpp`, pinhole model, l. 94 – 118, and `solvePnP`, l. 1031 – 1032](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L94-L118): Documentation HTML page denies automated access, source header to tag has been read.
- [REP 103, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst) : Axis Orientation, Suffix Frames, Rotation Representation.
- [Khronos, gluLookAt, Description](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml).
- [Related flashcards](../12-rotations-se3.md): CV-SE3-001 to 006.

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project. Revisions 3 and 4: self-review `revue-cartes` by Agent Claude Code on 2026-10-23, corrections and enrichments accepted by the learner, without independent validation.
