---
id: CV-VIO
type: methode
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 7
prerequis: ["CV-SE3", "CV-FUSION", "CV-FACTEURS", "CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d06]
---
# SLAM, VIO, IMU preintegration and loop closure

## Problem, data and assumptions

Estimate a trajectory and possibly a map by exploiting vision, IMU and place constraints. Outputs: poses, state/bias and uncertainties in a defined coordinate frame. Local odometry, relocation and SLAM with loop do not meet exactly the same contract.

## Prerequisites and competencies

**Required prerequisites**: [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md); [CV-FUSION](../../10-mathematiques-estimation/references/13-kalman-ekf-eskf.md); [CV-FACTEURS](../../10-mathematiques-estimation/references/14-graphes-facteurs.md); [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Track/associate observations, estimate movement, manage keyframes, optimize or filter, detect and then check loops. Preintegration condenses IMU measurements between keyframes with covariance and bias correction. MSCKF, VINS-Mono and OKVIS are different designs; one mention does not implement their variants.

## Mathematics, conventions and units

With $R_i$ body→world, $p_i,v_i$ position and speed in the world, $g$ gravity in the same coordinate frame and $\Delta t=t_j-t_i$ in seconds, $\Delta v_{ij}=R_i^T(v_j-v_i-g\Delta t)$ and $\Delta p_{ij}=R_i^T(p_j-p_i-v_i\Delta t-\tfrac12g\Delta t^2)$, in m/s and m. The accelerometer measures a specific force in its coordinate frame. A VIO without global references keeps global translation and yaw unobservable; the metric scale requires sufficient excitation and calibration.

## Parameters and properties

Intrinsic/extrinsic, timestamps, bias, initialization, window and loop policy. DBoW2/NetVLAD offer location candidates; geometric verification is still required.

## Cost and implementation

Number of states/landmarks, window size, tracking, and loop weigh on memory/latency. No VIO system executed; no encrypted drift or real time guaranteed.

## Evaluation and controlled variation

Proposed Variation: Remove the texture and then reduce the inertial excitation separately. Analyze tracking losses, scale and bias; do not equate local observation failure and global gauge. Evaluate with announced timestamps and alignment group.

## Failure modes and diagnosis

Repetitive corridor: check parallax, gradients, timing, bias and false loops. A Sim(3) alignment can hide a bad scale from a system that is supposed to be metric.

## Alternatives and applications

Single vision, stereo/RGB-D, VIO, LiDAR-odometry or fusion according to texture, excitation and reference. The check trajectory remains out of scope.

## Guided reasoning and proposed checks

These constructed cases develop inertial fusion, gauges and evaluation without masking the errors. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-VIO-001

**Question of work**: Does IMU preintegration alone constitute a VIO system?

**Reference Response**: No: it summarizes measurements between keyframes in constraints with noise and bias; the system must also associate the vision, initialize and estimate the states.

**Pre-integration contract**: Between two keyframes, the many inertial observations are condensed into motion constraints with their uncertainty and dependence on biases. These constraints must be combined with visual observations, initial state and gravity in consistent coordinate frames.

**Example of limit**: integrate an acceleration measured in the coordinate frame IMU as if it were directly an acceleration world confuses orientation, specific force and gravity. A very good vision does not automatically repair this model inconsistency. A complete system must also handle timestamps, extrinsic, bias, keyframes and observation losses. Pre-integration avoids naïvely resuming the entire raw sequence at each calculation; it does not provide an absolute pose or a global reference absent from the sensors. Validating the system therefore requires trajectory, uncertainty, availability and latency on representative movements.

### Case linked to CV-VIO-005

**Question of work**: Track B — diagnosis: VIO drifts in scale and yaw in a poorly textured corridor. Which checks distinguish possible causes?

**Reference Response**: Inspect texture/parallax, excitation, bias and synchronization; check false loops and alignment group used.

**Investigation by signatures**: A weak texture degrades visual constraints; insufficient excitation limits some inertial estimates; delay or bias can produce a motion-dependent error. Compare the timeline of residuals and tracking losses, rather than just the final trajectory.

**Proposed Ablations**: check timestamps on instrumented movements, inspect features and parallax, and then examine loop constraints one by one. Reserve sequences where a single factor changes to distinguish hypotheses. An alignment with free scale can make the visual overlay convincing while hiding the metric error. Report the error before and after the allowed alignment, with its justification. No single check proves a single cause when multiple sensor and estimation defects coexist.

**Documentary reference for this pass**: [Forster et al. 2016](https://dellaert.github.io/files/Forster16tro.pdf), §§IV – VI, pre-integration and estimation. The other developments are in the [flashcards](../63-slam-vio.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-VIO-001

**Situation**: Does IMU preintegration alone constitute a VIO system?

**Constraints between states**: with $R_i$ body→world, $p_i,v_i$ in world coordinates, $g$ in gravity acceleration and $\Delta t=t_j-t_i$, the ideal increments check $\Delta v_{ij}=R_i^T(v_j-v_i-g\Delta t)$ and $\Delta p_{ij}=R_i^T(p_j-p_i-v_i\Delta t-\tfrac12g\Delta t^2)$. They are expressed in the starting coordinate frame and must be compared with the pre-integrated IMU increments, with covariance and bias correction. These relationships make the additional states visible: positions, speeds, orientations and biases. Pre-integration is therefore a factor in joint estimation, not a replacement for these unknowns or the visual observations that constrain them.

### CV-VIO-002

**Situation**: What does loop closure change compared with local odometry?

**Relative constraint**: For poses $T_i,T_j$ sending local coordinate frames to the world, the predicted transformation from $j$ to $i$ is $T_i^{-1}T_j$. A loop provides a $Z_{ij}$ measurement of this relation; a possible residual is $\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)$, depending on the conventions and the graph model. Its weighting reflects the accuracy of the verified measurement. Appearance detection alone does not provide this geometric accuracy. A graph can redistribute an inconsistency over many poses: a moderate final cost does not clear a false loop. Comparing before/after consistency and independent observations remains essential.

### CV-VIO-003

**Situation**: Why should global yaw and VIO scale error not be diagnosed as the same ambiguity?

**Invariance and metric**: applying the same translation and rotation around gravity to the entire trajectory and the map retains the relative observations of a VIO without global reference. Changing the scale uniformly, however, modifies the predicted metric accelerations; the IMU can therefore constrain this scale when the movement provides the necessary information. Degenerate movement or misjudged biases can make this strain weak. For evaluation, document the freedoms withdrawn and keep an explicit metric check. An alignment Sim(3), which also adjusts the scale, is suitable for some monocular comparisons but can hide a scale error of a VIO declared metric.

### CV-VIO-004

**Situation**: Track B — design: localize an indoor AR headset with cameras and an IMU under a latency constraint. Which pipeline must be validated?

**Seniority budget of pose**: distinguish capture instant $t_c$, estimation availability $t_e$ and display instant $t_a$. A correct pose for $t_c$ comes already old from $t_a-t_c$ on the screen. The IMU propagation can predict up to $t_a$ under a motion model, with increasing uncertainty; it does not transform a future measurement into available observation. Measure the error at the time actually requested and report the time frames step by step with their percentiles. In a test built at 100°/s, 20 ms represents 2° of uncompensated rotation. This calculation directly links synchronization, prediction and visual stabilization requirement of the helmet.

### CV-VIO-005

**Situation**: Track B — diagnosis: VIO drifts in scale and yaw in a poorly textured corridor. Which checks distinguish possible causes?

**Drift due to bias, simplified case**: If a constant acceleration bias $b_a$ remains uncorrected in a fixed world direction, it produces approximately a speed error $b_at$ and position error $\tfrac12b_at^2$. A constant gyroscope bias produces an angular error of the order of $b_\omega t$; this error can also incorrectly orient gravity and contaminate translation. These constructed laws assume a simplified orientation and conditions, they do not predict a real trajectory. Looking for these time signatures in parallel with feature losses and loop corrections helps to propose discriminating essays rather than a single cause in view of the final plot.

**Passages consulted for these developments**: [Qin et al., VINS-Mono](https://arxiv.org/html/1708.03852v1), §IV-B, preintegration and bias; §V-B, metric initialization; algebraic add-ins and project scenarios.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-VIO-001 — Bias correction has a local validity range

Preintegrated increments are computed around a chosen bias estimate. First-order bias Jacobians allow a nearby correction without reintegrating every IMU sample, but a large bias change can require reintegration. Retain the time interval and linearization bias with the factor. Summarizing measurements reduces repeated work; it does not make their covariance, gravity convention, timestamp alignment or bias dependence optional.

### CV-VIO-002 — A corrected map can move discontinuously

A loop closure may change the global optimized trajectory even when the current local motion estimate remains smooth. A system driving a controller or renderer should specify how it exposes local odometry and globally corrected poses, including the transform between them. This is a project interface choice. Evaluate both local continuity and long-term consistency; a lower globally aligned trajectory error does not by itself establish an acceptable real-time pose signal.

### CV-VIO-003 — Alignment can hide the error being diagnosed

A similarity alignment can rescale a trajectory and remove a scale error from the reported position metric. If metric scale is a deployment requirement, evaluate with an alignment group that preserves that requirement and report the scale discrepancy separately. A free global yaw alignment removes a gauge choice under the stated sensor model; removing scale in an observable metric VIO instead conceals a potentially real estimation error.

### CV-VIO-004 — A recent timestamp is part of pose quality

Constructed latency case: at $180^\circ$/s head rotation, a pose 20 ms old differs by $3.6^\circ$ before prediction. A low offline trajectory error cannot establish acceptable display-time pose error. A proposed AR protocol measures pose age, prediction horizon, motion-to-estimate delay and failure recovery under fast rotation and visual dropout. It must distinguish causal estimates from trajectories improved later by smoothing or loop closure.

### CV-VIO-005 — Weak texture and weak excitation can coincide

A long straight corridor can provide repetitive visual structure and nearly constant velocity. Both association ambiguity and weak inertial scale/bias information can then contribute to drift. Compare controlled turns and accelerations while logging track geometry, innovation behavior, initialization and timing. Evaluate without freely correcting metric scale. A single low-texture explanation is insufficient when synchronization or an incorrectly modeled bias can produce similar trajectory symptoms.

Consulted foundations: [Forster et al. preintegration](https://dellaert.github.io/files/Forster16tro.pdf): §§IV–VI relative inertial factors, bias correction and estimation; [Qin et al. VINS-Mono](https://arxiv.org/html/1708.03852v1): §V-B initialization, §VI estimation and §VIII pose graph.

## Sources and flashcards

- [Forster, pre-integration §§IV – VI](https://dellaert.github.io/files/Forster16tro.pdf).
- [Zhang – Scaramuzza, alignment §III and Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf).
- [GTSAM, SLAM and factors](https://gtsam.org/tutorials/intro.html).
- [Related flashcards](../63-slam-vio.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
