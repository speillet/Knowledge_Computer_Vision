---
id: CV-FAST-BRIEF
type: methode
domaine: d04
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 4
prerequis: ["CV-CORNERS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# FAST and BRIEF — detecting corners and describing their neighborhoods

## Prerequisites and competencies

**Required prerequisites**: [CV-CORNERS](46-harris-shi-tomasi.md). **Target competencies**: explain the FAST test; calculate a binary distance; separate FAST BRIEF and ORB; isolate a failure under rotation; measure the compromise repeatability calculation. Related notions remain alternatives, not implicit dependencies.

## Problem and data contract

Build a light feature chain by separating detection and description. FAST takes local intensities and returns keypoints; BRIEF takes patches around keypoints and returns bit strings. A match then connects two descriptors. Positions, sampling pattern, smoothing, scale and orientation must be compatible between images.

## Intuition and mechanism

The FAST test segment compares the center to a circle of pixels: it looks for a contiguous arc that is uniformly lighter or darker. The decision tree of Rosten and Drummond speeds up the decision; removing non-maxima avoids clusters of answers. BRIEF smoothes a patch and then compares the intensity of pairs of positions. The binary response sequence describes the patch. BRIEF alone does not detect points; FAST alone does not create a descriptor.

## Mathematics and conventions

For the $p$ centre, the threshold $t>0$ is in the same units as the intensity $I$. On a discrete circle, FAST requires an arc of $n$ neighbors all above $I(p)+t$ or all below $I(p)-t$. $n$ and the circle depend on the variant; do not confuse FAST-9 and the historical test with 12 neighbors on 16. A BRIEF bit is $b_j=\mathbf1[I_s(x_j)<I_s(y_j)]$, with $I_s$ the patch smoothed and $(x_j,y_j)$ a set pair. The Hamming distance counts the different bits: $d_H(a,b)=\mathrm{popcount}(a\oplus b)$, without unit.

## Assumptions, parameters and cost

Threshold, FAST variant, non-maximum suppression and smoothing change repeatability and density. The shaft avoids unnecessary testing but does not add a geometric guarantee. A fixed BRIEF pattern is not invariant to any rotation or scale: it can compare other structures when the patch rotates. Cost of description and storage increase with the number of tests; binary matching remains a cost to be measured with the number of points. ORB enriches this family with orientation, pyramid and selection of tests; it is not reduced to the collage of standard FAST and BRIEF.

## Evaluation and controlled variation

Proposed baseline: fixed pattern and scale; variation: increasing rotation of the same scene, with truth of transformation. Separate re-detection rate and match accuracy to find out which step fails. Compare extraction time, matching time, coverage and inliers at equal budget. Analytical example: 101101 XOR 100001 gives 001100, so a Hamming distance of 2. An integer storing bits is not a Euclidean coordinate.

## Failure modes, diagnosis and alternatives

Fine Noise: Compare the smoothness and stability of binary tests. Blur: check the contrast of the circle FAST before lowering the threshold. Rotation: Keep detections and compare oriented patches to isolate the descriptor. At high scale variations, test SIFT or a learned detector/descriptor. OpenCV 4.13 API verified with Context7; no benchmark or feature extractor call executed.

## Guided reasoning and proposed checks

These constructed cases develop segment test and binary signature under transformations. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-FAST-BRIEF-001

**Question of work**: Which intensity pattern passes the FAST segment test, and what do the subsequent steps produce?

**Reference Response**: A contiguous arc of circle neighbors must be entirely lighter than the center plus a threshold, or darker than the center minus that threshold. The variant sets arc length and circle; removing maxima selects neighboring responses.

**Logical example**: In a given variant, several very clear neighbors distributed throughout the circle do not replace a long contiguous arc. The accepted pattern describes a spatial organization of the contrast around the center, not a simple histogram of neighboring values.

**Choice of implementation**: keep threshold, variant and unit of intensity in the protocol. A lower threshold potentially increases candidates, including unstable responses under noise; deletion of maxima check then local redundancy. To diagnose a drop in matches, first observe if the same positions are detected. A rapid extraction of candidates does not yet give any stable orientation, distinctive signature, or transformation between images. These responsibilities belong to the following components of the chain.

### Case linked to CV-FAST-BRIEF-005

**Question of work**: For an embedded camera, which results should be compared before replacing SIFT with FAST/BRIEF?

**Reference Response**: Compare repeatability, quality of matches validated, coverage, latency extraction+matching and memory, with resolution and budget of comparable points. Include representative rotations, scales and noise.

**Compare complete systems**: A gain on detection can be lost if more undistinguishable points multiply comparisons and robust estimation samples. Conversely, a more expensive description can reduce the number of bad assumptions to be addressed. The downstream cost therefore also depends on the quality and distribution of the features.

**Proposed criterion**: set a tolerance of registration and measure cases that are wrongly accepted, refused and correctly located, with the same reference transformations. Time any index construction, extraction, matching and geometry on the target CPU. Keep cases of low texture and strong rotation. This protocol turns a promise of historic speed into a verifiable decision for the current camera and product.

**Documentary reference for this pass**: [Rosten and Drummond 2006](https://www.edwardrosten.com/work/rosten_2006_machine.pdf), §§2 – 3, FAST test and tree learning. The other developments are in the [flashcards](../47-fast-brief.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-FAST-BRIEF-001

**Situation**: Which intensity pattern passes the FAST segment test, and what do the subsequent steps produce?

**Build an unambiguous test**: For a circle of 16 neighbors, code each position as light, dark or similar to the center depending on the threshold. Look for a fairly long contiguous sequence, taking into account the connection between the last and the first position of the circle; a naive implementation can double the sequence to verify this connection. This description is a logical pseudocode, not a benchmark program. Rapid tests of a subset of positions may reject some candidates before the full test, depending on the variant. A lower threshold makes more differences compatible with an arc, but also changes the noise sensitivity; choose the threshold in the effective intensity unit.

### CV-FAST-BRIEF-002

**Situation**: Two toy BRIEF descriptors are 101101 and 100001. Which distance should be used, and what is its value?

**Stability of one bit**: The $b_j=\mathbf1[I_s(x_j)<I_s(y_j)]$ test is particularly fragile if the $I_s(y_j)-I_s(x_j)$ difference is close to zero. A low noise can then return the bit, even if the patch represents the same point. Smoothing reduces some fluctuations but can remove the distinctive detail. Adding highly correlated bits does not provide as much information as complementary comparisons. Hamming's distance does not tell what disagreements arise from noise, rotation, or other object: it is the data and protocol that determine its interpretation. A threshold relating to the number of bits is not automatically a match probability.

### CV-FAST-BRIEF-003

**Situation**: Why are “FAST + BRIEF” and ORB not synonyms?

**Separate learned and calculated parameters**: in a ORB assembly, the selection of binary comparisons aims at informative and little redundant tests on learning data; at the extraction of a new image, the orientation and answers of these tests are calculated around each point. This is not an online trained network on the observed part. A BRIEF with a fixed pattern can share the same storage without sharing this selection or the orientation compensation. To compare two strings, record the pattern, support, smoothing and sampling coordinates; the name of the detector does not identify the descriptor that was produced.

### CV-FAST-BRIEF-004

**Situation**: After image rotation, FAST points remain well localized but BRIEF matching deteriorates. Which mechanism should be tested first?

**Compensation expected**: If a patch is rotated by $R_\theta$, the positions of the two readings of a test must undergo a consistent transformation, or the patch must be resampled in a canonical coordinate frame before comparison. The first strategy rotates the pattern, the second transforms the local image; their interpolations and edges may differ. With an exact known rotation, they give a discriminating experience to isolate the absence of orientation. With an estimated orientation, its noise becomes a new cause of binary disagreement. An improvement in this ablation does not demonstrate an invariance in perspective: anisotropic deformation is not compensated by a single angle.

### CV-FAST-BRIEF-005

**Situation**: For an embedded camera, which results should be compared before replacing SIFT with FAST/BRIEF?

**Connecting precision and robust cost**: for a minimum solver of size $s$ and a rate of inliers $w$, the nominal number of prints RANSAC with confidence $p$ is $N\ge\log(1-p)/\log(1-w^s)$ under independent and non-degenerate prints. A cheaper extraction but producing a lower $w$ can therefore greatly increase the cost of geometry. This calculation is an analytical model, not an exact latency prediction: stop, degeneration and repetition variants change the actual behavior. Also measure the time and memory for failures, where the maximum budget can be consumed, instead of only timing the easy pairs correctly registered.

**Passages consulted for these developments**: [OpenCV 4.13, FAST](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html), non-maxima testing and removal segment; fallback after timeout of the author PDF; [Calonder et al. 2010, BRIEF](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf), §3, tests, smoothing and patterns; [OpenCV 4.13, ORB](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html), orientation and rBRIEF selection.

## Sources and flashcards

- [Rosten and Drummond 2006, §§2 – 3, test and learning segment](https://www.edwardrosten.com/work/rosten_2006_machine.pdf).
- [Calonder et al. 2010, §3, BRIEF tests and smoothing](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf).
- [OpenCV 4.13, FAST, Theory](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html).
- [OpenCV 4.13, BRIEF, Theory](https://docs.opencv.org/4.13.0/dc/d7d/tutorial_py_brief.html).
- [OpenCV 4.13, ORB, orientation and rBRIEF](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html).
- [Related flashcards](../47-fast-brief.md): CV-FAST-BRIEF-001 to 005.

Editor: Agent Codex, 2026-10-24. Primary sources consulted and API OpenCV 4.13 verified with Context7. Analytical calculations and proposed protocols are distinguished from experiments; no actual export, video benchmark or independent scientific validation announced.
