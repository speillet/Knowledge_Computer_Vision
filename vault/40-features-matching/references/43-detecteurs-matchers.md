---
id: CV-MATCHING
type: methode
domaine: d04
poles: [B, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 7
prerequis: ["CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# Local detectors, descriptors and matchers

## Problem, data and assumptions

Separate the responsibilities of a local pipeline. Detector: points and location score; descriptor: patch vector; matcher: candidates; geometric estimation: pair consistency. Inputs retain resolution, coordinates, and type of representation.

## Prerequisites and competencies

**Required prerequisites**: [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Harris looks for an intensity variation in two directions; Shi – Tomasi uses the smallest eigenvalue of the local matrix. FAST uses comparisons on a circle. BRIEF described by binary tests without being a detector. AKAZE constructs a nonlinear multiscale representation; its descriptor variant must be named.

## Mathematics, conventions and units

The local matrix $M=\sum w\nabla I\nabla I^T$ describes the gradient information. Two high eigenvalues constrain two directions; only one gives ambiguity along an edge. The Harris $\det(M)-k\operatorname{tr}(M)^2$ score depends on its k parameter and scales; this is not a probability.

## Parameters and properties

Number of points, local NMS, thresholds, scale, norm and filtering must be consistent. BF compares exhaustively; FLANN approximates a search with indexes and compatible parameters. The metric comes from the descriptor, not the matcher's name.

## Cost and implementation

BF costs about n×m comparisons; an index changes build, memory and recall cost. No library example is executed. Compare extraction + matching + validation.

## Evaluation and controlled variation

Analytical variation: edge patch then corner. Predict an improperly constrained direction of movement on the edge. In practice, measure repeatability and geometric success under noise, without assimilating corner score and accuracy of registration.

## Failure modes and diagnosis

Many unnecessary points: inspect spatial distribution and repetition. Missing matches: Check norm/type, thresholds and actual number of neighbors before changing the detector.

## Alternatives and applications

SIFT/ORB are complete references; methods learned if they improve the target protocol. A comparison must keep the conditions of acquisition.

## Guided reasoning and proposed checks

These constructed cases develop contract steps and diagnosis before method change. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-MATCHING-001

**Question of work**: In a gradient-based model, why does a corner constrain 2D displacement better than an isolated edge?

**Reference Response**: Two directions of variation constrain the movement; on an edge, the tangent displacement is hardly observable.

**Local model**: for a small displacement $d$, the photometric variation is close to a quadratic form $d^TMd$. The matrix $M$ gathers the products of the gradients in the vicinity. Its eigenvectors indicate the directions of movement that change the appearance much or little.

**Constructed example**: On a uniform vertical edge, moving the patch horizontally changes its contents; moving it along the edge can almost leave it the same. A visible corner shows changes in two directions, which helps locate a move. This does not imply that it is unique in the image: the corners of a grid can all look the same. So distinguish local location information and ambiguity of association between images. A poorly lit, obscured or too large window can also invalidate the small photometric model despite favorable eigenvalues.

### Case linked to CV-MATCHING-004

**Question of work**: Two repeated logos produce similar descriptors. Which component can test a physical model of the correspondences?

**Reference Response**: A geometric check adapted to the scene, with residuals, thresholds and cover; the matcher alone does not guarantee it.

**What the Geometry Tests**: A homography for a plane, or an appropriate multiview constraint, links candidate positions in images. The residual expresses their disagreement with this model in a defined unit. A matcher chooses neighbors in an appearance representation; these two problems are different.

**Constructed limitation**: Two identical logos on the same medium can produce a coherent group of matches and a transformation that matches the wrong logo. A geometric model does not necessarily resolve a symmetry of the scene. Look for a single brand, an expected position, or an additional observation that distinguishes assumptions. check also supports spatial points and reserved observations. This step provides reasons for accepting a transformation for a specific purpose, without automatically transforming the consensus into proof of the object's identity.

**Documentary reference for this pass**: [OpenCV 4.13, Feature Matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), Brute-Force Matcher, norms and FLANN. The other developments are in the [flashcards](../43-detecteurs-matchers.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-MATCHING-001

**Situation**: In a gradient-based model, why does a corner constrain 2D displacement better than an isolated edge?

**Link to the aperture problem**: The linearized luminance constant gives $I_xu+I_yv+I_t=0$, an equation for two displacement components. On an edge, the neighboring gradients are almost parallel, so stacking their equations does not add a second independent direction. A corner brings different gradient orientations and can make the local system invertible. This reasoning assumes a movement common to the patch and small variations between images. A window through two objects can have a well-conditioned tensor but no longer respect the single movement. The corner score should be read with this model, and not as a universal utility score for all estimators.

### CV-MATCHING-002

**Situation**: Why are FAST and BRIEF not alternatives that perform exactly the same role?

**Expected equivariance and invariance**: If an image is geometrically transformed by $T$, a repeatable detector should find the transformed positions $T(p)$; it should therefore not produce the same numerical coordinates. On the contrary, the descriptor aims at a comparable representation of the corresponding neighborhoods after the planned standardizations. Confusing these two properties misconstrues a rotation test: the coordinates should change, while the description should stay close enough. Too much invariance can also remove distinctive information and make several patches similar. The aim is not to make all descriptors identical under any transformation, but to keep discrimination in the field of variations useful.

### CV-MATCHING-003

**Situation**: What should be checked if FLANN accelerates matching but degrades registration?

**Measuring the Cascade Effect**: on the same requests, keep successively the identity of the two neighbors, the decision of the ratio filter, the insider status and the reserved geometric error. This track allows you to locate where a search difference becomes a product error. If the index finds the exact neighbors but the registration changes, consider order of matches, separation of the ex æquo and randomness of the robust estimate. If neighbors differ, only increasing the budget or redoing the exact distances on additional candidates is a more targeted ablation. An identical recall average may still mask the loss of rare distinguishing points that are decisive for lifting a symmetry.

### CV-MATCHING-004

**Situation**: Two repeated logos produce similar descriptors. Which component can test a physical model of the correspondences?

**Choosing the right residual**: for a $H$ homography sending the image A to B, $e_i=\|\pi(H\tilde p_i)-q_i\|_2$ is a transfer error in B pixels, with $\pi$ the homogeneous division. An epipolar geometry imposes another constraint, and PnP combines points 3D and calibrated projection. Reusing a threshold without announcing the residual changes what “inlier” means. The geometric test checks for compatibility conditional to the model; one symmetry can provide another set equally compatible. Adding an independent constraint is then a change in available information, while tightening the threshold only changes the tolerance of the same test.

**Passages consulted for these developments**: [OpenCV 4.13, Feature Matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), BF/FLANN, metrics and filters; Context7 verification.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-MATCHING-001 — Local uncertainty follows the weakest direction

Under an ideal independent equal-variance photometric model, the displacement covariance is approximately $\sigma_I^2M^{-1}$. If $M=\operatorname{diag}(100,1)$, uncertainty along the second direction is one hundred times the first in variance, or ten times in standard deviation. This is a local linearized result, not a guarantee of correct correspondence. A repeated corner can constrain small motion precisely while still matching a distant copy incorrectly.

### CV-MATCHING-002 — Descriptor support can invalidate a detected point

A detector can return a valid point close to an image boundary, yet a descriptor may lack enough neighborhood support there. Rotation or scale normalization can move required sample positions outside the image as well. Record which points survive description and how coordinates and orientations are retained. Comparing only detector counts can otherwise attribute descriptor-border exclusions to matching, even though no usable descriptor was ever produced.

### CV-MATCHING-003 — Approximation can change the robust solver budget

If approximate search reduces the true inlier fraction, robust geometric estimation may need many more samples even when each match query becomes faster. Measure neighbor errors, accepted matches and geometric solver effort on the same image pairs. This proposed decomposition identifies whether the cost was saved in search and spent again in geometry, rather than assuming that a lower matching latency implies a faster reliable registration pipeline.

### CV-MATCHING-004 — Model compatibility is weaker than unique identity

A planar repeated texture can support two different homographies with similarly small transfer errors. A physically meaningful residual rejects pairs inconsistent with a chosen model, but cannot resolve a symmetry that preserves the measurements. Independent appearance, a motion bound or another sensor can break that ambiguity when justified. Otherwise return competing hypotheses or refuse the registration instead of treating a large consensus as proof of absolute alignment.

Consulted foundations: [OpenCV Harris](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html): local displacement quadratic and structure tensor; [OpenCV matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html): distance norms, mutual matching and two-neighbor matching; checked with Context7.

## Sources and flashcards

- [OpenCV 4.13.0, FAST, Feature Detection](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html)
- [OpenCV 4.13.0, BRIEF, Theory](https://docs.opencv.org/4.13.0/dc/d7d/tutorial_py_brief.html)
- [OpenCV 4.13.0, AKAZE, Detailed Description and DescriptorType](https://docs.opencv.org/4.13.0/d8/d30/classcv_1_1AKAZE.html)

- [OpenCV Harris, theory](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html).
- [OpenCV Shi–Tomasi](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html).
- [OpenCV matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
- [Related flashcards](../43-detecteurs-matchers.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
