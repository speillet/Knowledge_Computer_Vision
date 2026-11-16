# Flashcards — SO(3), SE(3) and transformation conventions

reference note: [[10-mathematiques-estimation/references/12-rotations-se3|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-SE3-001

Objective: Compose transforms between named coordinate frames. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-001
Question: For two images, a SLAM system provides poses $T_{wc_1}$ and $T_{wc_2}$ that map camera coordinates into the world frame: $p_w=T_{wc_i}\,p_{c_i}$. Which transformation expresses a point known in camera 2 coordinates in camera 1 coordinates?
Reponse: **Expected answer**: $T_{c_1c_2}=T_{wc_1}^{-1}T_{wc_2}=T_{c_1w}T_{wc_2}$: go back from $c_2$ to the world, then from the world to $c_1$. The adjacent indices must coincide ($c_1w$ then $wc_2$); the composition is not commutative.

**Further explanation**: with $T_{ab}=(R_{ab},t_{ab})$, $T_{ab}T_{bc}=(R_{ab}R_{bc},\;t_{ab}+R_{ab}t_{bc})$: the translation $t_{bc}$, expressed in $b$, is rotated in $a$ before addition. Check: $T_{c_1c_2}$ applied to the origin of $c_2$ must give the position of camera 2 seen from camera 1. If the poses supplied go from the world to the camera, like `rvec`/`tvec` from OpenCV, the inverses change places: $T_{c_1c_2}=T_{c_1w}T_{c_2w}^{-1}$.

**Constructed example**: with two identical orientations and centers offset on a world axis, the origin point of the second camera must appear at the same offset in the first. Turning only the first camera then makes it necessary to express this shift in its axes. This simple test reveals a translation added in the wrong coordinate frame, which a seemingly valid multiplication of matrices can pass.

**Calculation by blocks**: a homogeneous pose is written $T=\begin{bmatrix}R&t\\0&1\end{bmatrix}$, with $R\in SO(3)$, $t\in\mathbb R^3$ and homogeneous points $[p^T,1]^T$. Its inverse uses $R^T$ and $-R^Tt$. For the two poses of the question, the relative rotation is $R_{wc_1}^TR_{wc_2}$ and the translation is $R_{wc_1}^T(t_{wc_2}-t_{wc_1})$. The latter is the movement between centers re-expressed in camera 1, not just a difference in world coordinates. A homogeneous direction vector has a last zero coordinate and must not receive this translation. This check distinguishes applying a pose to a point from applying it to a direction.

**Composition checked by a round trip**: Use a constructed case with $R_{wc_1}=R_z(90^\circ)$, $t_{wc_1}=0$, $R_{wc_2}=I$ and $t_{wc_2}=(1,0,0)^T$ m. Camera 2's origin has coordinates $(0,-1,0)^T$ m in camera 1. Mapping it back with $T_{wc_1}$ must recover $(1,0,0)^T$ m. Nonzero translation and nonidentity rotation expose order errors that two identity poses cannot reveal.

**Blocking errors**: computing $T_{wc_2}T_{wc_1}^{-1}$ or $T_{wc_1}T_{wc_2}$; assuming commutative composition.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]] ; [Solà et al., A micro Lie theory, appendix D-A, equations 170 – 171](https://arxiv.org/html/1812.01537v9#A4.SS1). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SE3-001 provenance::agent pole::B pole::C
END

## CV-SE3-002

Objective: Invert a rigid pose. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-002
Question: Given $p_c=Rp_w+t$, how do you recover the camera center in world coordinates?
Reponse: **Expected answer**: $C_w=-R^Tt$; the inverse pose is $(R^T,-R^Tt)$.

**Further explanation**: The camera center has zero coordinates in its own coordinate frame. The translation t is therefore not directly its world position.

**Step-by-step derivation**: The optical center is the point whose coordinates are $p_c=0$ in the camera frame. By replacing it in $p_c=Rp_w+t$, we get $RC_w+t=0$, so $C_w=-R^{-1}t=-R^Tt$ for an orthonormal rotation. The inverse pose uses the inverse rotation and this translation re-expressed in the world frame.

**Worked example**: if $R=I$ and $t=(1,0,0)^T$ m, the camera center is $(-1,0,0)^T$ m in world coordinates. The opposite sign comes from the stated world→camera direction. If the camera is turned, changing only the sign without applying $R^T$ gives a position in the wrong axes. Numerically verify that the recovered center maps to the camera origin before any perspective division. This convention is fundamental for composing calibration, PnP and trajectory; an extrinsic translation is not a universal position independent of the direction of transformation.

**From pixel to world ray**: After removing the distortion, a homogeneous pixel $\tilde u$ defines a camera direction proportional to $K^{-1}\tilde u$, where $K$ is the intrinsic matrix. In world coordinates, the ray is written as $p_w(\lambda)=C_w+\lambda R^TK^{-1}\tilde u$, with a scale convention for $\lambda$. The center is its origin, the inverse rotation orients its direction and the depth remains unknown on a single view. This calculation shows the distinct role of the three elements: $t$ participates in the localization of the camera, $R$ in the change of axes and $K$ in the geometry in pixels. None of these elements alone provide the depth of a point.

**The optical center does not project to an image pixel**: At $C_w=-R^Tt$, the camera-space point is exactly zero. Its perspective projection requires division by $Z_c=0$ and is undefined. Therefore verify the center using the rigid transform before perspective division, rather than checking a pixel coordinate. Conversely, a point on a viewing ray with positive camera depth projects correctly, but different depths share that pixel. This separates a valid pose-inversion test from an invalid projection test at the optical center.

**Blocking errors**: answering $t$ or $-t$ without the rotation.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]] ; [Solà et al., A micro Lie theory, appendix D-A, equations 170 – 171](https://arxiv.org/html/1812.01537v9#A4.SS1). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-SE3-002 provenance::agent pole::B pole::C
END

## CV-SE3-003

Objective: Distinguish local and global perturbations. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-003
Question: Two implementations of the same cost parameterize rotation increments with a small vector $\delta\theta$ and obtain different Jacobians, both verified by finite differences. Which convention can explain this, how are the two related, and which should you choose?
Reponse: **Expected answer**: one perturbs on the right, $R\operatorname{Exp}(\delta\theta_L)$, with an increment expressed in the local coordinate frame; the other on the left, $\operatorname{Exp}(\delta\theta_G)R$, with an increment in the global coordinate frame. The adjoint connects them: $\operatorname{Exp}(R\,\delta\theta_L)\,R=R\operatorname{Exp}(\delta\theta_L)$, $\delta\theta_G=R\,\delta\theta_L$; Jacobians and covariances are transformed by $R$, for example $J_L=J_GR$. Choose the side where uncertainty is naturally expressed, sensor frame or world frame, and state it.

**Further explanation**: for SO(3), $\mathrm{Ad}_R=R$; for SE(3), the adjoint mixes rotation and translation. Solà uses local perturbations by default. A gyroscope covariance is naturally expressed in the sensor frame, a heading error provided by a GNSS in the world frame: these examples fall within the reasoning of the project. Library example: Ceres 2.2.0's `QuaternionManifold` applies its increment on the left, $\exp(\Delta)\otimes x$, and its $\Delta$ is half the rotation vector, so comparing it with a right-perturbation Jacobian needs both the adjoint and a factor of 2.

**Discriminating check**: Apply the same small physical displacement to the two parameterizations and compare the transformed point, not just the components of the increments. If the Jacobians have been validated in their respective conventions, their difference can be expected. Any associated covariance must follow the same coordinate change.

**Complete extension to poses**: by ordering increment $\xi=(\rho,\phi)$, translation then rotation, the adjoint of $T=(R,t)$ is $\operatorname{Ad}_T=\begin{bmatrix}R&[t]_\times R\\0&R\end{bmatrix}$, where $[t]_\times a=t\times a$. Switching from a right perturbation to the equivalent left perturbation uses $\xi_G=\operatorname{Ad}_T\xi_L$. A covariance follows $P_G=\operatorname{Ad}_TP_L\operatorname{Ad}_T^T$ in this local approximation. The cross block reflects the fact that a small rotation around another origin also induces a displacement. A simple block-by-block rotation would forget this lever arm effect. The translation/rotation conventions must accompany the matrix to avoid swapping its blocks.

**The same perturbation produces the same point change**: For $y=Rp$ and a right perturbation, the first-order change is $\delta y=-R[p]_\times\delta\theta_L$. Under a left perturbation it is $\delta y=-[Rp]_\times\delta\theta_G$. Substituting $\delta\theta_G=R\delta\theta_L$ makes the two identical. A finite-difference test should therefore perturb the same physical rotation before comparing outputs. Equal numeric increment components in different frames generally represent different motions.

**Blocking errors**: copying a Jacobian without checking on which side the perturbation is applied; believing that one of the two conventions is wrong.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]] ; [Solà et al., A micro Lie theory, §II-E, equations 25 – 28, and §II-F, equations 29 – 32](https://arxiv.org/html/1812.01537v9#S2.SS5) ; [Appendix B-C, equation 139](https://arxiv.org/html/1812.01537v9); [Ceres 2.2.0, `manifold.cc` L27–L60, `QuaternionPlusImpl`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/internal/ceres/manifold.cc#L27-L60). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::comparaison cv_id::CV-SE3-003 provenance::agent pole::B pole::C
END

## CV-SE3-004

Objective: check a quaternion. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-004
Question: A camera–IMU extrinsic calibration is passed between libraries as a unit quaternion and translation. Reprojection becomes incorrect even though the quaternion norm is 1. Which conventions should be checked, and which test distinguishes them?
Reponse: **Expected answer**: check the order of the components (scalar first or last), the multiplication algebra (Hamilton or JPL), the direction of the transformation (sensor to reference or vice versa) and the axes of the coordinate frames. The unit norm only constrains representation. Test: transform a known point or axis with both toolchains and compare the results, rather than the four numbers.

**Further explanation**: Solà distinguishes four binary choices: component order, algebra, active or passive function, and local-to-global direction or the reverse. Examples: Eigen's `Quaternion(w,x,y,z)` constructor takes the scalar first but stores `[x,y,z,w]`; SciPy's `Rotation.from_quat` assumes the scalar last by default. $q$ and $-q$ represent the same rotation: compare rotations, not components.

**Constructed test**: choose a single quarter-turn rotation and a reference axis, then compare the resulting coordinates in the two libraries. Then add a non-zero translation in order to also test its coordinate frame and its unit. A single identity rotation leaves several errors of order or meaning invisible; it is therefore an insufficient check of the interface.

**Representation check**: A unit quaternion describes a rotation, but its multiplication is noncommutative. In Hamilton convention, an angle $\theta$ around a unit axis $a$ is represented, scalar first, by $(\cos(\theta/2),a\sin(\theta/2))$. This writing makes it possible to build a verifiable quarter turn without converting ambiguous Euler angles. A convention conversion must address the order, signs and meaning of application in a consistent way: swapping the four numbers is not always enough. Testing the three basis axes in turn and a translated point verifies the whole transformation; normalization does not repair either an inversion of pose or an incompatible product convention.

**A round trip can preserve a shared mistake**: Two conversion routines that apply the same mistaken inverse can pass a round-trip test while both disagree with the sensor contract. Include an independently constructed axis-angle example, such as the Hamilton active rotation $q=(\sqrt2/2,0,0,\sqrt2/2)$ taking $e_x$ to $e_y$. Then compose two rotations about different axes. This second check exposes multiplication-order differences that testing one quaternion and its inverse may leave invisible.

**Blocking errors**: treating four numbers of unit norm as a universal convention; concluding that two rotations differ because $q$ and $-q$ differ.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]]; [Solà, Quaternion kinematics, §3.1, equations 140 – 143 and table 2](https://arxiv.org/abs/1711.02508); [Eigen 5.0.1-dev, Quaternion, constructor (accessed on 2026-10-23)](https://libeigen.gitlab.io/eigen/docs-nightly/classEigen_1_1Quaternion.html); [SciPy 1.18.0, Rotation.from_quat (accessed on 2026-10-23)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_quat.html); [Solà, Quaternion kinematics, §§2.4 and 3.1, quaternion and conventions](https://arxiv.org/html/1711.02508v1), consulted 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SE3-004 provenance::agent pole::B pole::C
END

## CV-SE3-005

Objective: Measure a rotation difference. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-005
Question: To evaluate an estimated orientation $\hat R$ against ground truth $R$, one report compares Euler angles component by component and another compares quaternions. Which measure should be used instead, and why can both direct comparisons mislead?
Reponse: **Expected answer**: measure the angle of the residual rotation $R^T\hat R$: $\theta=\arccos\frac{\operatorname{tr}(R^T\hat R)-1}{2}$, independent of parameterization. Euler angles depend on convention and are singular: near a pitch of 90°, large yaw and roll differences compensate each other. $q$ and $-q$ represent the same rotation: their components can be at Euclidean distance 2 for a zero error; for unit quaternions, use $\theta=2\arccos|\langle q_1,q_2\rangle|$.

**Further explanation**: case computed by the project: the ZYX rotations $(30°,89.9°,0°)$ and $(0°,89.9°,-30°)$ differ by 30° on two Euler angles, but their geodesic angle is 0.05°. Clamp the arccos argument to $[-1,1]$ against rounding. REP 103 advises against Euler angles, which allow 24 "valid" conventions. Do not average Euler angles to aggregate errors.

**Reading the score**: The angular error measures the relative rotation required to align the orientations, not their distance to a particular angle origin. Keep radians and degrees explicit in the calculation and report, and then examine the distribution of errors instead of a single average.

**More robust near-zero calculation**: From a unit relative quaternion in a stated convention, $q_{rel}=(w,v)$, the principal angle can be written as $\theta=2\operatorname{atan2}(\|v\|_2,|w|)\in[0,\pi]$. This form uses the vector part when the arccos becomes sensitive to rounding near 1. The absolute value handles the double cover, without erasing a true rotation error. Check that the two orientations express the same coordinate frame and the same direction before forming the relative rotation. For aggregations, report also quantiles and extreme cases: a low average error can hide some completely reversed orientations. These expressions give radians; explicitly convert only for display to degrees.

**Symmetry belongs to the evaluation contract**: The geodesic angle compares coordinate-frame orientations. If an object is physically indistinguishable after a half-turn, the raw angle may penalize an equivalent object pose; evaluating that application requires minimizing over its declared symmetry group. Do not silently apply this quotient to camera orientation, where a reversed optical axis is usually a real error. Parameterization invariance and task-specific symmetry invariance are separate properties of an evaluation measure.

**Blocking errors**: reporting Euler-angle differences as rotation error; concluding that there is an error because $q$ and $-q$ differ.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]]; [Solà et al., A micro Lie theory, appendix B, double cover and SO log(3), equation 135](https://arxiv.org/html/1812.01537v9); [REP 103, Rotation Representation, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst); calculation and formula by quaternion derived by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::evaluation cv_id::CV-SE3-005 provenance::agent pole::B pole::C
END

## CV-SE3-006

Objective: Convert between camera axis conventions. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-006
Question: A camera pose estimated with OpenCV is passed to an OpenGL renderer and a ROS node. The rendered scene appears upside down or behind the camera. Which axis conventions should be compared, and which transformation relates OpenCV and OpenGL?
Reponse: **Expected answer**: OpenCV places $x$ to the right, $y$ down and $z$ forward, visible points having $Z_c>0$; in OpenGL, the camera looks along $-z$ with $y$ up; ROS places the body frame with $x$ forward, $y$ left, $z$ up, and its `_optical` frame follows the OpenCV convention. Moving from OpenCV to OpenGL is a 180° rotation about $x$: $M=\mathrm{diag}(1,-1,-1)$, determinant $+1$. To compose homogeneous $4\times4$ poses, use $M_h=\mathrm{diag}(1,-1,-1,1)$ on the right of a camera→world pose, $T^{gl}_{wc}=T^{cv}_{wc}M_h$, or on the left of a world→camera matrix, $T^{gl}_{cw}=M_hT^{cv}_{cw}$. Check that a known point in front of the camera remains in front in each convention.

**Further explanation**: in OpenCV, $x'=X_c/Z_c$, then $v=f_yy'+c_y$ with pixel rows increasing downwards: for $f_y>0$, $Y_c$ points downwards. `gluLookAt` sends the target point on the $-z$ axis and the "high" direction on $+y$. Confusing the body frame and the `_optical` frame in ROS makes the camera aim up or to the side. Reversing a single axis gives a determinant $-1$: it is a reflection, not a rigid coordinate frame transformation.

**Change of bases on both sides**: if $p'_c=B_c p_c$ and $p'_w=B_w p_w$, then a world matrix→camera becomes $T'_{cw}=B_cT_{cw}B_w^{-1}$, using homogeneous matrices $4\times4$. The core example changes only the camera basis: $B_w=I$, hence the multiplication on the left. Changing the world frame also requires the second factor. This general rule avoids applying an "OpenGL conversion" without specifying which base changes. Camera coordinate conventions alone do not define clip space projection, depth buffer direction, or the origin of the framebuffer pixels: these additional contracts must be checked separately in the render.

**Handedness and visibility are separate tests**: The matrix $M=\operatorname{diag}(1,-1,-1)$ preserves lengths and handedness because $M^TM=I$ and $\det M=1$. A camera-space point $(0,0,2)^T$ becomes $(0,0,-2)^T$: it remains in front according to each convention, despite the sign change of depth. A single-axis reflection also preserves lengths, so checking distances alone misses a handedness error. Use an oriented basis and a point with positive source-camera depth.

**Blocking errors**: flipping a single axis; applying the conversion on the wrong side of the pose; assuming that all libraries share OpenCV's axes.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp`, pinhole model, l. 94 – 118](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L94-L118); [Khronos, gluLookAt, Description](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml); [REP 103, Axis Orientation and Suffix Frames, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst); diagnosis and composition side deduced by the project; [Solà et al., micro Lie theory, §II-F, adjoint; §II-H, covariances; appendices B and D](https://arxiv.org/html/1812.01537v9), consulted 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SE3-006 provenance::agent pole::B pole::C
END

## CV-SE3-007

Objective: Calculate a transported SE(3) covariance and interpret its coupling. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-007
Question: A visual–inertial filter estimates the IMU body pose $T_{wb}$, which maps body coordinates to world coordinates, $p_w=R_{wb}p_b+t_{wb}$, with mean rotation $R_{wb}=R_z(90^\circ)$. Its uncertainty is a covariance on a right (body-frame) increment, $T_{wb}=\bar T_{wb}\operatorname{Exp}(\tau_b)$ with $\tau_b=(\rho_b,\theta_b)$, translation first: $\Sigma_b=\operatorname{diag}(\sigma_\rho^2I_3,\sigma_\theta^2I_3)$, $\sigma_\rho=2$ mm, $\sigma_\theta=0.01$ rad. A camera is rigidly mounted with an exactly known extrinsic $T_{bc}$: $R_{bc}=I$, $t_{bc}=(0.5,0,0)^T$ m. A colleague passes $\Sigma_b$ unchanged to a module expecting the covariance of $T_{wc}=T_{wb}T_{bc}$ on the camera's own right increment $\tau_c$. (a) Compute that covariance: translation standard deviations and nonzero translation–rotation cross-covariances. (b) Interpret the coupling and what the copy loses. (c) What does the translation block of the result describe, and what are the camera-position standard deviations along the world axes?
Reponse: **Expected answer**: (1) The camera increment is $\tau_c=\mathrm{Ad}_{T_{cb}}\tau_b$ with $T_{cb}=T_{bc}^{-1}$, the Jacobian of $T_{wb}T_{bc}$ with respect to $T_{wb}$, so $\Sigma_c=\mathrm{Ad}_{T_{cb}}\Sigma_b\mathrm{Ad}_{T_{cb}}^T$. In general $\rho_c=R_{bc}^T(\rho_b+\theta_b\times t_{bc})$ and $\theta_c=R_{bc}^T\theta_b$; here $\rho_c=(\rho_x,\ \rho_y+0.5\,\theta_z,\ \rho_z-0.5\,\theta_y)$. Translation standard deviations: 2 mm along $x$ and $\sqrt{4\cdot10^{-6}+2.5\cdot10^{-5}}$ m $\approx5.39$ mm along $y$ and $z$; the rotation block stays $10^{-4}I_3$ rad²; $\operatorname{cov}(\rho_y,\theta_z)=+5\cdot10^{-5}$ m·rad and $\operatorname{cov}(\rho_z,\theta_y)=-5\cdot10^{-5}$ m·rad. (2) A body rotation error moves the camera by $\theta_b\times t_{bc}$: perpendicular to the arm and zero for a rotation about it, so nothing is added along $x$; a positive yaw pushes a camera at $+x$ toward $+y$, hence the positive sign. Each lateral position shares one error source with a rotation, with correlation $+0.93$ for $(\rho_y,\theta_z)$ and $-0.93$ for $(\rho_z,\theta_y)$: a perfectly known yaw would bring $\sigma_y$ back to 2 mm. The copy keeps 2 mm on every axis and no correlation, understating the $y$ and $z$ standard deviations by a factor of 2.7. (3) $\rho_c$ is a tangent coordinate in camera axes: to first order, the displacement of the camera origin in those axes, whereas $\rho_b$ described the body origin. For world axes, rotate it: $\Sigma_{t_{wc}}\approx R_{wc}\Sigma_{c,\rho\rho}R_{wc}^T$; with $R_{wc}=R_z(90^\circ)$, 5.39, 2 and 5.39 mm along world $x$, $y$, $z$.

**Further explanation**: The identity $T_{cb}\operatorname{Exp}(\tau_b)T_{bc}=\operatorname{Exp}(\mathrm{Ad}_{T_{cb}}\tau_b)$ holds for any increment, so with an exact extrinsic the transport is a linear map of the tangent vector, not a linearization. The approximation enters when $\rho_c$ is read as a displacement: the camera origin moves by $V(\theta_c)\rho_c$ in camera axes. For a body yaw of 0.01 rad, $\rho_c=(0,5,0)$ mm exactly, while the origin moves by $(-0.025,4.99992,0)$ mm. $\Sigma_c$ does not depend on $\bar T_{wb}$; only the world reading uses $R_{wc}=R_{wb}R_{bc}$.

**Discriminating checks**: $\mathrm{Ad}_{T_{bc}}$ gives the same variances here but flips both cross-covariance signs; perturb the body yaw and confirm that the camera moves toward $+y$. An uncertain, independent extrinsic adds its own covariance unchanged to first order, because the Jacobian with respect to $T_{bc}$ is the identity. A rotation-first library such as GTSAM `Pose3`, ordered $[\omega,v]$, stores the same blocks swapped.

**Global increments are not origin displacements**: on a left (world-frame) increment, body and camera share one covariance, $\mathrm{Ad}_{T_{wc}}\Sigma_c\mathrm{Ad}_{T_{wc}}^T=\mathrm{Ad}_{T_{wb}}\Sigma_b\mathrm{Ad}_{T_{wb}}^T$, because its translation moves the point at the world origin. For this camera placed at $t_{wc}=(100,0,0)$ m, that block shows about 1 m of standard deviation along world $y$ and $z$, while the camera position is known to a few millimetres. Constructed example; every number is recomputed by the check script of this pass.

**Blocking errors**: Copying or only rotating $\Sigma_b$. Adding standard deviations (7 mm) instead of variances. Using $\mathrm{Ad}_{T_{bc}}$, which flips the coupling signs. Reading the translation block as a world-axis position or as the body origin's displacement.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]]; [Solà et al., A micro Lie theory, §II-H, eq. 51–55: tangent covariance and its adjoint transport](https://arxiv.org/html/1812.01537v9#S2.SS8); [§II-F, eq. 29–34: adjoint](https://arxiv.org/html/1812.01537v9#S2.SS6); [§III-B, eq. 65–66: composition Jacobians](https://arxiv.org/html/1812.01537v9#S3.SS2.SSS2); [App. D, eq. 172–178 and 181–182: SE(3) exponential, adjoint, composition and action Jacobians](https://arxiv.org/html/1812.01537v9#A4.SS3); [GTSAM 4.2, `Pose3.h` L138–L141: rotation-first tangent order](https://github.com/borglab/gtsam/blob/4.2/gtsam/geometry/Pose3.h#L138-L141). The lever-arm scenario and its numbers are project constructions.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SE3-007 provenance::agent pole::B pole::C
END
