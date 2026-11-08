---
id: CV-MULTICALIB
type: methode
domaine: d05
poles: [B, C, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 7
prerequis: ["CV-ZHANG", "CV-SE3", "CV-CAPTEURS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Multisensor calibration, hand–eye calibration and timing

## Problem, data and assumptions

Estimate the transformations between sensors or robot/camera with consistent observations over time. Inputs: poses or measurements with coordinate frames, synchronization and units; output: extrinsic and possibly time offset depending on the model. The intrinsic calibration of each camera is a distinct problem.

## Prerequisites and competencies

**Required prerequisites**: [CV-ZHANG](52-calibration-zhang.md); [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md); [CV-CAPTEURS](../../20-acquisition-images/references/22-capteurs-horodatage.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Combine common observations and informative movements; solve an initialization and then refine and validate on other movements. Hand-eye connects relative movements; calibrating a fixed pose does not replace a synchronization model.

## Mathematics, conventions and units

For a camera carried by the tool and a fixed calibration target in the base, note $G_i={}^bT_{g_i}$ (tool→base), $C_i={} ^{c_i}T_t$ (calibration target→camera) and $X={}^gT_c$ (camera→tool). The equality $G_iXC_i=G_jXC_j$ gives $A_{ij}X=XB_{ij}$ with $A_{ij}=G_j^{-1}G_i$ and $B_{ij}=C_jC_i^{-1}$. This convention corresponds to the eye-in-hand case; changing the assembly requires redefining the chain. Rotations on a single axis and little varied translations can make components poorly observable. Translations follow the same unit of length.

## Parameters and properties

Set tool→base, calibration target→camera and composition order for the above convention. Record clocks, pose time, lever, uncertainties and movement. Do not announce a universal minimum independent of the solver and trajectories.

## Cost and implementation

The collection and diversity of movements often dominate the quality. No robots or sensors are ordered here; the procedures are validation proposals.

## Evaluation and controlled variation

Proposed variation: compare quasi-parallel movements to diversified rotations/positions, with comparable measurement quality. Evaluate the stability of extrinsic and residuals on reserved movements.

## Failure modes and diagnosis

Good still calibration, error in motion: measure timing and deskew. Reverse transformations: track a point through each coordinate frame before optimizing further.

## Alternatives and applications

Common target, targetless methods and joint temporal optimization according to equipment and observability. The robotic control safety remains out of this reference note.

## Guided reasoning and proposed checks

These constructed cases develop separate spatial transformations and desynchronization. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-MULTICALIB-001

**Question of work**: Why is writing $AX=XB$ insufficient to apply hand–eye calibration?

**Reference Response**: We must define the coordinate frames, the relative A/B movements, their meaning and the unknown transformation X.

**derivation per chain**: in eye-in-hand with a fixed calibration target, the composition tool→base, camera→tool then calibration target→camera must give the same pose calibration target→base for each acquisition. The equality of these compositions leads to relative movements on either side of the unknown extrinsic. The meaning of the products is not free: it comes from the adjacent coordinate frames.

**Constructed test**: take a known pose, transform a point from calibration target to the base, and then check the reverse of the string. Repeat with non-trivial rotation and non-zero translations in common units. An identity test can leave inversions invisible. This interface validation precedes the solver setting; if it fails, adding data or changing the optimization method addresses an issue other than the convention error.

### Case linked to CV-MULTICALIB-003

**Question of work**: Why does low intrinsic reprojection error fail to validate camera–LiDAR fusion during motion?

**Reference Response**: It does not alone test the extrinsic between sensors, their temporal offset or the deformation of the scan.

**Separate the Contracts**: Intrinsic links rays and pixels of a camera. The extrinsic connects the axes of the sensors. Time determines which positions of the scene and the wearer are compared. A merger can respect the first contract and violate the other two, especially during a rotation.

**Survey built**: start with motionless observations for check a part of the geometry, then compare translation and rotation by inspecting time by point of the LiDAR and camera capture moment. Separately correct offsets, deskew, and transformations to measure their effect. A translation adjusted for a single speed can hide a delay without generalizing. Reserve a sequence with other moves for final validation. A good camera reprojection remains useful, but it does not test either the simultaneity of the measurements or the entire projection of a cloud towards the image.

**Documentary reference for this pass**: [OpenCV 4.13, Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), projection models and extrinsic composition. The other developments are in the [flashcards](../55-calibration-multicapteurs.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-MULTICALIB-001

**Situation**: Why is writing $AX=XB$ insufficient to apply hand–eye calibration?

**Usable formulation**: Note $G_i={}^bT_{g_i}$, $C_i={} ^{c_i}T_t$ and $X={}^gT_c$, where the top coordinate frame receives the coordinates. The fixed calibration target imposes $G_iXC_i=Y$, with $Y={}^bT_t$ constant. Between two catches, multiply the equality left by $G_j^{-1}$ and right by $C_i^{-1}$ gives $(G_j^{-1}G_i)X=X(C_jC_i^{-1})$. The indices and the assembly therefore determine exactly $A$ and $B$. The case built with translations alone checks the units, but noncommutative rotations are needed to detect many order errors. The $X$ matrix must remain the same on all synchronized captures.

### CV-MULTICALIB-002

**Situation**: Many robot poses around the same axis produce unstable extrinsics. What should be changed?

**Component not constrained**: by developing homogeneous transformations, we obtain $(R_A-I)t_X=R_Xt_B-t_A$. For a rotation around a unit axis $n$, $(R_A-I)n=0$: this equation alone does not determine the component of $t_X$ following $n$. Repeating the same axis leaves this structural defect. Stacking movements of different axes can lift it, subject to a rotation $R_X$ itself correctly estimated. Examine the singular values of this system after scaling and compare the solutions by subsets of poses. A large number of correlated pairs does not transform into as many independent directions of information.

### CV-MULTICALIB-003

**Situation**: Why does low intrinsic reprojection error fail to validate camera–LiDAR fusion during motion?

**Order of temporal magnitude**: in a local rigid displacement model, the deviation of a point expressed in the same coordinate frame is of the order of $\delta p\simeq(v+\omega\times p)\delta t$, with speed $v$ in m/s, angular speed $\omega$ in rad/s and delay $\delta t$ in s. The sign depends on the sense of comparison. At 10 m/s, 20 ms already represent 20 cm of translation; the angular contribution increases with the lever arm. The image projection then adds its Jacobian and depends on the depth. This built-in calculation explains why testing multiple speeds, distances, and direction of rotation helps distinguish a delay from a constant extrinsic.

**Passages consulted for these developments**: [OpenCV 4.13.0, calibration hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), calibrateHandEye, coordinate frames, eye-in-hand and eye-to-hand chains and non-parallel axes; algebraic complements of the project; [Zhang–Singh, LOAM](https://www.roboticsproceedings.org/rss10/p07.pdf), context acquisition in motion; approximation speed, delay and lever arm deduced by the project.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-MULTICALIB-001 — Pair order must change on both sides

From $AX=XB$, reversing the same motion pair gives $A^{-1}X=XB^{-1}$. Inverting only one of the relative motions generally creates another equation with no common true solution. A constructed chain test should generate poses from known $X$ and a fixed target, then verify every relative pair before solving. This catches direction conventions independently of observation noise and the numerical hand-eye method.

### CV-MULTICALIB-002 — Pure translations leave hand-eye translation unconstrained

When $R_A=I$, the translation equation $(R_A-I)t_X=R_Xt_B-t_A$ has a zero left-hand coefficient. Such a motion can constrain the relation between observed translation vectors and rotation, but supplies no direct constraint on $t_X$ through this equation. Adding many pure-translation poses therefore does not replace informative rotations. Evaluate the stacked system's singular directions in the intended movement range.

### CV-MULTICALIB-003 — Static and dynamic tests isolate different contracts

A proposed validation sequence first checks static cross-sensor alignment, then repeats known translations and turns with the same extrinsics. Error proportional to speed or angular rate suggests a timing or deskew problem; persistent static offset instead directs attention toward the spatial chain or projection model. These are diagnostic tendencies, not proofs. Keep clock, timestamp reference and per-point acquisition conventions explicit before refitting a fixed transform.

Consulted foundations: [OpenCV hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html): calibrateHandEye transformation directions and nonparallel-motion requirement; checked with Context7; [LOAM](https://www.roboticsproceedings.org/rss10/p07.pdf): motion distortion and acquisition time.

## Sources and flashcards

- [Zhang – Singh 2014, LOAM, §§II, IV and V-B](https://www.roboticsproceedings.org/rss10/p07.pdf)

- [OpenCV calib3d, calibrateHandEye and robot-world hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Related flashcards](../55-calibration-multicapteurs.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
