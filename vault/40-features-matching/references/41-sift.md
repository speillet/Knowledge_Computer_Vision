---
id: CV-SIFT
type: methode
domaine: d04
poles: [B, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: []
revision: 7
tags: [cv/d04, matching, sift]
---
# SIFT — local features and multiscale descriptors

## Problem and data contract

SIFT (*Scale-Invariant Feature Transform*) provides feature points and descriptors to search for matches between images. It produces neither a global transformation nor an object identity on its own. Driver input: image 2D in grey; output: positions $(x,y)$ in pixels, scales, orientations and vectors of 128 components for the classic variant. The coordinates return to the coordinate frame of the provided image: keep the resize/crop applied before extraction. [Lowe, §§3 – 6][lowe]

**Competences**: explain the pipeline, interpret invariances, choose a distance, diagnose matches. **Required prerequisites**: [gradients, distances and coordinate frames](../../01-Parcours/Pre-requis.md). **Connexions**: [ORB](42-orb.md), [RANSAC/homographie](../../50-calibration-geometrie/references/51-ransac-homographie.md).

## Intuition and procedure

A visual detail must be found on a comparable scale before describing its vicinity. SIFT searches for extrema in a scale space, rejects unstable locations, chooses a local orientation, and then describes the spatial distribution of gradient directions.

1. Build a Gaussian Pyramid and Gaussian Differences (DoG).
2. Compare a candidate to its 26 spatial and scale neighbors.
3. Refine its location; reject low contrast and edge-dominated responses, whose position is poorly defined in one direction.
4. Assign one or more dominant orientations.
5. Accumulate gradients in oriented cells; normalize vector.
6. Offer matches with a suitable distance, then filter the ambiguities.
7. Check a geometric pattern if the problem requires one. [Lowe, §§3 – 7][lowe]

Steps 6 – 7 belong to the matching pipeline; a homography is not a mandatory component of the descriptor SIFT.

## Explained mathematics

$$
L(x,y,\sigma)=(G_\sigma*I)(x,y),\qquad
D(x,y,\sigma)=L(x,y,k\sigma)-L(x,y,\sigma).
$$

$I$ is the image, $G_\sigma$ a normalized Gaussian kernel, $*$ the convolution, $\sigma>0$ the pixel smoothing scale and $k>1$ the ratio between two successive scales. The DoG compares two neighboring levels; it approximates a Laplacian normalized in scale when their spacing is adapted. In an octave, $k=2^{1/s}$ for $s$ intervals: doubling $\sigma$ sets an octave. Intensity values and thresholds must remain consistent.

The classic descriptor includes $4\times4$ cells and eight orientations, or 128 components. Weighting and interpolation reduce abrupt changes due to gradient displacement. Normalization, clipping and renormalization mitigate some photometric variations; they compensate for neither saturation nor arbitrary shadows. [Lowe, §§3 and 6][lowe]

For a query, $d_1\le d_2$ are the distances to the two best candidates. Accepting $d_1<\tau d_2$, with $0<\tau<1$, rejects a match whose next neighbor is almost as plausible. A small absolute distance is not enough. If both distances are zero, ambiguity should not be blindly accepted. [Lowe, §7.1][lowe]

## Assumptions, properties and parameters

- Scale and rotation: normalization mechanisms, subject to sampling, noise and repeatability detection; no guarantee for any image.
- Perspective: limited robustness, without general projective invariance.
- Texture: necessary to form locally distinctive neighborhoods.
- Parameters: octave density, contrast threshold, edge rejection, number of points retained and ratio threshold. Change only one factor at a time on a validation set representing the industrial problem.

A stricter ratio threshold generally reduces retained matches; it is necessary to measure whether geometric recall and spatial coverage suffer. Lowe’s historical threshold of 0,8 depends on his experiences, without universal value.

## Cost and implementation

Pyramid, detection and description depend on the resolution, levels and number of points. An exhaustive matching of $n$ and $m$ vectors of dimension $d$ costs in the order of $nmd$ scalar comparisons; FLANN changes the time/recall compromise. No material speed gain is assumed here.

Extract **Illustrative not executed**, API OpenCV 4.13 checked:

```python
sift = cv.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(gray, None)
matcher = cv.BFMatcher(cv.NORM_L2, crossCheck=False)
# Handle missing descriptors and fewer than 2 neighbors before using knnMatch.
pairs = matcher.knnMatch(descriptors_a, descriptors_b, k=2)
good = [a for pair in pairs if len(pair) == 2
        for a, b in [pair] if a.distance < 0.75 * b.distance]
```

`gray`, `descriptors_a` and `descriptors_b` are prepared entries, not variables created by this extract. The 0,75 ratio is illustrative. The norm derives from the sense of the descriptor, not just its memory type. [OpenCV, matching][opencv]

## Evaluation, variation and diagnosis

**Proposed baseline, not an executed image experience**: two shots of a flat label with known geometry. Compare matches to true transformation, coverage, and projection error; measure full pipeline latency on the target machine.

**Proposed controlled variation**: Rotate alone, then scale, then add blur separately. Prediction: Orientation/scale help in their area of operation; blurring can destroy the necessary details. The actual result remains to be measured, without announcing a digital performance.

| Symptom | Causes to be distinguished | Discriminant verification |
| --- | --- | --- |
| Many matches on repeated grounds | Ambiguous descriptors, incorrect geometric model | Distribution of ratios, location of inliers, validation on reserved points |
| Almost no point after blur | Details removed, contrast threshold too strict | Inspect pyramid and detections before changing the matcher |
| Good consensus in one corner, false projection elsewhere | Poor coverage, unstable extrapolation | residuals and positions throughout the useful area |

**Cas industriel**: registration of a label under rotation with CPU budget. SIFT is a baseline to compare to ORB and the methods learned on success, robustness and total cost, without declaring it a winner a priori.

## Guided reasoning and proposed checks

These constructed cases develop normalizations, ratio ambiguity and geometric coverage. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-SIFT-001

**Question of work**: When registering two photos of a planar label, what does SIFT provide, and which additional steps are required to obtain a reliable transformation?

**Reference Response**: SIFT provides keypoints and their local descriptors. The matcher offers pairs; filtering limits ambiguities; a geometric estimate tests a transformation adapted to the plane. The matches are not proof of registration.

**Constructed decision chain**: For a known flat label, keep the keypoint coordinates in each image, calculate the candidates and inspect their distribution before estimating the warp. Four misplaced matches or several ambiguous pairs do not become reliable because they come from SIFT. A concentrated consensus in one corner may also misconstraint extrapolation to the other edge.

**Interpretation of the result**: check a geometry on points not used for its adjustment and in the area where the product must act. A piece in relief may require a different model than a single homography. The responsibility of SIFT is local representation; that of the pipeline is to establish that a transformation sufficiently explains the observations for the announced use.

### Case linked to CV-SIFT-007

**Question of work**: When choosing SIFT or ORB for industrial part registration, which measurements make the comparison useful to the product?

**Reference Response**: use the same representative pairs and reference geometry; measure success of registration, errors, coverage and full cost on the target hardware. Set to validation and then freeze for the test.

**Proposed product criteria**: Convert the registration error to business-related, such as an inspection region offset from the fault. Set a tolerance and count successes, refusals and dangerous mistakes. Two methods at residuals mean neighbors can differ greatly on oblique views or sparsely textured pieces.

**Complete measurement**: record resolution, number of points and same steps included in the timing. A faster extractor that produces a lot of ambiguous candidates can shift the cost towards matching and RANSAC. Also examine memory and latency of difficult cases. The right decision depends on the compromise observed on the target hardware and the consequences of a failure, not a general preference for a conventional or binary method.

**Documentary reference for this pass**: [Lowe 2004](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf), §§3 – 7.1, detection, orientation, descriptor and matching. The other developments are in the [flashcards](../41-sift.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-SIFT-001

**Situation**: When registering two photos of a planar label, what does SIFT provide, and which additional steps are required to obtain a reliable transformation?

**Linking Outputs to an Estimate**: represent the points by two tables $P_A\in\mathbb R^{n\times2}$ and $P_B\in\mathbb R^{m\times2}$, and their descriptors by two tables with 128 columns. The matcher returns $(i,j)$ indices, not directly the coordinates of a transformation. A robust estimate then uses the $(P_A[i],P_B[j])$ pairs in the same pixel contract as its threshold. If the extraction was done on a resized image, the estimated matrix connects these resized images; composing it with the preprocessing transformations is necessary to return to the initial images. Maintaining these associations of indices avoids confusing the quality of the descriptor and the error of manipulation of the coordinates.

### CV-SIFT-002

**Situation**: In SIFT, what does the difference of Gaussians compare, and why are extrema also sought across scale?

**Why DoG is Approaching a Laplacian**: for $k$ close to 1, a scale development gives $L(k\sigma)-L(\sigma)\approx(k-1)\sigma\,\partial L/\partial\sigma$. The Gaussian diffusion equation links this derivative to $\sigma\nabla^2L$: the difference is therefore proportional to a Laplacian normalized by $\sigma^2$. This approximation implies a suitable spacing of scales, not an exact identity for any $k$. Detecting an extremum is just the beginning: local refinement estimates position and scale between samples, then low-contrast and edge-dominated rejections avoid describing unstable points. The same number of candidates does not mean the same number of reliable keypoints.

### CV-SIFT-003

**Situation**: Once a SIFT keypoint is localized, how is its classical descriptor built, and what do the main steps seek to stabilize?

**Understanding normalization**: For a non-zero $d$ histogram, division by $\|d\|_2$ cancels out a common multiplicative gain; subtracting a constant from all intensities does not already change their differences in the ideal model. On the other hand, if a few gradients dominate, they can crush the contribution of other cells. A clipping followed by a new normalization limits this domination. Constructed example: two patches with a single edge becoming much stronger can keep a similar directional layout while changing the raw norm. Interpolation between cells and orientation bins also prevents a small geometric variation from abruptly shifting the entire contribution on one side of a discrete boundary.

### CV-SIFT-004

**Situation**: Two query descriptors have L2 distances $(20,21)$ and $(35,80)$ to their two nearest neighbors. With a ratio-test threshold of 0.8, which query is retained, and what does this test establish?

**Beware of squared distances**: If a routine provides $s_1=d_1^2$ and $s_2=d_2^2$, the criterion equivalent to $d_1<\tau d_2$ is $s_1<\tau^2s_2$, not $s_1<\tau s_2$. With $\tau=0,8$, directly comparing squares to 0,8 would be tolerating a distance ratio close to 0,894. This transformation is algebraically inferred for positive distances; it does not say which convention uses a particular API. Read the contract of the function and test a small known couple before reusing a threshold. The "second" neighbor must also come from the same set of candidates provided by the protocol; changing the base changes the measured ambiguity.

### CV-SIFT-005

**Situation**: A planar object is first rotated within the image, then viewed from a very oblique angle. Why do these changes pose different challenges for SIFT?

**Analyze local deformation**: In the vicinity of a point, a regular projective transformation is linearized by a matrix $2\times2$ which can have two different singular values. A rotation and an isotropic scale only compensate for a part of it; the ratio of the singular values measures a local anisotropy. Example built: a disc observed more and more obliquely becomes an ellipse, even after returning its main axis to the right orientation. The described neighborhood therefore changes shape. Rectifying can help if the geometry is known, but estimating this rectification from the same difficult matches is not a free solution. The occlusion additionally removes information that no coordinate transformation restores.

### CV-SIFT-006

**Situation**: A repetitive facade produces many SIFT matches and a high inlier ratio, but localization is displaced by one window. What diagnosis should be proposed, and how can it be checked?

**Ambiguity to several solutions**: A periodic pattern allows $H_0,H_1,\ldots$ candidate transformations that shift the alignment of a period while retaining small residuals on repeated windows. We must compare information that does not have this symmetry, or announce that the problem remains ambiguous. Then construct an acceptance rule including an absolute reference or a justified motion marker. A better score of a few inliers is not proof when all the observations are repeated. Examine several assumptions and their margin may be more informative than returning only the best model, provided you evaluate this rule on ambiguous reserved cases.

### CV-SIFT-007

**Situation**: When choosing SIFT or ORB for industrial part registration, which measurements make the comparison useful to the product?

**Break down the causes of failure**: separately measure repeatability of detection, match accuracy, recall of useful matches and registration rate accepted to business tolerance. A ratio of players can increase simply because almost all matches have been withdrawn; you have to keep its denominator and coverage. The exhaustive cost between $n$ and $m$ descriptors of dimension $d$ is of the order of $nmd$ scalar operations; varying the quota of points therefore also changes the matcher and the budget RANSAC. Comparing a quality-cost boundary for multiple settings is more instructive than confronting two default parameters, without announcing a winner before the measurements.

**Passages consulted for these developments**: [Lowe 2004](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf), §§3 – 7.1, scale space, location, description and matching.

## Sources and flashcards

- [Lowe 2004][lowe]: §§3 – 4 detection, §5 orientation, §6 description, §7.1 matching. Scientific source of the classical method.
- [OpenCV 4.13, matching][opencv]: norm and API; implementation source.
- [flashcards SIFT](../41-sift.md).

[lowe]: https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf
[opencv]: https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html
