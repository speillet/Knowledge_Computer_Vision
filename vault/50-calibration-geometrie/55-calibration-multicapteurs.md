# Flashcards — Multisensor calibration, hand–eye calibration and timing

reference note: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-MULTICALIB-001

Objective: Interpreting hand-eye. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-MULTICALIB-001
Question: Why is writing $AX=XB$ insufficient to apply hand–eye calibration?
Reponse: **Expected answer**: We must define the coordinate frames, the relative A/B movements, their meaning and the unknown transformation X.

**Further explanation**: Check a string of transformations on a point and reserved movements; different conventions give different equations.

**derivation per chain**: in eye-in-hand with a fixed calibration target, the composition tool→base, camera→tool then calibration target→camera must give the same pose calibration target→base for each acquisition. The equality of these compositions leads to relative movements on either side of the unknown extrinsic. The meaning of the products is not free: it comes from the adjacent coordinate frames.

**Constructed test**: take a known pose, transform a point from calibration target to the base, and then check the reverse of the string. Repeat with non-trivial rotation and non-zero translations in common units. An identity test can leave inversions invisible. This interface validation precedes the solver setting; if it fails, adding data or changing the optimization method addresses an issue other than the convention error.

**Usable formulation**: Note $G_i={}^bT_{g_i}$, $C_i={} ^{c_i}T_t$ and $X={}^gT_c$, where the top coordinate frame receives the coordinates. The fixed calibration target imposes $G_iXC_i=Y$, with $Y={}^bT_t$ constant. Between two catches, multiply the equality left by $G_j^{-1}$ and right by $C_i^{-1}$ gives $(G_j^{-1}G_i)X=X(C_jC_i^{-1})$. The indices and the assembly therefore determine exactly $A$ and $B$. The case built with translations alone checks the units, but noncommutative rotations are needed to detect many order errors. The $X$ matrix must remain the same on all synchronized captures.

**Blocking errors**: Copy the matrices of an API without checking their meaning.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Full reference]] ; [OpenCV 4.13.0, calibrateHandEye, eye-in-hand equations and note on axes](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-MULTICALIB-001 provenance::agent pole::B pole::C pole::E
END

## CV-MULTICALIB-002

Objective: Evaluate informative movements. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MULTICALIB-002
Question: Many robot poses around the same axis produce unstable extrinsics. What should be changed?
Reponse: **Expected answer**: Examine observability and vary rotations/positions that constrain missing components.

**Further explanation**: Compare stability and validation on another trajectory, without considering the gross number of poses as proof.

**Intuition of Observability**: Repeating a similar movement adds less average noise, but not necessarily new directions of stress. Some components of the extrinsic can then vary greatly without much change in the observed equations. All pairs built from the same poses also remain correlated.

**Proposed acquisition**: compare, with comparable poses numbers, a single-axis trajectory and a trajectory with various axes of rotation, within the physical limits of the device. Keep calibration target quality and synchronization controlled, and then check the chain on a reserved path. If the instability persists, also look for a timestamp or pose robot error. A diversity of motions is a source of information; it does not guarantee that every other calibration hypothesis is correct. The final criterion remains stability and useful error in the operating volume.

**Component not constrained**: by developing homogeneous transformations, we obtain $(R_A-I)t_X=R_Xt_B-t_A$. For a rotation around a unit axis $n$, $(R_A-I)n=0$: this equation alone does not determine the component of $t_X$ following $n$. Repeating the same axis leaves this structural defect. Stacking movements of different axes can lift it, subject to a rotation $R_X$ itself correctly estimated. Examine the singular values of this system after scaling and compare the solutions by subsets of poses. A large number of correlated pairs does not transform into as many independent directions of information.

**Blocking errors**: Reply only “more images” without diversity of movement.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Full reference]] ; [OpenCV 4.13.0, calibrateHandEye, eye-in-hand equations and note on axes](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-MULTICALIB-002 provenance::agent pole::B pole::C pole::E
END

## CV-MULTICALIB-003

Objective: separating intrinsic extrinsic and time. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-MULTICALIB-003
Question: Why does low intrinsic reprojection error fail to validate camera–LiDAR fusion during motion?
Reponse: **Expected answer**: It does not alone test the extrinsic between sensors, their temporal offset or the deformation of the scan.

**Further explanation**: Validate separately and then together on adapted movements and scenes.

**Separate the Contracts**: Intrinsic links rays and pixels of a camera. The extrinsic connects the axes of the sensors. Time determines which positions of the scene and the wearer are compared. A merger can respect the first contract and violate the other two, especially during a rotation.

**Survey built**: start with motionless observations for check a part of the geometry, then compare translation and rotation by inspecting time by point of the LiDAR and camera capture moment. Separately correct offsets, deskew, and transformations to measure their effect. A translation adjusted for a single speed can hide a delay without generalizing. Reserve a sequence with other moves for final validation. A good camera reprojection remains useful, but it does not test either the simultaneity of the measurements or the entire projection of a cloud towards the image.

**Order of temporal magnitude**: in a local rigid displacement model, the deviation of a point expressed in the same coordinate frame is of the order of $\delta p\simeq(v+\omega\times p)\delta t$, with speed $v$ in m/s, angular speed $\omega$ in rad/s and delay $\delta t$ in s. The sign depends on the sense of comparison. At 10 m/s, 20 ms already represent 20 cm of translation; the angular contribution increases with the lever arm. The image projection then adds its Jacobian and depends on the depth. This built-in calculation explains why testing multiple speeds, distances, and direction of rotation helps distinguish a delay from a constant extrinsic.

**Blocking errors**: Assimilate camera calibration quality and complete fusion quality.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Full reference]]; [Zhang – Singh 2014, LOAM, §§II, IV and V-B](https://www.roboticsproceedings.org/rss10/p07.pdf); intrinsic/extrinsic/time comparison deduced by the project.
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-MULTICALIB-003 provenance::agent pole::B pole::C pole::E
END
