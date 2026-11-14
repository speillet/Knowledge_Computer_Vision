# Flashcards — Metrics for segmentation, inspection and applications

reference note: [[130-evaluation-fiabilite/references/134-metriques-applications|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-METRIQUES-APPLIQUEES-001

Objective: Distinguish overlap and boundary. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-001
Question: Why can Dice and HD95 tell different stories about the same mask?
Reponse: **Expected answer**: Dice measures an overlap; HD95 a surface distance in a percentile/protocol, with physical unit if coordinates are calibrated.

**Further explanation**: Define empty masks, directions, and aggregation; a distant outline or small region may weigh differently.

**Example of divergence**: A large mask can keep almost all its volume while a small part of its surface is far away. Overlap and a surface distance weigh this deviation differently. A percentile also discards some of the extreme distances, depending on the definition used; it is not necessarily the maximum distance.

**Proposed protocol**: Declare the surface definition, directed or symmetrized distances, percentile, spacing and unit. Keep the handling of empty masks and the aggregation level (per case or per pixel). Examine examples where the metrics diverge to identify the error each reveals, rather than automatically choosing the favorable score. A distance in millimeters requires a consistent physical geometry. These measures are complementary when the use depends on both coverage and boundary; no single value demonstrates the full quality of the mask or its usefulness in another process.

**Relation and difference of units**: For two non-empty binary masks counted the same way, $Dice=2IoU/(1+IoU)$. These two overlaps are therefore linked for the same pair, while a surface distance uses the positions of the boundaries and a unit of length. Averaging Dice per case is not equivalent to converting a global IoU with this formula, because the conversion is nonlinear and the weights change. HD95 also requires a precise convention for directions and percentile. The choice of metrics must therefore state both the quantity per pair and the level at which averages are computed.

**A percentile deliberately ignores part of the tail**: HD95 summarizes a specified 95th percentile of surface distances, so a sufficiently small collection of extreme surface errors may lie outside its reported percentile. Dice can also remain high when a large region dominates. Include a maximum or task-specific local boundary check when a tiny outlying structure matters. State whether directed distances are pooled or their percentiles combined, because those conventions can produce different HD95 values.

**Blocking errors**: Comparing a unitless number directly with a length.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Full reference]]; [Maier-Hein et al., Metrics Reloaded, semantic segmentation recommendations and Suppl. Note 2.7.6 (DG7.3, HD versus percentile HD)](https://arxiv.org/html/2206.01653v8); [Reinke et al., P2.1 Fig. 4a (boundary-unaware overlap) and P2.3 Fig. 5c (HD and reference outliers)](https://arxiv.org/html/2302.01790v4); [MONAI 1.6.1 `hausdorff_distance.py` L224–L249 (maximum of directed percentiles)](https://github.com/Project-MONAI/MONAI/blob/1.6.1/monai/metrics/hausdorff_distance.py#L224-L249). Dice–IoU relation and percentile cases: project derivations.
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-METRIQUES-APPLIQUEES-001 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-002

Objective: Measure small defects. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-002
Question: Why can a global pixel score hide missed small defects in inspection?
Reponse: **Expected answer**: Background pixels or large defects dominate some aggregates; analysis by region/piece and size can reveal gaps.

**Further explanation**: Specify AU-PRO and its FPR range if used, plus the reject rate and misses at the operating threshold.

**Constructed example**: Missing a tiny defect changes only a few pixels in a large image otherwise perfectly segmented. An overall average remains high while the critical event for the part is lost. Several large, easy defects can also mask poor performance on rare regions.

**Proposed evaluation**: Measure defect recall, false rejects per part and localization at a useful scale, then stratify by size, type and acquisition. If a per-region metric such as PRO is used, state its conventions and the false-positive range of integration, because areas over different ranges are not comparable. Keep negatives and missed cases in the results. A good measurement should support the decision; it is not chosen because it aggregates pixels in a way that makes the result more flattering.

**Weighting by region**: A region-by-region overlap measure can assign to each annotated defect the fraction of its pixels found, and then average those fractions. A defect of 10 pixels then receives the same weight as a defect of 1,000 pixels, unlike a pooling of all defective pixels. This convention makes small regions visible without solving every localization ambiguity. An area under a curve must specify the false-positive axis, its range and its normalization. Adding part-level decisions and entirely missed defects keeps the link with the actual reject load and business risk.

**Pixel and part denominators imply different burdens**: One false-positive pixel per normal image and one entirely false detected part do not have the same operational meaning. Define how connected predictions become alarms and how alarms match real defects before reporting false positives per part. Stratify recall by defect size and type, retaining sample counts. This proposed protocol prevents a favorable background-dominated pixel aggregate from hiding missed critical regions or excessive review workload.

**Blocking errors**: Comparing AU-PRO values computed up to different FPR limits without reporting it.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Full reference]]; [Heckler-Kram et al., MVTec AD 2, §IV-B1 eq. 1 and Fig. 4 (PRO, region weighting, FPR limits 0.30 and 0.05) and §IV-B2 (thresholded F1)](https://arxiv.org/abs/2503.21622v1). Part-level protocol: project reasoning.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-APPLIQUEES-002 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-003

Objective: separate calibration and metrology. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-003
Question: Does low camera RMS establish the repeatability and reproducibility of a length measurement?
Reponse: **Expected answer**: No: Repeat measurements and vary relevant conditions/configurations, with dimensional reference and analysis of sources of variation.

**Further explanation**: Distinguish bias, repeatability, reproducibility and stability; set business tolerance.

**Difference in sources of error**: The reprojection RMS describes how well image points fit the camera model. The length measurement also depends on the scale, the pose, the acquisition, the fixturing and the measurement procedure. Repeating under the same conditions tests a different variation from the one obtained by changing operator or configuration.

**Constructed protocol**: Use an independent reference dimension, repeat the acquisitions and then vary the conditions planned by the study, keeping units and geometry. Separate the mean offset from the reference from the dispersion of repetitions; also examine drift over time. The factors of variation must correspond to actual operation. A low dispersion around a biased length is not good accuracy. This reasoning complements camera calibration without claiming that a pixel score directly gives the dimensional uncertainty of the whole chain.

**Dimensional propagation**: For a simplified planar measurement $L=s\,p$ with $p$ the length in pixels and $s$ the scale in mm/px, $\delta L\simeq p\,\delta s+s\,\delta p$. Under centered independent errors, $\sigma_L^2\simeq p^2\sigma_s^2+s^2\sigma_p^2$; otherwise add covariances. A repeatable location in pixels can therefore coexist with a dominant scale bias. This calculation assumes a planar geometry and a suitable scale, not an arbitrary perspective camera. Repeating the measurement and varying the conditions planned by the study then makes it possible to estimate contributions that the calibration RMS alone does not represent.

**Repeatability does not establish absence of bias**: A fixed camera can repeatedly report 10.2 mm for a true 10.0 mm reference with very small dispersion. Repeatability is good in this constructed example while bias remains 0.2 mm. Vary the relevant operator, setup or environmental factors to study reproducibility, and compare with an independent dimensional reference. Low calibration RMS does not directly measure either component of the final measurement process.

**Blocking errors**: Converting a fitting (reprojection) error in pixels directly into a guaranteed accuracy in millimeters.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Full reference]]; [NIST/SEMATECH e-Handbook, §2.4.4.1 repeatability](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc441.htm), [§2.4.4.2 reproducibility](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc442.htm), [§2.4.4.3 stability (not re-read on 2026-11-14)](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc443.htm), [§2.4.5 bias, including calibration versus working environment](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc45.htm). Propagation formula and 10.2 mm example: project constructions.
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-METRIQUES-APPLIQUEES-003 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-004

Objective: Handle empty masks. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-004
Question: What must be stated when a segmentation metric encounters an empty reference or prediction?
Reponse: **Expected answer**: The chosen convention and its effect on the score/aggregation; do not let an indefinite division become an implied result.

**Further explanation**: False positives on negative cases and lack of detection should remain visible.

**Distinguishing situations**: Two empty masks, an empty reference with a false positive and an empty prediction on a present object do not have the same meaning. A surface distance may be undefined when a surface is missing, while an overlap may require a special convention for a zero denominator.

**Proposed protocol choice**: Define these cases before the results and keep them in a separate count table if the main metric cannot summarize them. Declare conventional values, possible exclusions and their weight in the aggregation. Silently removing negative cases can hide false positives; removing empty predictions can hide entirely missed objects. Test a few known synthetic examples in the evaluation tool and record its version. The convention is not a numerical trick: it determines which errors the final score represents and which must be reported otherwise. Libraries already encode a default: in MONAI 1.6.1, Dice is NaN for an empty reference unless `ignore_empty=False`, the Hausdorff distance is infinite when one mask is empty and NaN when both are, and the default reduction averages only non-NaN values.

**Case table defined before measurement**: If both reference and prediction are empty, the denominator of Dice is zero and a convention is required. If only the prediction is empty with a present reference, the overlap is zero; if only the reference is empty with a present prediction, it is also zero, but the business error is a false positive rather than a missed object. A surface distance may lack a point set in each of these cases. Keeping counters of these situations and declaring their inclusion or exclusion prevents an epsilon or a filtered `NaN` from silently changing the evaluated population.

**Empty-case policy can dominate a rare-object mean**: Constructed example: 99 empty cases and one missed positive produce a mean Dice of 0.99 if empty/empty receives one and the missed positive receives zero. The sole real object was still missed. Report positive-case performance, negative-case false alarms and the empty-case convention separately where relevant. A defined aggregation policy makes the number reproducible; it does not automatically make it suitable for the application decision.

**Blocking errors**: Silently removing all empty cases to improve the average.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Full reference]]; [Reinke et al., P2.3–P2.4 and P3.2: empty references and predictions, aggregation](https://arxiv.org/html/2302.01790v4); [MONAI 1.6.1 `meandice.py` L106–L108 (`ignore_empty`) and `utils.py` L333–L343 (infinite distances for empty masks)](https://github.com/Project-MONAI/MONAI/blob/1.6.1/monai/metrics/meandice.py#L106-L108). Rare-object mean: constructed example.
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-METRIQUES-APPLIQUEES-004 provenance::agent pole::A pole::E
END
