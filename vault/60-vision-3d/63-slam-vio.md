# Flashcards — SLAM, VIO, IMU preintegration and loop closure

reference note: [[60-vision-3d/references/63-slam-vio|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-VIO-001

Objective: situate the preintegration. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-VIO-001
Question: Does IMU preintegration alone constitute a VIO system?
Reponse: **Expected answer**: No: it summarizes measurements between keyframes in constraints with noise and bias; the system must also associate the vision, initialize and estimate the states.

**Further explanation**: The accelerometer is not directly a gravity-free world acceleration.

**Pre-integration contract**: Between two keyframes, the many inertial observations are condensed into motion constraints with their uncertainty and dependence on biases. These constraints must be combined with visual observations, initial state and gravity in consistent coordinate frames.

**Example of limit**: integrate an acceleration measured in the coordinate frame IMU as if it were directly an acceleration world confuses orientation, specific force and gravity. A very good vision does not automatically repair this model inconsistency. A complete system must also handle timestamps, extrinsic, bias, keyframes and observation losses. Pre-integration avoids naïvely resuming the entire raw sequence at each calculation; it does not provide an absolute pose or a global reference absent from the sensors. Validating the system therefore requires trajectory, uncertainty, availability and latency on representative movements.

**Constraints between states**: with $R_i$ body→world, $p_i,v_i$ in world coordinates, $g$ in gravity acceleration and $\Delta t=t_j-t_i$, the ideal increments check $\Delta v_{ij}=R_i^T(v_j-v_i-g\Delta t)$ and $\Delta p_{ij}=R_i^T(p_j-p_i-v_i\Delta t-\tfrac12g\Delta t^2)$. They are expressed in the starting coordinate frame and must be compared with the pre-integrated IMU increments, with covariance and bias correction. These relationships make the additional states visible: positions, speeds, orientations and biases. Pre-integration is therefore a factor in joint estimation, not a replacement for these unknowns or the visual observations that constrain them.

**Blocking errors**: Describe pre-integration as a ready-made absolute pose.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]]; [Forster et al., §§V – VI, equations 31 – 34 and VI-C](https://dellaert.github.io/files/Forster16tro.pdf); [Qin et al., VINS-Mono, §IV-B, preintegration and bias; §V-B, metric initialization; algebraic add-ins and project scenarios](https://arxiv.org/html/1708.03852v1), see 2026-10-30.
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

**Constructed example**: After a long journey, recognizing an area already visited provides a relationship between states far away in time. This relationship may redistribute the corrections to the trajectory and the map, while a local odometry does not necessarily revisit all of these past estimates.

**Two separate validations**: The front-end proposes a place on the basis of appearance; a geometric check must establish that the observations support the same area. The back-end then integrates a constraint with its weight and assumptions. Identical corridors can deceive the first step and produce an overall deformation if the false stress is accepted. Review the residuals of other factors and a reserved reference. A correct loop can reduce relative drift, but it does not automatically create an absolute global position, a better-observed scale, or a complete absence of error.

**Relative constraint**: For poses $T_i,T_j$ sending local coordinate frames to the world, the predicted transformation from $j$ to $i$ is $T_i^{-1}T_j$. A loop provides a $Z_{ij}$ measurement of this relation; a possible residual is $\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)$, depending on the conventions and the graph model. Its weighting reflects the accuracy of the verified measurement. Appearance detection alone does not provide this geometric accuracy. A graph can redistribute an inconsistency over many poses: a moderate final cost does not clear a false loop. Comparing before/after consistency and independent observations remains essential.

**Blocking errors**: Guarantee an exact global position as soon as a loop is detected.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]]; [GTSAM, §4.1 Loop Closure Constraints, Viewed on 2026-10-20](https://gtsam.org/tutorials/intro.html); false loop: diagnosis of the project; [Qin et al., VINS-Mono, §IV-B, preintegration and bias; §V-B, metric initialization; algebraic add-ins and project scenarios](https://arxiv.org/html/1708.03852v1), consult the 2026-10-30.
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-VIO-002 provenance::agent pole::B pole::C
END

## CV-VIO-003

Objective: Identify the VIO gauges. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-VIO-003
Question: Why should global yaw and VIO scale error not be diagnosed as the same ambiguity?
Reponse: **Expected answer**: Without external reference, the global yaw can remain a gauge, while the metric scale depends on sufficient excitation and calibration and can be mistakenly estimated.

**Further explanation**: The global translation remains as free; distinguish alignment convention and physical information actually available.

**Conceptual difference**: a gauge transforms all estimates together without changing the relative observations. The choice of an arbitrary north in a trajectory without heading reference is a matter of this convention. An erroneous metric scale, when it is supposed to be observable with the IMU, instead reflects an estimate or model that is insufficiently constrained.

**Proposed diagnosis**: announce the allowed degrees of alignment before comparing to the ground truth. Using a transformation that only removes legitimate ambiguities; leaving the scale free would mask precisely the defect that one seeks to measure. Testing excitation, calibration, and bias on different sequences helps to understand a wrong scale estimate. It is also necessary to distinguish a constant yaw offset from a yaw drift over time. The final graph alone does not allow all these differences to be attributed to the same cause.

**Invariance and metric**: applying the same translation and rotation around gravity to the entire trajectory and the map retains the relative observations of a VIO without global reference. Changing the scale uniformly, however, modifies the predicted metric accelerations; the IMU can therefore constrain this scale when the movement provides the necessary information. Degenerate movement or misjudged biases can make this strain weak. For evaluation, document the freedoms withdrawn and keep an explicit metric check. An alignment Sim(3), which also adjusts the scale, is suitable for some monocular comparisons but can hide a scale error of a VIO declared metric.

**Blocking errors**: To say that any VIO is always on an arbitrary scale like a visual monocular.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]]; [Zhang – Scaramuzza 2018, §III and Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf); excitation condition: hypothesis of the inertial model; [Qin et al., VINS-Mono, §IV-B, preintegration and bias; §V-B, metric initialization; algebraic add-ins and project scenarios](https://arxiv.org/html/1708.03852v1), consult the 2026-10-30.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-VIO-003 provenance::agent pole::B pole::C
END

## CV-VIO-004

Objective: design a VIO for augmented reality. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-VIO-004
Question: Track B — design: localize an indoor AR headset with cameras and an IMU under a latency constraint. Which pipeline must be validated?
Reponse: **Expected answer**: Define coordinate frames/time, calibrate sensors and delays, choose causal estimation and loss management, then measure precision, drift and latency on representative movements.

**Further explanation**: Predict low texture, excitation, relocation and independent reference; announce gauges and behavior in case of uncertainty.

**Proposed channel**: first define when the pose should be valid, in what coordinate frame and with what maximum seniority. The latency of a camera, its transfer and processing can shift the observation used, even if the estimation algorithm is fast. The interface must communicate moment of validity and uncertainty.

**Transfer tests**: compare slow and fast movements, textured areas and uniform walls, then interruption and return of observations. Measure availability, relative drift and recovery with an independent reference, keeping the same alignment rules. An a posteriori smoothed path does not validate a causal pose available in time for display. These controls link geometric quality and AR usage; they constitute a design protocol, without demonstration performed on a real helmet.

**Seniority budget of pose**: distinguish capture instant $t_c$, estimation availability $t_e$ and display instant $t_a$. A correct pose for $t_c$ comes already old from $t_a-t_c$ on the screen. The IMU propagation can predict up to $t_a$ under a motion model, with increasing uncertainty; it does not transform a future measurement into available observation. Measure the error at the time actually requested and report the time frames step by step with their percentiles. In a test built at 100°/s, 20 ms represents 2° of uncompensated rotation. This calculation directly links synchronization, prediction and visual stabilization requirement of the helmet.

**Blocking errors**: Promising a reliable metric pose without time calibration or evaluation protocol.

**Criteria for correction of the case**: explicit task and constraints, announced assumptions, justified choice, discriminating verification, limit of the conclusion. Case built, without field observation.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]]; [Forster et al., §§V – VI, equations 31 – 34 and VI-C](https://dellaert.github.io/files/Forster16tro.pdf); [Zhang – Scaramuzza 2018, §III and Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf); project protocol; [Qin et al., VINS-Mono, §IV-B, preintegration and bias; §V-B, metric initialization; algebraic add-ins and project scenarios](https://arxiv.org/html/1708.03852v1), see the 2026-10-30.
Tags: cv::pilote cv::d06 famille::conception cv_id::CV-VIO-004 provenance::agent pole::B pole::C cas_pole::B::conception
END

## CV-VIO-005

Objective: Diagnose a drift in the corridor. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-VIO-005
Question: Track B — diagnosis: VIO drifts in scale and yaw in a poorly textured corridor. Which checks distinguish possible causes?
Reponse: **Expected answer**: Inspect texture/parallax, excitation, bias and synchronization; check false loops and alignment group used.

**Further explanation**: Separate unobservable global yaw and relative drift; retain a metric reference that does not hide the scale error. A single cause is not identifiable to the final path alone.

**Investigation by signatures**: A weak texture degrades visual constraints; insufficient excitation limits some inertial estimates; delay or bias can produce a motion-dependent error. Compare the timeline of residuals and tracking losses, rather than just the final trajectory.

**Proposed Ablations**: check timestamps on instrumented movements, inspect features and parallax, and then examine loop constraints one by one. Reserve sequences where a single factor changes to distinguish hypotheses. An alignment with free scale can make the visual overlay convincing while hiding the metric error. Report the error before and after the allowed alignment, with its justification. No single check proves a single cause when multiple sensor and estimation defects coexist.

**Drift due to bias, simplified case**: If a constant acceleration bias $b_a$ remains uncorrected in a fixed world direction, it produces approximately a speed error $b_at$ and position error $\tfrac12b_at^2$. A constant gyroscope bias produces an angular error of the order of $b_\omega t$; this error can also incorrectly orient gravity and contaminate translation. These constructed laws assume a simplified orientation and conditions, they do not predict a real trajectory. Looking for these time signatures in parallel with feature losses and loop corrections helps to propose discriminating essays rather than a single cause in view of the final plot.

**Blocking errors**: Correct by freely aligning the scale and then declare the VIO accurate.

**Criteria for correction of the case**: explicit task and constraints, announced assumptions, justified choice, discriminating verification, limit of the conclusion. Case built, without field observation.
Source: [[60-vision-3d/references/63-slam-vio|Full reference]]; [Forster et al., §§V – VI, equations 31 – 34 and VI-C](https://dellaert.github.io/files/Forster16tro.pdf); [Zhang – Scaramuzza 2018, §III and Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf); project diagnosis; [Qin et al., VINS-Mono, §IV-B, preintegration and bias; §V-B, metric initialization; algebraic add-ins and project scenarios](https://arxiv.org/html/1708.03852v1), consult the 2026-10-30.
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-VIO-005 provenance::agent pole::B pole::C cas_pole::B::diagnostic
END
