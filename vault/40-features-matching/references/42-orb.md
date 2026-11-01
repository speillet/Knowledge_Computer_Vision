---
id: CV-ORB
type: methode
domaine: d04
poles: [B, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: []
revision: 7
tags: [cv/d04, matching, orb]
---
# ORB — detection and oriented binary descriptors

## Problem, data and prerequisites

ORB (*Oriented FAST and Rotated BRIEF*) looks for local features with a binary representation suitable for fast comparisons. Input: image in gray, with coordinate frame and resolution preserved. Output: keypoints and descriptors; the classic variant has 256 bits per descriptor. We still need a matcher and a geometric validation. [Rublee et al., §§3 – 4][orbpaper]

**Competences**: rebuild the pipeline, choose the distance, compare under budget, diagnose a change of parameters. **Required prerequisites**: [coordinate frames/distances](../../01-Parcours/Pre-requis.md). **Connexions**: [SIFT](41-sift.md), [homographie](../../50-calibration-geometrie/references/51-ransac-homographie.md).

## Intuition and steps

1. Detect with FAST in a pyramid of images.
2. Classify candidates, including with Harris score in the original method.
3. Estimate an orientation thanks to the center of mass of the intensities of the patch.
4. Orient an intensity comparison test pattern of type BRIEF.
5. Form the binary vector from discriminating and poorly correlated tests.

The choice of rBRIEF tests is learned offline in the article; it does not mean that a network is trained on the two images to pair. [Rublee, §4][orbpaper]

## Orientation and distance

$$
m_{pq}=\sum_{(x,y)\in P}x^p y^q I(x,y),\qquad
\theta=\operatorname{atan2}(m_{01},m_{10}).
$$

$P$ is the patch, $(x,y)$ coordinates **Focus on the keypoint**, $I$ intensity and $m_{pq}$ its $p+q$ order moment. $\theta$ is an orientation in radians. A poor or symmetrical patch can make this orientation unstable; it does not add missing information to the image.

For two test positions $a,b$, one bit is $\mathbf1[I(a)<I(b)]$. The pattern is rotated with orientation. With two choices per test, the Hamming distance counts different bit positions; an L2 distance between stored bytes does not measure the same thing.

Example built: bytes `00000000` and `10000000`. Hamming = 1, while the numerical difference between bytes is 128. The `uint8` storage therefore does not justify a Euclidean distance on the bytes.

## Parameters and properties

OpenCV 4.13 offers `nfeatures`, `scaleFactor`, `nlevels`, `fastThreshold`, `patchSize`, `edgeThreshold` and `WTA_K`. Changing the pyramid changes both the coverage of the scales and the cost. Areas close to the edge can be excluded to ensure an actionable patch. [OpenCV ORB][opencv]

`WTA_K=2` produces binary tests: `NORM_HAMMING`. For `WTA_K=3` or `4`, the winning index is encoded on two bits: `NORM_HAMMING2` compares these symbols. It's not "Hamming Squared." This variant is a choice of implementation to record; do not generalize its norm to the original descriptor.

Rotation: local compensation, subject to stable orientation. Ladder: discreet cover by the pyramid, without perfect invariance. Perspective, motion blur and low contrasts remain causes of failure. The speed figures of 2011 are not guarantees on a current device.

## Implementation and cost

Extract **Illustrative not executed**, OpenCV 4.13:

```python
orb = cv.ORB_create(nfeatures=1000, WTA_K=4)
matcher = cv.BFMatcher(orb.defaultNorm(), crossCheck=True)
# After detectAndCompute on each image, verify that the outputs are nonempty:
matches = matcher.match(descriptors_a, descriptors_b)
```

Here the cross-check holds the closest mutual neighbors. It deals with an inconsistency of reciprocity; it does not prove that the match is physically fair. The ratio test compares the ambiguity between neighbors. Do not activate a cross-check and assume an interchangeable `knnMatch(k=2)` call. [OpenCV matcher][matcher]

The memory of binary descriptors and XOR/popcount comparisons are potential benefits. Also measure extraction, transfer, matching and geometric estimation; the number of features can dominate the downstream cost.

## Baseline, variation and diagnosis

**Proposal for non-executed experiment**: compare ORB and SIFT on the same annotated pairs, with true geometry and the same validation budget. Measure successful registration rate, residuals, spatial coverage, p50/p95 latency and memory. Do not compare only the gross number of matches.

**Controlled variation**: change only `WTA_K` from 2 to 4, adapt the norm and keep the rest of the protocol fixed. Prediction: results and cost may change; an old incorrect norm would introduce a confounding factor. The expected result is not “4 is always better”.

| Symptom | Possible causes | check useful |
| --- | --- | --- |
| Degradation after change of `WTA_K` | norm remained Hamming, other simultaneous modification | Read `defaultNorm()`, enter parameters |
| Failure to change scale | Pyramid range, missing details | View keypoint levels and repeatability |
| A lot of matches but false geometry | Repetitive patterns, parallax, false pattern | Ratio/cross-check then spatial and geometric verification |

**Choix industriel**: On-board CPU, start with a ORB baseline if the variations are compatible, and then measure SIFT or a learned approach if the success rate is insufficient. The time constraint does not replace the validation of the task.

## Guided reasoning and proposed checks

These constructed cases develop separate detection, orientation, representation and norm. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-ORB-001

**Question of work**: How does ORB turn an image into an oriented binary descriptor, and what is each component's role?

**Reference Response**: FAST detects candidates in a pyramid; a ranking, Harris in the article, selects points; the center of mass of intensities provides orientation; oriented BRIEF tests form the binary descriptor.

**Interpreted mechanism**: Detecting a position is not enough to compare two turned neighborhoods. The orientation establishes a local coordinate frame in which the test pattern is moved; the binary responses then describe intensity relationships in this coordinate frame. The pyramid provides several sizes of observation, without making all the details identical to the different resolutions.

**Constructed diagnosis**: If keypoints are detected but matches disappear under rotation, inspect orientation stability and patch content before changing the number of points. If the keypoints disappear themselves, examine thresholds, blur and pyramid levels. This separation of steps makes it possible to attribute a failure to a specific mechanism instead of treating ORB as a black box.

### Case linked to CV-ORB-006

**Question of work**: You must localize a marking on an embedded CPU with limited memory. How can an ORB baseline be built without assuming its final suitability?

**Reference Response**: set variations and location tolerance, extract ORB with recorded parameters, match with its norm and then validate geometrically. Measure full cost and failures on representative data, and then compare an alternative if the need is not met.

**Usable baseline**: Explicitly predict three outcomes: accepted transformation, uncertain outcome, and no outcome. Set the acceptance from the residuals, cover and plausibility of the movement, and then evaluate the acceptance errors on reserved parts. A controlled refusal may be preferable to a poorly placed inspection region.

**Proposed comparison**: Keep the same inputs and tolerances for a SIFT alternative, including steps that actually change in cost. Measure maximum memory and latency in representative conditions, not just the time of an isolated call. The compact representation of ORB motivates the test; it is the balance of precision, robustness, cost and behavior in failure that decides its suitability.

**Documentary reference for this pass**: [OpenCV 4.13, ORB](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html), Theory, orientation and steered BRIEF. The other developments are in the [flashcards](../42-orb.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-ORB-001

**Situation**: How does ORB turn an image into an oriented binary descriptor, and what is each component's role?

**Calculate the orientation**: In a keypoint-centric patch, set the $m_{pq}=\sum_{x,y}x^py^qI(x,y)$ moments. The direction to the centroid is obtained by $\theta=\operatorname{atan2}(m_{01},m_{10})$ when these moments give an actionable direction. The pattern of comparisons is then rotated according to $\theta$ before the intensity readings. If the patch is almost symmetrical or noisy, a small disturbance can strongly change this orientation: the position can remain repeatable without the tests describing the same oriented neighborhood. The edges of the patch and the actual presence of the required pixels must also be managed, not silently supplemented by unrelated content.

### CV-ORB-002

**Situation**: Why is L2 distance between bytes of a binary-test ORB descriptor different from Hamming distance?

**Computable version of Hamming**: for two binary suites $a,b$, $d_H(a,b)=\operatorname{popcount}(a\oplus b)$ adds the disagreements between tests. The operations are machine words or bytes, but the result does not depend on the numerical weight of the bits. A change in the placement of the same tests in the bytes therefore retains Hamming if applied to both descriptors; it can completely change L2 on the byte values. This reasoning gives a simple implementation check, without an image: build two patterns of which a single test differs in several positions. The expected distance remains one, which separates metric storage and metric representation.

### CV-ORB-003

**Situation**: In OpenCV 4.13, ORB changes from `WTA_K=2` to `WTA_K=4`. What must be checked in the matcher, and why?

**What the Winner Codes**: for each group of $K$ positions, the result indicates the index of the position of maximum intensity. With three or four candidates, the two bits are a categorical symbol, not two independent binary questions. The `00→01` and `00→11` disagreements must therefore count each for a different symbol. This logic explains why the change also requires reconstructing a persistent descriptor base: the same table length does not guarantee the same semantics. Also check that the approximate search index supports this metric; a correct norm in an exhaustive matcher does not automatically validate all binary indexes.

### CV-ORB-004

**Situation**: For ORB descriptors, how do cross-checking and a ratio test differ, and what does neither guarantee?

**Example of non-equivalent filter**: In a built-up distance matrix, request A can have candidates with distances 10 and 11; the former also prefers it to all other requests. The cross-check accepts it, while a ratio of 0,8 rejects it. A request B may have 10 and 30, but its best candidate prefers A: the ratio accepts it and reciprocity rejects it. These cases show that the two rules pose different questions. One can design an explicit combination, at the cost of additional calculations and reminders; it must define what to do with ex æquo and absent candidates, and then be geometrically validated.

### CV-ORB-005

**Situation**: ORB works at a fixed distance but fails when the camera moves away. Which assumptions should be examined before simply increasing the feature count?

**Scales and cost coverage**: with a pyramid factor $s>1$, a detail of size $r$ pixels at the initial level covers about $r/s^\ell$ pixels at the $\ell$ level. Increasing the number of levels extends the scales examined; reducing $s$ samples them more finely but increases the work for the same range. No level restores an already undersampled detail in the input image. In a constructed case, a three-pixel-wide tag reduced to one pixel no longer offers the same intensity tests, even if its overall position remains known. The detection thresholds and quotas distributed between levels must therefore be analysed with the resolution actually available on the target.

### CV-ORB-006

**Situation**: You must localize a marking on an embedded CPU with limited memory. How can an ORB baseline be built without assuming its final suitability?

**Establishing a concrete memory budget**: In the current OpenCV variant at 256 bits, a descriptor occupies 32 bytes; 2000 descriptors represent about 64 kB of raw data. This excludes keypoints, pyramid images, buffers, indexes, allocations, and program structures: this calculation is not a measure of memory peak. An exhaustive search between two sets of $n$ and $m$ points processes $nm$ pairs, even with a fast binary distance. Preparing behavior when there are no descriptors or too few pairs for the model prevents a speed optimization from turning a normal observation failure into an arbitrary result or execution error.

**Passages consulted for these developments**: [OpenCV 4.13, ORB](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html), Theory and WTA_K; [OpenCV 4.13, Feature Matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), norms, cross-check and knnMatch; verified with Context7.

## Sources and flashcards

- [Rublee et al., ICCV 2011][orbpaper]: §§3 – 4 mechanism; §§4.4, 5.3 and 6.1 evaluation.
- [OpenCV ORB 4.13][opencv]: Parameters and semantics of `WTA_K`.
- [OpenCV matching][matcher]: distances and cross-check.
- [flashcards ORB](../42-orb.md).

[orbpaper]: https://doi.org/10.1109/ICCV.2011.6126544
[opencv]: https://docs.opencv.org/4.13.0/db/d95/classcv_1_1ORB.html
[matcher]: https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html
