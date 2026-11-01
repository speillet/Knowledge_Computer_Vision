# Flashcards — Hand–eye calibration — solving AX = XB with consistent coordinate frames

reference note: [[50-calibration-geometrie/references/57-calibration-hand-eye|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-HANDEYE-001

Objective: drift the relative movements. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-001
Question: In eye-in-hand calibration, $G_i$ maps gripper to base and $C_i$ maps target to camera. With $X$ mapping camera to gripper and a fixed target, how is $AX=XB$ obtained?
Reponse: **Expected answer**: The fixed chain is $G_iXC_i=G_jXC_j$. By multiplying left by $G_j^{-1}$ and right by $C_i^{-1}$, we get $A=G_j^{-1}G_i$ and $B=C_jC_i^{-1}$, then $AX=XB$.

**Further explanation**: The homogeneous matrices are $4\times4$ and all translations use the same unit. Changing the definition of $A$ or $B$ requires redoing the derivation; memorizing products without coordinate frames promotes silent inversions.

**Reading the coordinate frames**: Following a point from the calibration target to the camera, then the tool and the base, the intermediate indices connect. The fixed calibration target requires the final transformation to be constant. The two acquisitions then provide two paths to the same result, hence the relative motion equation.

**check**: check this closure first with consistent synthetic transformations. Then introduce a single inversion of pose to observe the effect on the string residual. This check algebra without ordering a robot or pretending to validate actual captures. A formally recognized equation does not exempt from defining assembly, unknowns and synchronization in the device used.

**Consistent case generator**: choose rigid transformations $X$ and $Y$, then several poses robot $G_i$. Define synthetic observations by $C_i=X^{-1}G_i^{-1}Y$. We then have exactly $G_iXC_i=Y$ and the derived relative movements satisfy $AX-XB=0$ to the nearest numerical rounding. Then introducing noise on the observations makes it possible to study the sensitivity, but this test first verifies the algebra and conventions. It does not prove that the chosen movements make $X$ identifiable. Use rotations around distinct axes and non-zero translations to avoid a test that would mask product inversions or non-commutativity.

**Blocking errors**: Arbitrarily swap products; mix relative movements and absolute poses.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]] ; [OpenCV 4.13, CalibrateHandEye, coordinate frames, Equations and Minimum Movements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-HANDEYE-001 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-002

Objective: respect the meaning of the poses API. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-002
Question: Which coordinate-frame contract must be checked before calling OpenCV 4.13 calibrateHandEye for an eye-in-hand setup?
Reponse: **Expected answer**: Provide the poses gripper→base and calibration target→camera for the same acquisitions; the output is camera→gripper. Also check rotation order, translation units and synchronization.

**Further explanation**: The pose supplied by solvePnP for a calibration target is usually object/calibration target→camera. The robot controller convention may be the opposite of what is expected. Test the entire chain on a known point before comparing the values of the final matrix.

**Why the exit is surprising**: The camera→gripper transformation expresses where the camera is located relative to the tool. To get camera→base at a given pose, it is still necessary to deal with the pose of the tool in the base; this overall transformation varies when the robot moves.

**check interface proposed**: choose an observation, follow a point calibration target→camera→gripper→base, then compare with the same calibration target observed from another pose. Keep a single unit for all translations. A controller can store the inverse pose or another rotation convention; a matrix of correct shape does not ensure compatibility. This test links the API function to the actual mount, instead of interpreting the output as a universal pose.

**Verification of matrices**: a rotation block must satisfy $R^TR\simeq I$ and $\det R\simeq1$; the last homogeneous line is $(0,0,0,1)$. These conditions control a rigid transformation, not its physical meaning. To reverse it, use $T^{-1}=[R^T,-R^Tt;0,1]$, never the only negation of $t$ when $R$ is non-trivial. Convert all the translations in the same unit before the estimation: mixing meters and millimeters does not correct by a rotation convention. Finally, to distinguish a rotation represented in matrix, axis-angle vector or quaternion; the order of the components and the angle units belong to the interface contract.

**Blocking errors**: Interpret the output as base→camera; use the poses robot upside down without adapting the chain.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]] ; [OpenCV 4.13, CalibrateHandEye, coordinate frames, Equations and Minimum Movements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-HANDEYE-002 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-003

Objective: Exciting the observable directions. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-003
Question: Why can many poses around a single axis produce unstable hand–eye calibration?
Reponse: **Expected answer**: The number does not replace the diversity of movements: some components remain little constrained. Acquire rotations around non-parallel axes and poses covering the useful volume, and then examine conditioning and reserved validation.

**Further explanation**: OpenCV documents a minimum of two non-parallel axis movements, or three poses, while recommending more data. The theoretical minimum is not a sufficient industrial protocol. Pairs drawn from the same poses are correlated.

**Example of insufficient repetition**: multiplying the poses around a single axis can make very many equations from the same directions of motion. The volume of data then increases without removing any ambiguities. Covariance or dispersion calculated by assuming these independent pairs may also seem overly optimistic.

**Verification built**: Keep a reserved set with other axes and positions, then compare closed strings obtained from multiple learning subsets. A significant variation of the extrinsic despite a small adjustment residual signals a lack of information or a breached hypothesis. Also examine pose quality, timing and rigidity before concluding that a particular solver is responsible.

**Diagnostic by stacked system**: after estimating $R_X$, stack the $R_{A_k}-I$ blocks to solve the translation. A small singular value of this matrix signals a direction where large variations in translation little change the equations. Its interpretation depends on the noise, the angles actually traveled and the units of the complete system; a simple number of conditions is not a physical certification. The rotation must also be observable, because its errors pass into the second member $R_Xt_{B_k}-t_{A_k}$. To estimate stability by resampling, select whole acquisitions or sequences rather than treating all their pairs as independent samples.

**Blocking errors**: Assimilate all pairs of poses to as many independent observations.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]] ; [OpenCV 4.13, CalibrateHandEye, coordinate frames, Equations and Minimum Movements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::conception cv_id::CV-HANDEYE-003 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-004

Objective: Test the closing of the chain. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-004
Question: In an eye-in-hand setup, the camera is rigidly attached to the gripper and the target is fixed in the robot base frame. The estimated extrinsics look plausible, but reconstructed points move when the robot rotates. Which transformation-chain test and possible causes should be checked?
Reponse: **Expected answer**: Note $G_i$ the gripper→base transformation, $C_i$ calibration target→camera and $X$ camera →gripper, all homogeneous and with common translation units. Calculate $Y_i=G_iXC_i$ on several reserved poses: the fixed calibration target must give a coherent transformation calibration target→base. If it varies, check inversions, units, timestamps, intrinsics and rigidity of the calibration target.

**Further explanation**: Compare rotations and translations in their units before aggregating them. Repeating the experiment with a motionless robot and then in motion helps to isolate a delay. The test is proposed by the project; it does not automatically locate a single cause.

**Reading the test**: if the calibration target is really fixed, its pose in the base must not follow the rotation of the gripper. A variation of $Y_i$ reveals a disagreement in the entire string, even when the numbers of $X$ seem plausible. This consistency tests a physical property, not a numerical preference.

**Proposed investigation**: compare static poses, then different direction and speed movements, and separately inspect angular error and translation. An error that appears mainly in motion is compatible with a delay, but can also combine several defects. Validation on reserved poses limits the risk of explaining only adjustment acquisitions.

**residual measurable closure**: between two reserved poses, form $E_{ij}=Y_j^{-1}Y_i$. The ideal is identity. Report the norm of its translation in the assembly unit and its angle of rotation, for example $\phi=\arccos(\operatorname{clip}((\operatorname{tr}R_E-1)/2,-1,1))$, in radians. Near digitally sensitive cases, a robust logarithmic representation is preferable. Do not add centimeters and degrees directly: a combined score requires scaling or explicit covariance. Compare these residuals according to speed and amplitude of rotation, then an error on the useful points, because the closure alone does not give the accuracy of the entire measuring chain.

**Blocking errors**: Validate only on the appearance of X; correct a time error by arbitrarily adjusting the extrinsic.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]] ; [OpenCV 4.13, CalibrateHandEye, coordinate frames, Equations and Minimum Movements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-HANDEYE-004 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-005

Objective: Distinguish between eye-in-hand and eye-to-hand. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-HANDEYE-005
Question: Is switching from a gripper-mounted camera to a fixed camera simply a matter of inverting the solver output?
Reponse: **Expected answer**: No: the fixed coordinate frames and the unknowns of the chain change. Redefine the measured and unknown transformations, write the constant string, and then derive the appropriate equation and input contract.

**Further explanation**: In eye-in-hand, camera→ gripper is fixed. In eye-to-hand, it is camera→base that is fixed, while the relationship of the calibration target with the gripper depends on the mounting. Reversing a single matrix without rebuilding relationships can give a numerically valid but physically false result.

**Construction of the new problem**: Identify what is attached to the base, what follows the tool, and where the calibration target is located. Then write two paths connecting the same coordinate frames, with a constant unknown transformation only where the assembly justifies it. It is this equality that determines the necessary inverses and relative movements.

**Example of Trap**: A camera that has become fixed no longer has a constant pose camera→ gripper when the tool moves. Reversing this old unknown does not magically transform it into the new constant camera→base. Check the contracts of the solver suitable for mounting and closing on several poses. The reasoning remains a geometric derivation; no robot command or installation validation is performed here.

**Explicit eye-to-hand channel**: If the camera is fixed in the base and the calibration target is attached to the gripper, note $G_i={}^bT_{g_i}$, $C_i={}^cT_{t_i}$, $X={}^bT_c$ and $Y={}^gT_t$. We have $G_iY=XC_i$, so $G_i^{-1}XC_i=Y$ constant. The shape becomes that of a hand-eye chain using the inverted robot poses, under these precise conventions, and the unknown now corresponds to camera→base. The equation justifies adaptation; reversing only an old exit does not justify it. If the calibration target is not attached to the gripper, this constancy of $Y$ disappears and observations and unknowns must be reformulated before any resolution.

**Blocking errors**: Reuse the same inputs and reverse only the output.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Full reference]] ; [OpenCV 4.13, CalibrateHandEye, coordinate frames, Equations and Minimum Movements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-HANDEYE-005 provenance::agent pole::B pole::C pole::E
END
