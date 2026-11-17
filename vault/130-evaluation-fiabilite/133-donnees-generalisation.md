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

**Further explanation**: Split by sequence, site or patient according to the task, with a check of crops and duplicates.

**Why files remain linked**: Two neighboring frames often contain the same objects, the same background and almost the same acquisition. A model can find these cues in the test without having demonstrated its generalization to a new scene. Crops from the same original can further reinforce this proximity.

**Choice of protocol**: First define what will be new in operation, then group the data according to this unit before cropping, tiling and augmentation. For a new plant, separating only frames from a sequence does not test the site change. For another task, a more local generalization may be relevant. Check duplicates and overlaps, keep validation and test separate, and then report the groups actually evaluated. A more difficult split is not automatically better; it must represent the intended scenario without indirectly passing training observations to it.

**Data dependency graph**: Link images from the same acquisition, part, patient or spatial zone, then assign groups to the split before creating tiles and augmentations. A validation tile that overlaps a training tile can directly pass shared textures and objects. The relevant size of a group depends on the generalization claimed: a new viewpoint, a new object or a new site are not the same tests. To estimate the uncertainty of a metric, resample coherent groups rather than individual pixels or frames as if they were independent. A large number of files does not replace the diversity of acquisition units.

**Derived samples inherit their source group**: Creating crops, augmentations or neighboring frames before a random split can place near copies of one source acquisition in both training and test. Assign the source group first and propagate its split to every derivative. A proposed audit checks acquisition, part/site/patient and temporal identifiers according to the deployment question. More test files then do not necessarily mean more independent evidence of transfer to unseen conditions.

**Blocking errors**: Treating two different file names as two independent observations.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]]; [Kapoor and Narayanan, §2.4, leakage L1.4 (duplicates) and L3.2 (non-independence between train and test samples)](https://arxiv.org/abs/2207.07048); [Roberts et al. 2017, abstract (block cross-validation; full text not re-read on 2026-11-14)](https://doi.org/10.1111/ecog.02881). Application to frames and derived crops: project reasoning.
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-FIABILITE-001 provenance::agent pole::A pole::C pole::D pole::E pole::F
END

## CV-FIABILITE-002

Objective: distinguish between two calibrations. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FIABILITE-002
Question: How do camera calibration and calibration of a detector's scores differ?
Reponse: **Expected answer**: The first estimates geometry/optics; the second studies the agreement between scores and frequencies of events according to protocol.

**Further explanation**: Neither is demonstrated by good accuracy alone; specify the unit and the object of the calibration.

**Examples of quantities**: A focal length and a principal point are geometric parameters in pixels. A detection score of 0.9 is a numeric output whose relation to correct events, in a defined population and protocol, must be studied. These objects use neither the same reference data nor the same error criteria.

**Proposed verification**: For the camera, test projections and geometry on held-out observations. For scores, compare decisions and references in relevant score bins, specifying class, localization and distribution. Good accuracy can coexist with poor confidence, just as a low reprojection error can coexist with a poor physical measurement. Using the word calibration without its precise purpose makes the investigation ambiguous. The learning path therefore separates the image formation model, the recognition score and product validation, while explaining their interactions.

**Reliability diagram**: First define the correct event, e.g. correct class and sufficiently precise localization under a given matching. In score bins, compare the frequency of this event with the mean confidence, together with the bin counts. A typical ECE averages the absolute differences weighted by bin population; it depends on the binning and can hide subgroups. Geometric calibration compares projections with point measurements and estimates other parameters. Temperature scaling can change the scores without changing the order of the classes, while a change of intrinsics changes the geometry: these are two interventions of a different nature.

**Two estimation problems**: Camera calibration fits a projection model, an intrinsic matrix with scale factors $\alpha,\beta$ and principal point $(u_0,v_0)$ in pixels and a skew $\gamma$, plus distortion and one pose per view, by minimizing the summed squared distance between detected and projected pattern points [Zhang 1998, §2.1, §3.2 eq. 10]; OpenCV's `calibrateCamera` returns the overall RMS reprojection error in pixels. Score calibration fits no geometry: it maps a score to the observed frequency of a declared event, is checked on held-out labelled predictions by a binned, unitless ECE [Guo et al., §2, eq. 3], and can be fitted, for example, by one temperature on the validation negative log-likelihood [§4.2].

**Constructed example** (worked example B of the reference, recomputed in the check script of this pass): 100 detections all scored 0.8, of which 80 overlap their object with IoU at least 0.5 and 60 with IoU at least 0.75, are calibrated for the first event and overconfident by 0.2 for the second. Forty predictions at 0.95 and forty at 0.55, each group 75% correct, give an ECE of 0 with one or two bins and 0.20 with fifteen. Neither number contains a pixel, and a reprojection RMS contains no score: each validation is blind to the other's failure.

**Blocking errors**: Using the reprojection RMS to validate a class probability.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]]; [Guo et al. 2017, §2 eqs. 1–3 (perfect calibration, reliability diagrams, ECE) and §4.2 eq. 9 (temperature scaling)](https://arxiv.org/html/1706.04599v2); [Küppers et al. 2020, §3.1 eq. 1 (detection calibration event)](https://arxiv.org/abs/2004.13546); [Zhang 1998, §2.1 (intrinsic matrix) and §3.2 eq. 10 (maximum likelihood refinement), read on 2026-11-16](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [OpenCV 4.13.0, calib3d.hpp L1685: `calibrateCamera` returns the RMS reprojection error](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L1685). The detection and binning examples are project constructions.
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-FIABILITE-002 provenance::agent pole::A pole::C pole::D pole::E pole::F
END

## CV-FIABILITE-003

Objective: Keep a non-adaptive test. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FIABILITE-003
Question: Why must selecting active-learning examples not turn into repeatedly tuning the final test set after failures?
Reponse: **Expected answer**: The test must remain a measure independent of the chosen scenario; adapting its selection or thresholds after results biases the conclusion.

**Further explanation**: Keep validation for iteration and document the scope change if a new test is required.

**Why the selection is biased**: Observing test failures and then choosing prompts, thresholds, data or architecture to reduce them uses the test's information to tune the system. The best score among these trials may overestimate generalization, even if no gradient is computed directly on the test.

**Proposed organization**: Keep the annotation and active-learning cycles in a working set with its own validation. Preserve an independent assessment of the future scenario, with explicit collection and annotation rules. If field feedback leads to a new scope, create and document a new test rather than keeping the "final" label for a set that has become adaptive. The old results remain useful as history. The goal is not to prohibit error analysis, but to distinguish improvement work from the final evidence, in order to attribute the gain to the new version correctly.

**Test turned into development data**: After several cycles in which the errors of the same test guide the choices, this set feeds information into the selection process, even without direct training on it. The best result selected among many trials then incorporates this adaptation. Keep, for each cycle, the data version, the decisions made and the validation used; plan an independent evaluation after freezing the selected version. A targeted set of difficult cases remains useful for regression testing, but does not replace a representative test of the error frequency in operation. Naming these uses separately prevents interpreting a gain on an adaptive collection as general proof.

**An untouched test is consumed by repeated selection**: If the same test failures repeatedly guide prompt, threshold or dataset choices, the test becomes development evidence whether or not gradients were computed on it. A proposed workflow keeps active-learning selection in the training pool, uses validation for choices and reserves an independent final evaluation. When a benchmark has already influenced the design, report that history and obtain fresh evidence rather than relabeling the old score as unbiased.

**Blocking errors**: Calling the best iteration result on the same test the final performance.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]]; [Cawley and Talbot 2010, abstract: over-fitting in model selection and selection bias](https://www.jmlr.org/papers/v11/cawley10a.html); [Koh et al., WILDS, §9.3: use OOD validation for development, OOD test only for final evaluation](https://arxiv.org/abs/2012.07421). Application to the annotation cycle: project reasoning.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-FIABILITE-003 provenance::agent pole::A pole::C pole::D pole::E pole::F
END

## CV-FIABILITE-004

Objective: Diagnose a seasonal drift. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FIABILITE-004
Question: Track E — diagnosis: a remote-sensing model degrades between seasons. Which analysis can distinguish possible causes?
Reponse: **Expected answer**: check georeferencing, resolution/bands, labels and distribution; compare separate regions/dates and stratify errors by conditions.

**Further explanation**: Test a targeted intervention on validation and then on a held-out time period. Do not attribute the drop to seasonality without checking acquisition and taxonomy.

**Proposed decomposition**: A season can change light, vegetation and class distribution; it can also come with another sensor or another annotation policy. Comparing global errors without checking these elements mixes several hypotheses.

**Constructed ablation**: Align geometry and bands, examine common controlled areas and new regions, and then measure errors by class and condition. Check for a preprocessing change before adapting the model. If an intervention is chosen, tune it on validation and then test it on dates or regions that remain held out. Mixing neighboring tiles to artificially increase the similarity of the test does not establish seasonal generalization. The conclusion must identify what the observations separate and leave open the causes that remain confounded.

**Comparison plan**: Cross known/new region with known/new season to separate spatial and temporal novelty as far as possible. Check bands, physical resolution, alignment and label policy in each cell. A seasonal change can make an object really different or only change its appearance; the class definition must remain explicit. Examining paired areas helps to isolate acquisition effects, but does not by itself evaluate an area never seen before. Keeping results per cell and per class prevents a change in the proportion of easy terrain from artificially explaining the overall average. This plan remains a proposed protocol, not a measured remote-sensing result.

**Season and sensor can be confounded**: If all summer images come from one sensor and all winter images from another, a performance gap cannot be attributed uniquely to season. A proposed analysis seeks overlapping acquisition factors or controlled comparisons, then stratifies by site, band mapping, ground sampling distance, label policy and visible land-cover change. Geographic or temporal grouping must reflect deployment; shuffling nearby tiles does not isolate the source of the shift.

**Blocking errors**: Mixing neighboring tiles of the two seasons to remove the test gap.

**Grading criteria for the case**: explicit task and constraints, stated assumptions, justified choice, discriminating check, limit of the conclusion. Constructed case, without field observation.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]]; [Koh et al., WILDS, §3.3 and §4.3.1: FMoW domains defined by year and region, worst-region evaluation](https://arxiv.org/abs/2012.07421); [Roberts et al. 2017, abstract (blocking by space or time; full text not re-read on 2026-11-14)](https://doi.org/10.1111/ecog.02881). Constructed project case.
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-FIABILITE-004 provenance::agent pole::A pole::C pole::D pole::E pole::F cas_pole::E::diagnostic
END

## CV-FIABILITE-005

Objective: Avoid out-of-domain certainty. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FIABILITE-005
Question: A detector remains highly confident on a new sensor but makes more mistakes. What can be concluded?
Reponse: **Expected answer**: The confidence displayed is not a proof of calibration or reliability out of distribution.

**Further explanation**: Evaluate errors, rejections and calibration on representative acquisitions; review the input contract before adaptation.

**Reading confidence**: A high score can be learned in a distribution where certain cues were reliable, and then remain high when these cues change meaning. Output normalization does not automatically detect this shift. The new sensor can also break color, gamma, resolution or intensity range.

**Proposed investigation**: Compare an identical scene through the two acquisition chains and measure errors on a representative annotated batch from the new sensor. Examine calibration and rejection at the operating point, with the same matching rules. A drop in quality requires action, but the score alone does not say whether to correct the preprocessing, recollect or adapt the model. Keep an independent validation to verify the correction. Monitoring of distributions can provide a useful alarm; it does not by itself demonstrate a drop in precision without a labelled reference.

**Risk and coverage**: For a rule that rejects scores below a threshold, coverage is the fraction of cases where a decision is issued; risk is the error rate among those decisions under the protocol. A method can reduce the risk by rejecting more, without improving perception on the remaining cases. Compare risk–coverage curves and critical strata, with labels representative of the new sensor. A change in the distribution of features can serve as an alarm, but it does not directly give the error rate without a reference. Check the input contract and the relevance of the rejection rule separately after a change of domain; the risk guarantees of selective classification assume test samples drawn from the training distribution.

**Blocking errors**: Taking the softmax score as a generalization guarantee.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Full reference]]; [Ovadia et al. 2019, abstract, §1 and §5: calibration and uncertainty degrade under dataset shift](https://arxiv.org/abs/1906.02530); [Geifman and El-Yaniv 2017, §2 eqs. 1–2: coverage, selective risk and the i.i.d. assumption](https://arxiv.org/abs/1705.08500).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-FIABILITE-005 provenance::agent pole::A pole::C pole::D pole::E pole::F
END
