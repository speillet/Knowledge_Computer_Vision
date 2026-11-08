---
id: CV-METRIQUES-APPLIQUEES
type: metrique-protocole
domaine: d13
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-IOU-AP", "CV-SEGMENTATION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d13]
---
# Metrics for segmentation, inspection and applications

## Problem, data and assumptions

Choose the measure based on the decision to be made and the unit of assessment. A pixel, a defective region, a part, a patient, and a document must not be implicitly weighted the same. The protocols of empty masks, absent classes and aggregation are explained.

## Prerequisites and competencies

**Required prerequisites**: [CV-IOU-AP](131-iou-ap-coco.md); [CV-SEGMENTATION](../../90-segmentation/references/93-semantique-instances-panoptique.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Coverage (IoU/Dice), surface distance (HD95), fault detection/location (AUROC/PRO), text recognition (CER/WER), biometrics and metrology respond to different errors. The reference note compares the choices; the specialized detailed definitions remain to be explored separately.

## Mathematics, conventions and units

Dice=$2TP/(2TP+FP+FN)$ under defined convention. HD95 requires surfaces, physical unit and percentile/directions definition. PRO gives a weight per region according to protocol; specify the integration FPR domain AU-PRO. In metrology, bias, repeatability, reproducibility and stability are distinct; a RMS pixel camera is not a dimensional uncertainty.

## Parameters and properties

Units, ignored objects, size, negatives, thresholds, and aggregation. A patient with a large volume or an extended defect should not hide critical cases by an uncontrolled pooling pixel.

## Cost and implementation

Some surface distances cost more than counts; reference collection can dominate. No real R&R clinical, biometric or gauge use performed.

## Evaluation and controlled variation

Analytical variation: keep the large object properly segmented and then miss a small object. An average pixel can move little; one metric per region/case reveals the loss. Compare to business cost and operating threshold.

## Failure modes and diagnosis

Contradictory metrics: look for measured error, unity, voids, and protocol; do not automatically retain the most favorable score.

## Alternatives and applications

Report multiple complementary views and their limitations. The comparison rates FMR/FNMR, the system decisions FAR/FRR and PAD are not a single metric.

## Guided reasoning and proposed checks

These constructed cases develop topology, physical surfaces and uncertain references. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-METRIQUES-APPLIQUEES-001

**Question of work**: Why can Dice and HD95 tell different stories about the same mask?

**Reference Response**: Dice measures an overlap; HD95 a surface distance in a percentile/protocol, with physical unit if coordinates are calibrated.

**Example of Divergence**: A large mask can retain almost its entire volume while a small area is far away. Covering and a surface distance weighted this gap differently. A percentile also discards some of the extreme distances according to the definition used; it is not necessarily the maximum distance.

**Proposed Protocol**: announce definition of surfaces, directed or symmetrized distances, percentile, spacing and unity. Keep empty processing and aggregation level per case or pixel. Examine examples where metrics diverge to identify the error they reveal, rather than automatically choosing the favorable score. A distance in millimeters requires consistent physical geometry. These measures can be complementary if the use depends on both coverage and boundary; no isolated value demonstrates the full quality of the mask or its usefulness in another process.

### Case linked to CV-METRIQUES-APPLIQUEES-004

**Question of work**: What must be stated when a segmentation metric encounters an empty reference or prediction?

**Reference Response**: The chosen convention and its effect on the score/aggregation; do not let an indefinite division become an implied result.

**Distinguishing situations**: two empty masks, an empty reference with false positive and an empty prediction on a present object do not have the same meaning. A surface distance may be indefinite when a surface is missing, while an overlap may require a special convention for a zero denominator.

**Choice of proposed protocol**: define these cases before the results and keep them in a separate counting table if the main metric cannot summarize them. Announce conventional values, possible exclusions and weight in aggregation. Silently removing negative cases can hide false positives; removing empty predictions can hide entirely missed objects. Test some known synthetic examples in the evaluation tool and keep its version. The convention is not a digital trick: it determines which errors the final score represents and which must be reported otherwise.

**Documentary reference for this pass**: [Reinke et al., Understanding metric-related pitfalls](https://arxiv.org/html/2302.01790v4), P2.2 – P2.4: empty sizes, shapes, references/predictions. The other developments are in the [flashcards](../134-metriques-applications.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-METRIQUES-APPLIQUEES-001

**Situation**: Why can Dice and HD95 tell different stories about the same mask?

**Link and difference of units**: for two non-empty binary masks under the same count, $Dice=2IoU/(1+IoU)$. These two overlaps are therefore linked for the same pair, while a surface distance uses the geometric positions of the borders and a unit of length. Aggregating the Dice per case is not necessarily equivalent to converting a global IoU by this formula, because the conversion is nonlinear and the weights change. HD95 also requires a precise convention of directions and percentile. The choice of metrics must thus announce both the quantity per pair and the level at which the averages are calculated.

### CV-METRIQUES-APPLIQUEES-002

**Situation**: Why can a global pixel score hide missed small defects in inspection?

**Weighting by region**: A region-by-region overlap measure can assign to each annotated defect the fraction of its pixels found, and then average those fractions. A fault of 10 pixels then receives the same region weight as a fault of 1 000 pixels, unlike a pooling of all the defective pixels. This convention makes certain small regions visible without solving all the ambiguities of location. An area under a curve must specify the axis of false positives, its range and its normalization. Completing by decision by part and entirely missed defects retains the link with the actual load of rejects and business risks.

### CV-METRIQUES-APPLIQUEES-003

**Situation**: Does low camera RMS establish the repeatability and reproducibility of a length measurement?

**Dimensional propagation**: for a simplified flat measurement $L=s\,p$ with $p$ pixel length and $s$ scale in mm/px, $\delta L\simeq p\delta s+s\delta p$. Under centered independent errors, $\sigma_L^2\simeq p^2\sigma_s^2+s^2\sigma_p^2$; otherwise add covariances. A repeatable location in pixels can therefore coexist with a dominant scale bias. This calculation assumes a plane geometry and a scale adapted, not a perspective camera of any kind. Repeating the measurement and varying the conditions predicted by the study then makes it possible to estimate contributions that the only calibration RMS does not represent.

### CV-METRIQUES-APPLIQUEES-004

**Situation**: What must be stated when a segmentation metric encounters an empty reference or prediction?

**Case table defined before measurement**: if both reference and prediction are empty, the denominator of Dice is zero and a convention is required. If only the prediction is empty with present reference, the overlap is zero; if only the reference is empty with present prediction, it is also zero, but the business error is a false positive rather than a missed object. A surface distance may lack a set of points in each of these cases. Keeping counters of these situations and announcing their inclusion or exclusion prevents a filtered epsilon or `NaN` from silently changing the evaluated population.

**Passages consulted for these developments**: [NIST, repeatability](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc441.htm), repeatability analysis; Dice/IoU relationships, region counts, voids and uncertainty propagation derived by the project.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-METRIQUES-APPLIQUEES-001 — A percentile deliberately ignores part of the tail

HD95 summarizes a specified 95th percentile of surface distances, so a sufficiently small collection of extreme surface errors may lie outside its reported percentile. Dice can also remain high when a large region dominates. Include a maximum or task-specific local boundary check when a tiny outlying structure matters. State whether directed distances are pooled or their percentiles combined, because those conventions can produce different HD95 values.

### CV-METRIQUES-APPLIQUEES-002 — Pixel and part denominators imply different burdens

One false-positive pixel per normal image and one entirely false detected part do not have the same operational meaning. Define how connected predictions become alarms and how alarms match real defects before reporting false positives per part. Stratify recall by defect size and type, retaining sample counts. This proposed protocol prevents a favorable background-dominated pixel aggregate from hiding missed critical regions or excessive review workload.

### CV-METRIQUES-APPLIQUEES-003 — Repeatability does not establish absence of bias

A fixed camera can repeatedly report 10.2 mm for a true 10.0 mm reference with very small dispersion. Repeatability is good in this constructed example while bias remains 0.2 mm. Vary the relevant operator, setup or environmental factors to study reproducibility, and compare with an independent dimensional reference. Low calibration RMS does not directly measure either component of the final measurement process.

### CV-METRIQUES-APPLIQUEES-004 — Empty-case policy can dominate a rare-object mean

Constructed example: 99 empty cases and one missed positive produce a mean Dice of 0.99 if empty/empty receives one and the missed positive receives zero. The sole real object was still missed. Report positive-case performance, negative-case false alarms and the empty-case convention separately where relevant. A defined aggregation policy makes the number reproducible; it does not automatically make it suitable for the application decision.

Consulted foundations: [Metric-related pitfalls](https://arxiv.org/html/2302.01790v4): P2 boundary, size, empty-reference and aggregation pitfalls; [NIST repeatability](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc441.htm): repeatability variation and measurement-process evaluation.

## Sources and flashcards

- [Reinke et al., P2.1 – P2.4 and P3.2](https://www.nature.com/articles/s41592-023-02150-0): borders, voids and aggregation.

- [Metrics Reloaded](https://doi.org/10.1038/s41592-023-02151-z).
- [NIST, Gauge R&R](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm).
- [MVTec AD2, PRO and protocol](https://arxiv.org/abs/2503.21622v1).
- [Related flashcards](../134-metriques-applications.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
