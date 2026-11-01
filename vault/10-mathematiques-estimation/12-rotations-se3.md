# Flashcards — SO(3), SE(3) and transformation conventions

reference note: [[10-mathematiques-estimation/references/12-rotations-se3|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-SE3-001

Objective: deal with named coordinate frames. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-001
Question: For two images, a SLAM system provides poses $T_{wc_1}$ and $T_{wc_2}$ that map camera coordinates into the world frame: $p_w=T_{wc_i}\,p_{c_i}$. Which transformation expresses a point known in camera 2 coordinates in camera 1 coordinates?
Reponse: **Expected answer**: $T_{c_1c_2}=T_{wc_1}^{-1}T_{wc_2}=T_{c_1w}T_{wc_2}$: go back from $c_2$ to the world, then from the world to $c_1$. The adjacent indices must coincide ($c_1w$ then $wc_2$); the composition is not commutative.

**Further explanation**: with $T_{ab}=(R_{ab},t_{ab})$, $T_{ab}T_{bc}=(R_{ab}R_{bc},\;t_{ab}+R_{ab}t_{bc})$: the translation $t_{bc}$, expressed in $b$, is rotated in $a$ before addition. check: $T_{c_1c_2}$ originally applied to $c_2$ must give the position of the camera 2 seen from the camera 1. If the poses supplied go from the world to the camera, like `rvec`/`tvec` from OpenCV, the inverses change places: $T_{c_1c_2}=T_{c_1w}T_{c_2w}^{-1}$.

**Constructed example**: with two identical orientations and centers offset on a world axis, the origin point of the second camera must appear at the same offset in the first. Turning only the first camera then makes it necessary to express this shift in its axes. This simple test reveals a translation added in the wrong coordinate frame, which a seemingly valid multiplication of matrices can pass.

**Calculation by blocks**: a homogeneous pose is written $T=\begin{bmatrix}R&t\\0&1\end{bmatrix}$, with $R\in SO(3)$, $t\in\mathbb R^3$ and homogeneous points $[p^T,1]^T$. Its reverse uses $R^T$ and $-R^Tt$. For the two poses on the front, the relative rotation is $R_{wc_1}^TR_{wc_2}$ and the translation is $R_{wc_1}^T(t_{wc_2}-t_{wc_1})$. The latter is the movement between centers re-expressed in the 1 camera, not just a difference in world coordinates. A homogeneous direction vector has a last zero coordinate and must not receive this translation. This check distinguishes the application of a pose at a point of its application to a direction.

**Blocking errors**: calculate $T_{wc_2}T_{wc_1}^{-1}$ or $T_{wc_1}T_{wc_2}$; assume commutative composition.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]] ; [Solà et al., A micro Lie theory, appendix D-A, equations 170 – 171](https://arxiv.org/html/1812.01537v9#A4.SS1).
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SE3-001 provenance::agent pole::B pole::C
END

## CV-SE3-002

Objective: Reverse a rigid pose. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-002
Question: Given $p_c=Rp_w+t$, how do you recover the camera center in world coordinates?
Reponse: **Expected answer**: $C_w=-R^Tt$; the reverse pose is $(R^T,-R^Tt)$.

**Further explanation**: The camera center has zero coordinates in its own coordinate frame. The translation t is therefore not directly its world position.

**derivation step by step**: The optical center is the point that has $p_c=0$ coordinates in the coordinate frame camera. By replacing it in $p_c=Rp_w+t$, we get $RC_w+t=0$, so $C_w=-R^{-1}t=-R^Tt$ for an orthonormal rotation. The inverse of pose uses the same inverse rotation and this translation reexpressed in the world.

**Example interpreted**: if $R=I$ and $t=(1,0,0)^T$ m, the camera center is $(-1,0,0)^T$ m worldwide. The opposite sign comes from the sense world→camera announced. If the camera is turned, changing only the sign without applying $R^T$ gives a position in the wrong axes. Digitally verify that the center found originally projects camera before any perspective division. This convention is fundamental for composing calibration, PnP and trajectory; an extrinsic translation is not a universal position independent of the direction of transformation.

**From Pixel to World Ray**: After removing the distortion, a homogeneous pixel $\tilde u$ defines a camera direction proportional to $K^{-1}\tilde u$, where $K$ is the intrinsic matrix. Worldwide, the radius is written as $p_w(\lambda)=C_w+\lambda R^TK^{-1}\tilde u$, with a scale convention for $\lambda$. The center is its origin, the inverse rotation orients its direction and the depth remains unknown on a single view. This calculation shows the distinct role of the three elements: $t$ participates in the localization of the camera, $R$ in the change of axes and $K$ in the geometry in pixels. None of these elements alone provide the depth of a point.

**Blocking errors**: Simply answer t or −t without rotation.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]] ; [Solà et al., A micro Lie theory, appendix D-A, equations 170 – 171](https://arxiv.org/html/1812.01537v9#A4.SS1).
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-SE3-002 provenance::agent pole::B pole::C
END

## CV-SE3-003

Objective: distinguish between local and global disturbances. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-003
Question: Two implementations of the same cost parameterize rotation increments with a small vector $\delta\theta$ and obtain different Jacobians, both verified by finite differences. Which convention can explain this, how are the two related, and which should you choose?
Reponse: **Expected answer**: one perturbs on the right, $R\operatorname{Exp}(\delta\theta_L)$, with an increment expressed in the local coordinate frame; the other on the left, $\operatorname{Exp}(\delta\theta_G)R$, with an increment in the global coordinate frame. The adjoint connects them: $\operatorname{Exp}(R\,\delta\theta_L)\,R=R\operatorname{Exp}(\delta\theta_L)$, $\delta\theta_G=R\,\delta\theta_L$; Jacobians and covariances are transformed by $R$, for example $J_L=J_GR$. Choose the side where uncertainty is naturally expressed, coordinate frame sensor or coordinate frame world, and announce it.

**Further explanation**: for SO(3), $\mathrm{Ad}_R=R$; for SE(3), the adjoint mixes rotation and translation. Solà defaults to local disruption. A gyroscope covariance is naturally expressed in the sensor coordinate frame, a heading error provided by a GNSS in the world coordinate frame: these examples fall within the reasoning of the project.

**check**: Apply the same small physical displacement to the two parameterizations and compare the transformed point, not just the components of the increments. If the Jacobians have been validated in their respective conventions, their difference can be expected. Any associated covariance must follow the same coordinate change.

**Complete extension to poses**: by ordering increment $\xi=(\rho,\phi)$, translation then rotation, the adjoint of $T=(R,t)$ is $\operatorname{Ad}_T=\begin{bmatrix}R&[t]_\times R\\0&R\end{bmatrix}$, where $[t]_\times a=t\times a$. Switching from a right disturbance to the equivalent left disturbance uses $\xi_G=\operatorname{Ad}_T\xi_L$. A covariance follows $P_G=\operatorname{Ad}_TP_L\operatorname{Ad}_T^T$ in this local approximation. The cross block reflects the fact that a small rotation around another origin also induces a displacement. A simple block-by-block rotation would forget this lever arm effect. The translation/rotation conventions must accompany the matrix to avoid swapping its blocks.

**Blocking errors**: copy a Jacobian without checking where the disturbance is occurring; believe that one of the two conventions is false.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]] ; [Solà et al., A micro Lie theory, §II-E, equations 25 – 28, and §II-F, equations 29 – 32](https://arxiv.org/html/1812.01537v9#S2.SS5) ; [Annex B-C, equation 139](https://arxiv.org/html/1812.01537v9).
Tags: cv::pilote cv::d01 famille::comparaison cv_id::CV-SE3-003 provenance::agent pole::B pole::C
END

## CV-SE3-004

Objective: check a quaternion. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-004
Question: A camera–IMU extrinsic calibration is passed between libraries as a unit quaternion and translation. Reprojection becomes incorrect even though the quaternion norm is 1. Which conventions should be checked, and which test distinguishes them?
Reponse: **Expected answer**: check the order of the components (scalar first or last), the multiplication algebra (Hamilton or JPL), the direction of the transformation (sensor to reference or vice versa) and the axes of the coordinate frames. The unit norm only constrains representation. Test: Transform a point or axis known by the two strings and compare the results, rather than the four numbers.

**Further explanation**: Solà distinguishes between four binary choices: order, algebra, active or passive function, local sense→global or vice versa. Examples: Eigen's `Quaternion(w,x,y,z)` constructor takes the scalar first but stores `[x,y,z,w]`; SciPy's `Rotation.from_quat` assumes the scalar last by default. $q$ and $-q$ represent the same rotation: compare rotations, not components.

**Constructed test**: choose a single quarter-turn rotation and a reference axis, then compare the resulting coordinates in the two libraries. Then add a non-zero translation in order to also test its coordinate frame and its unit. A single identity rotation leaves several errors of order or meaning invisible; it is therefore an insufficient check of the interface.

**check of representation**: A unit quaternion describes a rotation, but its multiplication is noncommutative. In Hamilton convention, an angle $\theta$ around a unit axis $a$ is represented, scalar first, by $(\cos(\theta/2),a\sin(\theta/2))$. This writing makes it possible to build a verifiable quarter turn without converting ambiguous Euler angles. A convention conversion must address the order, signs and meaning of application in a consistent way: swapping the four numbers is not always enough. Test successively the three axes of the base and a translated point makes it possible to verify the entire transformation; normalization does not repair either an inversion of pose or an incompatible product convention.

**Blocking errors**: assimilate four numbers of norm one to a universal convention; conclude two different rotations because $q$ and $-q$ differ.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]]; [Solà, Quaternion kinematics, §3.1, equations 140 – 143 and table 2](https://arxiv.org/abs/1711.02508); [Eigen 5.0.1-dev, Quaternion, constructor (accessed on 2026-10-23)](https://libeigen.gitlab.io/eigen/docs-nightly/classEigen_1_1Quaternion.html); [SciPy 1.18.0, Rotation.from_quat (accessed on 2026-10-23)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_quat.html); [Solà, Quaternion kinematics, §§2.4 and 3.1, quaternion and conventions](https://arxiv.org/html/1711.02508v1), see the 2026-10-30.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SE3-004 provenance::agent pole::B pole::C
END

## CV-SE3-005

Objective: Measuring a rotation gap. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-005
Question: To evaluate an estimated orientation $\hat R$ against ground truth $R$, one report compares Euler angles component by component and another compares quaternions. Which measure should be used instead, and why can both direct comparisons mislead?
Reponse: **Expected answer**: measure the angle of the residual rotation $R^T\hat R$: $\theta=\arccos\frac{\operatorname{tr}(R^T\hat R)-1}{2}$, independent of parameterization. Euler angles depend on convention and are singular: near a pitch of 90°, large yaw and roll gaps compensate. $q$ and $-q$ represent the same rotation: their components may differ from 2 for a zero error; since unit quaternions, use $\theta=2\arccos|\langle q_1,q_2\rangle|$.

**Further explanation**: case calculated by the project: the rotations ZYX $(30°;89{,}9°;0°)$ and $(0°;89{,}9°;-30°)$ differ from 30° on two Euler angles, but their geodetic angle is 0,05°. Block the arccos argument in $[-1,1]$ against rounding. REP 103 advises against Euler angles, which allow 24 "valid" conventions. Do not average Euler angles to aggregate errors.

**Reading the score**: The angular error measures the relative rotation required to align the orientations, not their distance to a particular angle origin. Keep radians and degrees explicit in the calculation and report, and then examine the distribution of errors instead of a single average.

**More robust near-zero calculation**: From a unitary relative quaternion in convention announced, $q_{rel}=(w,v)$, the main angle can be written as $\theta=2\operatorname{atan2}(\|v\|_2,|w|)\in[0,\pi]$. This shape exploits the vector part when the arccos becomes sensitive to rounding near 1. The absolute value processes double coverage, without erasing a true rotation error. Check that the two orientations express the same coordinate frame and the same direction before forming the relative rotation. For aggregations, report also quantiles and extreme cases: a low average error can hide some completely reversed orientations. These expressions give radians; explicitly convert only for display to degrees.

**Blocking errors**: report Euler angle deviations as rotation error; conclude with error because $q$ and $-q$ differ.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]]; [Solà et al., A micro Lie theory, appendix B, double cover and SO log(3), equation 135](https://arxiv.org/html/1812.01537v9); [REP 103, Rotation Representation, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst); calculation and formula by quaternion derived by the project.
Tags: cv::pilote cv::d01 famille::evaluation cv_id::CV-SE3-005 provenance::agent pole::B pole::C
END

## CV-SE3-006

Objective: Convert between camera axis conventions. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SE3-006
Question: A camera pose estimated with OpenCV is passed to an OpenGL renderer and a ROS node. The rendered scene appears upside down or behind the camera. Which axis conventions should be compared, and which transformation relates OpenCV and OpenGL?
Reponse: **Expected answer**: OpenCV place $x$ to the right, $y$ Down and $z$ forward, the visible points having $Z_c>0$ ; in OpenGL, the camera aims $-z$ with $y$ up; ROS places the body in $x$ before, $y$ left, $z$ high, and its coordinate frame `_optical` the Convention ofOpenCV. Moving from OpenCV to OpenGL is like turning 180° around $x$: $M=\mathrm{diag}(1,-1,-1)$, determinant $+1$. To compose poses Homogenised $4\times4$, use $M_h=\mathrm{diag}(1,-1,-1,1)$ To the right of a pose Camera→monde, $T^{gl}_{wc}=T^{cv}_{wc}M_h$, or to the left of a world matrix→camera, $T^{gl}_{cw}=M_hT^{cv}_{cw}$. Check that a known point in front of the camera remains in each convention.

**Further explanation**: at OpenCV, $x'=X_c/Z_c$, then $v=f_yy'+c_y$ with lines of pixels that grow downwards: for $f_y>0$, $Y_c$ points downwards. `gluLookAt` sends the target point on the $-z$ axis and the "high" direction on $+y$. Confusing coordinate frame body and coordinate frame `_optical` in ROS makes the camera aim up or to the side. Reversing a single axis gives a determinant $-1$: it is a reflection, not a rigid coordinate frame transformation.

**Change of bases on both sides**: if $p'_c=B_c p_c$ and $p'_w=B_w p_w$, then a world matrix→camera becomes $T'_{cw}=B_cT_{cw}B_w^{-1}$, using homogeneous matrices $4\times4$. The kernel example changes only the camera base: $B_w=I$, hence the multiplication on the left. Changing the coordinate frame world also requires the second factor. This general rule avoids applying an "OpenGL conversion" without specifying which base changes. Camera coordinate conventions alone do not define clip space projection, depth buffer direction, or the origin of the framebuffer pixels: these additional contracts must be checked separately in the render.

**Blocking errors**: reverse a single axis; apply the conversion on the wrong side of the pose; assume that all libraries share the axes of OpenCV.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp`, pinhole model, l. 94 – 118](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L94-L118); [Khronos, gluLookAt, Description](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml); [REP 103, Axis Orientation and Suffix Frames, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst); diagnosis and composition side deduced by the project; [Solà et al., micro Lie theory, §II-F, adjoint; §II-H, covariances; appendices B and D](https://arxiv.org/html/1812.01537v9), consult the 2026-10-30.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SE3-006 provenance::agent pole::B pole::C
END
