# Flashcards — Evaluating identities, trajectories and 3D localization

reference note: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-METRIQUES-TEMPS-001

Objective: Separate detection and identity. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-001
Question: How can two systems have identical frame-by-frame AP but different tracking quality?
Reponse: **Expected answer**: Boxes/classes can be identical while IDs are exchanged or fragmented; AP does not measure this continuity.

**Further explanation**: Use metrics and association diagnostics under identical sequence protocol.

**Constructed example**: Keep the boxes and classes of two pedestrians exactly, but exchange their IDs in the middle of the video. Spatial associations to the GT can remain identical to each frame for detection evaluation. Temporal continuity becomes false.

**Choice of measures**: Examine detection, association, fragments, and disappearance in an announced sequence protocol. An identity metric requires its own association and aggregation rules; a number of ID changes may not replace all other aspects of tracking. Compare the same sequences, ignored periods and detections when looking for the contribution of the association. The result produced may also depend on the outputs issued during losses. This distinction explains why the path introduces the IoU before SORT, and then returns to the time metrics after defining the responsibilities of the tracker.

**Decomposition of monitoring**: An absence of a box on the right target is a detection error, while a correct box with a bad ID is the association according to the protocol. Fragmentation divides a real identity into several predicted trackss; merging identities links several objects to a track. A simple number of switches does not necessarily describe their duration or all these relationships. Building the same boxes with multiple ID schemes allows you to check what each metric penalizes. Presenting components and temporal examples helps explain the gain of a tracker instead of classifying two systems on a single scalar.

**Blocking errors**: Deduct identity quality from the AP alone.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; [HOTA, §§4 – 5: detection and association](https://arxiv.org/abs/2009.07736); swapping IDs: built case of the project; [Luiten et al., HOTA, §5, combination by threshold; inferred inequality of aggregation](https://arxiv.org/html/2009.07736v2); [Zhang – Scaramuzza, §IV, ATE and relative error; RPE formula and time controls explained by the project](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf), consult the 2026-10-30.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-TEMPS-001 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-002

Objective: Comply with the HOTA aggregation. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-002
Question: Why does calculating sqrt(mean DetA × mean AssA) not necessarily reproduce HOTA?
Reponse: **Expected answer**: The reference calculates the root of the product at each threshold and then averages these scores; operations do not switch in general.

**Further explanation**: Keep matching conventions, ignores and localization; a formula summary is not the whole evaluator.

**Analytical counter-example**: take two thresholds with couples $(DetA,AssA)=(1,0)$ and $(0,1)$. The root of the product is zero at each threshold, so their average is zero. The averages of the components are each 0,5; the root of their product is then 0,5. The order of operations changes the result well. This case shows an algebraic property, without constituting a HOTA benchmark.

**Practical consequence**: Keep the values at the level where the protocol combines them, and then use the reference code and its parameters. Different matching, class, or ignore rules can also modify components before aggregation. A summarized formula helps to interpret the balance between detection and association; it does not replace the whole definition. Comparing a hand-built figure to an official tool therefore requires reproducing the same entries and all relevant conventions.

**Average and covariance of components**: for positive $D_k,A_k$, Cauchy – Schwarz gives $\frac1n\sum_k\sqrt{D_kA_k}\le\sqrt{(\frac1n\sum_kD_k)(\frac1n\sum_kA_k)}$. Reconstructing the score from the average components can therefore overestimate the average of the combinations per threshold. Equality requires a compatible ratio between sequences, with zeros being processed. This algebraic property applies to the level of aggregation considered; the other means between classes or sequences have their own conventions. The numerical counter-example of the flashcard demonstrates this order of operations, without claiming to represent feasible components of a particular benchmark.

**Blocking errors**: Freely swap medium and root.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; [HOTA, §5: HOTA per threshold then average on the thresholds](https://arxiv.org/abs/2009.07736); [Luiten et al., HOTA, §5, combination by threshold; inferred inequality of aggregation](https://arxiv.org/html/2009.07736v2); [Zhang – Scaramuzza, §IV, ATE and relative error; RPE formula and time controls explained by the project](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf), see 2026-10-30.
Tags: cv::pilote cv::d13 famille::raisonnement cv_id::CV-METRIQUES-TEMPS-002 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-003

Objective: choose a trajectory alignment. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-003
Question: Why can Sim(3) alignment be inappropriate when evaluating VIO that is supposed to recover metric scale?
Reponse: **Expected answer**: Adjusts the scale and can therefore hide a metric error that the system had to avoid.

**Further explanation**: The alignment group must follow the gauges and the lens; with fixed gravity, free rotation can also mask tilt errors.

**Example of hidden error**: A trajectory twice as large can be visually superimposed on the reference if the alignment freely adjusts the scale. The score after this registration then no longer tests the mischievousness that the system had to provide. It may be correct for another free-scale task.

**Proposed Protocol**: advertise legitimate gauges before observing the results and keep an independent physical reference. Separate arbitrary global translation, global yaw and relative drifts over time. If gravity provides absolute direction under system assumptions, a fully free 3D rotation can also remove a useful error to be measured. The choice is not to look for the transformation giving the prettiest path: it defines which errors are deliberately excluded from the score. Report this transformation and justify it by the information actually available.

**Permitted processing**: a similarity written $p'=sRp+t$ and has a freedom of scale $s$ absent from a rigid transformation. If a metric estimate is everywhere $\hat p=2p$, choose $s=1/2$ removes this error entirely in an ideal case. For a system with only one global origin and one global yaw, the alignment must preserve the other physical information that you want to test. Document the adjusted parameters and report, if useful, the estimated scale factor as a separate diagnosis. Do not confuse correction of coordinate frame and correction of a property that the system was precisely supposed to provide correctly.

**Blocking errors**: Optimize alignment to get the best score without justification.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; [Zhang – Scaramuzza, §III and Table I: Alignment Groups](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf); [Luiten et al., HOTA, §5, combination by threshold; inferred inequality of aggregation](https://arxiv.org/html/2009.07736v2), see 2026-10-30.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-TEMPS-003 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-004

Objective: distinguish ATE and RPE. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-004
Question: Do ATE and RPE answer exactly the same question?
Reponse: **Expected answer**: ATE evaluates a trajectory after alignment; RPE evaluates relative displacements at defined intervals.

**Further explanation**: Specify time/interval distance, aggregation, translation/rotation and failures; path length and looping influence interpretation.

**Reading two time scales**: A trajectory can maintain fairly precise local displacements while accumulating a global drift. Conversely, a loop correction can improve overall overlay without making each local movement perfectly accurate. The two measures therefore question complementary properties.

**Proposed evaluation**: Set displacement interval, matching time and unit, then report translation and rotation separately. For a RPE, short and long intervals do not represent the same difficulty. For a ATE, the alignment group removes certain ambiguities and must be announced. Keep lost segments and uptime: A method that stops issuing on difficult cases should not appear perfect by measuring only easy portions. The numbers are read with length, movement and coverage of the sequence, not as universal quality constants.

**Explicit relative error**: for poses bodies→world $T_i$ real and $\hat T_i$ estimated, form $E_{ij}=(T_i^{-1}T_j)^{-1}(\hat T_i^{-1}\hat T_j)$. The ideal is identity. Report norm translation and angle of rotation with the chosen interval $i,j$. A common global coordinate frame transformation cancels out in relative displacements, while a drift between moments persists. An interval set in frames is not a fixed interval in seconds if the cadence varies. This formula and its conventions must accompany the name RPE for a result to be interpretable and reproducible.

**Blocking errors**: Compare numbers without protocol, unit, or interval.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; [Sturm et al., §VII-A/B: RPE and ATE](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf); [Zhang – Scaramuzza, §IV and Table II](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf); [Luiten et al., HOTA, §5, combination by threshold; inferred inequality of aggregation](https://arxiv.org/html/2009.07736v2), see 2026-10-30.
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-METRIQUES-TEMPS-004 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-005

Objective: Comparing temporal evaluators. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-005
Question: Two tools report different trajectory errors for the same poses. What should be checked?
Reponse: **Expected answer**: matching time, interpolation, conventions of pose, alignment, intervals and loss processing.

**Further explanation**: Replay a small known case and then the same file/version; do not assign the deviation immediately to the estimator.

**Reproducible investigation**: First check the timestamps and how many poses have actually been matched. check then sense camera→world or world→camera, units of translations and convention of rotation. Replay a known synthetic path with global translation and then a scale error to observe what each tool removes.

**Fair comparison**: Retain files and versions, alignment group, interpolation and RPE interval, as well as processing absences. Two tools can display ATE while differing in these choices. A protocol difference does not immediately constitute an estimator error. Once the conventions are aligned, the remaining deviations warrant a more accurate inspection of the calculation. The trace must allow another engineer to reproduce the same set of poses compared and the same size, and not just an image of superimposed trajectories.

**Interpolation and Time**: A trajectory sampled at different times of the reference requires a matching or announced interpolation. Interpolating a translation is different from directly interpolating the components of a rotation matrix, which can then leave $SO(3)$. A constant time shift produces a speed-dependent error and can be mistaken for a wrong trajectory. Testing a synthetic movement at known speed with an imposed offset allows to verify this signature. Also keep the number of poses excluded by time tolerance: a drop in error obtained by removing difficult segments does not measure the same coverage.

**Blocking errors**: Compare only the name ATE displayed by the tools.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; Project protocol diagnosis; [Sturm et al., §VII: synchronization and poses](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf); [Zhang – Scaramuzza, §§III – IV](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf); [Luiten et al., HOTA, §5, combination by threshold; inferred inequality of aggregation](https://arxiv.org/html/2009.07736v2), see the 2026-10-30.
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-METRIQUES-TEMPS-005 provenance::agent pole::B pole::C pole::D
END
