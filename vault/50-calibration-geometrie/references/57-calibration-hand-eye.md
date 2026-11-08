---
id: CV-HANDEYE
type: methode
domaine: d05
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-SE3", "CV-ZHANG"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Hand–eye calibration — solving AX = XB with consistent coordinate frames

## Prerequisites and competencies

**Required prerequisites**: [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md), [CV-ZHANG](52-calibration-zhang.md). **Target competencies**: derive relative movements; respect the direction of the poses API; excite observable directions; test the closing of the chain; distinguish eye-in-hand and eye-to-hand. Related notions remain alternatives, not implicit dependencies.

## Problem and data contract

Estimate the rigid extrinsic between camera and grip a robot in eye-in-hand configuration. The robot moves, the camera is attached to the gripper and the calibration target remains fixed in the base. Convention: $T_{ab}$ sends the coordinates of coordinate frame $b$ to $a$. The poses robot and camera must correspond at the same time, with common translation units. Neither an intrinsic calibration nor an isolated camera – calibration target transformation give this extrinsic.

## Transformation chain and equation

Note $G_i=T_{bg_i}$, $C_i=T_{c_it}$, $X=T_{gc}$ and $Y=T_{bt}$. The fixed chain imposes $G_iXC_i=Y$ for each pose $i$. For two poses $i,j$, put $A_{ij}=G_j^{-1}G_i$ and $B_{ij}=C_jC_i^{-1}$: $A_{ij}X=XB_{ij}$. All are $4\times4$ homogeneous matrices; rotations without unit, translations in m or mm but never mixed. The development gives $R_AR_X=R_XR_B$ and $(R_A-I)t_X=R_Xt_B-t_A$. The order of each product derives from the meaning of the coordinate frames.

## Mechanism, parameters and observability

Some solvers estimate rotation and translation separately; others treat them together, for example with dual quaternions. Compare solutions with a reserved residual on poses, not by name alone. Movements around a single axis or without rotation diversity leave poorly constrained directions. In OpenCV 4.13, `calibrateHandEye` receives gripper→base and target→camera and returns camera→gripper; its documentation requires at least two movements with non-parallel axes of rotation, i.e. three poses, and recommends more views. This minimum does not replace a conditioning diagnosis.

## Cost, synchronization and variants

The cost of the solver is often lower than that of a clean acquisition. Forming all pairs increases the number of equations but the pairs sharing a pose are not independent observations. Check timestamps, poses robot, intrinsics and rolling shutter effect before increasing the number of pairs. In eye-to-hand, the camera is fixed and the chain of unknowns changes: we do not correct the input contract by reversing only the output. No robot or hand-eye solver executed here; the derivation is algebraic.

## Evaluation and controlled variation

For a $X$ candidate, calculate $Y_i=G_iXC_i$ on reserved poses. Measure the dispersion of rotations and translations separately, in announced units, and then a reprojection or useful position error. Proposed variation: keep the number of poses but replace single axis movements with rotations around various axes; predict better conditioning. Introduce a time offset separately to test the sensitivity to synchronization. No physical results are claimed.

## Diagnosis and alternatives

If $Y_i$ varies with the robot pose, check direction of $G_i$, direction of $C_i$, multiplication, units and synchronization. A visually plausible result does not rule out an inversion. If the calibration target moves, the constant $Y$ model is violated. To simultaneously calibrate a robot base and a world of unknown vision, the robot-world/hand-eye problem has other unknowns; do not blindly apply this contract $AX=XB$.

## Guided reasoning and proposed checks

These built cases develop AX=XB conventions, excitation and independent validation. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-HANDEYE-001

**Question of work**: In eye-in-hand calibration, $G_i$ maps gripper to base and $C_i$ maps target to camera. With $X$ mapping camera to gripper and a fixed target, how is $AX=XB$ obtained?

**Reference Response**: The fixed chain is $G_iXC_i=G_jXC_j$. By multiplying left by $G_j^{-1}$ and right by $C_i^{-1}$, we get $A=G_j^{-1}G_i$ and $B=C_jC_i^{-1}$, then $AX=XB$.

**Reading the coordinate frames**: Following a point from the calibration target to the camera, then the tool and the base, the intermediate indices connect. The fixed calibration target requires the final transformation to be constant. The two acquisitions then provide two paths to the same result, hence the relative motion equation.

**check**: check this closure first with consistent synthetic transformations. Then introduce a single inversion of pose to observe the effect on the string residual. This check algebra without ordering a robot or pretending to validate actual captures. A formally recognized equation does not exempt from defining assembly, unknowns and synchronization in the device used.

### Case linked to CV-HANDEYE-005

**Question of work**: Is switching from a gripper-mounted camera to a fixed camera simply a matter of inverting the solver output?

**Reference Response**: No: the fixed coordinate frames and the unknowns of the chain change. Redefine the measured and unknown transformations, write the constant string, and then derive the appropriate equation and input contract.

**Construction of the new problem**: Identify what is attached to the base, what follows the tool, and where the calibration target is located. Then write two paths connecting the same coordinate frames, with a constant unknown transformation only where the assembly justifies it. It is this equality that determines the necessary inverses and relative movements.

**Example of Trap**: A camera that has become fixed no longer has a constant pose camera→ gripper when the tool moves. Reversing this old unknown does not magically transform it into the new constant camera→base. Check the contracts of the solver suitable for mounting and closing on several poses. The reasoning remains a geometric derivation; no robot command or installation validation is performed here.

**Documentary reference for this pass**: [OpenCV 4.13, calibrateHandEye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), CalibrateHandEye, minimum transformations and movements. The other developments are in the [flashcards](../57-calibration-hand-eye.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-HANDEYE-001

**Situation**: In eye-in-hand calibration, $G_i$ maps gripper to base and $C_i$ maps target to camera. With $X$ mapping camera to gripper and a fixed target, how is $AX=XB$ obtained?

**Consistent case generator**: choose rigid transformations $X$ and $Y$, then several poses robot $G_i$. Define synthetic observations by $C_i=X^{-1}G_i^{-1}Y$. We then have exactly $G_iXC_i=Y$ and the derived relative movements satisfy $AX-XB=0$ to the nearest numerical rounding. Then introducing noise on the observations makes it possible to study the sensitivity, but this test first verifies the algebra and conventions. It does not prove that the chosen movements make $X$ identifiable. Use rotations around distinct axes and non-zero translations to avoid a test that would mask product inversions or non-commutativity.

### CV-HANDEYE-002

**Situation**: Which coordinate-frame contract must be checked before calling OpenCV 4.13 calibrateHandEye for an eye-in-hand setup?

**Verification of matrices**: a rotation block must satisfy $R^TR\simeq I$ and $\det R\simeq1$; the last homogeneous line is $(0,0,0,1)$. These conditions control a rigid transformation, not its physical meaning. To reverse it, use $T^{-1}=[R^T,-R^Tt;0,1]$, never the only negation of $t$ when $R$ is non-trivial. Convert all the translations in the same unit before the estimation: mixing meters and millimeters does not correct by a rotation convention. Finally, to distinguish a rotation represented in matrix, axis-angle vector or quaternion; the order of the components and the angle units belong to the interface contract.

### CV-HANDEYE-003

**Situation**: Why can many poses around a single axis produce unstable hand–eye calibration?

**Diagnostic by stacked system**: after estimating $R_X$, stack the $R_{A_k}-I$ blocks to solve the translation. A small singular value of this matrix signals a direction where large variations in translation little change the equations. Its interpretation depends on the noise, the angles actually traveled and the units of the complete system; a simple number of conditions is not a physical certification. The rotation must also be observable, because its errors pass into the second member $R_Xt_{B_k}-t_{A_k}$. To estimate stability by resampling, select whole acquisitions or sequences rather than treating all their pairs as independent samples.

### CV-HANDEYE-004

**Situation**: In an eye-in-hand setup, the camera is rigidly attached to the gripper and the target is fixed in the robot base frame. The estimated extrinsics look plausible, but reconstructed points move when the robot rotates. Which transformation-chain test and possible causes should be checked?

**residual measurable closure**: between two reserved poses, form $E_{ij}=Y_j^{-1}Y_i$. The ideal is identity. Report the norm of its translation in the assembly unit and its angle of rotation, for example $\phi=\arccos(\operatorname{clip}((\operatorname{tr}R_E-1)/2,-1,1))$, in radians. Near digitally sensitive cases, a robust logarithmic representation is preferable. Do not add centimeters and degrees directly: a combined score requires scaling or explicit covariance. Compare these residuals according to speed and amplitude of rotation, then an error on the useful points, because the closure alone does not give the accuracy of the entire measuring chain.

### CV-HANDEYE-005

**Situation**: Is switching from a gripper-mounted camera to a fixed camera simply a matter of inverting the solver output?

**Explicit eye-to-hand channel**: If the camera is fixed in the base and the calibration target is attached to the gripper, note $G_i={}^bT_{g_i}$, $C_i={}^cT_{t_i}$, $X={}^bT_c$ and $Y={}^gT_t$. We have $G_iY=XC_i$, so $G_i^{-1}XC_i=Y$ constant. The shape becomes that of a hand-eye chain using the inverted robot poses, under these precise conventions, and the unknown now corresponds to camera→base. The equation justifies adaptation; reversing only an old exit does not justify it. If the calibration target is not attached to the gripper, this constancy of $Y$ disappears and observations and unknowns must be reformulated before any resolution.

**Passages consulted for these developments**: [OpenCV 4.13.0, calibration hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), calibrateHandEye, coordinate frames, eye-in-hand and eye-to-hand strings and non-parallel axes; algebraic complements of the project.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-HANDEYE-001 — Pose pairing creates correlated relative motions

All relative pairs derived from a small set of absolute poses are not independent observations: pairs sharing a pose share its error. Creating every possible pair can increase equation count without the equivalent number of independent measurements. Report the pairing scheme and evaluate held-out absolute-chain closure. This does not forbid pairwise solvers; it limits how their residual count or naive least-squares covariance should be interpreted.

### CV-HANDEYE-002 — A valid rigid matrix can still have wrong units

A transform with translation in millimeters passes orthogonality, determinant and homogeneous-row checks just as one in meters does. A thousandfold unit mismatch is therefore not a rotation-validity failure. Use a known baseline or target displacement in the same physical chain to check scale, and synchronize paired robot/camera poses. Correct matrix dimensions alone do not establish that they describe the same acquisition or the expected frame direction.

### CV-HANDEYE-003 — Tiny rotations provide weak translation leverage

For a small relative rotation vector $\phi$, $R_A-I\approx[\phi]_\times$. Even when rotation axes vary, very small angles make the translation system coefficients small relative to observation noise. Acquire safe, sufficiently distinct motions with nonparallel axes and retained target visibility. Assess singular values after appropriate scaling and validate at the actual working volume; the minimum pose count establishes algebraic possibility, not useful metrological precision.

### CV-HANDEYE-004 — Closure residuals need separate position and angle scales

For each held-out pose, compute $Y_i=G_iXC_i$ and compare it with a common target-to-base estimate. Report translation deviation in a declared metric unit and rotation deviation as a geodesic angle. Combining them into one scalar requires an explicit weighting or covariance; adding meters to radians has no physical default. Dependence on robot orientation, time or target location can help isolate lever-arm, synchronization or lens-model errors.

### CV-HANDEYE-005 — Write the new invariant before reusing a solver

In eye-to-hand operation with a gripper-fixed target, the invariant is target-to-gripper, while camera-to-base is fixed. Re-derive this chain using named transformations and compare it with the solver's documented eye-to-hand formulation. An inverse of the previous camera-to-gripper result generally describes a different physical relationship. A constructed synthetic pose set with known fixed transforms is an effective contract check before collecting noisy robot data.

Consulted foundations: [OpenCV calibrateHandEye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html): input/output frame directions, eye-in-hand/eye-to-hand equations and minimum motions; checked with Context7.

## Sources and flashcards

- [OpenCV 4.13, CalibrateHandEye, coordinate frames, Equations and Minimum Movements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Solà et al., micro Lie theory, appendix D-A, composition SE(3)](https://arxiv.org/html/1812.01537v9#A4.SS1).
- [Related flashcards](../57-calibration-hand-eye.md): CV-HANDEYE-001 to 005.

Editor: Agent Codex, 2026-10-24. Primary sources consulted and API OpenCV 4.13 verified with Context7. Analytical calculations and proposed protocols are distinguished from experiments; no actual export, video benchmark or independent scientific validation announced.
