# Flashcards — Hand–eye calibration — solving AX = XB with consistent coordinate frames

reference note: [[50-calibration-geometrie/references/57-calibration-hand-eye|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-HANDEYE-001

Objective: Derive the relative motions. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-001
Question: In eye-in-hand calibration, $G_i$ maps gripper to base and $C_i$ maps target to camera. With $X$ mapping camera to gripper and a fixed target, how is $AX=XB$ obtained?
Reponse: **Expected answer**: The fixed chain is $G_iXC_i=G_jXC_j$. Multiplying on the left by $G_j^{-1}$ and on the right by $C_i^{-1}$ gives $A=G_j^{-1}G_i$ and $B=C_jC_i^{-1}$, hence $AX=XB$.

**Further explanation**: The homogeneous matrices are $4\times4$ and all translations use the same unit. Changing the definition of $A$ or $B$ requires redoing the derivation; memorizing products without coordinate frames promotes silent inversions.

**Reading the coordinate frames**: Following a point from the calibration target to the camera, then the tool and the base, the intermediate indices connect. The fixed calibration target requires the final transformation to be constant. The two acquisitions then provide two paths to the same result, hence the relative motion equation.

**Discriminating check**: Check this closure first with consistent synthetic transformations. Then introduce a single pose inversion and observe its effect on the chain residual. This checks the algebra without commanding a robot or claiming to validate real captures. A formally recognized equation does not exempt one from defining the mounting, unknowns and synchronization of the actual device.

**Consistent case generator**: Choose rigid transformations $X$ and $Y$, then several robot poses $G_i$. Define synthetic observations by $C_i=X^{-1}G_i^{-1}Y$. Then $G_iXC_i=Y$ holds exactly and the derived relative motions satisfy $AX-XB=0$ up to numerical rounding. Adding noise to the observations then makes it possible to study the sensitivity, but this test first verifies the algebra and conventions. It does not prove that the chosen motions make $X$ identifiable. Use rotations about distinct axes and non-zero translations to avoid a test that would mask product inversions or non-commutativity.

**Pose pairing creates correlated relative motions**: All relative pairs derived from a small set of absolute poses are not independent observations: pairs sharing a pose share its error. Creating every possible pair can increase equation count without the equivalent number of independent measurements. Report the pairing scheme and evaluate held-out absolute-chain closure. This does not forbid pairwise solvers; it limits how their residual count or naive least-squares covariance should be interpreted.

**Blocking errors**: Swapping products arbitrarily; mixing relative motions and absolute poses.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L2322–L2335, eye-in-hand derivation](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2322-L2335); [OpenCV 4.13.0, `calibration_handeye.cpp` L279–L322, all pairs $i<j$](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration_handeye.cpp#L279-L322). Synthetic generator and pairing case: project deductions.
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-HANDEYE-001 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-002

Objective: Respect the direction of poses in the API. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-002
Question: Which coordinate-frame contract must be checked before calling OpenCV 4.13 calibrateHandEye for an eye-in-hand setup?
Reponse: **Expected answer**: Provide the poses gripper→base and calibration target→camera for the same acquisitions; the output is camera→gripper. Also check rotation order, translation units and synchronization.

**Further explanation**: The pose supplied by solvePnP for a calibration target is usually object/calibration target→camera. The robot controller convention may be the opposite of what is expected. Test the entire chain on a known point before comparing the values of the final matrix.

**Why the output is surprising**: The camera→gripper transformation expresses where the camera is located relative to the tool. To get camera→base at a given pose, it must still be composed with the pose of the tool in the base; this overall transformation varies when the robot moves.

**Proposed interface check**: Choose an observation, follow a point calibration target→camera→gripper→base, then compare with the same calibration target observed from another pose. Keep a single unit for all translations. A controller can store the inverse pose or another rotation convention; a matrix of correct shape does not ensure compatibility. This test links the API function to the actual mount, instead of interpreting the output as a universal pose.

**Matrix checks**: A rotation block must satisfy $R^TR\simeq I$ and $\det R\simeq1$; the last homogeneous row is $(0,0,0,1)$. These conditions check a rigid transformation, not its physical meaning. To invert it, use $T^{-1}=[R^T,-R^Tt;0,1]$, never the negation of $t$ alone when $R$ is non-trivial. Convert all translations to the same unit before estimation: a rotation convention cannot correct a mix of metres and millimetres. Finally, distinguish a rotation represented as a matrix, an axis-angle vector or a quaternion; the order of the components and the angle units belong to the interface contract.

**A valid rigid matrix can still have wrong units**: A transform with translation in millimeters passes orthogonality, determinant and homogeneous-row checks just as one in meters does. A thousandfold unit mismatch is therefore not a rotation-validity failure. Use a known baseline or target displacement in the same physical chain to check scale, and synchronize paired robot/camera poses. Correct matrix dimensions alone do not establish that they describe the same acquisition or the expected frame direction.

**Blocking errors**: Interpreting the output as base→camera; using inverted robot poses without adapting the chain.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L2210–L2233, input and output directions](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2210-L2233); [OpenCV 4.13.0, `calib3d.hpp` L1031–L1032, `solvePnP` direction](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L1031-L1032). Matrix and unit checks: project deductions.
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-HANDEYE-002 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-003

Objective: Excite the observable directions. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-003
Question: Why can many poses around a single axis produce unstable hand–eye calibration?
Reponse: **Expected answer**: The number does not replace the diversity of motions: some components remain weakly constrained. Acquire rotations about non-parallel axes and poses covering the useful volume, and then examine the conditioning and a held-out validation.

**Further explanation**: OpenCV documents a minimum of two motions with non-parallel rotation axes, i.e. three poses, while recommending more data. The theoretical minimum is not a sufficient industrial protocol. Pairs drawn from the same poses are correlated.

**Example of insufficient repetition**: Multiplying the poses around a single axis can make very many equations from the same directions of motion. The volume of data then increases without removing any ambiguities. Covariance or dispersion calculated by assuming these independent pairs may also seem overly optimistic.

**Constructed verification**: Keep a held-out set with other axes and positions, then compare the chain closures obtained from several training subsets. A significant variation of the extrinsic despite a small fitting residual signals a lack of information or a violated assumption. Also examine pose quality, timing and rigidity before concluding that a particular solver is responsible.

**Stacked-system diagnosis**: After estimating $R_X$, stack the $R_{A_k}-I$ blocks to solve for the translation. A small singular value of this matrix signals a direction in which large changes of translation barely change the equations. Its interpretation depends on the noise, the angles actually covered and the units of the complete system; a condition number alone is not a physical certification. The rotation must also be observable, because its errors enter the right-hand side $R_Xt_{B_k}-t_{A_k}$. To estimate stability by resampling, select whole acquisitions or sequences rather than treating all their pairs as independent samples.

**Tiny rotations provide weak translation leverage**: For a small relative rotation vector $\phi$, $R_A-I\approx[\phi]_\times$. Even when rotation axes vary, very small angles make the translation system coefficients small relative to observation noise. Acquire safe, sufficiently distinct motions with nonparallel axes and retained target visibility. Assess singular values after appropriate scaling and validate at the actual working volume; the minimum pose count establishes algebraic possibility, not useful metrological precision.

**OpenCV's default solver discards small motions**: In OpenCV 4.13, the Tsai path keeps only motion pairs whose rotation lies between about 17° and 116°; with fewer than two such pairs it logs an error and returns the identity rotation and a zero translation instead of raising an exception. A pose plan with only small rotations can therefore fail silently.

**Blocking errors**: Treating all pose pairs as that many independent observations.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]]; [Horaud and Dornaika 1995, §3, eqs. 18–19](https://arxiv.org/abs/2311.12655); [OpenCV 4.13.0, `calib3d.hpp` L2352–L2353](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2352-L2353); [OpenCV 4.13.0, `calibration_handeye.cpp` L307–L336, Tsai motion filter](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration_handeye.cpp#L307-L336). Stacked-system diagnosis: project deduction.
Tags: cv::pilote cv::d05 famille::conception cv_id::CV-HANDEYE-003 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-004

Objective: Test the closing of the chain. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-004
Question: In an eye-in-hand setup, the camera is rigidly attached to the gripper and the target is fixed in the robot base frame. The estimated extrinsics look plausible, but reconstructed points move when the robot rotates. Which transformation-chain test and possible causes should be checked?
Reponse: **Expected answer**: Let $G_i$ be the gripper→base transformation, $C_i$ calibration target→camera and $X$ camera→gripper, all homogeneous and with common translation units. Compute $Y_i=G_iXC_i$ on several held-out poses: the fixed calibration target must give a consistent calibration target→base transformation. If it varies, check inversions, units, timestamps, intrinsics and rigidity of the calibration target.

**Further explanation**: Compare rotations and translations in their units before aggregating them. Repeating the experiment with a motionless robot and then in motion helps to isolate a delay. The test is proposed by the project; it does not automatically locate a single cause.

**Reading the test**: If the calibration target is really fixed, its pose in the base must not follow the rotation of the gripper. A variation of $Y_i$ reveals a disagreement in the entire chain, even when the numbers of $X$ seem plausible. This consistency tests a physical property, not a numerical preference.

**Proposed investigation**: Compare static poses, then motions of different directions and speeds, and inspect angular and translation errors separately. An error that appears mainly in motion is compatible with a delay, but can also combine several defects. Validation on held-out poses limits the risk of explaining only the fitting acquisitions.

**Measurable closure residual**: Between two held-out poses, form $E_{ij}=Y_j^{-1}Y_i$. The ideal is the identity. Report the norm of its translation in the mounting unit and its rotation angle, for example $\phi=\arccos(\operatorname{clip}((\operatorname{tr}R_E-1)/2,-1,1))$, in radians. In numerically sensitive cases, a robust logarithm is preferable. Do not add centimetres and degrees directly: a combined score requires scaling or an explicit covariance. Compare these residuals as a function of speed and rotation amplitude, then an error on the points of interest, because closure alone does not give the accuracy of the entire measuring chain.

**Closure residuals need separate position and angle scales**: For each held-out pose, compute $Y_i=G_iXC_i$ and compare it with a common target-to-base estimate. Report translation deviation in a declared metric unit and rotation deviation as a geodesic angle. Combining them into one scalar requires an explicit weighting or covariance; adding meters to radians has no physical default. Dependence on robot orientation, time or target location can help isolate lever-arm, synchronization or lens-model errors.

**Blocking errors**: Validating only on the appearance of X; correcting a timing error by arbitrarily adjusting the extrinsic.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L2322–L2335](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2322-L2335). Closure test and residual metrics: project deductions.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-HANDEYE-004 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-005

Objective: Distinguish between eye-in-hand and eye-to-hand. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-005
Question: Is switching from a gripper-mounted camera to a fixed camera simply a matter of inverting the solver output?
Reponse: **Expected answer**: No: the fixed coordinate frames and the unknowns of the chain change. Redefine the measured and unknown transformations, write the constant chain, and then derive the appropriate equation and input contract.

**Further explanation**: In eye-in-hand, camera→gripper is fixed. In eye-to-hand, it is camera→base that is fixed, while the relationship of the calibration target with the gripper depends on the mounting. Reversing a single matrix without rebuilding relationships can give a numerically valid but physically false result.

**Construction of the new problem**: Identify what is attached to the base, what follows the tool, and where the calibration target is located. Then write two paths connecting the same coordinate frames, with a constant unknown transformation only where the mounting justifies it. It is this equality that determines the necessary inverses and relative motions.

**Example of a trap**: A camera that has become fixed no longer has a constant camera→gripper pose when the tool moves. Inverting this old unknown does not turn it into the new constant camera→base. Check the solver contract for this mounting and the chain closure on several poses. The reasoning remains a geometric derivation; no robot command or installation validation is performed here.

**Explicit eye-to-hand chain**: If the camera is fixed in the base and the calibration target is attached to the gripper, write $G_i={}^bT_{g_i}$, $C_i={}^cT_{t_i}$, $X={}^bT_c$ and $Y={}^gT_t$. Then $G_iY=XC_i$, so $G_i^{-1}XC_i=Y$ is constant. The problem takes the form of a hand–eye chain with inverted robot poses, under these precise conventions, and the unknown now corresponds to camera→base. The equation justifies the adaptation; inverting only the old output does not. If the calibration target is not attached to the gripper, the constancy of $Y$ disappears and observations and unknowns must be reformulated before any solution.

**Blocking errors**: Reusing the same inputs and inverting only the output.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L2245–L2250 and L2336–L2346, eye-to-hand configuration and chain](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2336-L2346).
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-HANDEYE-005 provenance::agent pole::B pole::C pole::E
END
