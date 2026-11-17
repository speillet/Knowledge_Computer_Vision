# Flashcards — Inspection: golden templates, PatchCore and PaDiM

reference note: [[70-reconnaissance-representations/references/73-patchcore-padim|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-ANOMALIES-001

Objective: Choose a nominal model. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ANOMALIES-001
Question: Which tradeoffs distinguish golden-template inspection, PatchCore and PaDiM?
Reponse: **Expected answer**: The template compares with an aligned reference; PatchCore uses a bank of nominal patch features; PaDiM estimates a multivariate Gaussian (mean and covariance) per patch position.

**Further explanation**: Choose according to nominal variability, alignment, memory and business evaluation; none of them models the possible defects.

**Reading the assumptions**: A direct comparison with the template requires that legitimate geometric and photometric deviations are sufficiently controlled. A nominal patch bank looks for representative neighbors; a per-position distribution model instead represents variability and correlations. The word anomaly here designates a deviation from this reference, not a universal definition of the business defect.

**Constructed example**: New lighting can move all features and increase scores without physically defective parts. Conversely, a defect that is absent from the learning process may not be very visible in the representation. Compare methods on independent batches, critical defects and nominal variations, with full cost and decision threshold. A good score location still needs to be linked to a business tolerance. The choice depends on what is stable in the acquisition and what should be considered acceptable.

**Geometry of distance**: In PaDiM, a direction of high nominal variance is less penalized by the Mahalanobis distance than a direction of low variance. Covariance is therefore not only used to change the global scale; it also represents correlations between features. When there are few observations relative to their dimension, regularizing $\Sigma$, for example with a diagonal term, is necessary to avoid an unstable inversion, under a documented choice. A pixel template can be more interpretable but very sensitive to registration. Comparing the three approaches therefore requires checking both the spatial coordinate frame and the representation of the acceptable variations.

**Registration is a stronger assumption for position statistics**: A nominal feature at one image location can move to another after a small part translation. A position-specific distribution may then score a normal part as unusual, while a location-flexible feature bank has a different sensitivity. Neither is universally preferable: excessive spatial flexibility can also overlook misplaced components. Test controlled shifts and missing/moved parts separately so tolerance to nuisance movement is not confused with tolerance to genuine assembly errors.

**Blocking errors**: Describing these scores as universal defect probabilities.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Full reference]]; [Roth et al., PatchCore, §§3.1 – 3.3](https://arxiv.org/abs/2106.08265); [Defard et al., PaDiM, §III, equations 1 – 2](https://arxiv.org/abs/2011.08785); baseline template defined by the project; [Defard et al., PaDiM, §III-B, equation 1, covariance and regularization; geometric interpretation deduced](https://arxiv.org/html/2011.08785v1), see the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-ANOMALIES-001 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-002

Objective: Explain the coreset. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ANOMALIES-002
Question: What is the purpose of a coreset of nominal features in PatchCore?
Reponse: **Expected answer**: Reduce the bank while keeping a useful representation of its diversity, to limit memory and nearest-neighbor search cost.

**Further explanation**: Subsampling trades coverage against cost; measure missed defects and false rejections, not just bank size.

**Representation tradeoff**: An exhaustive bank can contain many redundant patches. Selecting a representative subset reduces memory and neighbor calculation, but can remove rare nominal variations. A poorly represented conforming part can then become artificially distant from the bank.

**Proposed ablation**: keep extractor, data and comparison threshold, then vary only the bank size or selection. Measure time, memory, false rejections by nominal condition and missed defects. Also check that the bank is not contaminated with parts wrongly labeled as nominal. A coreset is an approximation of reference diversity, not a set of positive examples of defects. The reduced memory is a resource gain; its usefulness in production still requires that the necessary coverage be retained at the chosen operating point.

**Greedy selection**: After a defined initialization, a coverage policy chooses the nominal point currently farthest from its nearest neighbor in the already selected subset. It thus seeks to cover the feature space rather than to keep only the frequent examples. The paper uses a random projection to speed up the selection; the approximation must remain distinguished from a perfect cover. With $m$ features of dimension $d$ stored on $b$ bytes each, the bank alone costs about $mdb$ bytes, excluding indexes. Reducing $m$ acts directly on this storage, but search, feature extraction and memory transfers can limit full latency differently.

**Nominal contamination can become a prototype**: A rare defective patch mistakenly included in nominal training may be selected by a farthest-point coreset because it lies far from the existing bank. Covering feature diversity is useful only after defining what belongs to nominal operation. Audit suspicious extreme training examples and compare held-out defect scores before increasing coreset size. The selection objective is coverage of supplied features, not verification that those features are defect-free.

**Blocking errors**: Take the coreset for a set of supervised defects.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Full reference]]; [PatchCore, §§3.1 – 3.3](https://arxiv.org/abs/2106.08265); [PaDiM, §III](https://arxiv.org/abs/2011.08785); [Roth et al., PatchCore, §3.2, Algorithm 1, greedy selection; project cost scenarios and calculations](https://arxiv.org/html/2106.08265v2), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-ANOMALIES-002 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-003

Objective: detect a drift of the nominal. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ANOMALIES-003
Question: Anomaly scores rise for every part after an illumination change. What should be tested?
Reponse: **Expected answer**: Compare acquisition/preprocessing, registration and feature distribution with the nominal reference, then examine parts whose condition has been physically verified.

**Further explanation**: Revise the reference or the lighting system after validation; changing the threshold alone can hide real defects.

**Diagnosis by hypotheses**: The rise may correspond to a real product drift, a lighting change or a change in preprocessing. The score alone does not separate these explanations because it measures a deviation from the learned reference.

**Constructed investigation**: image physically inspected parts under both acquisition setups, compare images and features with constant preprocessing, and then test the registration. Also look at small critical areas, not just the average score. If lighting is the cause, stabilize the acquisition or revise the nominal with independent validation. Increasing the threshold can cause alerts to disappear while masking a previously detectable defect. A correction must therefore be evaluated simultaneously on conforming parts and known defects, with its scope of validity documented. The absence of an alert after setting is not in itself a proof of resolution.

**Paired experiment**: Image the same conforming parts before and after the lighting change and compare their scores by region. Then do the same for known defects. This makes it possible to study the displacement of the nominal population and the separation between conforming and defective parts, instead of arbitrarily moving a global threshold. If the two populations get closer, restoring the false-rejection rate by raising the threshold can greatly degrade defect recall. Also document exposure, saturation and white balance: a normalization of features does not recover visual information lost in saturated pixels. The result must be checked on other parts and batches.

**Why every score rises**: both deep methods score a patch by its distance to nominal features, PatchCore to the nearest bank feature and PaDiM in units of each position's training covariance, where a direction that never varied in training is amplified by $1/\sqrt{\epsilon}=10$ (reference, example C). A lighting change absent from training moves the features of every patch, and the image score, a maximum over patches, rises with them [PatchCore, §3.3; PaDiM, §III-C].

**Discriminating signature** (project deduction): on a verified conforming part imaged under both setups, compare the distribution of patch scores, not only the image maximum. An acquisition shift raises the median patch score with the maximum, over the whole map; a real defect raises a localized group of patches and leaves the median in place.

**Constructed threshold trap** (Gaussian scores for illustration, recomputed in the check script of this pass): good parts score $\mathcal N(1.0,0.2^2)$ and defects $\mathcal N(2.0,0.3^2)$; $\tau=1.465$ rejects 1% of good parts and catches 96.3% of defects. The new lighting moves good parts to $\mathcal N(1.5,0.2^2)$, so 57% are rejected, and defects only to $\mathcal N(2.2,0.3^2)$. Raising $\tau$ to 1.965 restores 1% false rejections, but recall falls to 78%.

**Blocking errors**: Automatically labeling any score increase as a physical defect. Restoring the false-rejection rate by raising the threshold without measuring defect recall under the new acquisition.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Full reference]]; [Roth et al., PatchCore, §§3.1–3.3, image score as the maximum patch distance](https://arxiv.org/abs/2106.08265); [Defard et al., PaDiM, §III-C, image score as the maximum of the map; §IV-B, $\epsilon=0.01$](https://arxiv.org/abs/2011.08785); acquisition diagnosis, the median-versus-maximum signature and the threshold example constructed by the project.
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-ANOMALIES-003 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-004

Objective: design an inspection with rare defects. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-ANOMALIES-004
Question: Track E — design: only a few defective images are available for a production line with a fixed cycle time. Which baseline and validation should be proposed?
Reponse: **Expected answer**: Stabilize acquisition, define critical defects and tolerances, compare a template baseline with a nominal-only anomaly model, then measure false rejections and missed defects on independent batches and realistic variations.

**Further explanation**: Plan review of uncertain cases, full cost and drift monitoring; no global rate replaces evidence on the rare critical defects.

**Proposed design**: distinguish a wrongly rejected part, a missed defect and a case sent for verification. Their cost is not the same. Stabilizing the image and the registration first makes the baseline interpretable; then choose whether a single reference or a nominal distribution sufficiently represents acceptable variability.

**Validation**: separate parts and batches between tuning and test, cover even rare critical defects and realistic nominal disturbances. Measure the operating point, verification rate and full latency on the target line. An AUROC summarizes a ranking curve; it does not directly give the number of defects missed at the threshold in use. Plan the collection and review of new cases before modifying the reference, so as not to silently integrate a product drift into the nominal reference.

**Translation into production load**: at a rate of $\lambda$ parts/s and a mean processing time of $T$ s/part, a service capacity below $\lambda$ builds up a queue even with a good detection score. At the operating point, report false rejections among conforming parts, missed defects among defective parts and the number of parts sent for verification per batch. Zero defects missed on a small sample does not prove a zero rate: the size of the test and the diversity of defects limit the conclusion. Defining held-out sets and critical cases before setting the threshold connects the learning metrics to the actual process being evaluated.

**Rare defects need operating-point evidence**: A high AUROC can coexist with unacceptable missed defects at the low false-rejection rate needed by production. Define that rate per part, not merely per pixel, and report recall by critical defect family with sample counts. Include full-cycle latency, memory-bank size and handling of camera changes. Nominal-only validation estimates false alarms under its sampled conditions; it cannot directly estimate recall of defect types never tested.

**Blocking errors**: Validate only on nominal images or the average AUROC.

**Grading criteria for the case**: explicit task and constraints, stated assumptions, justified choice, discriminating check, limit of the conclusion. Constructed case, without field observation.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Full reference]]; [Roth et al., PatchCore, §§3.1 – 3.3](https://arxiv.org/abs/2106.08265); [Defard et al., PaDiM, §III, equations 1 – 2](https://arxiv.org/abs/2011.08785); industrial protocol proposed by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d07 famille::conception cv_id::CV-ANOMALIES-004 provenance::agent pole::A pole::E cas_pole::E::conception
END
