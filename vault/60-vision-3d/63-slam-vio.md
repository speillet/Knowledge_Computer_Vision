# Flashcards — SLAM, VIO, IMU preintegration and loop closure

reference note: [[60-vision-3d/references/63-slam-vio|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-VIO-001

Objective: situate the preintegration. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-VIO-001
Question: Does IMU preintegration alone constitute a VIO system?
Reponse: **Expected answer**: No: it summarizes the measurements between keyframes into constraints with their noise and bias dependence; the system must also associate visual observations, initialize and estimate the states.

**Further explanation**: The accelerometer does not directly measure a gravity-free world acceleration.

**Preintegration contract**: Between two keyframes, the many inertial observations are condensed into motion constraints with their uncertainty and dependence on biases. These constraints must be combined with visual observations, the initial state and gravity in consistent coordinate frames.

**Example of a limit**: Integrating an acceleration measured in the IMU frame as if it were a world-frame acceleration confuses orientation, specific force and gravity. Very good vision does not automatically repair this model inconsistency. A complete system must also handle timestamps, extrinsics, biases, keyframes and observation losses. Preintegration avoids re-integrating the raw sequence each time the estimate of the starting state changes; it does not provide an absolute pose or a global reference absent from the sensors. Validating the system therefore requires trajectory, uncertainty, availability and latency on representative motions.

**Constraints between states**: With $R_i$ body→world, $p_i,v_i$ in world coordinates, $g$ the gravity vector in the world frame and $\Delta t=t_j-t_i$, the ideal increments satisfy $\Delta v_{ij}=R_i^T(v_j-v_i-g\Delta t)$ and $\Delta p_{ij}=R_i^T(p_j-p_i-v_i\Delta t-\tfrac12g\Delta t^2)$. They are expressed in the frame of keyframe $i$ and must be compared with the preintegrated IMU increments, with covariance and bias correction. These relationships show the additional states involved: positions, velocities, orientations and biases. Preintegration is therefore a factor in joint estimation, not a replacement for these unknowns or for the visual observations that constrain them.

**Bias correction has a local validity range**: Preintegrated increments are computed around a chosen bias estimate. First-order bias Jacobians allow a nearby correction without reintegrating every IMU sample, but a large bias change can require reintegration. Retain the time interval and linearization bias with the factor. Summarizing measurements reduces repeated work; it does not make their covariance, gravity convention, timestamp alignment or bias dependence optional.

**Blocking errors**: Describing preintegration as a ready-made absolute pose.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]] ; [Forster et al., §V eqs. 27–31, §VI eq. 33 and §VI-C eq. 44](https://arxiv.org/abs/1512.02363) ; [Qin et al., VINS-Mono, §IV-B, first-order bias correction or re-propagation](https://arxiv.org/html/1708.03852v1). Constructed cases: project deduction.
Tags: cv::pilote cv::d06 famille::comprehension cv_id::CV-VIO-001 provenance::agent pole::B pole::C
END

## CV-VIO-002

Objective: distinguish odometry and loop. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-VIO-002
Question: What does loop closure change compared with local odometry?
Reponse: **Expected answer**: It adds a constraint on a revisited location and can reduce the accumulated drift by re-estimating the map/trajectory.

**Further explanation**: The place candidate must be checked; a false loop can make the result worse despite a low cost.

**Constructed example**: After a long trajectory, recognizing an area already visited provides a relationship between states far apart in time. This relationship may redistribute the corrections to the trajectory and the map, while a local odometry does not necessarily revisit all of these past estimates.

**Two separate validations**: The front-end proposes a place on the basis of appearance; a geometric check must establish that the observations support the same area. The back-end then integrates a constraint with its weight and assumptions. Identical corridors can deceive the first step and produce a global deformation if the false constraint is accepted. Review the residuals of the other factors and a held-out reference. A correct loop can reduce relative drift, but it does not automatically create an absolute global position, a better-observed scale, or a complete absence of error.

**Relative constraint**: For poses $T_i,T_j$ mapping local frames to the world, the predicted transformation from $j$ to $i$ is $T_i^{-1}T_j$. A loop provides a measurement $Z_{ij}$ of this relation; a possible residual is $\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)$, depending on the conventions and the graph model. Its weight reflects the accuracy of the verified measurement. Appearance detection alone does not provide this geometric accuracy. A graph can redistribute an inconsistency over many poses: a moderate final cost does not clear a false loop. Comparing consistency before and after, and independent observations, remains essential.

**A corrected map can move discontinuously**: A loop closure may change the global optimized trajectory even when the current local motion estimate remains smooth. A system driving a controller or renderer should specify how it exposes local odometry and globally corrected poses, including the transform between them. This is a project interface choice. Evaluate both local continuity and long-term consistency; a lower globally aligned trajectory error does not by itself establish an acceptable real-time pose signal.

**Blocking errors**: Guaranteeing an exact global position as soon as a loop is detected.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]] ; [GTSAM tutorial, §4.1 loop-closure constraints, viewed 2026-10-20](https://gtsam.org/tutorials/intro.html) ; [Qin et al., VINS-Mono, §VII-A, §VII-B and §VIII, loop detection, verification and 4-DOF pose graph](https://arxiv.org/html/1708.03852v1) ; [Campos et al., ORB-SLAM3, §VI-A, geometric verification](https://arxiv.org/html/2007.11898). False-loop case and interface choice: project deduction.
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-VIO-002 provenance::agent pole::B pole::C
END

## CV-VIO-003

Objective: Identify the VIO gauges. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-VIO-003
Question: Why should global yaw and VIO scale error not be diagnosed as the same ambiguity?
Reponse: **Expected answer**: Without an external reference, global yaw remains a gauge freedom, while the metric scale depends on sufficient excitation and calibration and can be wrongly estimated.

**Further explanation**: Global translation is also free; distinguish the alignment convention from the physical information actually available.

**Conceptual difference**: A gauge transforms all estimates together without changing the relative observations. Choosing an arbitrary north for a trajectory without heading reference is such a convention. A wrong metric scale, when it is supposed to be observable with the IMU, instead reflects an estimate or a model that is insufficiently constrained.

**Proposed diagnosis**: State the alignment degrees of freedom allowed before comparing with ground truth. Use a transformation that removes only the legitimate ambiguities; leaving the scale free would mask precisely the defect being measured. Testing excitation, calibration and bias on different sequences helps to explain a wrong scale estimate. Also distinguish a constant yaw offset from a yaw drift over time. The final plot alone does not allow all these differences to be attributed to one cause.

**Invariance and metric**: Applying the same translation and rotation about gravity to the entire trajectory and map preserves the relative observations of a VIO without global reference. Changing the scale uniformly, however, modifies the predicted metric accelerations; the IMU can therefore constrain this scale when the motion provides the necessary information. Degenerate motion or misestimated biases can make this constraint weak. For evaluation, document the degrees of freedom removed by alignment and keep an explicit metric check. A Sim(3) alignment, which also adjusts the scale, is suitable for some monocular comparisons but can hide a scale error of a VIO declared metric.

**Why the IMU separates the two**: Apply one similarity $p'=sRp+t$, $v'=sRv$, $R_i'=RR_i$ to every state and landmark. Monocular projections do not change, whatever $s$, $R$ and $t$. The preintegrated velocity increment becomes $R_i^\top\big(s(v_k-v_i)-R^\top g\,\Delta t_{ik}\big)$: it matches the measurement for every motion only if $s=1$ and $R^\top g=g$, a rotation about gravity [Zhang and Scaramuzza, eqs. 8–12]. Yaw and global translation therefore leave every residual unchanged, and no excitation can reveal them. A tilt moves $R^\top g$ by about 0.17 m/s² per degree, which is why roll and pitch are observable. A wrong scale changes the increment by $(s-1)R_i^\top(v_k-v_i)$: nothing at constant velocity, more as the acceleration grows. Scale is information whose strength depends on the motion, not a gauge.

**Constructed check** (reference worked examples C and D, recomputed): with a residual accelerometer bias of 0.02 m/s² along the motion, a scale fitted on accelerations near 0.2 m/s² is 10% off, and 1% off near 2 m/s². On a straight 100 m path, a 5% scale error leaves an ATE of 1.46 m after the 4-DOF alignment, and 0 after a Sim(3) alignment. Align with yaw and translation only, then plot the scale error against acceleration magnitude: an error that shrinks on excited segments is an estimation defect, whereas a yaw offset changes no residual at any excitation.

**Blocking errors**: Saying that every VIO has an arbitrary scale, like monocular visual odometry.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]] ; [Zhang and Scaramuzza 2018, §III-A eqs. 8–12 and Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [Qin et al., VINS-Mono, §I (excitation for scale; roll and pitch observable) and §VII (drift in position and yaw)](https://arxiv.org/html/1708.03852v1). Reading of eq. 11 and constructed cases (reference worked examples B, C and D): project deduction.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-VIO-003 provenance::agent pole::B pole::C
END

## CV-VIO-004

Objective: design a VIO for augmented reality. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-VIO-004
Question: Track B — design: localize an indoor AR headset with cameras and an IMU under a latency constraint. Which pipeline must be validated?
Reponse: **Expected answer**: Define frames and time references, calibrate sensors and delays, choose causal estimation and tracking-loss handling, then measure accuracy, drift and latency on representative motions.

**Further explanation**: Plan for low texture, weak excitation, relocalization and an independent reference; state the gauges and the behavior under uncertainty.

**Proposed pipeline**: First define when the pose must be valid, in which coordinate frame and with what maximum age. The latency of a camera, its transfer and processing can shift the observation used, even if the estimation algorithm is fast. The interface must communicate the validity time and the uncertainty.

**Transfer tests**: Compare slow and fast motions, textured areas and uniform walls, then interruption and return of observations. Measure availability, relative drift and recovery with an independent reference, keeping the same alignment rules. A trajectory smoothed after the fact does not validate a causal pose available in time for display. These checks link geometric quality and AR use; they form a design protocol, without a demonstration on a real headset.

**Pose age budget**: Distinguish the capture time $t_c$, the time $t_e$ at which the estimate is available and the display time $t_a$. A pose correct at $t_c$ is already $t_a-t_c$ old when displayed. IMU propagation can predict up to $t_a$ under a motion model, with growing uncertainty; it does not turn a future measurement into an available observation. Measure the error at the time actually requested and report the latency of each stage with its percentiles. In a constructed case at 100°/s, 20 ms represents 2° of uncompensated rotation. This calculation directly links synchronization, prediction and the visual stabilization requirement of the headset.

**Outage budget** (constructed, recomputed in the reference, worked example F): ORB-SLAM3 predicts the state from the IMU when fewer than 15 map points are tracked and starts a new map after 5 s [§V-D]. Set an overlay tolerance, here $\varepsilon=1$ cm, against the uncorrected-bias laws $\tfrac12b_at^2$ and $g\,b_gt^3/6$ (tilt leaking gravity). An accelerometer bias of 0.02 m/s² reaches 1 cm after $\sqrt{2\varepsilon/b_a}=1.0$ s; a gyroscope bias of 0.1°/s after $(6\varepsilon/(g\,b_g))^{1/3}\approx1.5$ s. At 5 s the same biases give 0.25 m and 0.36 m of position error, but only 0.5° of orientation error, 8.7 mm at 1 m. A loss window that suits a SLAM map is therefore several times too long for a world-locked overlay. The design should flag position as degraded after about one second and may keep orientation-only rendering longer (project design choice). Validate the budget by covering the cameras for 0.5, 1, 2 and 5 s on a motion rig and plotting position and orientation error against outage length, separately from the overall trajectory error.

**Blocking errors**: Promising a reliable metric pose without time calibration or an evaluation protocol.

**Grading criteria for the case**: explicit task and constraints, stated assumptions, justified choice, discriminating check, limit of the conclusion. Constructed case, without field observation.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]] ; [Zhang and Scaramuzza 2018, §III and Table I, alignment](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [Campos et al., ORB-SLAM3, §V-D, tracking loss (IMU prediction below 15 tracked map points, new map after 5 s), and §VII-B, hand-held TUM-VI evaluation](https://arxiv.org/html/2007.11898) ; [Forster et al., §V, IMU integration](https://arxiv.org/abs/1512.02363). Design protocol, latency calculation, overlay tolerance and outage budget: project construction.
Tags: cv::pilote cv::d06 famille::conception cv_id::CV-VIO-004 provenance::agent pole::B pole::C cas_pole::B::conception
END

## CV-VIO-005

Objective: Diagnose a drift in the corridor. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-VIO-005
Question: Track B — diagnosis: VIO drifts in scale and yaw in a poorly textured corridor. Which checks distinguish possible causes?
Reponse: **Expected answer**: Inspect texture/parallax, excitation, bias and synchronization; check false loops and alignment group used.

**Further explanation**: Separate unobservable global yaw from relative drift; keep a metric reference that does not hide the scale error. A single cause cannot be identified from the final trajectory alone.

**Investigation by signatures**: Weak texture degrades visual constraints; insufficient excitation limits some inertial estimates; a delay or a bias can produce a motion-dependent error. Compare the timeline of residuals and tracking losses, rather than just the final trajectory.

**Proposed ablations**: Check timestamps on instrumented motions, inspect features and parallax, and then examine loop constraints one by one. Use held-out sequences in which a single factor changes to separate the hypotheses. An alignment with free scale can make the visual overlay convincing while hiding the metric error. Report the error before and after the allowed alignment, with its justification. No single check proves a single cause when several sensor and estimation defects coexist.

**Drift due to bias, simplified case**: If a constant acceleration bias $b_a$ remains uncorrected in a fixed world direction, it produces approximately a velocity error $b_at$ and a position error $\tfrac12b_at^2$. A constant gyroscope bias produces an angular error of the order of $b_\omega t$; when this error tilts the estimated attitude, gravity is subtracted in a wrong direction and the position error grows roughly as $g\,b_\omega t^3/6$, whereas a pure yaw error leaks no gravity. These constructed laws assume a simplified orientation and conditions; they do not predict a real trajectory. Looking for these time signatures alongside feature losses and loop corrections helps to propose discriminating tests rather than a single cause read from the final plot.

**Weak texture and weak excitation can coincide**: A long straight corridor can provide repetitive visual structure and nearly constant velocity. Both association ambiguity and weak inertial scale/bias information can then contribute to drift. Compare controlled turns and accelerations while logging track geometry, innovation behavior, initialization and timing. Evaluate without freely correcting metric scale. A single low-texture explanation is insufficient when synchronization or an incorrectly modeled bias can produce similar trajectory symptoms.

**Blocking errors**: Correcting by freely aligning the scale, then declaring the VIO accurate.

**Grading criteria for the case**: explicit task and constraints, stated assumptions, justified choice, discriminating check, limit of the conclusion. Constructed case, without field observation.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]] ; [Zhang and Scaramuzza 2018, §III-A and Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [Qin et al., VINS-Mono, §I (excitation) and §VII (drift directions)](https://arxiv.org/html/1708.03852v1) ; [Forster et al., §V eqs. 27–31, IMU model](https://arxiv.org/abs/1512.02363). Diagnosis and bias-drift laws: project construction.
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-VIO-005 provenance::agent pole::B pole::C cas_pole::B::diagnostic
END
