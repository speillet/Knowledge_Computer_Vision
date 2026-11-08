---
id: CV-FIABILITE
type: probleme
domaine: d13
poles: [A, C, D, E, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 7
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d13]
---
# Data splits, annotations, score calibration and drift

## Problem, data and assumptions

Establish whether a system is generalized to the scenes and uses actually targeted. Inputs: acquisition units, labels, sites/time and assumptions; output: protocol and error analysis. File separation does not guarantee data independence.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Define split unit (object, scene, sequence, patient, region), then annotate according to a controlled contract. Separate training, validation of choices and testing. Examine long-tail, ambiguities and subgroups before reducing everything to an average.

## Mathematics, conventions and units

Measured accuracy depends on point of use and prevalence. A calibrated score is a match between scores and frequencies according to protocol; it is not the geometric calibration of a camera. Uncertainty and OOD detection should be assessed on relevant changes, not inferred from a softmax.

## Parameters and properties

Taxonomy, ignores, quality of labels, split, thresholds and rules of selection of samples. Active learning chooses useful annotations according to a strategy; it can also bias the evaluation if the test becomes adaptive.

## Cost and implementation

Collect/review annotations have a cost; calculating some scores does not summarize it. No generalization or actual uncertainty is claimed.

## Evaluation and controlled variation

Baseline: split by sequence/site and frozen model; season/camera variation, with same comparable annotations. Decompose acquisition, distribution, labels and threshold. Report errors and coverage, including rare failures.

## Failure modes and diagnosis

Very good test but new site weak: look for leak and lag. An increase in confidence score does not prove better calibration; set protocol and sample before results.

## Alternatives and applications

Keep raw data, contracts and traceability, and then review collection/model under validation. Operational monitoring does not replace the initial test.

## Guided reasoning and proposed checks

These constructed cases develop split unit, selection, and probability calibration. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-FIABILITE-001

**Question of work**: Why do neighboring frames from the same video not necessarily provide independent training and test data?

**Reference Response**: They share scene, objects and conditions; the separation must follow the generalization scenario.

**Why files remain linked**: Two neighboring frames often contain the same objects, the same decor and almost the same acquisition. A model can find these clues in the test without having demonstrated its generalization to a new scene. Crops from the same original can further reinforce this proximity.

**Choice of protocol**: first define what will be new in operation, then group the data according to this unit before the diversions and increases. For a new plant, separating only frames from a sequence does not necessarily test the site change. For another task, a more local generalization may be relevant. check duplicates and overlaps, keep validation and test separate, and then report the groups actually evaluated. A more difficult split is not automatically better; it must represent the predicted scenario without indirectly transmitting training observations to it.

### Case linked to CV-FIABILITE-005

**Question of work**: A detector remains highly confident on a new sensor but makes more mistakes. What can be concluded?

**Reference Response**: The confidence displayed is not a proof of calibration or reliability out of distribution.

**Reading confidence**: A high score can be learned in a distribution where certain indices were reliable, and then remain high when these indices change meaning. Output normalization does not automatically detect this shift. The new sensor can also break color, gamma, resolution or intensity range.

**Proposed investigation**: compare an identical input across the two strings and measure errors on a representative annotated batch of the new sensor. Examine calibration and rejection at the point of operation, with the same location rules. A drop in quality requires action, but the score alone does not say whether to correct the preprocessing, recollect or adapt the model. Keep an independent validation to verify the correction. Monitoring of distributions can provide a useful alarm; it does not by itself demonstrate a drift of precision without appropriate reference.

**Documentary reference for this pass**: [Cawley and Talbot 2010](https://www.jmlr.org/papers/v11/cawley10a.html), summary and selection bias. The other developments are in the [flashcards](../133-donnees-generalisation.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-FIABILITE-001

**Situation**: Why do neighboring frames from the same video not necessarily provide independent training and test data?

**Data Dependency Graph**: Link images from the same acquisition, part, patient, or space zone, then assign groups to the split before creating tiles and augmentations. A validation tile that covers a training tile can directly transmit common textures and objects. The relevant size of a group depends on the generalization announced: new point of view, new object or new site are not the same tests. To estimate the uncertainty of a metric, resample coherent groups rather than all pixels or frames as if they were independent. The large number of files does not replace the diversity of acquisition units.

### CV-FIABILITE-002

**Situation**: How do camera calibration and calibration of a detector's scores differ?

**Reliability diagram**: first define the correct event, e.g. correct class and sufficiently precise location under a given matching. In score bins, compare the frequency of this event and average confidence with their numbers. A typical CDE averages the absolute differences weighted by the bin population; it depends on the binning and can hide subgroups. Geometric calibration compares projections to point measurements and estimates other parameters. A temperature transformation can change the scores without changing the order of the classes, while a change of intrinsics changes the geometry: these are two interventions of different nature.

### CV-FIABILITE-003

**Situation**: Why must selecting active-learning examples not turn into repeatedly tuning the final test set after failures?

**Test became development**: After several cycles where the errors of the same test guide the choices, this set brings information to the selection process, even without direct training on it. The best result selected among many essays then incorporates this adaptation. Keep for each cycle the version of the data, the decisions made and the validation used; provide for an independent evaluation after freezing of the selected version. A targeted set of difficult cases remains useful as a regression, but does not necessarily replace a representative test of frequency of errors in operation. Naming these uses separately makes it impossible to interpret a gain on an adaptive collection as a general proof.

### CV-FIABILITE-004

**Situation**: Track E — diagnosis: a remote-sensing model degrades between seasons. Which analysis can distinguish possible causes?

**Comparison plan**: cross known/new region and known/new season to separate as much as possible spatial and temporal novelty. check tapes, physical resolution, alignment and label policy in each box. A seasonal change can make an object really different or only its appearance different; the definition of the class must remain explicit. Examining paired areas helps to isolate the acquisition, but does not alone evaluate an area never seen before. Keeping the results per square and per class prevents a change in the proportion of easy terrain from artificially explaining the overall average. This plan remains a proposed protocol, not a measured remote sensing result.

### CV-FIABILITE-005

**Situation**: A detector remains highly confident on a new sensor but makes more mistakes. What can be concluded?

**Risk and Coverage**: For a rule that denies scores below a threshold, coverage is the fraction of cases where a decision is issued; risk is the error among those decisions according to the protocol. One method can reduce the risk by refusing more, without improving the perception on the remaining cases. Compare risk-coverage curves and critical layers, with labels representative of the new sensor. A change in the distribution of features can serve as an alarm, but it does not directly give the error rate without reference. Check separately the entry contract and the relevance of the rule of refusal after change of domain.

**Passages consulted for these developments**: [Guo et al., calibration](https://arxiv.org/html/1706.04599v2), §2, ECE and diagrams; detection protocol, splits and risk – covering built.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-FIABILITE-001 — Derived samples inherit their source group

Creating crops, augmentations or neighboring frames before a random split can place near copies of one source acquisition in both training and test. Assign the source group first and propagate its split to every derivative. A proposed audit checks acquisition, part/site/patient and temporal identifiers according to the deployment question. More test files then do not necessarily mean more independent evidence of transfer to unseen conditions.

### CV-FIABILITE-003 — An untouched test is consumed by repeated selection

If the same test failures repeatedly guide prompt, threshold or dataset choices, the test becomes development evidence whether or not gradients were computed on it. A proposed workflow keeps active-learning selection in the training pool, uses validation for choices and reserves an independent final evaluation. When a benchmark has already influenced the design, report that history and obtain fresh evidence rather than relabeling the old score as unbiased.

### CV-FIABILITE-004 — Season and sensor can be confounded

If all summer images come from one sensor and all winter images from another, a performance gap cannot be attributed uniquely to season. A proposed analysis seeks overlapping acquisition factors or controlled comparisons, then stratifies by site, band mapping, ground sampling distance, label policy and visible land-cover change. Geographic or temporal grouping must reflect deployment; shuffling nearby tiles does not isolate the source of the shift.

Consulted foundations: [Guo et al. calibration](https://proceedings.mlr.press/v70/guo17a.html): §2 confidence/calibration and reliability diagrams; [Cawley and Talbot](https://www.jmlr.org/papers/v11/cawley10a.html): model-selection overfitting and evaluation bias.

## Sources and flashcards

- [Ovadia et al., 2019, summary/introduction](https://arxiv.org/abs/1906.02530): Calibration limits under change of distribution.
- [Cawley – Talbot, 2010, summary and introduction](https://www.jmlr.org/papers/v11/cawley10a.html): over-adjustment of selection and evaluation bias.

- [Roberts et al., structured data cross-validation](https://doi.org/10.1111/ecog.02881).
- [Calibration of modern neural networks](https://proceedings.mlr.press/v70/guo17a.html).
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
- [Related flashcards](../133-donnees-generalisation.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
