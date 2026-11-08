---
id: CV-ECC
type: methode
domaine: d04
poles: [B, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-HOMOGRAPHIE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# Intensity-based registration and ECC

## Problem, data and assumptions

Align images by optimizing a photometric criterion under a motion model. Inputs: compatible images, possible mask and initialization; output: parameters of warp. This is not a matcher of local descriptors.

## Prerequisites and competencies

**Required prerequisites**: [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

The optimizer distorts one image to improve correlation with the other. Centering and normalization render the correlation unchanged under a positive gain and an overall offset on a fixed medium, of non-zero variance (algebraic deduction). This does not guarantee convergence of the registration ECC. A pyramid can improve initialization without guaranteeing a global optimum.

## Mathematics, conventions and units

A warp $W(x;\theta)$ transforms the coordinates according to the chosen model. A standardized correlation compares centered/standardized intensities over the common area; $\theta$ does not have the same dimensions for translation, affine, and homography. Specify the meaning of the warp and the use of its reciprocal to the display.

## Parameters and properties

Model, stop criterion, mask and scale must match the movement. Texture, overlay and initialization are essential. Simple gain robustness does not cover shadows, occlusions or arbitrary 3D geometry.

## Cost and implementation

Each iteration evaluates and derives the criterion on pixels; resolution and pyramid count. No `findTransformECC` calls executed; do not turn convergence into registration guarantee.

## Evaluation and controlled variation

Proposed variation: known translation then more and more remote initialization. Measure warp error on reserved points and convergence rate; a photometric score alone can favor a repetitive pattern.

## Failure modes and diagnosis

Failed despite close images: check range/type, direction of transformation, overlap and actual photometric disturbance.

## Alternatives and applications

Features + RANSAC for large transformations with distinctive points; registration by intensities for appropriate refinement. Compare on accuracy and useful basin.

## Guided reasoning and proposed checks

These constructed cases develop photometric criteria, convergence basin and masks. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-ECC-001

**Question of work**: Which input/output contract distinguishes ECC from a SIFT + RANSAC pipeline?

**Reference Response**: ECC optimizes an intensity criterion on an initialized warp; SIFT offers pairs and then a robust geometry.

**Interpreted mechanism**: ECC looks for transformation parameters by directly comparing intensities on a common area. Matches are not first expressed as a list of detected patches. SIFT and RANSAC can offer transformation from distinctive points; photometric refinement can then be tried if the model and the cover are suitable.

**Constructed example**: For two views close to a label, a suitable initialization can make it useful to optimize intensities. For a large move with low overlap, the same procedure can reach a bad optimum or fail. Check initialization, mask, photometric variations and motion pattern separately. A normalized correlation can tolerate a positive gain and a global offset on a fixed non-constant medium; this algebraic property does not cover a local shadow, a occlusion, or a global convergence of the registration.

### Case linked to CV-ECC-003

**Question of work**: Why should a homography not always be chosen for ECC registration?

**Reference Response**: More parameters can over-adjust or reduce stability while translation or affine is sufficient as needed.

**Reasoning about degrees of freedom**: a translation model requires that all points share two displacements; a homography allows a more general projective deformation. This flexibility can explain real variations of view on a plane, but also absorb noise or a photometric disturbance when the data does not constrain its parameters.

**Comparison built**: on an installation where the planned movement is a small translation, first adjust this model, then a richer model with the same images and useful area. Compare errors on reserved points, stability of parameters and extrapolation near edges. A better score on the adjustment pixels is not enough. Conversely, keeping a translation if the perspective really changes introduces a bias. The choice therefore links capture geometry, the richness of observations and the admitted error, rather than a principle of simplicity or flexibility applied blindly.

**Documentary reference for this pass**: [OpenCV 4.13, Video Tracking](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html), findTransformECC and warp parameters. The other developments are in the [flashcards](../45-recalage-ecc.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-ECC-001

**Situation**: Which input/output contract distinguishes ECC from a SIFT + RANSAC pipeline?

**Understanding the Standardized Criteria**: on a fixed support, center the intensities $a_i$ and $b_i(\theta)$ gives $\bar a_i=a_i-\mu_a$ and $\bar b_i=b_i(\theta)-\mu_b$. The correlation is $\rho(\theta)=\sum_i\bar a_i\bar b_i/(\sqrt{\sum_i\bar a_i^2}\sqrt{\sum_i\bar b_i^2})$ if the norms are non-zero. Multiply an image by a positive gain and add a global offset retains this ideal value; a negative gain reverses its sign. Optimization modifies the warp, thus the interpolated intensities and their gradient with respect to the parameters. Valid media and hidden pixels must remain explicitly controlled: changing the overlap can change the compared criterion.

### CV-ECC-002

**Situation**: ECC converges with high correlation on a repetitive grid, but the displacement is wrong. How should it be validated?

**Decouple score and plausibility**: A correlation close to 1 describes the standardized similarity of the actually compared content. It does not directly indicate the number of valid pixels, the uniqueness of the maximum, or the displacement error. A very small common area can therefore produce a high score with little geometric information. Report media size and error on reserved points, then test separate initializations of a period of the pattern. If several solutions keep scores close and physical constraints allowable, keep ambiguity in the decision. Turning the score into acceptance confidence requires calibration on representative cases, including false but visually plausible alignments.

### CV-ECC-003

**Situation**: Why should a homography not always be chosen for ECC registration?

**Dimension and identifiability of the warp**: translation: two parameters; plane Euclidean movement: rotation and two translations; affine: six parameters; homography: eight independent parameters after choice of scale. A homography acts by projective division: small changes in the denominator can strongly change the edges of the extrapolated region. With little overlap or texture, some parameters compensate and the local information matrix can become poorly conditioned. Compare models with reserved geometry rather than with the only optimized score. If a simpler model is sufficient, it can limit these compensations; if the capture violates its assumptions, this simplicity imposes on the contrary an irreducible bias.

**Passages consulted for these developments**: [OpenCV 4.13, computeECC/findTransformECC](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html), criterion, motionType, initialization and reverse warping.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-ECC-001 — Constant patches make normalization undefined

The normalized correlation denominator vanishes when either compared patch has zero centered-intensity norm. Almost constant support makes it poorly conditioned before exact degeneracy. Restricting to a seemingly clean ROI can therefore remove the texture required for alignment. A proposed check records support variance, valid overlap and the warp direction along with the returned score. Brightness normalization removes a global offset/gain under its assumptions, not missing geometric information.

### CV-ECC-002 — A periodic image permits several equally good optima

For an ideal intensity pattern with period $P$, translations separated by integer multiples of $P$ produce identical overlap content away from boundaries. A high normalized correlation cannot determine which period is physically correct. Initialize within a justified capture range and validate on nonperiodic structures or an external movement constraint. Repeated convergence from nearby initializations checks local stability; it does not establish uniqueness over the whole search region.

### CV-ECC-003 — Compare model complexity on held-out geometry

A project comparison can fit translation, affine and projective warps on the same textured support, then measure transfer on independently selected landmarks. Additional parameters may lower the fitted intensity cost while increasing held-out error or instability near the image boundary. Choose the simplest model meeting the geometric tolerance under the scene assumptions, recording failures as well as correlation. A homography is physically justified for a plane or pure rotation, not arbitrary parallax.

Consulted foundations: [OpenCV findTransformECC](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html): findTransformECC intensity objective, initialization, motion model and warp application.

## Sources and flashcards

- [OpenCV findTransformECC, motion and criteria](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html).
- [Related flashcards](../45-recalage-ecc.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
