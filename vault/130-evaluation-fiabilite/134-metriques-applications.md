# Flashcards — Metrics for segmentation, inspection and applications

reference note: [[130-evaluation-fiabilite/references/134-metriques-applications|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-METRIQUES-APPLIQUEES-001

Objective: Distinguish between border and border. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-001
Question: Why can Dice and HD95 tell different stories about the same mask?
Reponse: **Expected answer**: Dice measures an overlap; HD95 a surface distance in a percentile/protocol, with physical unit if coordinates are calibrated.

**Further explanation**: Define empty masks, directions, and aggregation; a distant outline or small region may weigh differently.

**Example of Divergence**: A large mask can retain almost its entire volume while a small area is far away. Covering and a surface distance weighted this gap differently. A percentile also discards some of the extreme distances according to the definition used; it is not necessarily the maximum distance.

**Proposed Protocol**: announce definition of surfaces, directed or symmetrized distances, percentile, spacing and unity. Keep empty processing and aggregation level per case or pixel. Examine examples where metrics diverge to identify the error they reveal, rather than automatically choosing the favorable score. A distance in millimeters requires consistent physical geometry. These measures can be complementary if the use depends on both coverage and boundary; no isolated value demonstrates the full quality of the mask or its usefulness in another process.

**Link and difference of units**: for two non-empty binary masks under the same count, $Dice=2IoU/(1+IoU)$. These two overlaps are therefore linked for the same pair, while a surface distance uses the geometric positions of the borders and a unit of length. Aggregating the Dice per case is not necessarily equivalent to converting a global IoU by this formula, because the conversion is nonlinear and the weights change. HD95 also requires a precise convention of directions and percentile. The choice of metrics must thus announce both the quantity per pair and the level at which the averages are calculated.

**Blocking errors**: Compare directly a number without a unit to a length.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Full reference]] ; [Metrics Reloaded, Semantic segmentation](https://doi.org/10.1038/s41592-023-02151-z) ; [Reinke et al., fig. 4a and 5c: overlap/borders and HD95](https://www.nature.com/articles/s41592-023-02150-0).
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-METRIQUES-APPLIQUEES-001 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-002

Objective: Measure the small flaws. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-002
Question: Why can a global pixel score hide missed small defects in inspection?
Reponse: **Expected answer**: Background pixels or large defects dominate some aggregates; analysis by region/piece and size can reveal gaps.

**Further explanation**: Specify AU-PRO and its FPR range if used, plus release rate/misses at useful threshold.

**Constructed example**: Missing a tiny flaw can only change a few pixels in a large image perfectly segmented elsewhere. An overall average remains high while the critical event for the piece is lost. Several large, easy flaws can also mask poor performance on rare regions.

**Proposed evaluation**: Measure default recall, false rejects per part and location at useful scale, then stratify size, type and acquisition. If a metric per region like PRO is used, announce its conventions and the built-in false positive range, as areas under different domains are not comparable. Keep negatives and missed cases in the balance sheet. A good measurement should allow the decision to be made; it is not chosen because it aggregates pixels in a way that makes the result more flattering.

**Weighting by region**: A region-by-region overlap measure can assign to each annotated defect the fraction of its pixels found, and then average those fractions. A fault of 10 pixels then receives the same region weight as a fault of 1 000 pixels, unlike a pooling of all the defective pixels. This convention makes certain small regions visible without solving all the ambiguities of location. An area under a curve must specify the axis of false positives, its range and its normalization. Completing by decision by part and entirely missed defects retains the link with the actual load of rejects and business risks.

**Blocking errors**: Compare AU-PRO with different ranges without reporting it.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Full reference]] ; [MVTec AD2 v1, evaluation protocol and fig. 4: PRO and weighting of regions](https://arxiv.org/abs/2503.21622v1).
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

**Difference in sources of error**: The reprojection RMS describes an adjustment of image points to the model. The length measurement also depends on the scale, the pose, the acquisition, the assembly and the measurement procedure. Repeating under the same conditions tests a variation different from that obtained by changing operator or configuration.

**Protocol built**: use an independent reference dimension, repeat the acquisitions and then vary the conditions provided by the study, keeping the units and geometry. Separate mean offset from reference and dispersion of repetitions; also examine evolution over time. The definition of the factors of variation must correspond to the actual exploitation. A low dispersion around a biased length is not good accuracy. This reasoning completes the camera calibration without claiming that a pixel score directly provides the dimensional uncertainty of the entire chain.

**Dimensional propagation**: for a simplified flat measurement $L=s\,p$ with $p$ pixel length and $s$ scale in mm/px, $\delta L\simeq p\delta s+s\delta p$. Under centered independent errors, $\sigma_L^2\simeq p^2\sigma_s^2+s^2\sigma_p^2$; otherwise add covariances. A repeatable location in pixels can therefore coexist with a dominant scale bias. This calculation assumes a plane geometry and a scale adapted, not a perspective camera of any kind. Repeating the measurement and varying the conditions predicted by the study then makes it possible to estimate contributions that the only calibration RMS does not represent.

**Blocking errors**: Directly convert an adjustment pixel error into a millimeter warranty.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Full reference]] ; [NIST, 2.4.4.1 repeatability](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc441.htm), [2.4.4.2 reproducibility](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc442.htm), [2.4.4.3 stability](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc443.htm), [2.4.5 bias](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc45.htm).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-METRIQUES-APPLIQUEES-003 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-004

Objective: Treat the empty masks. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-004
Question: What must be stated when a segmentation metric encounters an empty reference or prediction?
Reponse: **Expected answer**: The chosen convention and its effect on the score/aggregation; do not let an indefinite division become an implied result.

**Further explanation**: False positives on negative cases and lack of detection should remain visible.

**Distinguishing situations**: two empty masks, an empty reference with false positive and an empty prediction on a present object do not have the same meaning. A surface distance may be indefinite when a surface is missing, while an overlap may require a special convention for a zero denominator.

**Choice of proposed protocol**: define these cases before the results and keep them in a separate counting table if the main metric cannot summarize them. Announce conventional values, possible exclusions and weight in aggregation. Silently removing negative cases can hide false positives; removing empty predictions can hide entirely missed objects. Test some known synthetic examples in the evaluation tool and keep its version. The convention is not a digital trick: it determines which errors the final score represents and which must be reported otherwise.

**Case table defined before measurement**: if both reference and prediction are empty, the denominator of Dice is zero and a convention is required. If only the prediction is empty with present reference, the overlap is zero; if only the reference is empty with present prediction, it is also zero, but the business error is a false positive rather than a missed object. A surface distance may lack a set of points in each of these cases. Keeping counters of these situations and announcing their inclusion or exclusion prevents a filtered epsilon or `NaN` from silently changing the evaluated population.

**Blocking errors**: Silently remove all empty cases to improve the average.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Full reference]] ; [Reinke et al., P2.3 – P2.4 and P3.2: empty outputs/references and aggregation](https://www.nature.com/articles/s41592-023-02150-0).
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-METRIQUES-APPLIQUEES-004 provenance::agent pole::A pole::E
END
