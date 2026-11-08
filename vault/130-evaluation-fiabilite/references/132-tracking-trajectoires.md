---
id: CV-METRIQUES-TEMPS
type: metrique-protocole
domaine: d13
poles: [B, C, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-VIO", "CV-SORT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d13]
---
# Evaluating identities, trajectories and 3D localization

## Problem, data and assumptions

Evaluate the time or metric deliverable rather than a single detection. Inputs: sequences/tracks or poses timestamped and ground truth; outputs: scores under association rules and alignment announced. Absent trajectories and failures are part of the protocol.

## Prerequisites and competencies

**Required prerequisites**: [CV-VIO](../../60-vision-3d/references/63-slam-vio.md); [CV-SORT](../../110-tracking-association/references/111-sort.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

MOTA aggregates some false positives, lacks and identity exchanges; IDF1 targets an identity association; HOTA balances detection and association according to its thresholds. ATE compares an aligned trajectory; RPE compares relative displacements. Do not substitute one metric for another without defining the task.

## Mathematics, conventions and units

At a threshold $\alpha$, $HOTA_\alpha=\sqrt{DetA_\alpha AssA_\alpha}$ then the average score the thresholds; this is not the product root of the averages. For poses bodies→world, $T_i$ designating the ground truth and $\hat T_i$ estimating it, $E_{ij}=(T_i^{-1}T_j)^{-1}(\hat T_i^{-1}\hat T_j)$ defines a relative error. The translation is in meters and the rotation requires specified angle/unit.

## Parameters and properties

Association, classes, ignores, timestamps, interpolation, interval of RPE and alignment. Visual monocular: Sim(3) can be justified; VIO metric with fixed gravity: translation/yaw according to protocol. A free alignment can mask the errors that one seeks to measure.

## Cost and implementation

Evaluators have specific conventions; versioning output files and settings. No real benchmark is executed; no toy score is called a full HOTA.

## Evaluation and controlled variation

Analytical variation: keep boxes but swap IDs at crossing; AP per frame can remain the same while the association changes. For trajectory, inject a false scale and compare allowed alignments; a Sim(3) can hide it.

## Failure modes and diagnosis

Overall score good but rare trajectory lost: analyze lengths, segments and subgroups. Tool gap: Align protocol before concluding a bug.

## Alternatives and applications

Choose a battery related to the product: detection, identity, location and cost. NDS/mAP nuScenes are yet another 3D output protocol.

## Guided reasoning and proposed checks

These constructed cases develop identity, HOTA aggregation and trajectory alignment. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-METRIQUES-TEMPS-001

**Question of work**: How can two systems have identical frame-by-frame AP but different tracking quality?

**Reference Response**: Boxes/classes can be identical while IDs are exchanged or fragmented; AP does not measure this continuity.

**Constructed example**: Keep the boxes and classes of two pedestrians exactly, but exchange their IDs in the middle of the video. Spatial associations to the GT can remain identical to each frame for detection evaluation. Temporal continuity becomes false.

**Choice of measures**: Examine detection, association, fragments, and disappearance in an announced sequence protocol. An identity metric requires its own association and aggregation rules; a number of ID changes may not replace all other aspects of tracking. Compare the same sequences, ignored periods and detections when looking for the contribution of the association. The result produced may also depend on the outputs issued during losses. This distinction explains why the path introduces the IoU before SORT, and then returns to the time metrics after defining the responsibilities of the tracker.

### Case linked to CV-METRIQUES-TEMPS-005

**Question of work**: Two tools report different trajectory errors for the same poses. What should be checked?

**Reference Response**: matching time, interpolation, conventions of pose, alignment, intervals and loss processing.

**Reproducible investigation**: First check the timestamps and how many poses have actually been matched. check then sense camera→world or world→camera, units of translations and convention of rotation. Replay a known synthetic path with global translation and then a scale error to observe what each tool removes.

**Fair comparison**: Retain files and versions, alignment group, interpolation and RPE interval, as well as processing absences. Two tools can display ATE while differing in these choices. A protocol difference does not immediately constitute an estimator error. Once the conventions are aligned, the remaining deviations warrant a more accurate inspection of the calculation. The trace must allow another engineer to reproduce the same set of poses compared and the same size, and not just an image of superimposed trajectories.

**Documentary reference for this pass**: [Luiten et al., HOTA](https://arxiv.org/pdf/2009.07736), definition HOTA, DetA, AssA and aggregation. The other developments are in the [flashcards](../132-tracking-trajectoires.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-METRIQUES-TEMPS-001

**Situation**: How can two systems have identical frame-by-frame AP but different tracking quality?

**Decomposition of monitoring**: An absence of a box on the right target is a detection error, while a correct box with a bad ID is the association according to the protocol. Fragmentation divides a real identity into several predicted trackss; merging identities links several objects to a track. A simple number of switches does not necessarily describe their duration or all these relationships. Building the same boxes with multiple ID schemes allows you to check what each metric penalizes. Presenting components and temporal examples helps explain the gain of a tracker instead of classifying two systems on a single scalar.

### CV-METRIQUES-TEMPS-002

**Situation**: Why does calculating sqrt(mean DetA × mean AssA) not necessarily reproduce HOTA?

**Average and covariance of components**: for positive $D_k,A_k$, Cauchy – Schwarz gives $\frac1n\sum_k\sqrt{D_kA_k}\le\sqrt{(\frac1n\sum_kD_k)(\frac1n\sum_kA_k)}$. Reconstructing the score from the average components can therefore overestimate the average of the combinations per threshold. Equality requires a compatible ratio between sequences, with zeros being processed. This algebraic property applies to the level of aggregation considered; the other means between classes or sequences have their own conventions. The numerical counter-example of the flashcard demonstrates this order of operations, without claiming to represent feasible components of a particular benchmark.

### CV-METRIQUES-TEMPS-003

**Situation**: Why can Sim(3) alignment be inappropriate when evaluating VIO that is supposed to recover metric scale?

**Permitted processing**: a similarity written $p'=sRp+t$ and has a freedom of scale $s$ absent from a rigid transformation. If a metric estimate is everywhere $\hat p=2p$, choose $s=1/2$ removes this error entirely in an ideal case. For a system with only one global origin and one global yaw, the alignment must preserve the other physical information that you want to test. Document the adjusted parameters and report, if useful, the estimated scale factor as a separate diagnosis. Do not confuse correction of coordinate frame and correction of a property that the system was precisely supposed to provide correctly.

### CV-METRIQUES-TEMPS-004

**Situation**: Do ATE and RPE answer exactly the same question?

**Explicit relative error**: for poses bodies→world $T_i$ real and $\hat T_i$ estimated, form $E_{ij}=(T_i^{-1}T_j)^{-1}(\hat T_i^{-1}\hat T_j)$. The ideal is identity. Report norm translation and angle of rotation with the chosen interval $i,j$. A common global coordinate frame transformation cancels out in relative displacements, while a drift between moments persists. An interval set in frames is not a fixed interval in seconds if the cadence varies. This formula and its conventions must accompany the name RPE for a result to be interpretable and reproducible.

### CV-METRIQUES-TEMPS-005

**Situation**: Two tools report different trajectory errors for the same poses. What should be checked?

**Interpolation and Time**: A trajectory sampled at different times of the reference requires a matching or announced interpolation. Interpolating a translation is different from directly interpolating the components of a rotation matrix, which can then leave $SO(3)$. A constant time shift produces a speed-dependent error and can be mistaken for a wrong trajectory. Testing a synthetic movement at known speed with an imposed offset allows to verify this signature. Also keep the number of poses excluded by time tolerance: a drop in error obtained by removing difficult segments does not measure the same coverage.

**Passages consulted for these developments**: [Luiten et al., HOTA](https://arxiv.org/html/2009.07736v2), §5, threshold combination; inferred aggregation inequality; [Zhang–Scaramuzza](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf), §IV, ATE and relative error; RPE formula and time controls explained by the project.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-METRIQUES-TEMPS-002 — The aggregation gap has an angle interpretation

Set $u_k=\sqrt{D_k}$ and $v_k=\sqrt{A_k}$ across $n$ thresholds. The mean per-threshold geometric mean is $H=(u^Tv)/n$, while recombination of component means is $R=\|u\|\|v\|/n$. For nonzero vectors, $H=R\cos\phi$, where phi is their angle. Thus the recombination gap is $R(1-\cos\phi)$: different threshold profiles, not just different average component quality, create the discrepancy. This is an algebraic interpretation, not a feasibility claim about arbitrary benchmark profiles.

### CV-METRIQUES-TEMPS-004 — Relative error depends on the interval

A tracker may have low frame-to-frame relative error but accumulate substantial drift over long distances. Another system can exhibit a correction jump that improves globally aligned ATE while producing a large short-interval RPE. Evaluate relative error over declared time or distance intervals and report corrections or loop closures. The interval and whether future optimization was allowed are part of the metric, not minor implementation details.

### CV-METRIQUES-TEMPS-005 — Missing poses should not disappear from the denominator

If one tool silently drops difficult timestamps, its error over surviving matched poses may decrease while trajectory availability worsens. Align time association, tolerance and interpolation first, then report matched coverage and failures with error. A proposed fixture includes a deliberate gap and known time offset to test both tools' policies. Do not interpolate across an arbitrarily long outage and count the synthetic poses as equally observed estimates.

Consulted foundations: [HOTA](https://arxiv.org/html/2009.07736v2): §5 DetA/AssA and threshold aggregation; [Sturm et al. trajectory evaluation](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf): §VII-A/B RPE and ATE definitions.

## Sources and flashcards

- [Sturm et al., 2012, §VII-A/B, equations 1 – 4](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf): RPE and ATE; distinction with Zhang – Scaramuzza’s relative error by subtrajectories.

- [HOTA, §§5 – 6](https://arxiv.org/abs/2009.07736).
- [Zhang – Scaramuzza, §III/TableI and evaluation](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf).
- [nuScenes, detection metrics](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
- [Related flashcards](../132-tracking-trajectoires.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
