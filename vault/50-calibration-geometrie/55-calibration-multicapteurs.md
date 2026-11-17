# Flashcards — Multisensor calibration, hand–eye calibration and timing

reference note: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-MULTICALIB-001

Objective: Interpret hand-eye calibration. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-MULTICALIB-001
Question: Why is writing $AX=XB$ insufficient to apply hand–eye calibration?
Reponse: **Expected answer**: The coordinate frames, the relative motions A and B, their direction and the unknown transformation X must be defined.

**Further explanation**: Check the chain of transformations on a point and on held-out motions; different conventions give different equations.

**Derivation from the chain**: In eye-in-hand with a fixed calibration target, the composition tool→base, camera→tool and then calibration target→camera must give the same calibration target→base pose for each acquisition. Equating these compositions places relative motions on either side of the unknown extrinsic. The direction of the products is not free: it comes from the adjacent coordinate frames.

**Constructed test**: Take a known pose, transform a point from the calibration target to the base, and then check the inverse chain. Repeat with a non-trivial rotation and non-zero translations in common units. An identity test can leave inversions invisible. This interface validation precedes solver tuning; if it fails, adding data or changing the optimization method addresses a problem other than the convention error.

**Usable formulation**: Write $G_i={}^bT_{g_i}$, $C_i={}^{c_i}T_t$ and $X={}^gT_c$, where the upper-left frame receives the coordinates. The fixed calibration target imposes $G_iXC_i=Y$, with $Y={}^bT_t$ constant. Between two captures, multiplying the equality on the left by $G_j^{-1}$ and on the right by $C_i^{-1}$ gives $(G_j^{-1}G_i)X=X(C_jC_i^{-1})$. The indices and the mounting therefore determine $A$ and $B$ exactly. A constructed case with translations alone checks the units, but non-commuting rotations are needed to detect many order errors. The matrix $X$ must remain the same over all synchronized captures.

**Pair order must change on both sides**: From $AX=XB$, reversing the same motion pair gives $A^{-1}X=XB^{-1}$. Inverting only one of the relative motions generally creates another equation with no common true solution. A constructed chain test should generate poses from known $X$ and a fixed target, then verify every relative pair before solving. This catches direction conventions independently of observation noise and the numerical hand-eye method.

**Blocking errors**: Passing an API's matrices without checking their direction and meaning.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L2210–L2353, `calibrateHandEye` frames and eye-in-hand chain](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2210-L2353). Chain test and pair-order case: project deductions.
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-MULTICALIB-001 provenance::agent pole::B pole::C pole::E
END

## CV-MULTICALIB-002

Objective: Evaluate informative movements. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MULTICALIB-002
Question: Many robot poses around the same axis produce unstable extrinsics. What should be changed?
Reponse: **Expected answer**: Examine observability and vary rotations/positions that constrain missing components.

**Further explanation**: Compare stability and validation on another trajectory, without treating the raw number of poses as proof.

**Observability intuition**: Repeating a similar movement averages noise down, but does not necessarily add newly constrained directions. Some components of the extrinsic can then vary greatly without much change in the observed equations. All pairs built from the same poses also remain correlated.

**Proposed acquisition**: Compare, with comparable numbers of poses, a single-axis trajectory and a trajectory with various rotation axes, within the physical limits of the device. Keep calibration-target quality and synchronization controlled, and then check the chain on a held-out path. If the instability persists, also look for a timestamp or robot pose error. A diversity of motions is a source of information; it does not guarantee that every other calibration hypothesis is correct. The final criterion remains stability and useful error in the operating volume.

**Unconstrained component**: Expanding the homogeneous transformations gives $(R_A-I)t_X=R_Xt_B-t_A$. For a rotation about a unit axis $n$, $(R_A-I)n=0$: this equation alone does not determine the component of $t_X$ along $n$. Repeating the same axis leaves this structural defect. Stacking motions about different axes can remove it, provided the rotation $R_X$ is itself correctly estimated. Examine the singular values of this system after scaling and compare the solutions obtained on subsets of poses. A large number of correlated pairs does not transform into as many independent directions of information.

**Pure translations leave hand-eye translation unconstrained**: When $R_A=I$, the translation equation $(R_A-I)t_X=R_Xt_B-t_A$ has a zero left-hand coefficient. Such a motion can constrain the relation between observed translation vectors and rotation, but supplies no direct constraint on $t_X$ through this equation. Adding many pure-translation poses therefore does not replace informative rotations. Evaluate the stacked system's singular directions in the intended movement range.

**Which components drift**: The rotation equation $R_AR_X=R_XR_B$ gives $n_A=R_Xn_B$ [Horaud and Dornaika §3, eq. 18]. When every axis is parallel to $n_A$, all motions repeat this one constraint, so a separable solver's rotation step leaves $R_X$ free about $n_A$, while the translation equation leaves $t_X$ free along $n_A$. If the stations differ only by a wrist roll, $n_A$ is the tool axis and the camera's offset along it is unobserved. Discriminating check: express the spread of $X$ over pose subsets in a frame whose third axis is $n_A$. An observability defect concentrates in the rotation about that axis and the translation along it; a spread over all components, or one that grows with robot speed, points instead to pose noise or timing.

**Constructed example** (recomputed in the check script of this pass): for 20 motions of 30° about $z$, the stacked $(R_A-I)$ has singular values 2.31, 2.31 and 0, whatever the number of motions. Replacing two of them by 30° motions about $x$ keeps the count and gives 2.31, 2.20 and 0.73: the system becomes full rank. OpenCV 4.13's default Tsai path solves both of its systems with `solve(..., DECOMP_SVD)` and only checks that two pairs pass its angle filter, so a single-axis plan returns an estimate without any warning. A ground vehicle that only turns about its vertical axis has the same defect for a camera–IMU or camera–LiDAR extrinsic estimated from motion: its vertical lever arm needs pitch and roll excitation or an independent measurement.

**Blocking errors**: Answering only “more images” without diversity of motion.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Full reference]]; [OpenCV 4.13.0, `calib3d.hpp` L2352–L2353, non-parallel rotation axes](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2352-L2353); [Horaud and Dornaika 1995, §3, eqs. 18–19](https://arxiv.org/abs/2311.12655); [OpenCV 4.13.0, `calibration_handeye.cpp` L334–L376, Tsai pair check and SVD solves](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration_handeye.cpp#L334-L376). Translation null-space derivation, rotation ambiguity, singular values and acquisition protocol: project deductions, the numbers recomputed in the 2026-11-16 check script.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-MULTICALIB-002 provenance::agent pole::B pole::C pole::E
END

## CV-MULTICALIB-003

Objective: Separate intrinsic, extrinsic and temporal calibration. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-MULTICALIB-003
Question: Why does low intrinsic reprojection error fail to validate camera–LiDAR fusion during motion?
Reponse: **Expected answer**: On its own, it tests neither the extrinsic between the sensors, nor their temporal offset, nor the motion distortion of the scan.

**Further explanation**: Validate separately and then together on suitable motions and scenes.

**Separate the contracts**: The intrinsics link the rays and pixels of one camera. The extrinsic connects the axes of the sensors. Time determines which positions of the scene and of the carrier platform are compared. A fusion can respect the first contract and violate the other two, especially during a rotation.

**Constructed protocol**: Start with static observations to check part of the geometry, then compare translations and rotations while inspecting the per-point LiDAR timestamps and the camera capture instants. Correct offsets, deskew and transformations separately to measure their effect. A translation fitted at a single speed can hide a delay without generalizing. Hold out a sequence with other motions for final validation. A good camera reprojection remains useful, but it tests neither the simultaneity of the measurements nor the full projection of a point cloud into the image.

**Order of magnitude of a time offset**: In a local rigid-motion model, the displacement of a point expressed in one coordinate frame is of the order of $\delta p\simeq(v+\omega\times p)\delta t$, with speed $v$ in m/s, angular speed $\omega$ in rad/s and delay $\delta t$ in s. The sign depends on the direction of the comparison. At 10 m/s, 20 ms already represent 20 cm of translation; the angular contribution grows with the lever arm. The image projection then adds its Jacobian and depends on the depth. This constructed calculation explains why testing several speeds, distances and directions of rotation helps distinguish a delay from a constant extrinsic.

**Static and dynamic tests isolate different contracts**: A proposed validation sequence first checks static cross-sensor alignment, then repeats known translations and turns with the same extrinsics. Error proportional to speed or angular rate suggests a timing or deskew problem; persistent static offset instead directs attention toward the spatial chain or projection model. These are diagnostic tendencies, not proofs. Keep clock, timestamp reference and per-point acquisition conventions explicit before refitting a fixed transform.

**Blocking errors**: Equating camera calibration quality with the quality of the complete fusion.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Full reference]]; [Zhang and Singh 2014, LOAM, Fig. 1 and §V-C](https://www.roboticsproceedings.org/rss10/p07.pdf); [Qin and Shen 2018, §III-A to §III-C](https://arxiv.org/abs/1808.00692). Intrinsic/extrinsic/time comparison and order of magnitude: project deductions.
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-MULTICALIB-003 provenance::agent pole::B pole::C pole::E
END
