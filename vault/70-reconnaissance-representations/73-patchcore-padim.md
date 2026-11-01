# Flashcards — Inspection: golden templates, PatchCore and PaDiM

reference note: [[70-reconnaissance-representations/references/73-patchcore-padim|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-ANOMALIES-001

Objective: Choose a nominal model. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ANOMALIES-001
Question: Which tradeoffs distinguish golden-template inspection, PatchCore and PaDiM?
Reponse: **Expected answer**: Template compares to an aligned reference; PatchCore uses a feature bank; PaDiM estimates covariance distributions by position.

**Further explanation**: Choose according to nominal variability, alignment, memory and business evaluation; none knows about any possible defects.

**Reading the assumptions**: A direct comparison to the template requires that legitimate geometric and photometric deviations are sufficiently controlled. A nominal patch bank looks for representative neighbors; a position distribution model otherwise represents variability and correlations. The word anomaly here designates a deviation from this reference, not a universal definition of the business defect.

**Constructed example**: New lighting can move all features and increase scores without physically defective parts. On the contrary, a defect that is absent from the learning process may not be very visible in the representation. Compare methods on independent batches, critical defects and nominal variations, with full cost and decision threshold. A good score location still needs to be linked to a business tolerance. The choice depends on what is stable in the acquisition and what should be considered acceptable.

**Geometry of distance**: In PaDiM, a direction of high nominal variance is less penalized by the Mahalanobis distance than a direction of low variance. Covariance is therefore not only used to change the global scale; it also represents correlations between features. When there are few observations relative to their size, regularizing $\Sigma$ for example with a diagonal term is necessary to avoid an unstable inversion, under a documented choice. A pixel template can be more interpretable but very sensitive to registration. Comparing the three approaches thus imposes of check both the spatial coordinate frame and the representation of the acceptable variations.

**Blocking errors**: Describe these scores as universal probabilities of failure.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Full reference]]; [Roth et al., PatchCore, §§3.1 – 3.3](https://arxiv.org/abs/2106.08265); [Defard et al., PaDiM, §III, equations 1 – 2](https://arxiv.org/abs/2011.08785); baseline template defined by the project; [Defard et al., PaDiM, §III-B, equation 1, covariance and regularization; geometric interpretation deduced](https://arxiv.org/html/2011.08785v1), see the 2026-10-30.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-ANOMALIES-001 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-002

Objective: Explain the coreset. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ANOMALIES-002
Question: What is the purpose of a coreset of nominal features in PatchCore?
Reponse: **Expected answer**: Reduce the bank by maintaining a useful representation of its diversity, to limit memory and research.

**Further explanation**: Undersampling changes a hedging/cost trade-off; measuring defects and false releases, not just bank size.

**Compromise of representation**: An exhaustive bank can contain many redundant patches. Selecting a representative subset reduces memory and neighbor calculation, but can remove rare nominal variations. A poorly represented compliant coin can then become artificially distant from the bank.

**Proposed deletion**: keep extractor, data and comparison threshold, then vary only the bank size or selection. Measure time, memory, false rejections by nominal condition and missed defects. Also check that the bank is not contaminated with coins misclassified as nominal. A coreset is an approximation of reference diversity, not a set of positive examples of defects. The reduced memory is a resource gain; its product utility still requires that the necessary coverage be retained at the chosen operating point.

**Gluttony Selection**: After a defined initialization, a hedging policy chooses the nominal point currently furthest from its neighbor in the subset already selected. It thus seeks to cover the space of features rather than to keep only the frequent examples. The paper uses a projection to speed up the selection; the approximation must remain distinguished from a perfect cover. With $m$ features of dimension $d$ stored on $b$ bytes, the bank alone costs about $mdb$ bytes, excluding indexes. Reducing $m$ acts directly on this storage, but searching, extracting, and transferring memory can limit full latency differently.

**Blocking errors**: Take the coreset for a set of supervised defects.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Full reference]]; [PatchCore, §§3.1 – 3.3](https://arxiv.org/abs/2106.08265); [PaDiM, §III](https://arxiv.org/abs/2011.08785); [Roth et al., PatchCore, §3.2, Algorithm 1, gluton selection; project cost scenarios and calculations](https://arxiv.org/html/2106.08265v2), see 2026-10-30.
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-ANOMALIES-002 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-003

Objective: detect a drift of the nominal. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ANOMALIES-003
Question: Anomaly scores rise for every part after an illumination change. What should be tested?
Reponse: **Expected answer**: Compare acquisition/preprocessing, registration and feature distribution to nominal, then examine actually controlled parts.

**Further explanation**: Revise the reference or the light system after validation; changing the threshold alone can hide real defects.

**Diagnosis by Hypotheses**: The rise may correspond to a real product drift, a light change or a break in the pretreatment. The score alone does not separate these explanations because it measures a deviation from the learned reference.

**Survey built**: iron physically controlled parts under the two acquisitions, compare images and features with constant preprocessing, and then test the registration. Also look at small critical areas, not just the average score. If lighting is the cause, stabilize the acquisition or revise the nominal with independent validation. Increasing the threshold can cause alerts to disappear while masking a previously detectable defect. A correction must therefore be evaluated simultaneously on conformity and known defects, and its documented scope of validity. The absence of an alert after setting is not in itself a proof of resolution.

**Paired experience**: Pick up the same compliant parts before and after the light change and compare their scores by region. Then do the same for known defects. This makes it possible to study the displacement of the nominal and the separation between conformity and defect, instead of arbitrarily moving an overall threshold. If the two populations get closer, restoring the rate of false releases by increasing the threshold can greatly degrade the recall of defects. Documenting also exposure, saturation and white balance: a normalization of features does not recover visual information lost in saturated pixels. The result must be checked on other parts and lots.

**Blocking errors**: Automatically label any score increase as a physical defect.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Full reference]]; [Roth et al., PatchCore, §§3.1 – 3.3](https://arxiv.org/abs/2106.08265); acquisition diagnosis deducted by the project.
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-ANOMALIES-003 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-004

Objective: design an inspection with rare defects. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-ANOMALIES-004
Question: Track E — design: only a few defective images are available for a production line with a fixed cycle time. Which baseline and validation should be proposed?
Reponse: **Expected answer**: Stabilize acquisition, define critical defects and tolerances, compare template/nominal anomaly then measure rejections and defects missed on independent batches and realistic variations.

**Further explanation**: Provide for review of uncertain cases, full cost and tracking of drifts; no global rate replaces rare defects of need.

**Proposed design**: distinguish a wrongly rejected part, a missed defect and a case subject to verification. Their cost is not the same. Stabilizing the image first and the registration makes the baseline interpretable; then choosing whether a single reference or a nominal distribution sufficiently represents acceptable variability.

**Validation**: separate parts and batches between adjustment and test, cover even rare critical defects and realistic nominal disturbances. Measure the decision point, verification rate and full latency on the target line. A AUROC summarizes a ranking curve; it does not directly give the number of defects missed at the threshold exploited. Provide for the collection and review of new cases before modifying the reference, so as not to silently integrate a drift produced at the nominal.

**Translation in industrial load**: at a rate of $\lambda$ pieces/s and average processing time $T$ s/piece, a service capacity of less than $\lambda$ accumulates a queue even with a good detection score. For the point of operation, report false discharges among the conformants, missed defects among the defectives and number of batch checks. Zero defects missed on a small sample does not prove a zero rate: the size of the test and the diversity of defects limit the conclusion. Defining set-aside sets and critical cases before threshold setting connects the learning metrics to the actual process being evaluated.

**Blocking errors**: Validate only on nominal images or the average AUROC.

**Criteria for correction of the case**: explicit task and constraints, announced assumptions, justified choice, discriminating verification, limit of the conclusion. Case built, without field observation.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Full reference]]; [Roth et al., PatchCore, §§3.1 – 3.3](https://arxiv.org/abs/2106.08265); [Defard et al., PaDiM, §III, equations 1 – 2](https://arxiv.org/abs/2011.08785); industrial protocol proposed by the project.
Tags: cv::pilote cv::d07 famille::conception cv_id::CV-ANOMALIES-004 provenance::agent pole::A pole::E cas_pole::E::conception
END
