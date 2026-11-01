---
id: CV-ANOMALIES
type: methode
domaine: d07
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 5
prerequis: ["CV-REPRESENTATIONS", "CV-ACQUISITION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# Inspection: golden templates, PatchCore and PaDiM

## Problem, data and assumptions

Detect nominal deviations when defects are rare. Inputs: nominal images of reference and acquisition; outputs: image score and/or localization map. The anomaly depends on the reference distribution: lighting change and fault produced are not equivalent.

## Prerequisites and competencies

**Required prerequisites**: [CV-REPRESENTATIONS](71-representations-transfert.md); [CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

In the baseline proposed by the project, golden template means compare to a reference after registration. PatchCore keeps a database of features of nominal patches, reduced by coreset, and score by proximity. PaDiM models Gaussian distributions of features by position and uses their correlations.

## Mathematics, conventions and units

A simple proximity score is $a(p)=\min_{m\in M}\|f(p)-m\|_2$ for feature f and bank M; the PatchCore paper includes an aggregation/weighting to be distinguished from this summary. PaDiM uses $\sqrt{(f-\mu)^T\Sigma^{-1}(f-\mu)}$ with estimated/regularized covariance. These scores are not calibrated fault probabilities.

## Parameters and properties

Nominal selection, layers, scale, coreset/covariance, alignment and threshold. Contamination of the nominal or uncovered variability changes the result. The detection of any future defects is not guaranteed.

## Cost and implementation

Banking and finding neighbors consume memory/calculation; covariance and map have another cost. No model or industrial game executed.

## Evaluation and controlled variation

Compare a baseline template and methods with the same splits per piece/lot. Vary lighting or orientation separately; measure false rejection rate, missed defects and location, not just AUROC image.

## Failure modes and diagnosis

High scores on all parts of a new camera: check acquisition, nominal domain and registration before relabeling everything as defect. A dominant background can hide a small anomaly in a global pixel metric.

## Alternatives and applications

Supervised detection if known defects annotable; classic hybrid / learned according to variation and business tolerance. Keep procedure for analyzing false positives.

## Guided reasoning and proposed checks

These constructed cases develop normal reference, neighborhood patches and business decision. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-ANOMALIES-001

**Question of work**: Which tradeoffs distinguish golden-template inspection, PatchCore and PaDiM?

**Reference Response**: Template compares to an aligned reference; PatchCore uses a feature bank; PaDiM estimates covariance distributions by position.

**Reading the assumptions**: A direct comparison to the template requires that legitimate geometric and photometric deviations are sufficiently controlled. A nominal patch bank looks for representative neighbors; a position distribution model otherwise represents variability and correlations. The word anomaly here designates a deviation from this reference, not a universal definition of the business defect.

**Constructed example**: New lighting can move all features and increase scores without physically defective parts. On the contrary, a defect that is absent from the learning process may not be very visible in the representation. Compare methods on independent batches, critical defects and nominal variations, with full cost and decision threshold. A good score location still needs to be linked to a business tolerance. The choice depends on what is stable in the acquisition and what should be considered acceptable.

### Case linked to CV-ANOMALIES-004

**Question of work**: Track E — design: only a few defective images are available for a production line with a fixed cycle time. Which baseline and validation should be proposed?

**Reference Response**: Stabilize acquisition, define critical defects and tolerances, compare template/nominal anomaly then measure rejections and defects missed on independent batches and realistic variations.

**Proposed design**: distinguish a wrongly rejected part, a missed defect and a case subject to verification. Their cost is not the same. Stabilizing the image first and the registration makes the baseline interpretable; then choosing whether a single reference or a nominal distribution sufficiently represents acceptable variability.

**Validation**: separate parts and batches between adjustment and test, cover even rare critical defects and realistic nominal disturbances. Measure the decision point, verification rate and full latency on the target line. A AUROC summarizes a ranking curve; it does not directly give the number of defects missed at the threshold exploited. Provide for the collection and review of new cases before modifying the reference, so as not to silently integrate a drift produced at the nominal.

**Documentary reference for this pass**: [PatchCore](https://arxiv.org/html/2106.08265v2), §3, feature bank and scoring. The other developments are in the [flashcards](../73-patchcore-padim.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-ANOMALIES-001

**Situation**: Which tradeoffs distinguish golden-template inspection, PatchCore and PaDiM?

**Geometry of distance**: In PaDiM, a direction of high nominal variance is less penalized by the Mahalanobis distance than a direction of low variance. Covariance is therefore not only used to change the global scale; it also represents correlations between features. When there are few observations relative to their size, regularizing $\Sigma$ for example with a diagonal term is necessary to avoid an unstable inversion, under a documented choice. A pixel template can be more interpretable but very sensitive to registration. Comparing the three approaches thus imposes of check both the spatial coordinate frame and the representation of the acceptable variations.

### CV-ANOMALIES-002

**Situation**: What is the purpose of a coreset of nominal features in PatchCore?

**Gluttony Selection**: After a defined initialization, a hedging policy chooses the nominal point currently furthest from its neighbor in the subset already selected. It thus seeks to cover the space of features rather than to keep only the frequent examples. The paper uses a projection to speed up the selection; the approximation must remain distinguished from a perfect cover. With $m$ features of dimension $d$ stored on $b$ bytes, the bank alone costs about $mdb$ bytes, excluding indexes. Reducing $m$ acts directly on this storage, but searching, extracting, and transferring memory can limit full latency differently.

### CV-ANOMALIES-003

**Situation**: Anomaly scores rise for every part after an illumination change. What should be tested?

**Paired experience**: Pick up the same compliant parts before and after the light change and compare their scores by region. Then do the same for known defects. This makes it possible to study the displacement of the nominal and the separation between conformity and defect, instead of arbitrarily moving an overall threshold. If the two populations get closer, restoring the rate of false releases by increasing the threshold can greatly degrade the recall of defects. Documenting also exposure, saturation and white balance: a normalization of features does not recover visual information lost in saturated pixels. The result must be checked on other parts and lots.

### CV-ANOMALIES-004

**Situation**: Track E — design: only a few defective images are available for a production line with a fixed cycle time. Which baseline and validation should be proposed?

**Translation in industrial load**: at a rate of $\lambda$ pieces/s and average processing time $T$ s/piece, a service capacity of less than $\lambda$ accumulates a queue even with a good detection score. For the point of operation, report false discharges among the conformants, missed defects among the defectives and number of batch checks. Zero defects missed on a small sample does not prove a zero rate: the size of the test and the diversity of defects limit the conclusion. Defining set-aside sets and critical cases before threshold setting connects the learning metrics to the actual process being evaluated.

**Passages consulted for these developments**: [Defard et al., PaDiM](https://arxiv.org/html/2011.08785v1), §III-B, equation 1, covariance and regularization; geometric interpretation deduced; [Roth et al., PatchCore](https://arxiv.org/html/2106.08265v2), §3.2, Algorithm 1, gluton selection; scenarios and cost calculations of the project.

## Sources and flashcards

- [PatchCore, §§3.1 – 3.3](https://arxiv.org/abs/2106.08265).
- [PaDiM, §III](https://arxiv.org/abs/2011.08785).
- [Related flashcards](../73-patchcore-padim.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
