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

**Example of a pipeline built**: extract the features compatible with the checkpoint, convert the positions in the declared coordinate frames, get the candidates, and then estimate a homography if the observed object is plane. check error and coverage on useful region. If the scene has parallax, a large number of matches do not automatically allow a global warp. Compare to a baseline SIFT or ORB on the same pairs. Replacing the matcher changes the match proposal; it does not alone provide calibration or final validation of the system.

**Why these bricks are learned together or separately**: SuperPoint shares an encoder between a detection head and a description head; the homographic adaptation matches predictions of transformed views to build more repeatable supervision. LightGlue shares features already extracted and contextualizes them between the two sets. A point is therefore no longer only compared by an isolated distance to each descriptor: its compatibility may depend on the other observations of the pair. This dependence justifies freezing extractor and matching for a reproducible baseline. If an image does not offer enough points or overlap, the context does not create new physical observations.

**Blocking errors**: Present LightGlue as an object detector or camera calibration.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [DeTone et al. 2018, SuperPoint, §§3 and 5](https://arxiv.org/abs/1712.07629); [LightGlue, README, Usage and Advanced configuration, viewed on 2026-10-20](https://github.com/cvg/LightGlue); [SuperPoint, §§3 and 5, two heads and homographic adaptation](https://arxiv.org/html/1712.07629v4); [LoFTR, §§3.1 – 3.4, context and bracket-to-fine](https://arxiv.org/html/2104.00680v1), see the 2026-10-30.
Tags: cv::pilote cv::d04 famille::comprehension cv_id::CV-MATCH-APPRIS-001 provenance::agent pole::B
END

## CV-MATCH-APPRIS-002

Objective: Distinguish between detector-free and dense flow. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-002
Question: LoFTR is detector-free. Does this imply a reliable trajectory for every pixel?
Reponse: **Expected answer**: No: it produces coarse-to-fine matches without explicit split detector; it is neither a guaranteed flow anywhere nor a complete time tracker.

**Further explanation**: Set coordinate frames, scores and geometric validation as for any match proposal.

**Reading architecture**: coarse-level search constructs matching hypotheses from the context of the two images; the fine step specifies certain selected positions. "Without detector" refers to the absence of the classical sparse detector as a mandatory entry point, not the assurance that each point of the scene will have a visible matching point.

**Example of limit**: A region occulted in the second view has no observable physical correspondence, even if a model returns a score or candidate position. A trajectory would also require associating the observations through several moments and managing disappearance and return. Declare representation, validity masks, and rejection criteria, and then evaluate positions with independent geometry or annotations. Network trust is decision data to be checked on the target domain, not a correct path certificate.

**Coarse at the end**: LoFTR computes multi-resolution representations, uses intra-image and inter-image interactions to establish coarse-level candidates, and then refines positions in local neighborhoods. The coarse level reduces the search space but quantifies the locations; the refinement aims to recover a finer precision than this grid. A gross match error does not become correct simply because the refinement produces a subpixel position. “Subpixel” describes a digital location resolution, not guaranteed accuracy. The density of the candidates and their concentration must be evaluated with the visibility mask and the final geometry, including in areas with little texture.

**Blocking errors**: Assimilate detector-free to dense without holes and without errors.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [Sun et al. 2021, LoFTR, §§3.1 – 3.4 and 4.1 – 4.2](https://arxiv.org/abs/2104.00680); [SuperPoint, §§3 and 5, two heads and homographic adaptation](https://arxiv.org/html/1712.07629v4); [LightGlue, official repository, README Usage and Advanced configuration, calculation adaptation](https://github.com/cvg/LightGlue); [LoFTR, §§3.1 – 3.4, context and bracket-to-fine](https://arxiv.org/html/2104.00680v1), see the 2026-10-30.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-MATCH-APPRIS-002 provenance::agent pole::B
END

## CV-MATCH-APPRIS-003

Objective: Keep the features compatible. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-003
Question: Why can the input descriptors of a learned-matcher checkpoint not be replaced arbitrarily?
Reponse: **Expected answer**: Expected weights and distributions are associated with a representation; equal dimensions do not guarantee compatibility.

**Further explanation**: Check feature extractor, normalization, coordinates and version of the checkpoint, and then measure.

**Why size is not enough**: Two vectors of the same length can encode different properties, with other distributions of norms, orientations and scores. The layers of the matcher learn to exploit these conventions. Connecting an unknown representation eventually respects the shapes of the tensors while breaking the statistical contract of the model.

**check**: First reproduce the extractor and checkpoint indicated by the authors, on a control pair whose transformation is known. Keep coordinate transformations explicitly. Then replace one component at a time and measure matches, coverage and geometric error. If another representation is considered, look for compatible weights or a truly evaluated adaptation. An execution without exception does not demonstrate this compatibility or a matching gain. This reasoning is about the learned interface; it does not condemn changes in representation when accompanied by appropriate validation.

**Learned contract and adaptive budget**: LightGlue can stop certain steps earlier or remove points that have become unhelpful according to its internal criteria. These decisions are based on the statistics of the features and the planned checkpoint; a representation of the same size but excluding distribution can therefore change both the matches and the calculation time. For comparison, also record thresholds and adaptive policy, not just the weight file. Check the latency dispersion between easy and difficult pairs. Disabling an adaptation for an ablation can help assign the change, but does not alone provide an exact match reference or an optimal setting for the new domain.

**Blocking errors**: Deduct compatibility of only the number of components.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [LightGlue, README, Usage and Advanced configuration, viewed on 2026-10-20](https://github.com/cvg/LightGlue); [SuperPoint, §§3 and 5, two heads and homographic adaptation](https://arxiv.org/html/1712.07629v4); [LoFTR, §§3.1 – 3.4, context and bracket-to-fine](https://arxiv.org/html/2104.00680v1), see 2026-10-30.
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

**Define the useful gain**: first set the final task, e.g. register a part with a permissible error in a given region. A matcher can produce more pairs but focus them on an unhelpful area, or increase the cost of checking. The interim accounts do not therefore indicate only a progress produced.

**Comparison built**: Use reserved pairs covering texture, blur, lighting and change of point of view. Keep the rules of geometric acceptance and separate threshold setting and final test. Report success, acceptance errors, rejection, memory, and end-to-end latency on the same hardware. If a method uses a higher resolution or other preprocessing, declare it as a pipeline difference. The comparison remains valid for this protocol; its generalization to a new camera or another factory still requires representative observations.

**Distinguish between location accuracy and quantity**: A pose can be estimated with few precise and distributed matches, or fail with many pairs close to a single line. Compare to fixed point budget isolates certain causes; compare to the best quality – cost point achievable by each pipeline answers another question, to be announced. Images very close to training or pairs of the same sequence can also favor a learned model: separate groups according to future use. For a measurement of pose, specify calibration, geometric threshold, alignment group and failure processing. The name of a benchmark does not guarantee that these conventions are common to two publications.

**Blocking errors**: Compare raw numbers of matches or times covering different stages.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [Sun et al. 2021, LoFTR, §§3.1 – 3.4 and 4.1 – 4.2](https://arxiv.org/abs/2104.00680); comparative protocol proposed by the project; [SuperPoint, §§3 and 5, two heads and homographic adaptation](https://arxiv.org/html/1712.07629v4); [LightGlue, official repository, README Usage and Advanced configuration, calculation adaptation](https://github.com/cvg/LightGlue); [LoFTR, §§3.1 – 3.4, context and bracket-to-fine](https://arxiv.org/html/2104.00680v1), consult the 2026-10-30.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-MATCH-APPRIS-004 provenance::agent pole::B
END

## CV-MATCH-APPRIS-005

Objective: check the coordinates of the matching. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-005
Question: After padding is added, matches look visually correct but the homography is biased. What should be tested?
Reponse: **Expected answer**: The conversion of positions from the coordinate frame of the network to each real image, including resize and offsets.

**Further explanation**: Check a known point and the residuals scale before accusing the matcher.

**Analytical example**: If the network receives $x'=sx+p_x$ and $y'=sy+p_y$, where $s$ is the resize factor and $(p_x,p_y)$ the padding in network pixels, the return is $x=(x'-p_x)/s$, $y=(y'-p_y)/s$. Each image can have its own parameters. Subtracting only the padding without resetting the scale leaves a systematic error.

**Proposed verification**: follow three known points, including a point close to the origin and a distant point, through the preprocessing and its inverse. check then that the reprojection threshold is expressed in the same coordinate frame as the residuals. A visual overlay on the paged image may seem right as the estimator receives coordinates of two different spaces. The problem is then in the data contract, and changing the checkpoint or threshold of the matcher may hide it without solving it.

**Compose the pretreatment matrices**: if $A$ and $B$ respectively send the original images to the network inputs and if $H_{net}$ connects these two inputs, the original homography is $H_{orig}=B^{-1}H_{net}A$. This relationship comes from the original path A→network A→network B→original B. It also deals with distinct horizontal and vertical factors or a crop expressed in a homogeneous affine. Padding pixels are not observations of the scene: their validity must be managed, rather than converted to image coordinates as if they were from a sensor. The subpixel positions and pixel center conventions finally require testing a digital round trip on known points.

**Blocking errors**: Mix normalized coordinates and pixels in the same estimate.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Full reference]]; [LightGlue, README, Usage and Advanced configuration, viewed on 2026-10-20](https://github.com/cvg/LightGlue); diagnosis of coordinate frame transformation deduced by the project; [SuperPoint, §§3 and 5, two heads and homographic adaptation](https://arxiv.org/html/1712.07629v4); [LoFTR, §§3.1 – 3.4, context and bracket-to-fine](https://arxiv.org/html/2104.00680v1), consult the 2026-10-30.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-MATCH-APPRIS-005 provenance::agent pole::B
END
