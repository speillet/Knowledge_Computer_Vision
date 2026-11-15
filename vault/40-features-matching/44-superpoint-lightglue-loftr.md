# Flashcards — SuperPoint, LightGlue and LoFTR

reference note: [[40-features-matching/references/44-superpoint-lightglue-loftr|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-MATCH-APPRIS-001

Objective: Assign the role of components. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-001
Question: What does SuperPoint provide, and what does LightGlue add for registration between two images?
Reponse: **Expected answer**: SuperPoint provides keypoints and descriptors; LightGlue searches for matches between compatible features.

**Further explanation**: Geometric estimation and validation are still required after matching.

**Successive contracts**: Coordinates indicate where the observations are, the descriptors represent their neighborhoods, and the matcher uses both sets to decide which pairs are compatible. The contextual information of the matcher can help to separate local similarities, but it remains a learned prediction about a data distribution.

**Constructed pipeline example**: extract the features the checkpoint expects, convert the positions into the declared coordinate frames, obtain the candidates, and then estimate a homography if the observed object is planar. Check the error and the coverage over the useful region. If the scene has parallax, a large number of matches does not automatically allow a global warp. Compare with a SIFT or ORB baseline on the same pairs. Replacing the matcher changes the match proposals; it does not by itself provide calibration or final validation of the system.

**Why these components are learned together or separately**: SuperPoint shares an encoder between a detection head and a description head; homographic adaptation aggregates the detector's predictions over randomly warped views to build more repeatable supervision. LightGlue takes features already extracted and contextualizes them across the two sets. A point is therefore no longer compared only by an isolated descriptor distance: its compatibility may depend on the other observations of the pair. This dependence justifies freezing the extractor and the matcher for a reproducible baseline. If an image does not offer enough points or overlap, the context does not create new physical observations.

**Unmatched points are a necessary output**: An occluded keypoint has no valid partner in the other image. A matcher that forces every feature into a pair creates geometric outliers by construction. Evaluate both matched-pair accuracy and treatment of unmatched points, with overlap recorded. Contextual matching can use relations among features to resolve ambiguity, but those relations do not make invisible surface points observable or remove the need for a downstream geometric acceptance test.

**Blocking errors**: Present LightGlue as an object detector or camera calibration.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [DeTone et al. 2018, SuperPoint, §3 two heads, §5 eq. 10 homographic adaptation](https://arxiv.org/abs/1712.07629); [Lindenberger et al. 2023, LightGlue, §3 problem formulation and §3.2 matchability](https://arxiv.org/abs/2306.13643); [Sarlin et al. 2020, SuperGlue, §3 partial assignment](https://arxiv.org/abs/1911.11763); [LightGlue, README, Usage and Advanced configuration, viewed on 2026-10-20](https://github.com/cvg/LightGlue). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d04 famille::comprehension cv_id::CV-MATCH-APPRIS-001 provenance::agent pole::B
END

## CV-MATCH-APPRIS-002

Objective: Distinguish between detector-free and dense flow. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-002
Question: LoFTR is detector-free. Does this imply a reliable trajectory for every pixel?
Reponse: **Expected answer**: No: it produces coarse-to-fine matches without an explicit sparse detector; it is neither a flow guaranteed everywhere nor a complete temporal tracker.

**Further explanation**: Set coordinate frames, scores and geometric validation as for any match proposal.

**Reading the architecture**: the coarse-level search builds matching hypotheses from the context of both images; the fine step refines some of the selected positions. "Without detector" refers to the absence of the classical sparse detector as a mandatory entry point, not the assurance that each point of the scene will have a visible matching point.

**Example of a limit**: A region occluded in the second view has no observable physical correspondence, even if a model returns a score or a candidate position. A trajectory would also require associating the observations over several time steps and handling disappearance and return. Declare the representation, validity masks and rejection criteria, and then evaluate positions with independent geometry or annotations. The network's confidence is decision evidence to be checked on the target domain, not a certificate of a correct trajectory.

**Coarse to fine**: LoFTR computes multi-resolution representations, uses intra-image and inter-image interactions to establish coarse-level candidates, and then refines positions in local neighborhoods. The coarse level reduces the search space but quantizes the locations; the refinement aims to recover a finer precision than this grid. A gross match error does not become correct simply because the refinement produces a subpixel position. “Subpixel” describes the numerical resolution of a location, not a guaranteed accuracy. The density of the candidates and their concentration must be evaluated with the visibility mask and the final geometry, including in areas with little texture.

**Detector-free does not mean confidence-free**: Dense coarse features still require selection of confident correspondences and visibility-compatible evidence. Low-texture regions may benefit from contextual information while remaining ambiguous under repetition or domain shift. A proposed evaluation partitions jointly visible points, occluded points and unmatched image regions. This prevents interpreting the number of returned pairs as full-image coverage or assuming that absent correspondences are failures of a guaranteed per-pixel flow estimator.

**Blocking errors**: Equating detector-free with dense, hole-free and error-free.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [Sun et al. 2021, LoFTR, §3.3 coarse matching with threshold and mutual nearest neighbour, §3.4 refinement in a 5×5 window, §3.6 settings](https://arxiv.org/abs/2104.00680); [LoFTR official code, fine_matching.py L40–L73](https://github.com/zju3dv/LoFTR/blob/df7ca80f917334b94cfbe32cc2901e09a80e70a8/src/loftr/utils/fine_matching.py). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-MATCH-APPRIS-002 provenance::agent pole::B
END

## CV-MATCH-APPRIS-003

Objective: Keep the features compatible. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-003
Question: Why can the input descriptors of a learned-matcher checkpoint not be replaced arbitrarily?
Reponse: **Expected answer**: The learned weights, and the input distributions they expect, are tied to one representation; equal dimensions do not guarantee compatibility.

**Further explanation**: Check feature extractor, normalization, coordinates and version of the checkpoint, and then measure.

**Why size is not enough**: Two vectors of the same length can encode different properties, with other distributions of norms, orientations and scores. The layers of the matcher learn to exploit these conventions. Plugging in an unknown representation may respect the tensor shapes while breaking the statistical contract of the model.

**Discriminating check**: First reproduce the extractor and checkpoint indicated by the authors, on a control pair whose transformation is known. Keep coordinate transformations explicitly. Then replace one component at a time and measure matches, coverage and geometric error. If another representation is considered, look for compatible weights or a truly evaluated adaptation. An execution without exception does not demonstrate this compatibility or a matching gain. This reasoning is about the learned interface; it does not condemn changes in representation when accompanied by appropriate validation.

**Learned contract and adaptive budget**: LightGlue can stop after fewer layers or remove points that have become unhelpful according to its internal criteria. These decisions depend on the feature statistics the checkpoint was trained on; a representation of the same size but with a different distribution can therefore change both the matches and the computation time. For a comparison, also record thresholds and the adaptive policy, not just the weight file. Check the spread of latency between easy and difficult pairs. Disabling an adaptation for an ablation can help attribute the change, but does not by itself provide a reference set of exact matches or an optimal setting for the new domain.

**Coordinate metadata is part of feature compatibility**: A learned matcher can consume point coordinates and image dimensions in addition to descriptor vectors. Replacing descriptors while keeping dimensions equal is only one possible mismatch; supplying positions in a cropped frame with the original image size can also change positional normalization. Verify descriptor preprocessing, point ordering, scale/orientation fields where applicable and coordinate metadata against the checkpoint contract. A successful forward pass checks tensor compatibility, not learned semantic compatibility.

**Blocking errors**: Inferring compatibility from the number of components alone.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [Lindenberger et al. 2023, LightGlue, §3.3 adaptive depth and width, App. C.2 local features](https://arxiv.org/abs/2306.13643); [LightGlue v0.2, lightglue.py, normalize_keypoints L25–L36, features L344–L366, dimension assertion L498–L499](https://github.com/cvg/LightGlue/blob/v0.2/lightglue/lightglue.py); [LightGlue, README, Usage and Advanced configuration, viewed on 2026-10-20](https://github.com/cvg/LightGlue). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-MATCH-APPRIS-003 provenance::agent pole::B
END

## CV-MATCH-APPRIS-004

Objective: Build a comparable baseline. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-004
Question: Which conditions make an improvement from learned matching over ORB/SIFT credible?
Reponse: **Expected answer**: Same problem, pairs/splits, effective resolution and geometric validation; count the cost of the whole chain and failures.

**Further explanation**: Report coverage, robustness and hardware; a benchmark score does not guarantee success on a new acquisition.

**Define the useful gain**: first set the final task, e.g. register a part with a permissible error in a given region. A matcher can produce more pairs but focus them on an unhelpful area, or increase the cost of checking. Intermediate counts therefore do not by themselves indicate progress on the product.

**Constructed comparison**: Use held-out pairs covering texture, blur, lighting and viewpoint change. Keep the geometric acceptance rules fixed and separate threshold tuning from the final test. Report success, false acceptances, rejections, memory and end-to-end latency on the same hardware. If a method uses a higher resolution or other preprocessing, declare it as a pipeline difference. The comparison remains valid for this protocol; its generalization to a new camera or another factory still requires representative observations.

**Distinguish localization accuracy from quantity**: A pose can be estimated with few precise and well-distributed matches, or fail with many pairs close to a single line. Comparing at a fixed keypoint budget isolates some causes; comparing the best quality–cost point achievable by each pipeline answers another question, which must be stated. Images very close to the training data, or pairs from the same sequence, can also favor a learned model: split the data according to the intended use. For a pose measurement, specify the calibration, the geometric threshold, the transformation group used to align estimated and reference poses, and the handling of failures. The name of a benchmark does not guarantee that two publications share these conventions.

**The estimator and the timing scope are part of the protocol**: the LightGlue authors tune the RANSAC or MAGSAC inlier threshold separately for each matcher, because a fixed threshold is suboptimal for some of them; on outdoor relative pose, tuning alone gave SuperGlue +7% AUC at 5°. Their timings also cover matching only, excluding feature extraction and robust estimation. Tune the threshold per arm on validation data, or fix it identically and say so, and time the whole chain when the decision is about a product.

**Adaptive computation needs latency distributions**: If difficult image pairs trigger more matching layers or retain more points, average runtime over easy pairs understates the operational tail. Benchmark by overlap, blur, repetition and input feature count, reporting both successful and failed registrations. Include extraction, device transfer and geometric validation. A lower median matcher time is useful only with the relevant tail latency and acceptance quality; the adaptive design makes those distributions part of the comparison.

**Blocking errors**: Compare raw numbers of matches or times covering different stages.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [Lindenberger et al. 2023, LightGlue, §5.1–§5.2 protocols, App. C.5 threshold tuning, App. D timings](https://arxiv.org/abs/2306.13643); [Sun et al. 2021, LoFTR, §4.1 HPatches protocol and §4.2](https://arxiv.org/abs/2104.00680); [DeTone et al. 2018, SuperPoint, §7.3 and Table 4](https://arxiv.org/abs/1712.07629); comparative protocol proposed by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-MATCH-APPRIS-004 provenance::agent pole::B
END

## CV-MATCH-APPRIS-005

Objective: check the coordinates of the matching. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-005
Question: After a change in image preprocessing, matches look correct when drawn on the network inputs, but the homography estimated in the original images is biased. What should be tested first?
Reponse: **Expected answer**: The conversion of positions from the coordinate frame of the network to each real image, including resize and offsets.

**Further explanation**: Check a known point and the residuals scale before accusing the matcher.

**Analytical example**: If the network receives $x'=sx+p_x$ and $y'=sy+p_y$, where $s$ is the resize factor and $(p_x,p_y)$ the padding in network pixels, the return is $x=(x'-p_x)/s$, $y=(y'-p_y)/s$. Each image can have its own parameters. Subtracting only the padding without undoing the scale leaves a systematic error.

**Proposed verification**: follow three known points, including a point close to the origin and a distant point, through the preprocessing and its inverse. Then check that the reprojection threshold is expressed in the same coordinate frame as the residuals. A visual overlay on the padded image may look right while the estimator receives coordinates from two different spaces. The problem then lies in the data contract, and changing the checkpoint or the matcher threshold may hide it without solving it.

**Compose the preprocessing matrices**: if $A$ and $B$ respectively send the original images to the network inputs and if $H_{net}$ connects these two inputs, the original homography is $H_{orig}=B^{-1}H_{net}A$. This relationship follows the path original A → network A → network B → original B. It also handles distinct horizontal and vertical factors, or a crop written as a homogeneous affine transform. Padding pixels are not observations of the scene: their validity must be managed, rather than converted to image coordinates as if they came from the sensor. Finally, subpixel positions and pixel-centre conventions require a numerical round trip on known points.

**One landmark gives a preprocessing round trip**: Constructed example: resizing by one half and adding padding $(20,10)$ maps original point $(100,60)$ to $(70,40)$. Inversion must subtract padding before dividing by one half, recovering $(100,60)$. Dividing first and then subtracting padding gives the wrong point. Test each image independently, then compose the two preprocessing transforms around the network homography. The same ordering rule applies to cropping and anisotropic resizing.

**Blocking errors**: Mix normalized coordinates and pixels in the same estimate.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [LightGlue v0.2, utils.py, Extractor.extract L137–L147, keypoints returned with (x + 0.5)/s − 0.5](https://github.com/cvg/LightGlue/blob/v0.2/lightglue/utils.py); [LoFTR official code, coarse_matching.py L242–L250, scale0 and scale1](https://github.com/zju3dv/LoFTR/blob/df7ca80f917334b94cfbe32cc2901e09a80e70a8/src/loftr/utils/coarse_matching.py); diagnosis of coordinate frame transformation deduced by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-MATCH-APPRIS-005 provenance::agent pole::B
END
