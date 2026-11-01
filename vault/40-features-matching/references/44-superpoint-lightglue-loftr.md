---
id: CV-MATCH-APPRIS
type: pipeline
domaine: d04
poles: [B]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-SIFT", "CV-ORB", "CV-HOMOGRAPHIE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# SuperPoint, LightGlue and LoFTR

## Problem, data and assumptions

Build matches with learned components, without confusing detector, descriptor and matcher. SuperPoint produces points/descriptors; LightGlue matches compatible features; LoFTR offers detector-free bracket-to-fine matches. These outputs are not automatically a correct pose.

## Prerequisites and competencies

**Required prerequisites**: [CV-SIFT](41-sift.md); [CV-ORB](42-orb.md); [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

SuperPoint learns detection and description with homographic adaptation. LightGlue exploits context and interactions between features, with calculation adaptation. LoFTR uses context and coarse and then fine matches without requiring an explicit sparse detector.

## Mathematics, conventions and units

Each $(x_i,x'_i)$ pair is in two explicit coordinate frames images. After resize or padding, return to comparable coordinates before the geometric residual. A learned matching score is a score of the model; it is not automatically a calibrated probability on the factory.

## Parameters and properties

Choose checkpoints that are compatible with the feature type, resolution, threshold, and calculation policy. Detector-free means neither flow for each pixel nor absence of errors. Do not compare weights or licenses as if they were a single product.

## Cost and implementation

Resolution, number of features, attention and downstream verification dominate cost/memory. No checkpoint downloaded or executed. The results of the authors remain linked to their protocol.

## Evaluation and controlled variation

Baseline proposed: SIFT/ORB + same geometry and same pair set. Vary texture and lighting separately; measure registration success, coverage, full latency and failures. Predict a possible effect of the context, without announcing a measured gain.

## Failure modes and diagnosis

Failed on repetitive surfaces: inspect matches, repetition and geometric pattern. Checkpoint change: Check normalization and expected extraction before setting only the threshold.

## Alternatives and applications

Sparse learned for explicit points; LoFTR for another match strategy; ECC when the objective and initialization of a registration by intensities are adapted.

## Guided reasoning and proposed checks

These built-in cases develop compatibility features – matcher, resolution and validation. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-MATCH-APPRIS-001

**Question of work**: What does SuperPoint provide, and what does LightGlue add for registration between two images?

**Reference Response**: SuperPoint provides keypoints and descriptors; LightGlue searches for matches between compatible features.

**Successive contracts**: Coordinates indicate where the observations are, the descriptors represent their neighborhoods, and the matcher uses both sets to decide which pairs are compatible. The contextual information of the matcher can help to separate local similarities, but it remains a learned prediction about a data distribution.

**Example of a pipeline built**: extract the features compatible with the checkpoint, convert the positions in the declared coordinate frames, get the candidates, and then estimate a homography if the observed object is plane. check error and coverage on useful region. If the scene has parallax, a large number of matches do not automatically allow a global warp. Compare to a baseline SIFT or ORB on the same pairs. Replacing the matcher changes the match proposal; it does not alone provide calibration or final validation of the system.

### Case linked to CV-MATCH-APPRIS-005

**Question of work**: After padding is added, matches look visually correct but the homography is biased. What should be tested?

**Reference Response**: The conversion of positions from the coordinate frame of the network to each real image, including resize and offsets.

**Analytical example**: If the network receives $x'=sx+p_x$ and $y'=sy+p_y$, where $s$ is the resize factor and $(p_x,p_y)$ the padding in network pixels, the return is $x=(x'-p_x)/s$, $y=(y'-p_y)/s$. Each image can have its own parameters. Subtracting only the padding without resetting the scale leaves a systematic error.

**Proposed verification**: follow three known points, including a point close to the origin and a distant point, through the preprocessing and its inverse. check then that the reprojection threshold is expressed in the same coordinate frame as the residuals. A visual overlay on the paged image may seem right as the estimator receives coordinates of two different spaces. The problem is then in the data contract, and changing the checkpoint or threshold of the matcher may hide it without solving it.

**Documentary reference for this pass**: [LightGlue, official deposit](https://github.com/cvg/LightGlue), README, Compatible Use and Extractors. The other developments are in the [flashcards](../44-superpoint-lightglue-loftr.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-MATCH-APPRIS-001

**Situation**: What does SuperPoint provide, and what does LightGlue add for registration between two images?

**Why these bricks are learned together or separately**: SuperPoint shares an encoder between a detection head and a description head; the homographic adaptation matches predictions of transformed views to build more repeatable supervision. LightGlue shares features already extracted and contextualizes them between the two sets. A point is therefore no longer only compared by an isolated distance to each descriptor: its compatibility may depend on the other observations of the pair. This dependence justifies freezing extractor and matching for a reproducible baseline. If an image does not offer enough points or overlap, the context does not create new physical observations.

### CV-MATCH-APPRIS-002

**Situation**: LoFTR is detector-free. Does this imply a reliable trajectory for every pixel?

**Coarse at the end**: LoFTR computes multi-resolution representations, uses intra-image and inter-image interactions to establish coarse-level candidates, and then refines positions in local neighborhoods. The coarse level reduces the search space but quantifies the locations; the refinement aims to recover a finer precision than this grid. A gross match error does not become correct simply because the refinement produces a subpixel position. “Subpixel” describes a digital location resolution, not guaranteed accuracy. The density of the candidates and their concentration must be evaluated with the visibility mask and the final geometry, including in areas with little texture.

### CV-MATCH-APPRIS-003

**Situation**: Why can the input descriptors of a learned-matcher checkpoint not be replaced arbitrarily?

**Learned contract and adaptive budget**: LightGlue can stop certain steps earlier or remove points that have become unhelpful according to its internal criteria. These decisions are based on the statistics of the features and the planned checkpoint; a representation of the same size but excluding distribution can therefore change both the matches and the calculation time. For comparison, also record thresholds and adaptive policy, not just the weight file. Check the latency dispersion between easy and difficult pairs. Disabling an adaptation for an ablation can help assign the change, but does not alone provide an exact match reference or an optimal setting for the new domain.

### CV-MATCH-APPRIS-004

**Situation**: Which conditions make an improvement from learned matching over ORB/SIFT credible?

**Distinguish between location accuracy and quantity**: A pose can be estimated with few precise and distributed matches, or fail with many pairs close to a single line. Compare to fixed point budget isolates certain causes; compare to the best quality – cost point achievable by each pipeline answers another question, to be announced. Images very close to training or pairs of the same sequence can also favor a learned model: separate groups according to future use. For a measurement of pose, specify calibration, geometric threshold, alignment group and failure processing. The name of a benchmark does not guarantee that these conventions are common to two publications.

### CV-MATCH-APPRIS-005

**Situation**: After padding is added, matches look visually correct but the homography is biased. What should be tested?

**Compose the pretreatment matrices**: if $A$ and $B$ respectively send the original images to the network inputs and if $H_{net}$ connects these two inputs, the original homography is $H_{orig}=B^{-1}H_{net}A$. This relationship comes from the original path A→network A→network B→original B. It also deals with distinct horizontal and vertical factors or a crop expressed in a homogeneous affine. Padding pixels are not observations of the scene: their validity must be managed, rather than converted to image coordinates as if they were from a sensor. The subpixel positions and pixel center conventions finally require testing a digital round trip on known points.

**Passages consulted for these developments**: [SuperPoint](https://arxiv.org/html/1712.07629v4), §§3 and 5, two heads and homographic adaptation; [LightGlue, official deposit](https://github.com/cvg/LightGlue), README Usage and Advanced configuration, calculation adaptation; [LoFTR](https://arxiv.org/html/2104.00680v1), §§3.1 – 3.4, context and bracket-to-fine.

## Sources and flashcards

- [SuperPoint, Method and Homographic Adaptation](https://arxiv.org/abs/1712.07629).
- [LightGlue, README, Usage and Advanced configuration (consulted on 2026-10-20)](https://github.com/cvg/LightGlue).
- [LoFTR, §3](https://arxiv.org/abs/2104.00680).
- [Related flashcards](../44-superpoint-lightglue-loftr.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
