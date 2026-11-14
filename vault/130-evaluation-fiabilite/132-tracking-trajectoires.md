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

**Constructed example**: Keep the boxes and classes of two pedestrians exactly, but exchange their IDs in the middle of the video. Spatial associations to the GT can remain identical in each frame for detection evaluation. Temporal continuity becomes false.

**Choice of metrics**: Examine detection, association, fragmentation and disappearances under a declared sequence protocol. An identity metric requires its own association and aggregation rules; a count of ID switches cannot replace all other aspects of tracking. Compare the same sequences, ignored periods and detections when looking for the contribution of association. The result may also depend on the outputs emitted during track losses. This distinction explains why the learning path introduces IoU before SORT, and then returns to temporal metrics after defining the tracker's responsibilities.

**Decomposition of tracking errors**: A missing box on the right target is a detection error, while a correct box with a wrong ID is an association error under the protocol. Fragmentation splits one true identity into several predicted tracks; a merge links several objects to one track. A simple number of switches does not necessarily describe their duration or all these relationships. Building the same boxes with several ID schemes lets you check what each metric penalizes. Presenting components and temporal examples helps explain a tracker's gain instead of ranking two systems on a single scalar.

**Blocking errors**: Deducing identity quality from AP alone.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; [Luiten et al., HOTA, §4.1 (IDSW), §4.2 (IDF1 matching) and §5 (association scores TPA, FNA, FPA)](https://arxiv.org/abs/2009.07736); [Ristani et al., §3.3, truth-to-result match](https://arxiv.org/abs/1609.01775). Swapped-ID case: project construction.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-TEMPS-001 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-002

Objective: Comply with the HOTA aggregation. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-002
Question: Why does calculating sqrt(mean DetA × mean AssA) not necessarily reproduce HOTA?
Reponse: **Expected answer**: The reference calculates the root of the product at each threshold and then averages these scores; the two operations do not commute in general.

**Further explanation**: Keep matching conventions, ignore rules and localization; a formula summary is not the whole evaluator.

**Analytical counterexample**: Take two thresholds with pairs $(DetA,AssA)=(1,0)$ and $(0,1)$. The root of the product is zero at each threshold, so their average is zero. The averages of the components are each 0.5; the root of their product is then 0.5. The order of operations does change the result. This case shows an algebraic property, without constituting a HOTA benchmark.

**Practical consequence**: Keep the values at the level where the protocol combines them, and then use the reference code and its parameters. Different matching, class or ignore rules can also modify components before aggregation. A summarized formula helps to interpret the balance between detection and association; it does not replace the whole definition. Comparing a hand-built figure with an official tool therefore requires reproducing the same inputs and all relevant conventions. The reference implementation also differs from the paper's per-threshold matching: it runs one assignment per frame and filters it at each threshold.

**Mean of components and their covariation**: For nonnegative $D_k,A_k$, Cauchy–Schwarz gives $\frac1n\sum_k\sqrt{D_kA_k}\le\sqrt{(\frac1n\sum_kD_k)(\frac1n\sum_kA_k)}$. Reconstructing the score from the averaged components can therefore overestimate the mean of the per-threshold combinations. Equality requires proportional profiles, that is, the same ratio $D_k/A_k$ at every threshold, with zero components handled separately. This algebraic property applies at the aggregation level considered; other averages over classes or sequences have their own conventions. The numerical counterexample of the flashcard demonstrates this order of operations, without claiming to represent feasible components of a particular benchmark.

**The aggregation gap has an angle interpretation**: Set $u_k=\sqrt{D_k}$ and $v_k=\sqrt{A_k}$ across $n$ thresholds. The mean per-threshold geometric mean is $H=(u^Tv)/n$, while recombination of component means is $R=\|u\|\|v\|/n$. For nonzero vectors, $H=R\cos\phi$, where $\phi$ is their angle. Thus the recombination gap is $R(1-\cos\phi)$: different threshold profiles, not just different average component quality, create the discrepancy. This is an algebraic interpretation, not a feasibility claim about arbitrary benchmark profiles.

**Blocking errors**: Freely swapping the mean and the square root.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; [Luiten et al., HOTA, §5 eqs. 13–16 (HOTA per threshold, then mean over 19 thresholds) and §6 eqs. 18–21](https://arxiv.org/abs/2009.07736); [TrackEval `hota.py` at 12c8791, L66–L97 and L166–L173](https://github.com/JonathonLuiten/TrackEval/blob/12c8791b303e0a0b50f753af204249e622d0281a/trackeval/metrics/hota.py#L66-L173). Counterexample, Cauchy–Schwarz bound and angle reading: project derivations.
Tags: cv::pilote cv::d13 famille::raisonnement cv_id::CV-METRIQUES-TEMPS-002 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-003

Objective: choose a trajectory alignment. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-003
Question: Why can Sim(3) alignment be inappropriate when evaluating VIO that is supposed to recover metric scale?
Reponse: **Expected answer**: Adjusts the scale and can therefore hide a metric error that the system had to avoid.

**Further explanation**: The alignment group must follow the gauge freedoms and the evaluation objective; with gravity fixing roll and pitch, a free 3D rotation can also mask tilt errors.

**Example of hidden error**: A trajectory twice as large can be visually superimposed on the reference if the alignment freely adjusts the scale. The score after this registration then no longer tests the metric scale that the system had to provide. It may be correct for another, scale-free task.

**Proposed protocol**: Declare the legitimate gauge freedoms before observing the results and keep an independent physical reference. Separate arbitrary global translation, global yaw and relative drift over time. If gravity provides an absolute direction under the system's assumptions, a fully free 3D rotation can also remove an error that should be measured. The choice is not to look for the transformation giving the best-looking trajectory: it defines which errors are deliberately excluded from the score. Report this transformation and justify it by the information actually available.

**Permitted transformation**: A similarity, written $p'=sRp+t$, has a scale freedom $s$ absent from a rigid transformation. If a metric estimate is everywhere $\hat p=2p$, choosing $s=1/2$ removes this error entirely in an ideal case. For a system whose only unobservable quantities are a global origin and a global yaw, the alignment must preserve the other physical information you want to test. Document the fitted parameters and, if useful, report the estimated scale factor as a separate diagnostic. Do not confuse correcting the coordinate frame with correcting a property that the system was supposed to provide.

**Blocking errors**: Optimizing the alignment to get the best score without justification.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; [Zhang and Scaramuzza 2018, §III-A (ambiguities), §III-C eq. 13 and Table I (alignment groups)](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf); [Sturm et al. 2012, §VII-B (ATE after least-squares alignment)](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf). Scale and tilt examples: project constructions.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-TEMPS-003 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-004

Objective: distinguish ATE and RPE. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-004
Question: Do ATE and RPE answer exactly the same question?
Reponse: **Expected answer**: ATE evaluates a trajectory after alignment; RPE evaluates relative displacements at defined intervals.

**Further explanation**: Specify the interval in time or distance, the aggregation, translation versus rotation and the handling of failures; path length and loop closures influence the interpretation.

**Reading two time scales**: A trajectory can keep fairly precise local displacements while accumulating a global drift. Conversely, a loop-closure correction can improve the overall overlay without making each local motion accurate. The two measures therefore probe complementary properties.

**Proposed evaluation**: Set the displacement interval, the time association and the unit, then report translation and rotation separately. For an RPE, short and long intervals do not represent the same difficulty. For an ATE, the alignment group removes certain ambiguities and must be declared. Keep lost segments and availability: a method that stops producing output on difficult cases should not appear perfect by measuring only easy portions. The numbers are read with the length, motion and coverage of the sequence, not as universal quality constants.

**Explicit relative error**: For body-to-world poses $T_i$ (ground truth) and $\hat T_i$ (estimate), form $E_{ij}=(T_i^{-1}T_j)^{-1}(\hat T_i^{-1}\hat T_j)$. The ideal is the identity. Report the translation norm and the rotation angle with the chosen interval $i,j$. A common global transformation of the coordinate frame cancels out in relative displacements, while drift between instants persists. An interval fixed in frames is not a fixed interval in seconds if the frame rate varies. This formula and its conventions must accompany the name RPE for a result to be interpretable and reproducible.

**Relative error depends on the interval**: A tracker may have low frame-to-frame relative error but accumulate substantial drift over long distances. Another system can exhibit a correction jump that improves globally aligned ATE while producing a large short-interval RPE. Evaluate relative error over declared time or distance intervals and report corrections or loop closures. The interval and whether future optimization was allowed are part of the metric, not minor implementation details.

**Blocking errors**: Comparing numbers without protocol, unit or interval.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; [Sturm et al. 2012, §VII-A eqs. 1–3 (RPE) and §VII-B eqs. 4–5 (ATE)](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf); [Zhang and Scaramuzza 2018, §IV and Table II](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf). Frame invariance and interval cases: project deductions.
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-METRIQUES-TEMPS-004 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-005

Objective: Comparing temporal evaluators. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-005
Question: Two tools report different trajectory errors for the same poses. What should be checked?
Reponse: **Expected answer**: Time association, interpolation, pose conventions, alignment, intervals and the handling of lost or missing poses.

**Further explanation**: Replay a small known case, then the same file and version; do not attribute the deviation immediately to the estimator. The tools' defaults also differ in the reported statistic: the TUM `evaluate_rpe.py` prints a mean translational error by default, whereas the paper defines an RMSE.

**Reproducible investigation**: First check the timestamps and how many poses were actually associated. Then check the direction (camera→world or world→camera), translation units and the rotation convention. Replay a known synthetic trajectory with a global translation and then with a scale error to observe what each tool removes.

**Fair comparison**: Keep the files and versions, the alignment group, interpolation and RPE interval, as well as the handling of missing poses. Two tools can both display "ATE" while differing in these choices. A protocol difference is not in itself an estimator error. Once the conventions are aligned, the remaining deviations warrant a closer inspection of the calculation. The trace must allow another engineer to reproduce the same set of compared poses and the same quantity, not just an image of superimposed trajectories.

**Interpolation and time**: A trajectory sampled at times different from the reference requires a declared association or interpolation. Interpolating a translation differs from interpolating the components of a rotation matrix directly, which can leave $SO(3)$. A constant time shift produces a speed-dependent error and can be mistaken for a wrong trajectory. Testing a synthetic motion at known speed with an imposed offset verifies this signature. Also report the number of poses excluded by the time tolerance: an error reduction obtained by removing difficult segments does not measure the same coverage.

**Missing poses should not disappear from the denominator**: If one tool silently drops difficult timestamps, its error over surviving matched poses may decrease while trajectory availability worsens. Align time association, tolerance and interpolation first, then report matched coverage and failures with error. A proposed fixture includes a deliberate gap and known time offset to test both tools' policies. Do not interpolate across an arbitrarily long outage and count the synthetic poses as equally observed estimates.

**Blocking errors**: Comparing only the "ATE" name displayed by the tools.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Full reference]]; [Sturm et al. 2012, §VI (time delays, `associate.py`) and §VII (RPE, ATE)](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf); [TUM RGB-D tools page, `evaluate_ate.py` and `evaluate_rpe.py` options](https://cvg.cit.tum.de/data/datasets/rgbd-dataset/tools); [Zhang and Scaramuzza 2018, §§III–IV](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf). Diagnostic order and fixtures: project protocol.
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-METRIQUES-TEMPS-005 provenance::agent pole::B pole::C pole::D
END
