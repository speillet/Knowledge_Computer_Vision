# Flashcards — Data splits, annotations, score calibration and drift

reference note: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-FIABILITE-001

Objective: Choose a split unit. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FIABILITE-001
Question: Why do neighboring frames from the same video not necessarily provide independent training and test data?
Reponse: **Expected answer**: They share scene, objects and conditions; the separation must follow the generalization scenario.

**Further explanation**: Split by sequence/site/patient according to task, with check of crops and duplicates.

**Why files remain linked**: Two neighboring frames often contain the same objects, the same decor and almost the same acquisition. A model can find these clues in the test without having demonstrated its generalization to a new scene. Crops from the same original can further reinforce this proximity.

**Choice of protocol**: first define what will be new in operation, then group the data according to this unit before the diversions and increases. For a new plant, separating only frames from a sequence does not necessarily test the site change. For another task, a more local generalization may be relevant. check duplicates and overlaps, keep validation and test separate, and then report the groups actually evaluated. A more difficult split is not automatically better; it must represent the predicted scenario without indirectly transmitting training observations to it.

**Data Dependency Graph**: Link images from the same acquisition, part, patient, or space zone, then assign groups to the split before creating tiles and augmentations. A validation tile that covers a training tile can directly transmit common textures and objects. The relevant size of a group depends on the generalization announced: new point of view, new object or new site are not the same tests. To estimate the uncertainty of a metric, resample coherent groups rather than all pixels or frames as if they were independent. The large number of files does not replace the diversity of acquisition units.

**Derived samples inherit their source group**: Creating crops, augmentations or neighboring frames before a random split can place near copies of one source acquisition in both training and test. Assign the source group first and propagate its split to every derivative. A proposed audit checks acquisition, part/site/patient and temporal identifiers according to the deployment question. More test files then do not necessarily mean more independent evidence of transfer to unseen conditions.

**Blocking errors**: Assimilate two different file names to two independent observations.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]]; [Roberts et al., blocking summary and recommendations](https://doi.org/10.1111/ecog.02881); application to frames: project reasoning. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-FIABILITE-001 provenance::agent pole::A pole::C pole::D pole::E pole::F
END

## CV-FIABILITE-002

Objective: distinguish between two calibrations. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FIABILITE-002
Question: How do camera calibration and calibration of a detector's scores differ?
Reponse: **Expected answer**: The first estimates geometry/optics; the second studies the agreement between scores and frequencies of events according to protocol.

**Further explanation**: Neither is demonstrated by good accurancy alone; specify unit and object of calibration.

**Examples of quantities**: A focal length and a main dot are geometric parameters in pixels. A detection score of 0,9 is a digital output whose relation to the correct events in a defined population and protocol must be studied. These objects use neither the same reference data nor the same error criteria.

**Proposed verification**: for the camera, test projections and geometry on reserved observations. For scores, compare decisions and references in relevant score groups, specifying class, location and distribution. Good accuracy can co-exist with poor confidence, as a low reprojection error can co-exist with a poor physical measure. Using the word calibration without its precise purpose makes the investigation ambiguous. The course therefore separates image formation model, recognition score and product validation, while explaining their interactions.

**Reliability diagram**: first define the correct event, e.g. correct class and sufficiently precise location under a given matching. In score bins, compare the frequency of this event and average confidence with their numbers. A typical CDE averages the absolute differences weighted by the bin population; it depends on the binning and can hide subgroups. Geometric calibration compares projections to point measurements and estimates other parameters. A temperature transformation can change the scores without changing the order of the classes, while a change of intrinsics changes the geometry: these are two interventions of different nature.

**Calibration needs a defined correctness event**: For a detector, correct class alone and correct class plus sufficient localization are different events. Matching, ignored annotations and score filtering alter which outcomes enter a reliability diagram. Declare that event and evaluate the operational prediction population. A score calibrated on source data need not stay calibrated on a new sensor; camera geometric calibration and probability calibration address distinct models even if both use the word calibration.

**Blocking errors**: Use RMS of reprojection to validate a class probability.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]]; [Guo et al., §2, equation 1: confidence calibration](https://proceedings.mlr.press/v70/guo17a.html); [Zhang, §2: Geometric calibration](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [Guo et al., calibration, §2, ECE and diagrams; detection protocol, splits and cover risk built](https://arxiv.org/html/1706.04599v2), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-FIABILITE-002 provenance::agent pole::A pole::C pole::D pole::E pole::F
END

## CV-FIABILITE-003

Objective: Keep a non-adaptive test. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FIABILITE-003
Question: Why must selecting active-learning examples not turn into repeatedly tuning the final test set after failures?
Reponse: **Expected answer**: The test must remain a measure independent of the chosen scenario; adapting its selection or thresholds after results biases the conclusion.

**Further explanation**: Keep validation for iteration and document the perimeter change if a new test is required.

**Why the selection is biased**: observing test failures and then choosing prompts, thresholds, data or architecture to reduce them uses its information to set the system. The best score among these trials may overestimate generalization, even if no gradient is calculated directly on the test.

**Proposed organization**: Keep the annotation and active learning cycles in a set of work with dedicated validation. Preserve an independent assessment of the future scenario, with explicit collection and annotation rules. If field feedback leads to a new perimeter, create and document a new test rather than keeping the final label for a set that has become adaptive. The old results remain useful as well as historical. The correct goal is not to prohibit error analysis, but to distinguish the improvement work from the final proof, in order to correctly attribute the gain to the new version.

**Test became development**: After several cycles where the errors of the same test guide the choices, this set brings information to the selection process, even without direct training on it. The best result selected among many essays then incorporates this adaptation. Keep for each cycle the version of the data, the decisions made and the validation used; provide for an independent evaluation after freezing of the selected version. A targeted set of difficult cases remains useful as a regression, but does not necessarily replace a representative test of frequency of errors in operation. Naming these uses separately makes it impossible to interpret a gain on an adaptive collection as a general proof.

**An untouched test is consumed by repeated selection**: If the same test failures repeatedly guide prompt, threshold or dataset choices, the test becomes development evidence whether or not gradients were computed on it. A proposed workflow keeps active-learning selection in the training pool, uses validation for choices and reserves an independent final evaluation. When a benchmark has already influenced the design, report that history and obtain fresh evidence rather than relabeling the old score as unbiased.

**Blocking errors**: Call final performance the best iteration result on the same test.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]]; [Cawley – Talbot, summary/introduction: selection bias](https://www.jmlr.org/papers/v11/cawley10a.html); application to the annotation cycle: project reasoning. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-FIABILITE-003 provenance::agent pole::A pole::C pole::D pole::E pole::F
END

## CV-FIABILITE-004

Objective: Diagnose a seasonal drift. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FIABILITE-004
Question: Track E — diagnosis: a remote-sensing model degrades between seasons. Which analysis can distinguish possible causes?
Reponse: **Expected answer**: check georeferencing, resolution/bands, labels and distribution; compare separate regions/dates and stratify errors by conditions.

**Further explanation**: Test a targeted intervention on validation and then a reserved time set. Do not assign any seasonality to the network without checking acquisition and taxonomy.

**Proposed decomposition**: A season can change light, vegetation and class distribution; it can also be accompanied by another sensor or other annotation policy. Comparing global errors without checking these elements mixes several assumptions.

**Constructed ablation**: align geometry and bands, examine common controlled areas and new regions, and then measure errors by class and condition. Check for a pre-treatment change before a model adaptation. If an intervention is chosen, set it to validation and then test it on dates or regions that remain reserved. Mixing neighboring tiles to artificially increase the similarity of the test does not establish seasonal generalization. The conclusion must identify what the observations separate and leave open the causes still confused.

**Comparison plan**: cross known/new region and known/new season to separate as much as possible spatial and temporal novelty. check tapes, physical resolution, alignment and label policy in each box. A seasonal change can make an object really different or only its appearance different; the definition of the class must remain explicit. Examining paired areas helps to isolate the acquisition, but does not alone evaluate an area never seen before. Keeping the results per square and per class prevents a change in the proportion of easy terrain from artificially explaining the overall average. This plan remains a proposed protocol, not a measured remote sensing result.

**Season and sensor can be confounded**: If all summer images come from one sensor and all winter images from another, a performance gap cannot be attributed uniquely to season. A proposed analysis seeks overlapping acquisition factors or controlled comparisons, then stratifies by site, band mapping, ground sampling distance, label policy and visible land-cover change. Geographic or temporal grouping must reflect deployment; shuffling nearby tiles does not isolate the source of the shift.

**Blocking errors**: Mix the neighboring tiles of the two seasons to remove the gap of the test.

**Criteria for correction of the case**: explicit task and constraints, announced assumptions, justified choice, discriminating verification, limit of the conclusion. Case built, without field observation.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]]; Case built from project; [Roberts et al., spatial/temporal separation](https://doi.org/10.1111/ecog.02881). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-FIABILITE-004 provenance::agent pole::A pole::C pole::D pole::E pole::F cas_pole::E::diagnostic
END

## CV-FIABILITE-005

Objective: Avoiding certainty outside the field. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FIABILITE-005
Question: A detector remains highly confident on a new sensor but makes more mistakes. What can be concluded?
Reponse: **Expected answer**: The confidence displayed is not a proof of calibration or reliability out of distribution.

**Further explanation**: Evaluate errors, rejections and calibration on representative acquisition; review entry contract before adaptation.

**Reading confidence**: A high score can be learned in a distribution where certain indices were reliable, and then remain high when these indices change meaning. Output normalization does not automatically detect this shift. The new sensor can also break color, gamma, resolution or intensity range.

**Proposed investigation**: compare an identical input across the two strings and measure errors on a representative annotated batch of the new sensor. Examine calibration and rejection at the point of operation, with the same location rules. A drop in quality requires action, but the score alone does not say whether to correct the preprocessing, recollect or adapt the model. Keep an independent validation to verify the correction. Monitoring of distributions can provide a useful alarm; it does not by itself demonstrate a drift of precision without appropriate reference.

**Risk and Coverage**: For a rule that denies scores below a threshold, coverage is the fraction of cases where a decision is issued; risk is the error among those decisions according to the protocol. One method can reduce the risk by refusing more, without improving the perception on the remaining cases. Compare risk-coverage curves and critical layers, with labels representative of the new sensor. A change in the distribution of features can serve as an alarm, but it does not directly give the error rate without reference. Check separately the entry contract and the relevance of the rule of refusal after change of domain.

**Selective prediction needs both risk and coverage**: Raising a rejection threshold can lower error among accepted outputs while leaving almost no usable predictions. Report accepted coverage and conditional risk together, by relevant domain and class. If confidently wrong cases remain above the threshold, rejection based on raw confidence may not resolve the shift. Compare empirical calibration and error types on labeled new-sensor data before claiming the displayed confidence establishes reliability.

**Blocking errors**: Take the softmax for a generalization guarantee.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]] ; [Ovadia et al., summary and introduction: uncertainty and calibration under shift distribution](https://arxiv.org/abs/1906.02530). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-FIABILITE-005 provenance::agent pole::A pole::C pole::D pole::E pole::F
END
